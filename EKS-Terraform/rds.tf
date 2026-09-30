###########################################################
# RDS SECURITY GROUP
###########################################################

resource "aws_security_group" "rds_sg" {
  name        = "rds-mysql-sg"
  description = "Allow MySQL access from EKS"
  vpc_id      = aws_vpc.eks_vpc.id

  ingress {
    description = "MySQL from EKS VPC"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    description = "Allow outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-mysql-sg"
  }
}



###########################################################
# RDS SUBNET GROUP
###########################################################

resource "aws_db_subnet_group" "mysql" {
  name = "shopping-mysql-subnet-group"

  subnet_ids = [
    aws_subnet.private1.id,
    aws_subnet.private2.id
  ]

  tags = {
    Name = "shopping-mysql-subnet-group"
  }
}


###########################################################
# MYSQL RDS
###########################################################

resource "aws_db_instance" "mysql" {

  identifier = "shopping-mysql"

  engine         = "mysql"
  engine_version = "8.0"

  instance_class = "db.t3.micro"

  allocated_storage     = 20
  max_allocated_storage = 50
  storage_type          = "gp3"

  db_name  = "shopping"
  username = "admin"
  password = qazqaz123

  port = 3306

  db_subnet_group_name = aws_db_subnet_group.mysql.name

  vpc_security_group_ids = [
    aws_security_group.rds_sg.id
  ]

  publicly_accessible = true

  backup_retention_period = 7

  multi_az = false



  skip_final_snapshot = true

  deletion_protection = false

  tags = {
    Name        = "shopping-mysql"
    Environment = "dev"
    Project     = "eks-project"
  }
}
