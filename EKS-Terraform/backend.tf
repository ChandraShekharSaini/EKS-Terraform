terraform {
  backend "s3" {
    bucket       = "aws-terraform54433355f"
    key          = "terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}
