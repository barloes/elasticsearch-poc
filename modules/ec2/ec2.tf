resource "aws_instance" "ec2" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.key_name
  subnet_id                   = var.subnet_id
  user_data                   = data.template_file.init.rendered
  vpc_security_group_ids      = [aws_security_group.main.id]
  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.iam_profile.name

  credit_specification {
    cpu_credits = "standard"
  }

  tags = {
    Name = var.project_name
  }

  lifecycle {
    ignore_changes = [instance_state]
  }
}


