terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aeza = {
      source  = "aeza-tech/aeza"
      version = "~> 1.0"
    }
  }
}

provider "aeza" {
  api_token = var.aeza_api_token
}

resource "aeza_ssh_key" "deploy_key" {
  name       = "devops-key"
  public_key = var.ssh_public_key
}

resource "aeza_server" "vpn_node" {
  name      = "frankfurt.ptr.network"
  location  = "fra"
  os        = "ubuntu-24-04"
  preset    = "promo-fra-1"
  ssh_keys  = [aeza_ssh_key.deploy_key.id]
}
