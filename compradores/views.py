from rest_framework import viewsets

from .models import Comprador
from .serializers import CompradorCreateSerializer, CompradorSerializer


class CompradorViewSet(viewsets.ModelViewSet):
    """
    CRUD de compradores.
    Criação usa CompradorCreateSerializer (aceita CPF/RG em texto plano, armazena hash).
    Leitura usa CompradorSerializer (nunca expõe dados sensíveis).
    """

    queryset = Comprador.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CompradorCreateSerializer
        return CompradorSerializer
