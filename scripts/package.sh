#!/bin/bash

set -e

PROJECT_DIR=$(git rev-parse --show-toplevel)
PACKAGE_FILE=$PROJECT_DIR/terraform/package.zip
VENV_DIR=$(pipenv --venv)

echo "Packaging app code"
cd $PROJECT_DIR && zip $PACKAGE_FILE ./*.py
echo "Packaging dependencies"
cd $VENV_DIR/lib/python3.6/site-packages && zip $PACKAGE_FILE ./*
