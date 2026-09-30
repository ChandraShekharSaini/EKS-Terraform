



output "rds_endpoint" {
  description = "RDS MySQL endpoint"
  value       = aws_db_instance.mysql.address
}

output "rds_port" {
  description = "RDS MySQL port"
  value       = aws_db_instance.mysql.port
}

output "rds_database" {
  description = "RDS database name"
  value       = aws_db_instance.mysql.db_name
}

output "rds_username" {
  description = "RDS master username"
  value       = aws_db_instance.mysql.username
}
