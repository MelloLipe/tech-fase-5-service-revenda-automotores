from django.contrib import admin

from .models import Comprador


@admin.register(Comprador)
class CompradorAdmin(admin.ModelAdmin):
    list_display = ["nome", "email", "telefone", "cpf_masked", "cidade", "estado", "ativo"]
    list_filter = ["ativo", "estado"]
    search_fields = ["nome", "email"]
    readonly_fields = ["id", "cpf_hash", "cpf_masked", "rg_hash", "criado_em", "atualizado_em"]
    exclude = []
