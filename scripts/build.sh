#!/bin/bash

set -e

PROJECT_DIR=$(git rev-parse --show-toplevel)

cd $PROJECT_DIR
pipenv install --skip-lock
