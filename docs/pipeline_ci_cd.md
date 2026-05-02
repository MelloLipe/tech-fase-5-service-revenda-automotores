# Pipeline CI/CD - Qualidade, Seguranca e Prontidao de Deploy

Este projeto possui uma pipeline no GitHub Actions em:

```text
.github/workflows/ci.yml
```

O objetivo e simular um processo de deploy bem estruturado antes da publicacao no Render.

## Disparo do Workflow

A pipeline foi configurada para evitar execucoes duplicadas:

- `push`: roda apenas nas branches `main` e `develop`;
- `pull_request`: roda quando um PR aponta para `main` ou `develop`;
- `concurrency`: cancela uma execucao antiga quando um novo commit chega para o mesmo PR ou branch.

Assim, uma branch de trabalho como `devin/1776620241-fase5-revenda-veiculos` executa a pipeline pelo PR, sem disparar outra execucao redundante por push.

## Etapas da Pipeline

## 1. Code Quality - Ruff and Black

Valida qualidade e padronizacao do codigo da aplicacao Django.

Ferramentas:

- `ruff`: lint estatico para encontrar imports nao usados, problemas simples de codigo e padroes ruins.
- `black`: valida se o codigo esta formatado de forma padronizada.

Comandos:

```bash
ruff check compradores veiculos vendas revenda_veiculos manage.py
black --check compradores veiculos vendas revenda_veiculos manage.py
```

## 2. Application Tests and Coverage

Executa os testes automatizados da aplicacao e mede cobertura.

Ferramentas:

- `coverage`: executa os testes Django e calcula cobertura.
- `manage.py test`: roda os testes unitarios e de API.

Comandos:

```bash
python manage.py migrate --noinput
coverage run --source=compradores,veiculos,vendas,revenda_veiculos manage.py test
coverage report --fail-under=70
coverage xml
```

Resultado validado localmente:

```text
9 testes executados
Coverage total: 73%
Limite minimo configurado: 70%
```

## 3. SAST - Bandit

Executa analise estatica de seguranca no codigo Python.

Ferramenta:

- `bandit`: procura vulnerabilidades comuns em codigo Python, como uso inseguro de funcoes, hardcoded secrets, execucao dinamica e padroes de risco.

Comando:

```bash
bandit -r compradores veiculos vendas revenda_veiculos -c pyproject.toml -f json -o bandit-report.json
```

O relatorio e salvo como artifact da pipeline:

```text
bandit-sast-report
```

## 4. SCA - Dependency Vulnerability Scan e SBOM

Executa analise de componentes de software, procurando vulnerabilidades conhecidas nas dependencias, e gera um SBOM para inventariar a cadeia de dependencias.

Ferramenta:

- `pip-audit`: consulta bases de vulnerabilidades para pacotes Python.
- `CycloneDX JSON`: formato usado para gerar o SBOM.

Comando:

```bash
pip-audit -r requirements.txt --format=json --output=pip-audit-report.json
pip-audit -r requirements.txt --format=cyclonedx-json --output=sbom.cdx.json
```

Os relatorios sao salvos como artifacts da pipeline:

```text
pip-audit-sca-report
sbom-cyclonedx-json
```

Resultado validado localmente:

```text
No known vulnerabilities found
```

## 5. GitHub Actions Summary

Cada job escreve um resumo no `GITHUB_STEP_SUMMARY`, que aparece na pagina da execucao do workflow.

O summary consolida:

- resultado de lint e formatacao;
- tabela de cobertura de testes;
- metricas do Bandit;
- quantidade de dependencias auditadas;
- quantidade de vulnerabilidades encontradas;
- quantidade de componentes no SBOM;
- status final de cada stage.

Isso facilita a demonstracao no video, porque a evidencia fica visivel no proprio GitHub Actions, sem precisar abrir cada artifact manualmente.

## 6. Deploy Readiness - Django and Render Simulation

Simula as etapas importantes antes do deploy no Render.

Essa etapa roda apenas se qualidade, testes, SAST, SCA e SBOM passarem.

Valida:

- configuracoes de producao do Django;
- migrations pendentes;
- coleta de arquivos estaticos;
- aplicacao das migrations no banco.

Comandos:

```bash
python manage.py check --deploy
python manage.py makemigrations --check --dry-run
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

## Dependabot

Tambem foi configurado:

```text
.github/dependabot.yml
```

Ele monitora semanalmente:

- dependencias Python (`pip`);
- GitHub Actions.

Isso ajuda a manter as dependencias atualizadas e abre pull requests automaticos quando houver novas versoes.

## Ordem Recomendada Para Apresentacao

1. Mostrar o arquivo `.github/workflows/ci.yml`.
2. Explicar que a pipeline evita duplicidade: push apenas em `main/develop`, PR para `main/develop` e cancelamento automatico de execucoes antigas.
3. Mostrar a etapa de qualidade com `ruff` e `black`.
4. Mostrar os testes e a cobertura minima de 70%.
5. Mostrar SAST com `bandit`.
6. Mostrar SCA com `pip-audit`.
7. Mostrar SBOM CycloneDX como artifact.
8. Mostrar o GitHub Actions Summary consolidado.
9. Mostrar a etapa final de prontidao de deploy simulando Render.
10. Explicar que o deploy real no Render deve ocorrer somente depois dessas etapas passarem.
