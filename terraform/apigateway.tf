data "template_file" "lambda_cakebot_swagger" {
  template = "${file("swagger.json")}"

  vars {
    lambda_arn = "${aws_lambda_function.lambda_cakebot.arn}"
  }
}

resource "aws_api_gateway_rest_api" "lambda_cakebot" {
  name        = "lambda_cakebot_terraform"
  description = "Cakebot managed by Terraform"
  body        = "${data.template_file.lambda_cakebot_swagger.rendered}"
}

resource "aws_api_gateway_deployment" "production" {
  depends_on  = ["aws_api_gateway_rest_api.lambda_cakebot"]
  rest_api_id = "${aws_api_gateway_rest_api.lambda_cakebot.id}"
  stage_name  = "production"
}

resource "aws_lambda_permission" "lambda_permission" {
  action        = "lambda:InvokeFunction"
  function_name = "lambda_cakebot"
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.lambda_cakebot.execution_arn}/*/*/*"
}
