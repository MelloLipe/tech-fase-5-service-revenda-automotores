variable "project_name" {
  description = "Nome curto do projeto usado nos recursos."
  type        = string
  default     = "autorevenda"
}

variable "environment" {
  description = "Ambiente logico da infraestrutura."
  type        = string
  default     = "reference"
}

variable "aws_region" {
  description = "Regiao principal para os recursos regionais."
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR da VPC usada por Lambda e Aurora."
  type        = string
  default     = "10.40.0.0/16"
}

variable "lambda_package_path" {
  description = "Caminho para o pacote .zip da Lambda. Necessario apenas para provisionamento real."
  type        = string
  default     = "build/lambda.zip"
}

variable "database_name" {
  description = "Nome do banco PostgreSQL."
  type        = string
  default     = "autorevenda"
}

variable "database_master_username" {
  description = "Usuario administrador inicial do Aurora."
  type        = string
  default     = "autorevenda_admin"
}

variable "allowed_origins" {
  description = "Origens permitidas para CORS no API Gateway."
  type        = list(string)
  default     = ["https://example.com"]
}

variable "alarm_email" {
  description = "Email opcional para alarmes. Quando vazio, nao cria subscription."
  type        = string
  default     = ""
}
