#!/bin/bash
set -e

echo "🚀 Starting RESOURCE Helm setup..."

ROOT_DIR=$(pwd)

# 1️⃣ ArgoCD Project (resource)
echo "👉 Applying Resource Project"
cd "$ROOT_DIR/helm/project"
kubectl apply -f resource-project.yaml

# 2️⃣ Repo Secret (resource)
echo "👉 Applying Resource Repo Secret"
cd "$ROOT_DIR/helm/Resource-Service Repo Connect"
kubectl apply -f resource-repo-secret.yaml

# 3️⃣ Namespace
echo "👉 Creating Namespace"
cd "$ROOT_DIR/helm/allFiles"
kubectl apply -f Namespace.yaml

# 4️⃣ Application
echo "👉 Creating Resource Application"
kubectl apply -f Applications.yaml

# Back to repo root
cd "$ROOT_DIR"

echo "✅ RESOURCE Helm setup completed successfully!"

# ▶️ RUN:
# chmod +x helm-setup.sh
# ./helm-setup.sh