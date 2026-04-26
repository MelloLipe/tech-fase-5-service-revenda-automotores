from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Venda
from .serializers import (
    CancelarVendaSerializer,
    ConfirmarPagamentoSerializer,
    IniciarVendaSerializer,
    VendaSerializer,
)
from .services import (
    cancelar_venda,
    concluir_venda,
    confirmar_pagamento,
    gerar_codigo_pagamento,
    reservar_veiculo,
    selecionar_veiculo,
)


class VendaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vendas — fluxo SAGA coreografado.

    Endpoints:
    - POST /api/vendas/iniciar/ — seleciona veículo
    - POST /api/vendas/{id}/reservar/ — reserva veículo
    - POST /api/vendas/{id}/gerar-pagamento/ — gera código de pagamento
    - POST /api/vendas/{id}/confirmar-pagamento/ — confirma pagamento
    - POST /api/vendas/{id}/concluir/ — conclui venda (retirada)
    - POST /api/vendas/{id}/cancelar/ — cancela em qualquer etapa
    """

    queryset = Venda.objects.select_related("veiculo", "comprador").prefetch_related("historico")
    serializer_class = VendaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status", "comprador"]
    ordering_fields = ["preco_venda", "criado_em"]
    ordering = ["-criado_em"]

    @action(detail=False, methods=["post"], url_path="iniciar")
    def iniciar(self, request):
        """Etapa 1: Seleciona veículo para compra."""
        serializer = IniciarVendaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        venda = selecionar_veiculo(
            serializer.validated_data["veiculo_id"],
            serializer.validated_data["comprador_id"],
        )
        return Response(
            VendaSerializer(venda).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="reservar")
    def reservar(self, request, pk=None):
        """Etapa 2: Reserva o veículo."""
        venda = reservar_veiculo(pk)
        return Response(VendaSerializer(venda).data)

    @action(detail=True, methods=["post"], url_path="gerar-pagamento")
    def gerar_pagamento(self, request, pk=None):
        """Etapa 3: Gera código de pagamento."""
        venda = gerar_codigo_pagamento(pk)
        return Response(VendaSerializer(venda).data)

    @action(detail=True, methods=["post"], url_path="confirmar-pagamento")
    def confirmar_pagamento(self, request, pk=None):
        """Etapa 4: Confirma pagamento."""
        serializer = ConfirmarPagamentoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        venda = confirmar_pagamento(
            pk,
            serializer.validated_data["codigo_pagamento"],
        )
        return Response(VendaSerializer(venda).data)

    @action(detail=True, methods=["post"], url_path="concluir")
    def concluir(self, request, pk=None):
        """Etapa 5: Conclui venda (retirada do veículo)."""
        venda = concluir_venda(pk)
        return Response(VendaSerializer(venda).data)

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        """Cancela a venda em qualquer etapa."""
        serializer = CancelarVendaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        venda = cancelar_venda(pk, serializer.validated_data["motivo"])
        return Response(VendaSerializer(venda).data)
