resource "aws_scheduler_schedule" "xero_lambda" {
  name       = "xero_lambda"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "rate(1 days)"

  target {
    arn      = aws_lambda_function.xero_lambda.arn
    role_arn = aws_iam_role.scheduler.arn
  }
}