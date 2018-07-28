#!/bin/bash

PROJECT_DIR=$(git rev-parse --show-toplevel)

if ! [[ $TRAVIS = "true" ]] ; then
  echo "Setting local environment variables"
  # expects a localsecrts.sh file to supply SLACK_ env vars
  source $PROJECT_DIR/scripts/localsecrets.sh
fi

export TF_VAR_FOODA_ACCOUNT_ID=$FOODA_ACCOUNT_ID
export TF_VAR_FOODA_BUILDING_ID=$FOODA_BUILDING_ID
export TF_VAR_FOODA_SEED_EVENT_ID=$FOODA_SEED_EVENT_ID
export TF_VAR_SLACK_BOT_OAUTH_TOKEN=$SLACK_BOT_OAUTH_TOKEN
export TF_VAR_SLACK_VERIFICATION_TOKEN=$SLACK_VERIFICATION_TOKEN
export TF_VAR_SLACK_WEBHOOK_URL=$SLACK_WEBHOOK_URL
