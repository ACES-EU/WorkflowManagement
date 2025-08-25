#!/bin/bash

set -e

echo "ACES Prefect work pool and MinIO setup"
echo "======================================"

# Ensure PATH includes local bin
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi

# Choose Python interpreter
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    PYTHON_BIN="python"
fi

# Set Prefect API URL
export PREFECT_API_URL=${1:?"Provide Prefect API URL as first argument"}
echo "Setting Prefect API URL: $PREFECT_API_URL"

# Set MinIO cloud endpoint
export CLOUD_MINIO_ENDPOINT=${2:?"Provide Cloud MinIO Endpoint as second argument"}
echo "Setting Cloud MinIO Endpoint: $CLOUD_MINIO_ENDPOINT"

# Check if Prefect server is reachable
echo "Checking Prefect server connectivity..."
if curl -s "$PREFECT_API_URL/health" > /dev/null 2>&1; then
    echo "Prefect server is reachable"
else
    echo "WARNING: Cannot reach Prefect server at $PREFECT_API_URL"
    echo "Please ensure Prefect server is running with:"
    echo "  prefect server start --host 0.0.0.0 --port 4200"
    echo "Or check if the URL is correct."
    echo ""
    exit 1
fi

prefect config set PREFECT_API_URL=$PREFECT_API_URL

# Step 1: Install dependencies
echo ""
echo "Step 1: Installing dependencies..."
pip install "prefect-aws>=0.5.0"
prefect block register -m prefect_aws
echo "Dependencies installed"

# Step 2: Create work pool
echo ""
echo "Step 2: Creating Kubernetes work pool..."
"$PYTHON_BIN" create_work_pool.py
echo "Work pool created"

# Step 3: Create MinIO storage blocks and configure them
echo ""
echo "Step 3: Create MinIO storage blocks and configure them..."
"$PYTHON_BIN" configure_minio_storage.py
echo "Configuration complete"

echo ""
echo "Setup completed successfully!"
echo ""
echo "What was configured:"
echo "  - Prefect API connection"
echo "  - Kubernetes work pool 'aces'"
echo "  - MinIO storage blocks (flows, data, results, config)"
echo "  - Work pool storage configuration"
echo "  - Default result storage"
echo ""
echo "Next steps:"
echo "  1. Deploy your flows: python your_flow.py"
echo "  2. Check Prefect UI for work pool and storage blocks"
echo "  3. Run flows: prefect deployment run flow-name/deployment-name"
