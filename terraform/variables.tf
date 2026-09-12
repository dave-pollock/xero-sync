variable "xero_client_id" {
    description = "The Xero client id"
    sensitive   = true
}

variable "xero_client_secret" {
    description = "The Xero client secret"
    sensitive   = true
}

variable "xero_tenant_id" {
    description = "The Xero tenant id"
    sensitive   = true
}

variable "xero_contact_id_stripe" {
    description = "The id of the Xero contact id which will be associated with Stripe fees"
}

variable "xero_account_id" {
    description = "The Xero account id where bank transactions will be synced to"
}

variable "stripe_api_token" {
    description = "The Stripe API token"
    sensitive   = true
}

variable "wix_api_token" {
    description = "The Wix API token"
    sensitive   = true
}

variable "wix_site_id" {
    description = "The Wix site id"
    sensitive   = true
}
