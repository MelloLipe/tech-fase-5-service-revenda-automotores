from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Veiculo


class VeiculoAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.veiculo_data = {
            "marca": "Toyota",
            "modelo": "Corolla",
            "ano": 2023,
            "cor": "Prata",
            "preco": "120000.00",
            "placa": "ABC1D23",
            "chassi": "9BWZZZ377VT004251",
            "quilometragem": 15000,
            "descricao": "Veiculo em otimo estado",
        }

    def test_criar_veiculo(self):
        response = self.client.post("/api/veiculos/", self.veiculo_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["marca"], "Toyota")
        self.assertEqual(response.data["status"], "disponivel")

    def test_listar_veiculos_ordenados_por_preco(self):
        Veiculo.objects.create(
            marca="Fiat",
            modelo="Uno",
            ano=2020,
            cor="Branco",
            preco=Decimal("45000.00"),
            placa="XYZ1A23",
            chassi="9BWZZZ377VT004252",
        )
        Veiculo.objects.create(
            marca="BMW",
            modelo="X1",
            ano=2022,
            cor="Preto",
            preco=Decimal("250000.00"),
            placa="DEF2B34",
            chassi="9BWZZZ377VT004253",
        )
        response = self.client.get("/api/veiculos/")
        self.assertEqual(response.status_code, 200)
        results = response.data["results"]
        self.assertEqual(len(results), 2)
        self.assertLessEqual(
            Decimal(results[0]["preco"]),
            Decimal(results[1]["preco"]),
        )

    def test_filtrar_por_status(self):
        Veiculo.objects.create(
            marca="Honda",
            modelo="Civic",
            ano=2021,
            cor="Azul",
            preco=Decimal("95000.00"),
            placa="GHI3C45",
            chassi="9BWZZZ377VT004254",
        )
        response = self.client.get("/api/veiculos/?status=disponivel")
        self.assertEqual(response.status_code, 200)
        for v in response.data["results"]:
            self.assertEqual(v["status"], "disponivel")

    def test_editar_veiculo(self):
        v = Veiculo.objects.create(
            marca="VW",
            modelo="Golf",
            ano=2019,
            cor="Vermelho",
            preco=Decimal("80000.00"),
            placa="JKL4D56",
            chassi="9BWZZZ377VT004255",
        )
        response = self.client.patch(
            f"/api/veiculos/{v.id}/",
            {"preco": "75000.00"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["preco"], "75000.00")
