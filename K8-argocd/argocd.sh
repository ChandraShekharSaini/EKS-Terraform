#!/bin/bash

set -e

echo "======================================"
echo " Installing Argo CD"
echo "======================================"

# ------------------------------------------------------
# Check kubectl
# ------------------------------------------------------

if ! command -v kubectl >/dev/null 2>&1; then
    echo "ERROR: kubectl is not installed"
    exit 1
fi

echo "kubectl found:"
kubectl version --client

# ------------------------------------------------------
# Check Kubernetes connection
# ------------------------------------------------------

echo ""
echo "Checking Kubernetes cluster..."

kubectl cluster-info

echo ""
echo "Kubernetes nodes:"
kubectl get nodes

# ------------------------------------------------------
# Create Argo CD namespace
# ------------------------------------------------------

echo ""
echo "Creating argocd namespace..."

kubectl create namespace argocd \
    --dry-run=client \
    -o yaml | kubectl apply -f -

# ------------------------------------------------------
# Install Argo CD
# ------------------------------------------------------

echo ""
echo "Installing Argo CD..."

kubectl apply \
    --server-side \
    --force-conflicts \
    -n argocd \
    -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo ""
echo "Argo CD manifests installed."

# ------------------------------------------------------
# Wait for Argo CD server
# ------------------------------------------------------

echo ""
echo "Waiting for Argo CD server..."

kubectl rollout status \
    deployment/argocd-server \
    -n argocd \
    --timeout=10m

echo ""
echo "Argo CD server is Ready."

# ------------------------------------------------------
# Change Argo CD service to LoadBalancer
# ------------------------------------------------------

echo ""
echo "======================================"
echo " Configuring LoadBalancer"
echo "======================================"

kubectl patch service argocd-server \
    -n argocd \
    -p '{"spec":{"type":"LoadBalancer"}}'

echo ""
echo "Argo CD service changed to LoadBalancer."

# ------------------------------------------------------
# Wait for AWS Load Balancer
# ------------------------------------------------------

echo ""
echo "Waiting for AWS Load Balancer..."

ARGOCD_LB=""

for i in $(seq 1 60)
do

    ARGOCD_LB=$(kubectl get service argocd-server \
        -n argocd \
        -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' \
        2>/dev/null || true)

    if [ -n "$ARGOCD_LB" ]; then
        break
    fi

    echo "Waiting for LoadBalancer... $i/60"

    sleep 10

done

# ------------------------------------------------------
# Check LoadBalancer
# ------------------------------------------------------

echo ""
echo "======================================"
echo " Argo CD Service"
echo "======================================"

kubectl get service argocd-server -n argocd

echo ""

if [ -n "$ARGOCD_LB" ]; then

    echo "======================================"
    echo " Argo CD URL"
    echo "======================================"

    echo "https://$ARGOCD_LB"

else

    echo "======================================"
    echo " LoadBalancer is still pending"
    echo "======================================"

    echo "Run:"
    echo ""
    echo "kubectl get svc argocd-server -n argocd"

fi

# ------------------------------------------------------
# Wait for admin secret
# ------------------------------------------------------

echo ""
echo "Waiting for Argo CD admin password..."

ARGOCD_PASSWORD=""

for i in $(seq 1 30)
do

    if kubectl get secret \
        argocd-initial-admin-secret \
        -n argocd >/dev/null 2>&1
    then

        ARGOCD_PASSWORD=$(kubectl get secret \
            argocd-initial-admin-secret \
            -n argocd \
            -o jsonpath='{.data.password}' | base64 -d)

        break

    fi

    echo "Waiting for admin secret... $i/30"

    sleep 5

done

# ------------------------------------------------------
# Display login information
# ------------------------------------------------------

echo ""
echo "======================================"
echo " Argo CD Login"
echo "======================================"

echo "Username: admin"

if [ -n "$ARGOCD_PASSWORD" ]; then
    echo "Password: $ARGOCD_PASSWORD"
else
    echo "Password not available yet."
    echo ""
    echo "Run:"
    echo "kubectl -n argocd get secret argocd-initial-admin-secret \\"
    echo "  -o jsonpath='{.data.password}' | base64 -d"
fi

# ------------------------------------------------------
# Argo CD Pods
# ------------------------------------------------------

echo ""
echo "======================================"
echo " Argo CD Pods"
echo "======================================"

kubectl get pods -n argocd

# ------------------------------------------------------
# Final Service
# ------------------------------------------------------

echo ""
echo "======================================"
echo " Argo CD Services"
echo "======================================"

kubectl get svc -n argocd

echo ""
echo "======================================"
echo " Argo CD Installation Complete"
echo "======================================"
