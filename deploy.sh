#!/bin/bash

cd terraform
terraform init -reconfigure
terraform apply -auto-approve
cd ..
