#!/bin/bash

set -e

PROJECT_DIR=$(git rev-parse --show-toplevel)
PACKAGE_FILE=$PROJECT_DIR/terraform/package.zip

# terraform apply
