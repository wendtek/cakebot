#!/bin/bash

set -e

PROJECT_DIR=$(git rev-parse --show-toplevel)
PACKAGE_FILE=$PROJECT_DIR/package.zip
DEP_DIR=$(pipenv run python -c "import sys ; [print(x) for x in sys.path if x.endswith('site-packages')]")

rm -f $PACKAGE_FILE

echo "Packaging app code..."
cd $PROJECT_DIR && zip -r $PACKAGE_FILE ./*.py ./*/*.py

echo "Packaging dependencies..."
cd $DEP_DIR && zip -r $PACKAGE_FILE ./*
