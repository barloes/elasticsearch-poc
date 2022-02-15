data "template_file" "init" {
  template = file("${path.module}/init-script.sh")
  vars = {
    NAME         = "${var.bucket_name}",
    PROJECT_NAME = "${var.project_name}",
    AWS_ID       = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${data.aws_region.current.name}.amazonaws.com",
    AZ           = "${var.az}"
  }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
