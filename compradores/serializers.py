import hashlib
import re

from rest_framework import serializers

from .models import Comprador


class CompradorCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação - aceita CPF e RG em texto plano."""

    cpf = serializers.CharField(write_only=True, max_length=14)
    rg = serializers.CharField(write_only=True, max_length=20)

    class Meta:
        model = Comprador
        fields = [
            "id",
            "nome",
            "email",
            "telefone",
            "cpf",
            "rg",
            "endereco",
            "cidade",
            "estado",
            "cep",
            "data_nascimento",
            "criado_em",
        ]
        read_only_fields = ["id", "criado_em"]

    def validate_cpf(self, value):
        cpf = re.sub(r"\D", "", value)
        if len(cpf) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos.")
        if cpf == cpf[0] * 11:
            raise serializers.ValidationError("CPF inválido.")
        for i in range(9, 11):
            total = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
            digit = ((total * 10) % 11) % 10
            if digit != int(cpf[i]):
                raise serializers.ValidationError("CPF inválido.")
        return cpf

    def validate_rg(self, value):
        rg = re.sub(r"\D", "", value)
        if len(rg) < 5:
            raise serializers.ValidationError("RG deve ter pelo menos 5 dígitos.")
        return rg

    def create(self, validated_data):
        cpf = validated_data.pop("cpf")
        rg = validated_data.pop("rg")

        validated_data["cpf_hash"] = hashlib.sha256(cpf.encode()).hexdigest()
        validated_data["cpf_masked"] = f"***.***.*{cpf[7:9]}-{cpf[9:11]}"
        validated_data["rg_hash"] = hashlib.sha256(rg.encode()).hexdigest()

        return super().create(validated_data)


class CompradorSerializer(serializers.ModelSerializer):
    """Serializer para leitura - nunca expõe dados sensíveis."""

    class Meta:
        model = Comprador
        fields = [
            "id",
            "nome",
            "email",
            "telefone",
            "cpf_masked",
            "endereco",
            "cidade",
            "estado",
            "cep",
            "data_nascimento",
            "ativo",
            "criado_em",
            "atualizado_em",
        ]
        read_only_fields = ["id", "cpf_masked", "criado_em", "atualizado_em"]
