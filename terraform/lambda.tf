data "archive_file" "xero_lambda" {
  type        = "zip"
  source_dir  = "${path.module}/package"
  output_path = "${path.module}/xero_lambda.zip"
}

resource "aws_lambda_function" "xero_lambda" {
  filename         = data.archive_file.xero_lambda.output_path
  function_name    = "xero_lambda"
  role             = aws_iam_role.xero_lambda.arn
  handler          = "lambda_handler.lambda_handler"
  source_code_hash = data.archive_file.xero_lambda.output_base64sha256
  runtime          = "python3.13"
  publish          = true
  timeout          = 300
}
