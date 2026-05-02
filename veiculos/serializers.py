from rest_framework import serializers

from .models import Veiculo


class VeiculoSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Veiculo
        fields = [
            "id",
            "marca",
            "modelo",
            "ano",
            "cor",
            "preco",
            "placa",
            "chassi",
            "quilometragem",
            "descricao",
            "status",
            "status_display",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["id", "status", "criado_em", "atualizado_em"]
