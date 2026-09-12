data "aws_iam_policy_document" "xero_lambda" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "xero_lambda_access_secrets" {
  statement {
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:PutSecretValue"
    ]
    effect = "Allow"
    resources = [
      aws_secretsmanager_secret.xero_lambda.arn,
      aws_secretsmanager_secret.xero_oauth_token.arn
    ]
  }
}

resource "aws_iam_role_policy" "xero_lambda_access_secrets" {
  name   = "xero_lambda_access_secrets"
  role   = aws_iam_role.xero_lambda.id
  policy = data.aws_iam_policy_document.xero_lambda_access_secrets.json
}

resource "aws_iam_role" "xero_lambda" {
  name               = "xero_lambda"
  assume_role_policy = data.aws_iam_policy_document.xero_lambda.json
}

resource "aws_iam_role_policy_attachment" "xero_lambda_basic" {
  role       = aws_iam_role.xero_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "scheduler" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy" "scheduler" {
  name   = "xero_lambda_scheduler"
  role   = aws_iam_role.scheduler.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["lambda:InvokeFunction"]
        Effect   = "Allow"
        Resource = aws_lambda_function.xero_lambda.arn
      },
    ]
  })
}

resource "aws_iam_role" "scheduler" {
  name               = "xero_lambda_scheduler"
  assume_role_policy = data.aws_iam_policy_document.scheduler.json
}
