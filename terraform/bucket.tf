resource "aws_s3_bucket" "sometest" {
  bucket = "us-marcyoung-sometest"
  acl    = "private"

  tags = {
    Name       = "us-marcyoung-sometest"
    managed_by = "terraform"
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
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
