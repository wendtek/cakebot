#!/bin/bash

set -e

PROJECT_DIR=$(git rev-parse --show-toplevel)
PACKAGE_FILE=$PROJECT_DIR/package.zip

[ -f $PACKAGE_FILE ]

source $PROJECT_DIR/script/setenv.sh

#echo "Starting terraform deploy..."
#cd $PROJECT_DIR/terraform
#terraform init
#terraform apply --auto-approve
#
#echo "Terraform deployed successfully!"
