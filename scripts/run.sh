#!/bin/bash

set -e

PROJECT_DIR=$(git rev-parse --show-toplevel)
cd $PROJECT_DIR

pwd

if ! [[ $TRAVIS = "true" ]] ; then
  echo "Setting local env vars"
  source scripts/localenv.sh
fi

pipenv run python app.py
