from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    # API REST
    path("api/veiculos/", include("veiculos.urls")),
    path("api/compradores/", include("compradores.urls")),
    path("api/vendas/", include("vendas.urls")),
    # Frontend (Django Templates)
    path("", views.dashboard, name="dashboard"),
    path("devsecops/", views.devsecops_dashboard, name="devsecops_dashboard"),
    path("veiculos/", views.veiculos_list, name="veiculos_list"),
    path("veiculos/novo/", views.veiculo_create, name="veiculo_create"),
    path("veiculos/<uuid:pk>/", views.veiculo_detail, name="veiculo_detail"),
    path("veiculos/<uuid:pk>/editar/", views.veiculo_edit, name="veiculo_edit"),
    path("compradores/", views.compradores_list, name="compradores_list"),
    path("compradores/novo/", views.comprador_create, name="comprador_create"),
    path("vendas/", views.vendas_list, name="vendas_list"),
    path("vendas/nova/", views.venda_create, name="venda_create"),
    path("vendas/<uuid:pk>/", views.venda_detail, name="venda_detail"),
    path("vendas/<uuid:pk>/<str:action>/", views.venda_action, name="venda_action"),
]
