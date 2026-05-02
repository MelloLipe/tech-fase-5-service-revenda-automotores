# Serverless Reference Infrastructure

Esta pasta descreve, em Terraform, a arquitetura cloud serverless pensada para a plataforma de revenda de veiculos. Ela nao precisa ser aplicada para o trabalho funcionar localmente; serve como evidencia tecnica de como a solucao poderia evoluir para producao em nuvem.

## Componentes

- CloudFront + WAF para borda, TLS, cache e protecao OWASP.
- S3 para frontend estatico, caso o frontend seja separado do Django.
- API Gateway HTTP API para expor rotas REST.
- AWS Lambda para executar os casos de uso da aplicacao sob demanda.
- EventBridge + SQS + DLQ para eventos da SAGA e retentativas.
- Aurora Serverless v2 PostgreSQL para dados relacionais com transacoes ACID.
- Secrets Manager + KMS para segredos e criptografia.
- CloudWatch para logs, metricas e alarmes.

## Como validar sem provisionar

```bash
cd infra/serverless
terraform fmt -recursive
terraform init -backend=false
terraform validate
```

## Como seria um plano real

Antes de rodar `plan` ou `apply`, crie um pacote Lambda e informe o caminho na variavel `lambda_package_path`.

```bash
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
```

## Observacao importante

Esta infra e uma referencia arquitetural. O projeto executavel continua usando Django local/Render para permitir demonstracao gratuita e gravacao do video sem provisionar recursos pagos.
