resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${local.name_prefix}-vpc"
  }
}

resource "aws_subnet" "private" {
  for_each = {
    for index, az in local.azs : az => index
  }

  vpc_id                  = aws_vpc.main.id
  availability_zone       = each.key
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, each.value + 10)
  map_public_ip_on_launch = false

  tags = {
    Name = "${local.name_prefix}-private-${each.value + 1}"
    Tier = "private"
  }
}

resource "aws_security_group" "lambda" {
  name        = "${local.name_prefix}-lambda-sg"
  description = "Permite saida da Lambda para servicos internos"
  vpc_id      = aws_vpc.main.id

  egress {
    description = "Saida HTTPS e banco via VPC"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.vpc_cidr]
  }

  tags = {
    Name = "${local.name_prefix}-lambda-sg"
  }
}

resource "aws_security_group" "database" {
  name        = "${local.name_prefix}-database-sg"
  description = "Acesso PostgreSQL apenas pela Lambda"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "PostgreSQL a partir da Lambda"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda.id]
  }

  tags = {
    Name = "${local.name_prefix}-database-sg"
  }
}

resource "aws_security_group" "vpc_endpoints" {
  name        = "${local.name_prefix}-vpc-endpoints-sg"
  description = "Permite Lambda acessar endpoints privados da AWS"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "HTTPS a partir da Lambda"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda.id]
  }

  tags = {
    Name = "${local.name_prefix}-vpc-endpoints-sg"
  }
}

resource "aws_vpc_endpoint" "interface" {
  for_each = toset([
    "events",
    "kms",
    "logs",
    "secretsmanager",
    "sqs"
  ])

  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${data.aws_region.current.name}.${each.key}"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = values(aws_subnet.private)[*].id
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true

  tags = {
    Name = "${local.name_prefix}-${each.key}-endpoint"
  }
}
