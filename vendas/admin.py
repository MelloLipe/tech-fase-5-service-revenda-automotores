from django.contrib import admin

from .models import HistoricoVenda, Venda


class HistoricoInline(admin.TabularInline):
    model = HistoricoVenda
    readonly_fields = ["id", "status_anterior", "status_novo", "descricao", "criado_em"]
    extra = 0
    can_delete = False


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ["id", "veiculo", "comprador", "status", "preco_venda", "criado_em"]
    list_filter = ["status"]
    search_fields = ["veiculo__marca", "veiculo__modelo", "comprador__nome"]
    readonly_fields = [
        "id",
        "codigo_pagamento",
        "data_selecao",
        "data_reserva",
        "data_pagamento",
        "data_conclusao",
        "data_cancelamento",
        "reserva_expira_em",
        "criado_em",
        "atualizado_em",
    ]
    inlines = [HistoricoInline]
