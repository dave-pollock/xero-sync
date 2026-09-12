resource "aws_secretsmanager_secret" "xero_lambda" {
  name = "xero_lambda"
}

resource "aws_secretsmanager_secret_version" "xero_lambda" {
  secret_id     = aws_secretsmanager_secret.xero_lambda.id
  secret_string = jsonencode({
    xero_account_id = var.xero_account_id
    xero_client_id     = var.xero_client_id
    xero_client_secret = var.xero_client_secret
    xero_contact_id_stripe = var.xero_contact_id_stripe
    xero_tenant_id = var.xero_tenant_id
    stripe_api_token = var.stripe_api_token
    wix_api_token = var.wix_api_token
    wix_site_id = var.wix_site_id
  })
}

resource "aws_secretsmanager_secret" "xero_oauth_token" {
  name = "xero_lambda_oauth_token"
}
