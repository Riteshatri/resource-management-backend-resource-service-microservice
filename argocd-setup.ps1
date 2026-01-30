Write-Host "🚀 Starting ArgoCD Resource-Service setup..." -ForegroundColor Cyan

# # 1️⃣ ArgoCD RBAC / Config
# Write-Host "1️⃣ Applying ArgoCD RBAC Config"
# kubectl apply -f argocd/project/argocd-rbac-cm.yaml

# 2️⃣ ArgoCD Project
Write-Host "2️⃣ Applying Resource Service Project"
kubectl apply -f argocd/project/resource-project.yaml

# 3️⃣ Repo Secret
Write-Host "3️⃣ Applying Resource Repo Secret"
kubectl apply -f "argocd/Resource-Service Repo Connect/resource-repo-secret.yaml"

# 4️⃣ Namespace
Write-Host "4️⃣ Creating Namespace"
kubectl apply -f argocd/allFiles/Namespace.yaml

# 5️⃣ ArgoCD Application
Write-Host "5️⃣ Creating ArgoCD Application"
kubectl apply -f argocd/allFiles/Applications.yaml

# 6️⃣ ConfigMap
Write-Host "6️⃣ Applying ConfigMap"
kubectl apply -f argocd/allFiles/ConfigMap.yaml

# 7️⃣ Secret
Write-Host "7️⃣ Applying Secret"
kubectl apply -f argocd/allFiles/Secret.yaml

Write-Host "✅ ArgoCD Resource-Service setup completed successfully!" -ForegroundColor Green


# ▶️ Run:
# cd resource-management-resource-microservice
# .\argocd-setup.ps1