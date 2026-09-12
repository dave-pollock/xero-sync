# Xero Sync

Syncs orders and transactions from Wix and Stripe to Xero.

## Running
1. Set the following environment variables or put them in a `.env` file:
   - `XERO_ACCOUNT_ID`: The ID of a Xero account where transactions will be synced to.
   - `XERO_CONTACT_ID_STRIPE`: The UUID of a contact ID in Xero which will be associated with any Stripe fees.
1. Authenticate with AWS:
   ```
   aws login --remote
   ```
1. If it's the first time the sync is run, the AWS secret will need to be pre-populated by applying the secrets
   manager part of the Terraform code (see Deploying section below).
1. Run `main.py`.

## Packaging
1. Run the `./package.sh` script to package the lambda ready for deployment.

## Deploying
1. Set the following environment variables or put them in a `.env` file:
   - `AWS_REGION`: The AWS region to deploy the cloudfunction to.
   - `TF_VAR_stripe_api_token`: The Stripe API token
   - `TF_VAR_wix_api_token`: The Wix API token
   - `TF_VAR_wix_site_id`: The Wix site id
   - `TF_VAR_xero_client_id`: The Xero client id
   - `TF_VAR_xero_client_secret`: The Xero client secret
   - `TF_VAR_xero_tenant_id`: The Xero tenant id
   - `TF_VAR_xero_contact_id_stripe`: The Xero contact id which will Stripe fees will be associated with
   - `TF_VAR_xero_account_id`: The Xero account id which bank transactions will be associated with
1. Create a `providers.tf` file in the `terraform` folder with the following contents (modify as required).
   ```
   terraform {
      backend "s3" {
         bucket = ""
         key = ""
      }

      required_providers {
         aws = {
            source  = "hashicorp/aws"
            version = "~> 5.0"
         }
      }
   }

   provider "aws" {
   }
   ```
1. Run the deploy script.
   ```
   ./deploy.sh
   ```
