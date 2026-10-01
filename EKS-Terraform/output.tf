###########################################################
# OUTPUTS
###########################################################

output "vpc_id" {
  value = aws_vpc.eks_vpc.id
}

output "eks_cluster_name" {
  value = aws_eks_cluster.eks.name
}

output "eks_cluster_endpoint" {
  value = aws_eks_cluster.eks.endpoint
}

output "eks_admin_ec2_public_ip" {
  value = aws_instance.eks.public_ip
}

output "eks_admin_ec2_private_ip" {
  value = aws_instance.eks.private_ip
}

output "eks_admin_role_arn" {
  value = aws_iam_role.eks_admin_role.arn
}

output "eks_cluster_version" {
  value = aws_eks_cluster.eks.version
}



# output "rds_endpoint" {
#   description = "RDS MySQL endpoint"
#   value       = aws_db_instance.mysql.address
# }

# output "rds_port" {
#   description = "RDS MySQL port"
#   value       = aws_db_instance.mysql.port
# }

# output "rds_database" {
#   description = "RDS database name"
#   value       = aws_db_instance.mysql.db_name
# }

# output "rds_username" {
#   description = "RDS master username"
#   value       = aws_db_instance.mysql.username
# }
