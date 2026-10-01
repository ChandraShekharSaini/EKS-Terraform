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

# =====================================================
# Install kubectl
# =====================================================

KUBECTL_VERSION="v1.35.0"

curl -fL \
  "https://dl.k8s.io/release/$${KUBECTL_VERSION}/bin/linux/amd64/kubectl" \
  -o /tmp/kubectl

install -m 0755 /tmp/kubectl /usr/local/bin/kubectl
rm -f /tmp/kubectl

/usr/local/bin/kubectl version --client

# =====================================================
# Install eksctl
# =====================================================

curl -fL \
  "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_linux_amd64.tar.gz" \
  -o /tmp/eksctl.tar.gz

tar -xzf /tmp/eksctl.tar.gz -C /tmp

install -m 0755 /tmp/eksctl /usr/local/bin/eksctl

rm -f /tmp/eksctl.tar.gz /tmp/eksctl

/usr/local/bin/eksctl version

# =====================================================
# Wait for EKS cluster
# =====================================================

echo "Waiting for EKS cluster..."

until aws eks describe-cluster \
  --name naresh \
  --region us-east-1 >/dev/null 2>&1
do
    echo "EKS cluster not available yet..."
    sleep 20
done

# =====================================================
# Wait until EKS cluster is ACTIVE
# =====================================================

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

# =====================================================
# Create kubeconfig
# =====================================================

mkdir -p /root/.kube

aws eks update-kubeconfig \
  --name naresh \
  --region us-east-1 \
  --kubeconfig /root/.kube/config

chmod 600 /root/.kube/config

export KUBECONFIG=/root/.kube/config

# =====================================================
# Wait for Kubernetes nodes
# =====================================================

echo "Waiting for Kubernetes nodes..."

until /usr/local/bin/kubectl get nodes >/dev/null 2>&1; do

    echo "Waiting for Kubernetes API/nodes..."
    sleep 15

done

# Wait until at least one node becomes Ready

until /usr/local/bin/kubectl get nodes \
    --no-headers 2>/dev/null | grep -q " Ready "; do

    echo "Waiting for Ready Kubernetes node..."
    sleep 15

done

echo "Kubernetes nodes are Ready"

# =====================================================
# Verify cluster
# =====================================================

/usr/local/bin/kubectl get nodes -o wide

/usr/local/bin/kubectl get pods -A

# =====================================================
# INSTALL ARGO CD
# =====================================================

echo "====================================="
echo "Installing Argo CD"
echo "====================================="

# Create namespace

if ! /usr/local/bin/kubectl get namespace argocd >/dev/null 2>&1; then

    /usr/local/bin/kubectl create namespace argocd

fi

# Install Argo CD

/usr/local/bin/kubectl apply \
  -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "Waiting for Argo CD components..."

# Wait for Argo CD server deployment

/usr/local/bin/kubectl rollout status \
  deployment/argocd-server \
  -n argocd \
  --timeout=10m

# =====================================================
# CHANGE ARGO CD SERVER TO LOADBALANCER
# =====================================================

echo "====================================="
echo "Changing Argo CD Service to LoadBalancer"
echo "====================================="

/usr/local/bin/kubectl patch svc argocd-server \
  -n argocd \
  -p '{"spec":{"type":"LoadBalancer"}}'

# =====================================================
# Wait for AWS Load Balancer
# =====================================================

echo "Waiting for AWS Load Balancer..."

for i in $(seq 1 60); do

    ARGOCD_LB=$(
      /usr/local/bin/kubectl get svc argocd-server \
        -n argocd \
        -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' \
        2>/dev/null || true
    )

    if [ -n "$ARGOCD_LB" ]; then
        break
    fi

    echo "Load Balancer not ready yet..."
    sleep 15

done

# =====================================================
# Display Argo CD information
# =====================================================

echo "====================================="
echo "ARGO CD INSTALLATION COMPLETED"
echo "====================================="

echo "Argo CD Services:"
/usr/local/bin/kubectl get svc -n argocd

echo "Argo CD Pods:"
/usr/local/bin/kubectl get pods -n argocd

echo "Argo CD Load Balancer:"
echo "$ARGOCD_LB"

echo "====================================="
echo "Argo CD URL"
echo "====================================="

if [ -n "$ARGOCD_LB" ]; then
    echo "https://$ARGOCD_LB"
else
    echo "Load Balancer hostname not available yet."
    echo "Run:"
    echo "kubectl get svc argocd-server -n argocd"
fi

# =====================================================
# Get Initial Argo CD Admin Password
# =====================================================

echo "====================================="
echo "Argo CD Initial Admin Password"
echo "====================================="

for i in $(seq 1 30); do

    if /usr/local/bin/kubectl get secret argocd-initial-admin-secret \
        -n argocd >/dev/null 2>&1; then

        ARGOCD_PASSWORD=$(
          /usr/local/bin/kubectl -n argocd get secret \
            argocd-initial-admin-secret \
            -o jsonpath="{.data.password}" | base64 -d
        )

        echo "Username: admin"
        echo "Password: $ARGOCD_PASSWORD"

        break
    fi

    echo "Waiting for Argo CD admin secret..."
    sleep 10

done

# =====================================================
# Final verification
# =====================================================

echo "====================================="
echo "FINAL CLUSTER STATUS"
echo "====================================="

/usr/local/bin/kubectl get nodes

/usr/local/bin/kubectl get pods -n argocd

/usr/local/bin/kubectl get svc -n argocd

echo "====================================="
echo "EKS Admin setup completed successfully"
echo "====================================="

EOF
}
