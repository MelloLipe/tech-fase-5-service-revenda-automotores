resource "aws_cloudwatch_event_bus" "saga" {
  name = "${local.name_prefix}-saga"
}

resource "aws_sqs_queue" "saga_dlq" {
  name              = "${local.name_prefix}-saga-dlq"
  kms_master_key_id = aws_kms_key.main.arn
}

resource "aws_sqs_queue" "saga" {
  name                       = "${local.name_prefix}-saga"
  visibility_timeout_seconds = 60
  message_retention_seconds  = 345600
  kms_master_key_id          = aws_kms_key.main.arn

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.saga_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_cloudwatch_event_rule" "saga_events" {
  name           = "${local.name_prefix}-saga-events"
  description    = "Roteia eventos do fluxo SAGA para fila de processamento"
  event_bus_name = aws_cloudwatch_event_bus.saga.name

  event_pattern = jsonencode({
    source = ["autorevenda.vendas"]
  })
}

resource "aws_cloudwatch_event_target" "saga_queue" {
  rule           = aws_cloudwatch_event_rule.saga_events.name
  event_bus_name = aws_cloudwatch_event_bus.saga.name
  arn            = aws_sqs_queue.saga.arn
}

resource "aws_sqs_queue_policy" "saga" {
  queue_url = aws_sqs_queue.saga.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "events.amazonaws.com"
      }
      Action   = "sqs:SendMessage"
      Resource = aws_sqs_queue.saga.arn
      Condition = {
        ArnEquals = {
          "aws:SourceArn" = aws_cloudwatch_event_rule.saga_events.arn
        }
      }
    }]
  })
}
