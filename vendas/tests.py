import hashlib
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from compradores.models import Comprador
from veiculos.models import Veiculo


class VendaFluxoCompletoTest(TestCase):
    """Testa o fluxo completo de compra (SAGA)."""

    def setUp(self):
        self.client = APIClient()
        self.veiculo = Veiculo.objects.create(
            marca="Toyota",
            modelo="Corolla",
            ano=2023,
            cor="Prata",
            preco=Decimal("120000.00"),
            placa="TEST123",
            chassi="9BWZZZ377VT099999",
        )
        cpf = "12345678901"
        rg = "123456789"
        self.comprador = Comprador.objects.create(
            nome="Joao Silva",
            email="joao@email.com",
            telefone="11999990000",
            cpf_hash=hashlib.sha256(cpf.encode()).hexdigest(),
            cpf_masked=f"***.***.*{cpf[7:9]}-{cpf[9:11]}",
            rg_hash=hashlib.sha256(rg.encode()).hexdigest(),
            endereco="Rua A, 123",
            cidade="Sao Paulo",
            estado="SP",
            cep="01001000",
            data_nascimento="1990-01-01",
        )

    def test_fluxo_completo_compra(self):
        # 1. Selecionar veiculo
        resp = self.client.post(
            "/api/vendas/iniciar/",
            {
                "veiculo_id": str(self.veiculo.id),
                "comprador_id": str(self.comprador.id),
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 201)
        venda_id = resp.data["id"]
        self.assertEqual(resp.data["status"], "selecionado")

        # 2. Reservar veiculo
        resp = self.client.post(f"/api/vendas/{venda_id}/reservar/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "reservado")

        # 3. Gerar pagamento
        resp = self.client.post(f"/api/vendas/{venda_id}/gerar-pagamento/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "pagamento_pendente")
        codigo = resp.data["codigo_pagamento"]
        self.assertIsNotNone(codigo)

        # 4. Confirmar pagamento
        resp = self.client.post(
            f"/api/vendas/{venda_id}/confirmar-pagamento/",
            {
                "codigo_pagamento": codigo,
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "pago")

        # 5. Concluir venda
        resp = self.client.post(f"/api/vendas/{venda_id}/concluir/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "concluido")

        # Verificar veiculo vendido
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.status, "vendido")

    def test_cancelamento_em_qualquer_etapa(self):
        resp = self.client.post(
            "/api/vendas/iniciar/",
            {
                "veiculo_id": str(self.veiculo.id),
                "comprador_id": str(self.comprador.id),
            },
            format="json",
        )
        venda_id = resp.data["id"]

        resp = self.client.post(
            f"/api/vendas/{venda_id}/cancelar/",
            {
                "motivo": "Cliente desistiu",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "cancelado")

    def test_reserva_por_outro_cliente(self):
        # Cliente 1 seleciona e reserva
        resp1 = self.client.post(
            "/api/vendas/iniciar/",
            {
                "veiculo_id": str(self.veiculo.id),
                "comprador_id": str(self.comprador.id),
            },
            format="json",
        )
        venda1_id = resp1.data["id"]
        self.client.post(f"/api/vendas/{venda1_id}/reservar/")

        # Cliente 2 tenta reservar o mesmo veiculo
        cpf2 = "98765432100"
        comprador2 = Comprador.objects.create(
            nome="Maria Santos",
            email="maria@email.com",
            telefone="11888880000",
            cpf_hash=hashlib.sha256(cpf2.encode()).hexdigest(),
            cpf_masked=f"***.***.*{cpf2[7:9]}-{cpf2[9:11]}",
            rg_hash=hashlib.sha256(b"987654321").hexdigest(),
            endereco="Rua B, 456",
            cidade="Rio de Janeiro",
            estado="RJ",
            cep="20000000",
            data_nascimento="1985-05-15",
        )
        resp2 = self.client.post(
            "/api/vendas/iniciar/",
            {
                "veiculo_id": str(self.veiculo.id),
                "comprador_id": str(comprador2.id),
            },
            format="json",
        )
        self.assertEqual(resp2.status_code, 400)

    def test_codigo_pagamento_invalido(self):
        resp = self.client.post(
            "/api/vendas/iniciar/",
            {
                "veiculo_id": str(self.veiculo.id),
                "comprador_id": str(self.comprador.id),
            },
            format="json",
        )
        venda_id = resp.data["id"]
        self.client.post(f"/api/vendas/{venda_id}/reservar/")
        self.client.post(f"/api/vendas/{venda_id}/gerar-pagamento/")

        resp = self.client.post(
            f"/api/vendas/{venda_id}/confirmar-pagamento/",
            {
                "codigo_pagamento": "codigo-invalido",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    def test_listar_vendas(self):
        resp = self.client.get("/api/vendas/")
        self.assertEqual(resp.status_code, 200)
