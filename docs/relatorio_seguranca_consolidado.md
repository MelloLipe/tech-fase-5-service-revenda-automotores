# Relatorio Consolidado de Seguranca - AutoRevenda

## 1. Objetivo

Este relatorio consolida as praticas de seguranca implementadas na plataforma AutoRevenda, incluindo seguranca de dados, seguranca da aplicacao, controles operacionais, auditoria, analise estatica de codigo, analise de dependencias e verificacoes de qualidade executadas na pipeline.

O objetivo e demonstrar que a aplicacao possui controles tecnicos para proteger dados pessoais, reduzir riscos operacionais e simular um processo de deploy mais seguro.

## 2. Escopo da Analise

Componentes avaliados:

- Aplicacao Django e Django REST Framework.
- Apps `veiculos`, `compradores` e `vendas`.
- Fluxo SAGA de compra/venda.
- Banco de dados SQLite local e PostgreSQL gerenciado em producao.
- Configuracoes de producao para Render.
- Pipeline GitHub Actions.
- Dependencias Python declaradas em `requirements.txt`.

## 3. Dados Armazenados

### 3.1 Veiculos

| Dado | Sensibilidade | Tratamento |
|---|---|---|
| Marca, modelo, ano, cor | Publica | Texto plano |
| Preco | Publica/comercial | Decimal |
| Placa | Moderada | Texto unico |
| Chassi | Moderada | Texto unico |
| Quilometragem | Publica | Inteiro |
| Status | Operacional | Enum |

### 3.2 Compradores

| Dado | Sensibilidade | Tratamento |
|---|---|---|
| Nome | Pessoal | Texto plano |
| Email | Pessoal | Texto plano com unicidade |
| Telefone | Pessoal | Texto plano |
| Endereco, cidade, estado, CEP | Pessoal | Texto plano |
| Data de nascimento | Pessoal | Data |
| CPF | Identificador critico | Hash SHA-256 + CPF mascarado |
| RG | Identificador critico | Hash SHA-256 |

### 3.3 Vendas

| Dado | Sensibilidade | Tratamento |
|---|---|---|
| Veiculo e comprador | Operacional/pessoal | Referencias por UUID |
| Status da venda | Operacional | Enum |
| Codigo de pagamento | Confidencial | UUID |
| Preco de venda | Comercial | Decimal |
| Historico da venda | Auditoria | Registro imutavel de transicoes |
| Timestamps | Auditoria | Datas automaticas |

## 4. Controles de Protecao de Dados

### 4.1 Mascaramento de CPF

O sistema nao exibe o CPF completo na interface nem na API de leitura. A tela de compradores mostra apenas o CPF mascarado.

Exemplo:

```text
***.***.*47-25
```

Arquivos relacionados:

```text
compradores/serializers.py
revenda_veiculos/forms.py
templates/compradores/list.html
```

### 4.2 Hash de CPF e RG

CPF e RG sao recebidos no cadastro e convertidos em hash SHA-256 antes do armazenamento.

Arquivos relacionados:

```text
compradores/serializers.py
revenda_veiculos/forms.py
compradores/models.py
```

Observacao de risco residual:

> Para o escopo academico, SHA-256 demonstra protecao contra exposicao direta dos documentos. Para producao, recomenda-se evoluir para HMAC com segredo/salt ou algoritmo resistente a ataques por dicionario, como bcrypt ou argon2.

### 4.3 Controle de Exposicao na API

O projeto usa serializers diferentes para escrita e leitura:

- `CompradorCreateSerializer`: recebe CPF/RG como `write_only`.
- `CompradorSerializer`: retorna apenas `cpf_masked`, sem CPF/RG em texto puro.

Com isso, os documentos completos sao usados somente no momento do cadastro.

### 4.4 Campos Sensíveis no Admin

No Django Admin, os campos `cpf_hash`, `cpf_masked` e `rg_hash` sao definidos como somente leitura.

Arquivo relacionado:

```text
compradores/admin.py
```

## 5. Seguranca da Aplicacao

### 5.1 CSRF

Os formularios Django usam token CSRF, protegendo contra Cross-Site Request Forgery.

Arquivos relacionados:

```text
templates/form.html
templates/vendas/detail.html
revenda_veiculos/settings.py
```

Middleware:

```python
django.middleware.csrf.CsrfViewMiddleware
```

### 5.2 Protecao contra SQL Injection

O projeto utiliza Django ORM e nao usa queries SQL raw. Isso reduz risco de injecao SQL por meio de queries parametrizadas pelo framework.

### 5.3 UUID como Identificador

Os modelos principais usam `UUIDField` como chave primaria. Isso reduz risco de enumeracao sequencial de IDs.

Arquivos relacionados:

```text
veiculos/models.py
compradores/models.py
vendas/models.py
```

### 5.4 Headers e Cookies de Producao

Quando `DEBUG=False`, o projeto ativa controles de seguranca:

- `SECURE_SSL_REDIRECT`
- `SESSION_COOKIE_SECURE`
- `CSRF_COOKIE_SECURE`
- `X_FRAME_OPTIONS = DENY`
- `SECURE_HSTS_SECONDS`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS`
- `SECURE_HSTS_PRELOAD`

Arquivo relacionado:

```text
revenda_veiculos/settings.py
```

Observacao:

> Em ambiente local, a demonstracao roda com `DEBUG=True`. Em producao, no Render, a aplicacao deve rodar com `DEBUG=False` e HTTPS/TLS gerenciado pela plataforma.

## 6. Seguranca Operacional e Infraestrutura

### 6.1 Render Web Service

O deploy previsto usa Render como PaaS gerenciado, reduzindo necessidade de administrar servidores, sistema operacional, patches e certificados manualmente.

### 6.2 HTTPS/TLS Gerenciado

O Render fornece HTTPS/TLS com certificados gerenciados, protegendo a comunicacao entre navegador e aplicacao.

### 6.3 Banco Gerenciado

Em producao, a aplicacao usa PostgreSQL gerenciado pelo Render via `DATABASE_URL`.

Beneficios:

- banco relacional com transacoes ACID;
- conexao gerenciada;
- isolamento operacional;
- adequado ao uso de `transaction.atomic()` e `select_for_update()`.

## 7. SAGA, Consistencia e Auditoria

### 7.1 Fluxo da Venda

O processo de venda segue os estados:

```text
selecionado -> reservado -> pagamento_pendente -> pago -> concluido
```

Tambem permite cancelamento antes da conclusao.

### 7.2 Transacoes Atomicas

As etapas da SAGA sao protegidas por `transaction.atomic()`.

Arquivo:

```text
vendas/services.py
```

### 7.3 Controle de Concorrencia

O projeto usa `select_for_update()` para bloquear registros durante etapas criticas, reduzindo risco de dois compradores reservarem o mesmo veiculo.

### 7.4 Compensacao

Em caso de cancelamento, reserva expirada ou falha no processo, a venda e cancelada e o veiculo pode ser liberado novamente.

### 7.5 Auditoria

Todas as transicoes relevantes sao registradas em `HistoricoVenda`, contendo:

- status anterior;
- status novo;
- descricao;
- timestamp.

Isso permite rastrear o ciclo de vida da venda e demonstrar governanca operacional.

## 8. Pipeline de Seguranca e Qualidade

A pipeline criada em `.github/workflows/ci.yml` possui etapas separadas para qualidade, testes, SAST, SCA e prontidao de deploy.

### 8.1 Qualidade de Codigo

Ferramentas:

- `ruff`
- `black`

Comandos:

```bash
ruff check compradores veiculos vendas revenda_veiculos manage.py
black --check compradores veiculos vendas revenda_veiculos manage.py
```

Objetivo:

- padronizar codigo;
- evitar imports nao usados;
- detectar problemas simples antes do deploy.

### 8.2 Testes Automatizados e Cobertura

Ferramentas:

- `coverage`
- `manage.py test`

Comando:

```bash
coverage run --source=compradores,veiculos,vendas,revenda_veiculos manage.py test
coverage report --fail-under=70
```

Resultado validado localmente:

```text
9 testes executados
Coverage total: 73%
Limite minimo: 70%
```

### 8.3 SAST - Static Application Security Testing

Ferramenta:

- `bandit`

Comando:

```bash
bandit -r compradores veiculos vendas revenda_veiculos -c pyproject.toml -f json -o bandit-report.json
```

Objetivo:

- identificar padroes inseguros em codigo Python;
- gerar relatorio em JSON como artifact da pipeline.

Resultado validado localmente:

```text
Bandit executado com sucesso.
```

### 8.4 SCA - Software Composition Analysis e SBOM

Ferramenta:

- `pip-audit`
- SBOM em formato CycloneDX JSON

Comando:

```bash
pip-audit -r requirements.txt --format=json --output=pip-audit-report.json
pip-audit -r requirements.txt --format=cyclonedx-json --output=sbom.cdx.json
```

Objetivo:

- verificar vulnerabilidades conhecidas nas dependencias Python.
- gerar inventario de componentes de software para rastreabilidade de supply chain.
- manter evidencia auditavel da composicao da aplicacao.

Resultado validado localmente:

```text
No known vulnerabilities found
```

Artifact gerado:

```text
sbom-cyclonedx-json
```

O SBOM ajuda a responder quais componentes e versoes fazem parte da aplicacao em cada execucao da pipeline.

### 8.5 GitHub Actions Summary

A pipeline escreve evidencias no `GITHUB_STEP_SUMMARY`, criando um resumo visual no proprio GitHub Actions.

O summary inclui:

- resultado de qualidade de codigo;
- cobertura de testes;
- metricas do SAST;
- metricas do SCA;
- quantidade de componentes no SBOM;
- status consolidado dos gates;
- lista de artifacts de evidencia.

Essa etapa facilita auditoria e demonstracao, pois permite visualizar rapidamente se a aplicacao esta pronta para deploy.

### 8.6 Deploy Readiness

Etapa final da pipeline. Roda apenas depois de qualidade, testes, SAST e SCA.

Comandos:

```bash
python manage.py check --deploy
python manage.py makemigrations --check --dry-run
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

Objetivo:

- validar configuracoes de producao;
- garantir ausencia de migrations pendentes;
- simular coleta de arquivos estaticos;
- simular aplicacao de migrations antes do deploy.

## 9. Dependabot

O projeto possui Dependabot configurado em:

```text
.github/dependabot.yml
```

Ecossistemas monitorados:

- `pip`
- `github-actions`

Frequencia:

```text
semanal
```

Objetivo:

- manter dependencias atualizadas;
- receber pull requests automaticos para novas versoes;
- melhorar postura de seguranca ao longo do tempo.

## 10. Riscos Residuais

| Risco | Impacto | Mitigacao Atual | Evolucao Recomendada |
|---|---:|---|---|
| API aberta | Alto | Uso academico e demonstracao | JWT/OAuth2, permissoes por perfil e rate limiting |
| Hash de CPF/RG sem salt | Medio | Hash SHA-256 e mascaramento | HMAC com segredo/salt ou bcrypt/argon2 |
| Dados pessoais em texto plano | Medio | Coleta minima para o processo | Criptografia em campo para endereco/telefone em producao |
| Ambiente free instavel | Baixo/medio | Deploy local para video e Render para demonstracao | Plano pago ou plataforma com SLA |
| Sem logs centralizados | Medio | HistoricoVenda no banco | Observabilidade com logs estruturados e alertas |

## 11. Conclusao

A plataforma AutoRevenda possui controles de seguranca coerentes com o escopo academico:

- protecao de documentos com hash e mascaramento;
- API de leitura sem exposicao de CPF/RG completos;
- formularios com CSRF;
- UUIDs como identificadores;
- ORM para reduzir risco de SQL Injection;
- transacoes atomicas e locks pessimistas no fluxo SAGA;
- auditoria por historico de venda;
- configuracoes de producao com HTTPS, HSTS, cookies seguros e anti-clickjacking;
- pipeline com qualidade, testes, cobertura, SAST, SCA, SBOM, summary e verificacao de deploy.

Como evolucao para ambiente produtivo real, recomenda-se adicionar autenticacao, autorizacao por perfil, rate limiting, logs centralizados, criptografia adicional para dados pessoais e fortalecimento do hash de documentos com segredo/salt.
