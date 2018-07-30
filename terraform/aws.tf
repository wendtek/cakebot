provider "aws" {
  region = "${var.aws_region}"
}

terraform {
  backend "s3" {
    bucket = "wendtek-terraform"
    key    = "cakebot.tfstate"
    region = "us-east-1"
  }
}
