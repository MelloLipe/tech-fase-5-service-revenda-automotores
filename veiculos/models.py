import uuid

from django.db import models


class Veiculo(models.Model):
    """Modelo de veículo para revenda."""

    class StatusVeiculo(models.TextChoices):
        DISPONIVEL = "disponivel", "Disponível"
        RESERVADO = "reservado", "Reservado"
        VENDIDO = "vendido", "Vendido"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.PositiveIntegerField()
    cor = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    placa = models.CharField(max_length=10, unique=True)
    chassi = models.CharField(max_length=17, unique=True)
    quilometragem = models.PositiveIntegerField(default=0)
    descricao = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusVeiculo.choices,
        default=StatusVeiculo.DISPONIVEL,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["preco"]
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano}) - R${self.preco}"
