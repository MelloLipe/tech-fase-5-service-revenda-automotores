import uuid

from django.db import models


class Comprador(models.Model):
    """
    Modelo de comprador/cliente.
    Dados sensíveis (CPF, RG) são armazenados com criptografia.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)

    # Dados sensíveis - armazenados com mascaramento
    cpf_hash = models.CharField(max_length=64, unique=True, help_text="Hash SHA-256 do CPF")
    cpf_masked = models.CharField(max_length=14, help_text="CPF mascarado: ***.***.***-XX")
    rg_hash = models.CharField(max_length=64, unique=True, help_text="Hash SHA-256 do RG")

    # Dados para documentação do veículo
    endereco = models.TextField()
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    data_nascimento = models.DateField()

    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Comprador"
        verbose_name_plural = "Compradores"

    def __str__(self):
        return f"{self.nome} ({self.cpf_masked})"
