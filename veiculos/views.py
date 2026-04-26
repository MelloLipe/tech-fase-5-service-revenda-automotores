from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Veiculo
from .serializers import VeiculoSerializer


class VeiculoViewSet(viewsets.ModelViewSet):
    """
    CRUD de veículos.
    - GET /api/veiculos/ — lista todos (filtro por status)
    - GET /api/veiculos/?status=disponivel — veículos à venda
    - GET /api/veiculos/?status=vendido — veículos vendidos
    """

    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ["status", "marca", "ano", "cor"]
    ordering_fields = ["preco", "ano", "criado_em"]
    ordering = ["preco"]
    search_fields = ["marca", "modelo", "placa"]
