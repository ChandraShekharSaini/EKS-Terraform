terraform {
  backend "s3" {
    bucket       = "terraform-state-storage-78hh"
    key          = "terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}
