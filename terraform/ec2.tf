data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_vpc" "video_vpc" {
  cidr_block = "172.16.0.0/16"

  tags = {
    Name = "tf-example"
  }
}

resource "aws_subnet" "video_subnet" {
  vpc_id            = aws_vpc.video_vpc.id
  cidr_block        = "172.16.10.0/24"
  availability_zone = var.aws_availability_zone_a

  tags = {
    Name = "tf-example"
  }
}

resource "aws_security_group" "video_security_group" {
  name        = "video_security_group"
  description = "Allow TLS inbound traffic"
  vpc_id      = aws_vpc.video_vpc.id

  ingress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description      = "TLS from VPC"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "video_security_group"
  }
}

resource "aws_network_interface" "video_network_interface" {
  subnet_id   = aws_subnet.video_subnet.id
  private_ips = ["172.16.10.100"]
  security_groups = [aws_security_group.video_security_group.id]

  tags = {
    Name = "primary_network_interface"
  }
}

resource "aws_instance" "host" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"

  network_interface {
    network_interface_id = aws_network_interface.video_network_interface.id
    device_index         = 0
  }

  credit_specification {
    cpu_credits = "standard"
  }

  tags = {
    Name = "HelloWorld"
  }
}
