provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "options" {
  cidr_block = "10.0.0.0/16"

  tags {
    Name = "options"
  }
}

resource "aws_instance" "main" {
  ami = "ami-xxx"
  instance_type = "t2.micro"
}