#!/bin/bash

set -e

NAMESPACE="argocd"
ARGOCD_MANIFEST="https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml"

echo "=========================================="
echo "        Argo CD Installation"
echo "=========================================="

# ==========================================================
# 1. Check kubectl,,,
# ==========================================================

if ! command -v kubectl >/dev/null 2>&1; then
    echo "❌ kubectl is not installed"
    exit 1
fi

echo "✅ kubectl found"


# ==========================================================
# 2. Check Kubernetes cluster
# ==========================================================

echo ""
echo "Checking Kubernetes cluster..."

kubectl cluster-info

echo "✅ Kubernetes cluster is accessible"


# ==========================================================
# 3. Create Argo CD namespace
# ==========================================================

echo ""
echo "Creating namespace: $NAMESPACE"

kubectl get namespace "$NAMESPACE" >/dev/null 2>&1 || \
kubectl create namespace "$NAMESPACE"

echo "✅ Namespace ready"


# ==========================================================
# 4. Install Argo CD
# ==========================================================

echo ""
echo "Installing Argo CD..."

kubectl apply \
  -n "$NAMESPACE" \
  -f "$ARGOCD_MANIFEST"

echo "✅ Argo CD manifests applied"


# ==========================================================
# 5. Wait for Argo CD pods
# ==========================================================

echo ""
echo "Waiting for Argo CD pods..."

kubectl wait \
  --namespace "$NAMESPACE" \
  --for=condition=Ready \
  pod \
  --all \
  --timeout=600s

echo "✅ Argo CD pods are ready"


# ==========================================================
# 6. Change Argo CD Server to LoadBalancer
# ==========================================================

echo ""
echo "Changing argocd-server Service to LoadBalancer..."

kubectl patch svc argocd-server \
  -n "$NAMESPACE" \
  -p '{"spec":{"type":"LoadBalancer"}}'

echo "✅ LoadBalancer configured"


# ==========================================================
# 7. Wait for LoadBalancer
# ==========================================================

echo ""
echo "Waiting for LoadBalancer..."

for i in {1..60}; do

    ARGOCD_ADDRESS=$(kubectl get svc argocd-server \
      -n "$NAMESPACE" \
      -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

    if [ -z "$ARGOCD_ADDRESS" ]; then
        ARGOCD_ADDRESS=$(kubectl get svc argocd-server \
          -n "$NAMESPACE" \
          -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    fi

    if [ -n "$ARGOCD_ADDRESS" ]; then
        break
    fi

    echo "Waiting for LoadBalancer... ($i/60)"
    sleep 10

done


# ==========================================================
# 8. Check LoadBalancer address
# ==========================================================

if [ -z "$ARGOCD_ADDRESS" ]; then

    echo ""
    echo "⚠️ LoadBalancer address not available yet."

    kubectl get svc argocd-server -n "$NAMESPACE"

else

    echo ""
    echo "✅ LoadBalancer ready"
    echo "Argo CD Address: $ARGOCD_ADDRESS"

fi


# ==========================================================
# 9. Get Argo CD initial admin password
# ==========================================================

echo ""
echo "Getting Argo CD admin password..."

ARGOCD_PASSWORD=$(kubectl get secret \
  argocd-initial-admin-secret \
  -n "$NAMESPACE" \
  -o jsonpath='{.data.password}' | base64 --decode)

echo "✅ Password retrieved"


# ==========================================================
# 10. Display information
# ==========================================================

echo ""
echo "=========================================="
echo "        Argo CD CONFIGURATION"
echo "=========================================="

echo ""
echo "Namespace:"
echo "$NAMESPACE"

echo ""
echo "Username:"
echo "admin"

echo ""
echo "Password:"
echo "$ARGOCD_PASSWORD"

echo ""

if [ -n "$ARGOCD_ADDRESS" ]; then

    echo "Argo CD URL:"
    echo "https://$ARGOCD_ADDRESS"

else

    echo "Run:"
    echo "kubectl get svc argocd-server -n argocd"

fi

echo ""
echo "=========================================="
echo "        Argo CD STATUS"
echo "=========================================="

kubectl get pods -n "$NAMESPACE"

echo ""

kubectl get svc -n "$NAMESPACE"

echo ""
echo "=========================================="
echo "        INSTALLATION COMPLETE"
echo "=========================================="