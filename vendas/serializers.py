from rest_framework import serializers

from compradores.serializers import CompradorSerializer
from veiculos.serializers import VeiculoSerializer

from .models import HistoricoVenda, Venda


class HistoricoVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoVenda
        fields = ["id", "status_anterior", "status_novo", "descricao", "criado_em"]


class VendaSerializer(serializers.ModelSerializer):
    veiculo_detail = VeiculoSerializer(source="veiculo", read_only=True)
    comprador_detail = CompradorSerializer(source="comprador", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    historico = HistoricoVendaSerializer(many=True, read_only=True)
    reserva_expirada = serializers.BooleanField(read_only=True)

    class Meta:
        model = Venda
        fields = [
            "id",
            "veiculo",
            "comprador",
            "veiculo_detail",
            "comprador_detail",
            "status",
            "status_display",
            "codigo_pagamento",
            "preco_venda",
            "motivo_cancelamento",
            "data_selecao",
            "data_reserva",
            "data_pagamento",
            "data_conclusao",
            "data_cancelamento",
            "reserva_expira_em",
            "reserva_expirada",
            "historico",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = [
            "id",
            "status",
            "codigo_pagamento",
            "preco_venda",
            "data_selecao",
            "data_reserva",
            "data_pagamento",
            "data_conclusao",
            "data_cancelamento",
            "reserva_expira_em",
            "criado_em",
            "atualizado_em",
        ]


class IniciarVendaSerializer(serializers.Serializer):
    veiculo_id = serializers.UUIDField()
    comprador_id = serializers.UUIDField()


class ConfirmarPagamentoSerializer(serializers.Serializer):
    codigo_pagamento = serializers.CharField(max_length=36)


class CancelarVendaSerializer(serializers.Serializer):
    motivo = serializers.CharField(required=False, default="Cliente desistiu da compra.")
