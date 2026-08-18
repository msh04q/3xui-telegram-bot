variable "aeza_api_token" {
  type        = string
  sensitive   = true
  description = "API Токен личного кабинета Aeza"
}

variable "ssh_public_key" {
  type        = string
  description = "Публичный SSH ключ (~/.ssh/id_rsa.pub)"
}
