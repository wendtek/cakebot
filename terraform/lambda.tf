resource "aws_lambda_function" "lambda_cakebot" {
  filename         = "../package.zip"
  source_code_hash = "${base64sha256(file("../package.zip"))}"
  function_name    = "lambda_cakebot"
  role             = "${aws_iam_role.lambda_cakebot.arn}"
  handler          = "app.handler"
  runtime          = "python3.6"
  timeout          = "${var.timeout}"
  memory_size      = "${var.memory_size}"
  description      = "Scrapes Fooda and posts to Slack"

  environment {
    variables = {
      FOODA_ACCOUNT_ID         = "${var.FOODA_ACCOUNT_ID}"
      FOODA_BUILDING_ID        = "${var.FOODA_BUILDING_ID}"
      FOODA_SEED_EVENT_ID      = "${var.FOODA_SEED_EVENT_ID}"
      SLACK_BOT_OAUTH_TOKEN    = "${var.SLACK_BOT_OAUTH_TOKEN}"
      SLACK_VERIFICATION_TOKEN = "${var.SLACK_VERIFICATION_TOKEN}"
      SLACK_WEBHOOK_URL        = "${var.SLACK_WEBHOOK_URL}"
      LOG_LEVEL                = "${var.LOG_LEVEL}"
      RUNTIME_ENVIRONMENT      = "lambda"
    }
  }
}
