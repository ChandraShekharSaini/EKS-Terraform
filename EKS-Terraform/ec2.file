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
