data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_region" "current" {}

locals {
  name_prefix = "${var.project_name}-${var.environment}"

  azs = slice(data.aws_availability_zones.available.names, 0, 2)

  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Workload    = "revenda-automotores"
  }

  lambda_environment = {
    DJANGO_SETTINGS_MODULE = "revenda_veiculos.settings"
    DEBUG                  = "False"
    DATABASE_SECRET_ARN    = aws_secretsmanager_secret.database.arn
    EVENT_BUS_NAME         = aws_cloudwatch_event_bus.saga.name
    SAGA_QUEUE_URL         = aws_sqs_queue.saga.url
  }
}
