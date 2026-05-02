resource "aws_kms_key" "main" {
  description             = "Chave KMS para criptografia da plataforma AutoRevenda"
  deletion_window_in_days = 10
  enable_key_rotation     = true
}

resource "aws_kms_alias" "main" {
  name          = "alias/${local.name_prefix}"
  target_key_id = aws_kms_key.main.key_id
}

resource "aws_secretsmanager_secret" "database" {
  name        = "${local.name_prefix}/database"
  description = "Credenciais do Aurora PostgreSQL"
  kms_key_id  = aws_kms_key.main.arn
}

resource "random_password" "database_master" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_secretsmanager_secret_version" "database" {
  secret_id = aws_secretsmanager_secret.database.id

  secret_string = jsonencode({
    username = var.database_master_username
    password = random_password.database_master.result
    engine   = "postgres"
    host     = aws_rds_cluster.main.endpoint
    port     = 5432
    dbname   = var.database_name
  })
}
