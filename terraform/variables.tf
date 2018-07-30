variable aws_region {
  default = "us-east-1"
}

variable timeout {
  default = "30"
}

variable memory_size {
  default = "1024"
}

# Environment variables. Override by setting TF_VAR_<VARIABLE_NAME>

variable FOODA_ACCOUNT_ID {}
variable FOODA_BUILDING_ID {}
variable FOODA_SEED_EVENT_ID {}
variable SLACK_BOT_OAUTH_TOKEN {}
variable SLACK_VERIFICATION_TOKEN {}
variable SLACK_WEBHOOK_URL {}
variable LOG_LEVEL { default = "INFO" }
