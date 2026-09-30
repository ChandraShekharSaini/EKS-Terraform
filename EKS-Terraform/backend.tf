terraform {
  backend "s3" {
    bucket       = "aws-terraform7789jbbncd"
    key          = "terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}
