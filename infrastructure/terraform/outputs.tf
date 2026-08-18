output "server_ip" {
  value       = aeza_server.vpn_node.ip_address
  description = "Публичный IP адрес созданного VDS"
}
