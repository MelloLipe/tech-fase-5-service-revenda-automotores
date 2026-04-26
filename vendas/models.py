import uuid

from django.db import models
from django.utils import timezone


class Venda(models.Model):
    """
    Modelo de venda com máquina de estados (SAGA Coreografada).

    Fluxo: SELECIONADO -> RESERVADO -> PAGAMENTO_PENDENTE -> PAGO -> CONCLUIDO
    Cancelamentos possíveis em qualquer etapa antes de CONCLUIDO.
    """

    class StatusVenda(models.TextChoices):
        SELECIONADO = "selecionado", "Veículo Selecionado"
        RESERVADO = "reservado", "Veículo Reservado"
        PAGAMENTO_PENDENTE = "pagamento_pendente", "Pagamento Pendente"
        PAGO = "pago", "Pago"
        CONCLUIDO = "concluido", "Concluído (Veículo Retirado)"
        CANCELADO = "cancelado", "Cancelado"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    veiculo = models.ForeignKey(
        "veiculos.Veiculo",
        on_delete=models.PROTECT,
        related_name="vendas",
    )
    comprador = models.ForeignKey(
        "compradores.Comprador",
        on_delete=models.PROTECT,
        related_name="compras",
    )
    status = models.CharField(
        max_length=30,
        choices=StatusVenda.choices,
        default=StatusVenda.SELECIONADO,
    )
    codigo_pagamento = models.CharField(
        max_length=36,
        blank=True,
        null=True,
        unique=True,
    )
    preco_venda = models.DecimalField(max_digits=12, decimal_places=2)
    motivo_cancelamento = models.TextField(blank=True)

    # Timestamps de cada etapa
    data_selecao = models.DateTimeField(auto_now_add=True)
    data_reserva = models.DateTimeField(null=True, blank=True)
    data_pagamento = models.DateTimeField(null=True, blank=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    data_cancelamento = models.DateTimeField(null=True, blank=True)

    # Expiração da reserva (30 min)
    reserva_expira_em = models.DateTimeField(null=True, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

    def __str__(self):
        return f"Venda {self.id} - {self.veiculo} -> {self.comprador}"

    @property
    def reserva_expirada(self):
        if self.reserva_expira_em and self.status == self.StatusVenda.RESERVADO:
            return timezone.now() > self.reserva_expira_em
        return False


class HistoricoVenda(models.Model):
    """Log de auditoria para cada mudança de estado da venda."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venda = models.ForeignKey(
        Venda,
        on_delete=models.CASCADE,
        related_name="historico",
    )
    status_anterior = models.CharField(max_length=30, blank=True)
    status_novo = models.CharField(max_length=30)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["criado_em"]
        verbose_name = "Histórico de Venda"
        verbose_name_plural = "Históricos de Vendas"

    def __str__(self):
        return f"{self.venda.id}: {self.status_anterior} -> {self.status_novo}"
