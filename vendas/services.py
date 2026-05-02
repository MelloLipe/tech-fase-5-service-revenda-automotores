"""
Serviço de orquestração de vendas - SAGA Coreografada.

Cada etapa do processo de compra é uma transação independente
com compensação (rollback) em caso de falha.
"""

import uuid
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from compradores.models import Comprador
from veiculos.models import Veiculo

from .models import HistoricoVenda, Venda


def _registrar_historico(venda, status_anterior, status_novo, descricao=""):
    HistoricoVenda.objects.create(
        venda=venda,
        status_anterior=status_anterior,
        status_novo=status_novo,
        descricao=descricao,
    )


def selecionar_veiculo(veiculo_id, comprador_id):
    """Etapa 1: Cliente seleciona um veículo disponível."""
    with transaction.atomic():
        veiculo = Veiculo.objects.select_for_update().get(id=veiculo_id)
        comprador = Comprador.objects.get(id=comprador_id)

        if not comprador.ativo:
            raise ValidationError({"comprador": "Comprador inativo."})

        if veiculo.status != Veiculo.StatusVeiculo.DISPONIVEL:
            raise ValidationError({"veiculo": "Veículo não está disponível para venda."})

        venda = Venda.objects.create(
            veiculo=veiculo,
            comprador=comprador,
            preco_venda=veiculo.preco,
            status=Venda.StatusVenda.SELECIONADO,
        )

        _registrar_historico(
            venda, "", Venda.StatusVenda.SELECIONADO, "Cliente selecionou o veículo."
        )
        return venda


def reservar_veiculo(venda_id):
    """
    Etapa 2: Reserva o veículo para o cliente.
    Compensação: se outro cliente já reservou, retorna erro.
    """
    with transaction.atomic():
        venda = Venda.objects.select_for_update().get(id=venda_id)
        veiculo = Veiculo.objects.select_for_update().get(id=venda.veiculo_id)

        if venda.status != Venda.StatusVenda.SELECIONADO:
            raise ValidationError(
                {
                    "status": (
                        "Venda não pode ser reservada no status atual: "
                        f"{venda.get_status_display()}"
                    )
                }
            )

        if veiculo.status != Veiculo.StatusVeiculo.DISPONIVEL:
            venda.status = Venda.StatusVenda.CANCELADO
            venda.motivo_cancelamento = "Veículo já foi reservado por outro cliente."
            venda.data_cancelamento = timezone.now()
            venda.save()
            _registrar_historico(
                venda,
                Venda.StatusVenda.SELECIONADO,
                Venda.StatusVenda.CANCELADO,
                "Compensação: veículo indisponível.",
            )
            raise ValidationError({"veiculo": "Veículo já foi reservado por outro cliente."})

        veiculo.status = Veiculo.StatusVeiculo.RESERVADO
        veiculo.save()

        venda.status = Venda.StatusVenda.RESERVADO
        venda.data_reserva = timezone.now()
        venda.reserva_expira_em = timezone.now() + timedelta(minutes=30)
        venda.save()

        _registrar_historico(
            venda,
            Venda.StatusVenda.SELECIONADO,
            Venda.StatusVenda.RESERVADO,
            "Veículo reservado com sucesso. Reserva expira em 30 minutos.",
        )
        return venda


def gerar_codigo_pagamento(venda_id):
    """
    Etapa 3: Gera código de pagamento para o cliente.
    """
    with transaction.atomic():
        venda = Venda.objects.select_for_update().get(id=venda_id)

        if venda.status != Venda.StatusVenda.RESERVADO:
            raise ValidationError(
                {"status": "Código de pagamento só pode ser gerado para vendas reservadas."}
            )

        if venda.reserva_expirada:
            _compensar_reserva(venda, "Reserva expirou antes do pagamento.")
            raise ValidationError({"reserva": "Reserva expirada. Tente novamente."})

        venda.codigo_pagamento = str(uuid.uuid4())
        venda.status = Venda.StatusVenda.PAGAMENTO_PENDENTE
        venda.save()

        _registrar_historico(
            venda,
            Venda.StatusVenda.RESERVADO,
            Venda.StatusVenda.PAGAMENTO_PENDENTE,
            f"Código de pagamento gerado: {venda.codigo_pagamento}",
        )
        return venda


def confirmar_pagamento(venda_id, codigo_pagamento):
    """
    Etapa 4: Confirma o pagamento do veículo.
    Compensação: se pagamento falhar, libera reserva.
    """
    with transaction.atomic():
        venda = Venda.objects.select_for_update().get(id=venda_id)

        if venda.status != Venda.StatusVenda.PAGAMENTO_PENDENTE:
            raise ValidationError({"status": "Venda não está aguardando pagamento."})

        if venda.reserva_expirada:
            _compensar_reserva(venda, "Reserva expirou durante o pagamento.")
            raise ValidationError({"reserva": "Reserva expirada."})

        if venda.codigo_pagamento != codigo_pagamento:
            raise ValidationError({"codigo_pagamento": "Código de pagamento inválido."})

        venda.status = Venda.StatusVenda.PAGO
        venda.data_pagamento = timezone.now()
        venda.save()

        _registrar_historico(
            venda,
            Venda.StatusVenda.PAGAMENTO_PENDENTE,
            Venda.StatusVenda.PAGO,
            "Pagamento confirmado com sucesso.",
        )
        return venda


def concluir_venda(venda_id):
    """
    Etapa 5: Conclui a venda - veículo retirado pelo cliente.
    Veículo passa para status VENDIDO.
    """
    with transaction.atomic():
        venda = Venda.objects.select_for_update().get(id=venda_id)
        veiculo = Veiculo.objects.select_for_update().get(id=venda.veiculo_id)

        if venda.status != Venda.StatusVenda.PAGO:
            raise ValidationError({"status": "Venda precisa estar paga para ser concluída."})

        veiculo.status = Veiculo.StatusVeiculo.VENDIDO
        veiculo.save()

        venda.status = Venda.StatusVenda.CONCLUIDO
        venda.data_conclusao = timezone.now()
        venda.save()

        _registrar_historico(
            venda,
            Venda.StatusVenda.PAGO,
            Venda.StatusVenda.CONCLUIDO,
            "Veículo retirado. Venda concluída.",
        )
        return venda


def cancelar_venda(venda_id, motivo="Cliente desistiu da compra."):
    """
    Cancelamento: pode ocorrer em qualquer etapa antes de CONCLUIDO.
    Executa compensações necessárias (liberar reserva do veículo).
    """
    with transaction.atomic():
        venda = Venda.objects.select_for_update().get(id=venda_id)

        if venda.status in (Venda.StatusVenda.CONCLUIDO, Venda.StatusVenda.CANCELADO):
            raise ValidationError({"status": "Venda já foi concluída ou cancelada."})

        status_anterior = venda.status

        if venda.status in (
            Venda.StatusVenda.RESERVADO,
            Venda.StatusVenda.PAGAMENTO_PENDENTE,
            Venda.StatusVenda.PAGO,
        ):
            veiculo = Veiculo.objects.select_for_update().get(id=venda.veiculo_id)
            veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
            veiculo.save()

        venda.status = Venda.StatusVenda.CANCELADO
        venda.motivo_cancelamento = motivo
        venda.data_cancelamento = timezone.now()
        venda.save()

        _registrar_historico(
            venda,
            status_anterior,
            Venda.StatusVenda.CANCELADO,
            f"Compensação SAGA: venda cancelada. Motivo: {motivo}",
        )
        return venda


def _compensar_reserva(venda, motivo):
    """Compensação: libera veículo reservado."""
    veiculo = Veiculo.objects.select_for_update().get(id=venda.veiculo_id)
    veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
    veiculo.save()

    status_anterior = venda.status
    venda.status = Venda.StatusVenda.CANCELADO
    venda.motivo_cancelamento = motivo
    venda.data_cancelamento = timezone.now()
    venda.save()

    _registrar_historico(
        venda,
        status_anterior,
        Venda.StatusVenda.CANCELADO,
        f"Compensação SAGA: {motivo}",
    )
