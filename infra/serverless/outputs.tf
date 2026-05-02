output "api_endpoint" {
  description = "Endpoint HTTP da API Gateway."
  value       = aws_apigatewayv2_api.http.api_endpoint
}

output "cloudfront_domain_name" {
  description = "Dominio CloudFront do frontend estatico."
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "frontend_bucket_name" {
  description = "Bucket S3 do frontend."
  value       = aws_s3_bucket.frontend.bucket
}

output "database_cluster_endpoint" {
  description = "Endpoint do Aurora Serverless v2."
  value       = aws_rds_cluster.main.endpoint
  sensitive   = true
}

output "database_secret_arn" {
  description = "ARN do segredo com credenciais do banco."
  value       = aws_secretsmanager_secret.database.arn
}

output "saga_event_bus_name" {
  description = "Nome do EventBridge Bus usado pela SAGA."
  value       = aws_cloudwatch_event_bus.saga.name
}

output "saga_queue_url" {
  description = "URL da fila SQS da SAGA."
  value       = aws_sqs_queue.saga.url
}
