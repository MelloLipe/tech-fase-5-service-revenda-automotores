from django.contrib import admin

from .models import Veiculo


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ["marca", "modelo", "ano", "cor", "preco", "status", "placa"]
    list_filter = ["status", "marca", "ano", "cor"]
    search_fields = ["marca", "modelo", "placa", "chassi"]
    readonly_fields = ["id", "criado_em", "atualizado_em"]
