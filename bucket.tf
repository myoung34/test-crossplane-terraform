provider "aws" {
    region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "us-marcyoung-crossplane"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_s3_bucket" "sometest" {
  bucket = "us-marcyoung-sometest"
  acl    = "private"

  tags = {
    Name       = "us-marcyoung-sometest"
    managed_by = "terraform"
  }

  lifecycle_rule {
    enabled                                = true
    prefix                                 = ""
    abort_incomplete_multipart_upload_days = 1

    expiration {
      days                         = 1
      expired_object_delete_marker = true
    }
  }
}
