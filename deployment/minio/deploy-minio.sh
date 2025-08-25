#!/bin/bash
set -e

# ACES MinIO Deployment Script
# This script deploys MinIO Operator and Tenant using Helm

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE_OPERATOR="aces-minio-operator"
NAMESPACE_TENANT="aces-minio-tenant"
TENANT_NAME="minio"

echo "Starting ACES MinIO deployment..."

# Step 1: Deploy local-path-provisioner
echo "Deploying local-path-provisioner..."
kubectl apply -f "${SCRIPT_DIR}/local-path-storage.yaml"

# Step 2: Add MinIO Helm repository
echo "Adding MinIO Helm repository..."
helm repo add minio https://operator.minio.io/ 2>/dev/null || true
helm repo update

# Step 3: Install MinIO Operator
echo "️Installing MinIO Operator..."
helm upgrade --install \
  --namespace "${NAMESPACE_OPERATOR}" \
  --create-namespace \
  --wait \
  --timeout=5m \
  aces-operator minio/operator

# Step 4: Install MinIO Tenant
echo "Installing MinIO Tenant..."
helm upgrade --install \
  --namespace "${NAMESPACE_TENANT}" \
  --create-namespace \
  --wait \
  --timeout=10m \
  --values "${SCRIPT_DIR}/helm-values-tenant.yaml" \
  aces-tenant minio/tenant

echo "MinIO deployment completed successfully!"
echo ""
echo "Next steps:"
echo "  1. Create the 'prefect' bucket:"
echo "     kubectl apply -f s3-add-prefect-bucket.yaml"
echo ""
echo "  2. Access MinIO Console (port-forward):"
echo "     kubectl port-forward svc/${TENANT_NAME}-console 9001:9090 -n ${NAMESPACE_TENANT}"
echo ""
echo "  3. Credentials: admin/martel2024"
