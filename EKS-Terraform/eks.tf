terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

############################
# VARIABLES
############################

variable "cluster_version" {
  default = "1.35"
}

variable "aws_region" {
  default = "us-east-1"
}

############################
# VPC
############################

resource "aws_vpc" "eks_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "eks-vpc"
  }
}

############################
# INTERNET GATEWAY
############################

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.eks_vpc.id

  tags = {
    Name = "eks-igw"
  }
}

############################
# PUBLIC SUBNET 1
############################

resource "aws_subnet" "public1" {
  vpc_id                  = aws_vpc.eks_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "eks-public-1"

    "kubernetes.io/role/elb" = "1"
  }
}

############################
# PUBLIC SUBNET 2
############################

resource "aws_subnet" "public2" {
  vpc_id                  = aws_vpc.eks_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true

  tags = {
    Name = "eks-public-2"

    "kubernetes.io/role/elb" = "1"
  }
}

############################
# PRIVATE SUBNET 1
############################

resource "aws_subnet" "private1" {
  vpc_id            = aws_vpc.eks_vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "eks-private-1"

    "kubernetes.io/role/internal-elb" = "1"
  }
}

############################
# PRIVATE SUBNET 2
############################

resource "aws_subnet" "private2" {
  vpc_id            = aws_vpc.eks_vpc.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "eks-private-2"

    "kubernetes.io/role/internal-elb" = "1"
  }
}

############################
# NAT ELASTIC IP
############################

resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name = "eks-nat-eip"
  }
}

############################
# NAT GATEWAY
############################

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public1.id

  depends_on = [
    aws_internet_gateway.igw
  ]

  tags = {
    Name = "eks-nat"
  }
}

############################
# PUBLIC ROUTE TABLE
############################

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.eks_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "eks-public-rt"
  }
}

############################
# PUBLIC ROUTE ASSOCIATION 1
############################

resource "aws_route_table_association" "pub1" {
  subnet_id      = aws_subnet.public1.id
  route_table_id = aws_route_table.public.id
}

############################
# PUBLIC ROUTE ASSOCIATION 2
############################

resource "aws_route_table_association" "pub2" {
  subnet_id      = aws_subnet.public2.id
  route_table_id = aws_route_table.public.id
}

############################
# PRIVATE ROUTE TABLE
############################

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.eks_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = {
    Name = "eks-private-rt"
  }
}

############################
# PRIVATE ROUTE ASSOCIATION 1
############################

resource "aws_route_table_association" "priv1" {
  subnet_id      = aws_subnet.private1.id
  route_table_id = aws_route_table.private.id
}

############################
# PRIVATE ROUTE ASSOCIATION 2
############################

resource "aws_route_table_association" "priv2" {
  subnet_id      = aws_subnet.private2.id
  route_table_id = aws_route_table.private.id
}

############################
# SECURITY GROUP
############################

resource "aws_security_group" "allow_all" {
  name        = "allow-all-sg"
  description = "Allow all inbound and outbound traffic"
  vpc_id      = aws_vpc.eks_vpc.id

  ingress {
    description = "Allow all inbound"

    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  egress {
    description = "Allow all outbound"

    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = {
    Name = "allow-all-sg"
  }
}

###########################################################
# EKS CLUSTER IAM ROLE
###########################################################

resource "aws_iam_role" "cluster_role" {
  name = "eks-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "eks.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "eks-cluster-role"
  }
}

############################
# EKS CLUSTER POLICY
############################

resource "aws_iam_role_policy_attachment" "cluster_policy" {
  role = aws_iam_role.cluster_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

###########################################################
# EKS WORKER NODE IAM ROLE
###########################################################

resource "aws_iam_role" "worker_role" {
  name = "eks-worker-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "eks-worker-role"
  }
}

############################
# WORKER NODE POLICY
############################

resource "aws_iam_role_policy_attachment" "worker_node" {
  role = aws_iam_role.worker_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

############################
# CNI POLICY
############################

resource "aws_iam_role_policy_attachment" "cni" {
  role = aws_iam_role.worker_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

############################
# ECR POLICY
############################

resource "aws_iam_role_policy_attachment" "ecr" {
  role = aws_iam_role.worker_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

###########################################################
# EKS CLUSTER
###########################################################

resource "aws_eks_cluster" "eks" {
  name = "naresh"

  role_arn = aws_iam_role.cluster_role.arn

  version = var.cluster_version

  access_config {
    authentication_mode = "API_AND_CONFIG_MAP"
  }

  vpc_config {
    subnet_ids = [
      aws_subnet.private1.id,
      aws_subnet.private2.id
    ]

    endpoint_public_access = true
  }

  depends_on = [
    aws_iam_role_policy_attachment.cluster_policy
  ]

  tags = {
    Name        = "naresh"
    Environment = "dev"
    Project     = "eks-project"
  }
}

###########################################################
# EKS NODE GROUP
###########################################################

resource "aws_eks_node_group" "node_group" {
  cluster_name = aws_eks_cluster.eks.name

  node_group_name = "eks-node-group"

  node_role_arn = aws_iam_role.worker_role.arn

  version = var.cluster_version

  subnet_ids = [
    aws_subnet.private1.id,
    aws_subnet.private2.id
  ]

  instance_types = [
    "t3.medium"
  ]

  scaling_config {
    desired_size = 2
    max_size     = 6
    min_size     = 1
  }

  depends_on = [
    aws_iam_role_policy_attachment.worker_node,
    aws_iam_role_policy_attachment.cni,
    aws_iam_role_policy_attachment.ecr
  ]

  tags = {
    Name        = "eks-node"
    Environment = "dev"
    Project     = "eks-project"
    Owner       = "veeraops"
  }
}

###########################################################
# EKS ADDON - VPC CNI
###########################################################

resource "aws_eks_addon" "vpc_cni" {
  cluster_name = aws_eks_cluster.eks.name

  addon_name = "vpc-cni"

  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_node_group.node_group
  ]
}

###########################################################
# EKS ADDON - COREDNS
###########################################################

resource "aws_eks_addon" "coredns" {
  cluster_name = aws_eks_cluster.eks.name

  addon_name = "coredns"

  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_node_group.node_group
  ]
}

###########################################################
# EKS ADDON - KUBE PROXY
###########################################################

resource "aws_eks_addon" "kube_proxy" {
  cluster_name = aws_eks_cluster.eks.name

  addon_name = "kube-proxy"

  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_node_group.node_group
  ]
}

###########################################################
# EKS POD IDENTITY AGENT
###########################################################

resource "aws_eks_addon" "pod_identity" {
  cluster_name = aws_eks_cluster.eks.name

  addon_name = "eks-pod-identity-agent"

  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_node_group.node_group
  ]
}

###########################################################
# EBS CSI IAM ROLE
###########################################################

resource "aws_iam_role" "ebs_csi_role" {
  name = "AmazonEKS_EBS_CSI_DriverRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "pods.eks.amazonaws.com"
        }

        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
      }
    ]
  })

  tags = {
    Name = "AmazonEKS_EBS_CSI_DriverRole"
  }
}

###########################################################
# EBS CSI POLICY
###########################################################

resource "aws_iam_role_policy_attachment" "ebs_csi_policy" {
  role = aws_iam_role.ebs_csi_role.name

  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy"
}

###########################################################
# EBS CSI POD IDENTITY
###########################################################

resource "aws_eks_pod_identity_association" "ebs_csi" {
  cluster_name = aws_eks_cluster.eks.name

  namespace = "kube-system"

  service_account = "ebs-csi-controller-sa"

  role_arn = aws_iam_role.ebs_csi_role.arn

  depends_on = [
    aws_eks_addon.pod_identity,
    aws_iam_role_policy_attachment.ebs_csi_policy
  ]
}

###########################################################
# EBS CSI DRIVER
###########################################################

resource "aws_eks_addon" "ebs_csi" {
  cluster_name = aws_eks_cluster.eks.name

  addon_name = "aws-ebs-csi-driver"

  resolve_conflicts_on_update = "OVERWRITE"

  depends_on = [
    aws_eks_node_group.node_group,
    aws_eks_pod_identity_association.ebs_csi
  ]
}

###########################################################
# IAM ROLE FOR ADMIN EC2
###########################################################

resource "aws_iam_role" "eks_admin_role" {
  name = "eks-admin-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "eks-admin-ec2-role"
  }
}

###########################################################
# EKS ADMIN POLICY
###########################################################

resource "aws_iam_role_policy_attachment" "eks_admin_policy" {
  role = aws_iam_role.eks_admin_role.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

###########################################################
# EKS DESCRIBE POLICY
###########################################################

resource "aws_iam_role_policy" "eks_describe" {
  name = "eks-describe"

  role = aws_iam_role.eks_admin_role.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "eks:DescribeCluster",
          "eks:ListClusters",
          "eks:AccessKubernetesApi"
        ]

        Resource = "*"
      }
    ]
  })
}

###########################################################
# EC2 INSTANCE PROFILE
###########################################################

resource "aws_iam_instance_profile" "eks_admin_profile" {
  name = "eks-admin-ec2-profile"

  role = aws_iam_role.eks_admin_role.name
}

###########################################################
# EKS ACCESS ENTRY FOR ADMIN EC2
###########################################################

resource "aws_eks_access_entry" "eks_admin" {
  cluster_name = aws_eks_cluster.eks.name

  principal_arn = aws_iam_role.eks_admin_role.arn

  type = "STANDARD"

  depends_on = [
    aws_eks_cluster.eks
  ]
}

###########################################################
# EKS ADMIN ACCESS POLICY
###########################################################

resource "aws_eks_access_policy_association" "eks_admin" {
  cluster_name = aws_eks_cluster.eks.name

  principal_arn = aws_iam_role.eks_admin_role.arn

  policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"

  access_scope {
    type = "cluster"
  }

  depends_on = [
    aws_eks_access_entry.eks_admin
  ]
}

###########################################################
# ADMIN EC2
###########################################################

resource "aws_instance" "eks" {
  ami = "ami-02dfbd4ff395f2a1b"

  instance_type = "t2.medium"

  subnet_id = aws_subnet.public1.id

  vpc_security_group_ids = [
    aws_security_group.allow_all.id
  ]

  iam_instance_profile = aws_iam_instance_profile.eks_admin_profile.name

  root_block_device {
    volume_size = 30
  }

  tags = {
    Name = "eks-admin"
  }

  depends_on = [
    aws_eks_access_policy_association.eks_admin
  ]

 user_data = <<-EOF
#!/bin/bash

set -euxo pipefail

exec > /var/log/eks-admin-setup.log 2>&1

echo "====================================="
echo "Starting EKS Admin EC2 setup"
echo "====================================="

# Install required packages
dnf install -y unzip tar gzip

# Verify existing curl
curl --version

# Install AWS CLI
if ! command -v aws >/dev/null 2>&1; then
    curl -fL \
      "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" \
      -o /tmp/awscliv2.zip

    unzip -q /tmp/awscliv2.zip -d /tmp
    /tmp/aws/install
fi

aws --version
aws configure set region us-east-1

# Install kubectl
KUBECTL_VERSION="v1.35.0"

curl -fL \
  "https://dl.k8s.io/release/$${KUBECTL_VERSION}/bin/linux/amd64/kubectl" \
  -o /tmp/kubectl

install -m 0755 /tmp/kubectl /usr/local/bin/kubectl
rm -f /tmp/kubectl

/usr/local/bin/kubectl version --client

# Install eksctl
curl -fL \
  "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_linux_amd64.tar.gz" \
  -o /tmp/eksctl.tar.gz

tar -xzf /tmp/eksctl.tar.gz -C /tmp
install -m 0755 /tmp/eksctl /usr/local/bin/eksctl

rm -f /tmp/eksctl.tar.gz /tmp/eksctl

/usr/local/bin/eksctl version

# Wait for EKS cluster
echo "Waiting for EKS cluster..."

until aws eks describe-cluster \
  --name naresh \
  --region us-east-1 >/dev/null 2>&1
do
    sleep 20
done

# Wait until ACTIVE
while true; do
    STATUS=$(aws eks describe-cluster \
      --name naresh \
      --region us-east-1 \
      --query 'cluster.status' \
      --output text)

    echo "Cluster status: $STATUS"

    if [ "$STATUS" = "ACTIVE" ]; then
        break
    fi

    sleep 20
done

# Create kubeconfig
mkdir -p /root/.kube

aws eks update-kubeconfig \
  --name naresh \
  --region us-east-1 \
  --kubeconfig /root/.kube/config

chmod 600 /root/.kube/config

export KUBECONFIG=/root/.kube/config

# Wait for Kubernetes nodes
until /usr/local/bin/kubectl get nodes >/dev/null 2>&1; do
    echo "Waiting for Kubernetes nodes..."
    sleep 15
done

# Verify
/usr/local/bin/kubectl get nodes -o wide
/usr/local/bin/kubectl get pods -A

echo "====================================="
echo "EKS Admin setup completed successfully"
echo "====================================="
EOF
}


