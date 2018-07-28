#!/bin/bash

set -e

PROJECT_DIR=$(git rev-parse --show-toplevel)
cd $PROJECT_DIR

echo "Setting environment variables"
source scripts/setenv.sh
echo $SLACK_WEBHOOK_URL
pipenv run python app.py
