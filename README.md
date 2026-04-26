# AutoRevenda - Plataforma de Revenda de Veículos

**Tech Challenge SOAT - Fase 5**

Plataforma web para revenda de veículos automotores com API REST, frontend Django e processo de compra com orquestração SAGA.

## Funcionalidades

- **Veículos**: Cadastro, edição, listagem ordenada por preço (à venda e vendidos)
- **Compradores**: Cadastro com proteção de dados sensíveis (CPF/RG com hash SHA-256)
- **Processo de Compra (SAGA Coreografada)**:
  1. Seleção do veículo
  2. Reserva (30 min de expiração)
  3. Geração de código de pagamento
  4. Confirmação de pagamento
  5. Conclusão (retirada do veículo)
  - Cancelamento em qualquer etapa com compensações automáticas
- **Dashboard**: Painel com métricas, últimas vendas e veículos disponíveis
- **Segurança**: Hashing de documentos, HTTPS, CSRF, headers de segurança

## Tecnologias

- Python 3.12 + Django 6
- Django REST Framework
- PostgreSQL (produção) / SQLite (desenvolvimento)
- Bootstrap 5 (frontend)
- Gunicorn + WhiteNoise
- Deploy: Render (free tier)

## Instalação Local

```bash
# Clonar repositório
git clone https://github.com/MelloLipe/tech-fase-5-service-revenda-automotores.git
cd tech-CHALLENGE-felipe

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Rodar migrações
DEBUG=True python manage.py migrate

# Criar superusuário (opcional)
DEBUG=True python manage.py createsuperuser

# Rodar servidor
DEBUG=True python manage.py runserver
```

Acesse: http://localhost:8001

## API REST

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET/POST | `/api/veiculos/` | Listar/Cadastrar veículos |
| GET/PUT/PATCH/DELETE | `/api/veiculos/{id}/` | Detalhe/Editar/Excluir veículo |
| GET/POST | `/api/compradores/` | Listar/Cadastrar compradores |
| GET | `/api/vendas/` | Listar vendas |
| POST | `/api/vendas/iniciar/` | Iniciar compra (selecionar veículo) |
| POST | `/api/vendas/{id}/reservar/` | Reservar veículo |
| POST | `/api/vendas/{id}/gerar-pagamento/` | Gerar código de pagamento |
| POST | `/api/vendas/{id}/confirmar-pagamento/` | Confirmar pagamento |
| POST | `/api/vendas/{id}/concluir/` | Concluir venda (retirada) |
| POST | `/api/vendas/{id}/cancelar/` | Cancelar venda |

### Filtros e Ordenação

- `GET /api/veiculos/?status=disponivel` — Veículos à venda
- `GET /api/veiculos/?status=vendido` — Veículos vendidos
- `GET /api/veiculos/?ordering=preco` — Ordenar por preço
- `GET /api/vendas/?status=concluido` — Vendas concluídas

## Testes

```bash
DEBUG=True python manage.py test
```

## Deploy no Render (Gratuito)

1. Faça fork/push do repositório no GitHub
2. Acesse [render.com](https://render.com) e conecte seu GitHub
3. Clique em **New Blueprint** e selecione este repositório
4. O `render.yaml` configura automaticamente o web service + PostgreSQL
5. Aguarde o deploy automático

## Documentação

- [Arquitetura](docs/arquitetura.md) — Desenho da solução, justificativas e serviços de segurança
- [Relatório de Segurança](docs/relatorio_seguranca.md) — Dados sensíveis, políticas de acesso e mitigação de riscos
- [Relatório SAGA](docs/relatorio_saga.md) — Tipo de orquestração, justificativa e fluxo de compensações

## Estrutura do Projeto

```
tech-CHALLENGE-felipe/
├── revenda_veiculos/      # Configuração Django + views frontend
├── veiculos/              # App de veículos (CRUD)
├── compradores/           # App de compradores (cadastro seguro)
├── vendas/                # App de vendas (SAGA coreografada)
│   └── services.py        # Lógica de negócio e compensações
├── templates/             # Frontend Django + Bootstrap
├── docs/                  # Documentação (arquitetura, segurança, SAGA)
├── requirements.txt       # Dependências Python
├── Procfile               # Deploy config
├── render.yaml            # Render Blueprint (deploy gratuito)
└── manage.py
```
