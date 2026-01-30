#!/bin/bash
set -e

echo "🚀 Starting ArgoCD Resource-Service setup..."

# # 1️⃣ ArgoCD RBAC / Config
# echo "1️⃣ Applying ArgoCD RBAC Config"
# kubectl apply -f argocd/project/argocd-rbac-cm.yaml

# 2️⃣ ArgoCD Project
echo "2️⃣ Applying Resource Service Project"
kubectl apply -f argocd/project/resource-project.yaml

# 3️⃣ Repo Secret
echo "3️⃣ Applying Resource Repo Secret"
kubectl apply -f "argocd/Resource-Service Repo Connect/resource-repo-secret.yaml"

# 4️⃣ Namespace
echo "4️⃣ Creating Namespace"
kubectl apply -f argocd/allFiles/Namespace.yaml

# 5️⃣ ArgoCD Application
echo "5️⃣ Creating ArgoCD Application"
kubectl apply -f argocd/allFiles/Applications.yaml

# 6️⃣ ConfigMap
echo "6️⃣ Applying ConfigMap"
kubectl apply -f argocd/allFiles/ConfigMap.yaml

# 7️⃣ Secret
echo "7️⃣ Applying Secret"
kubectl apply -f argocd/allFiles/Secret.yaml

echo "✅ ArgoCD Resource-Service setup completed successfully!"

# ▶️ Run:
# chmod +x argocd-setup.sh
# ./argocd-setup.sh