#!/bin/bash

set -e

PROJECT_DIR=$(git rev-parse --show-toplevel)
PACKAGE_FILE=$PROJECT_DIR/package.zip

[ -f $PACKAGE_FILE ]

source $PROJECT_DIR/scripts/setenv.sh

if [[ $TRAVIS = "true" ]] ; then
  echo "Downloading Terraform..."
  curl -LO $TERRAFORM_ZIP_URL
  unzip terraform*.zip -d ./
  export PATH="$PATH:$PROJECT_DIR"
fi


echo "Starting terraform deploy..."
cd $PROJECT_DIR/terraform
terraform init
terraform plan -out tfplan

if [[ $1 = "--plan-only" ]] ; then
  echo "Exiting without apply Terraform changes because \"--plan-only\" was specified."
else
  terraform apply tfplan
  echo "Terraform deployed successfully!"
fi
