Write-Host "🚀 Starting RESOURCE Helm setup..." -ForegroundColor Cyan

# Save repo root
$ROOT = Get-Location

# 1️⃣ ArgoCD Project (resource)
Write-Host "👉 Applying Resource Project"
Set-Location "$ROOT\helm\project"
kubectl apply -f resource-project.yaml

# 2️⃣ Repo Secret (resource)
Write-Host "👉 Applying Resource Repo Secret"
Set-Location "$ROOT\helm\Resource-Service Repo Connect"
kubectl apply -f resource-repo-secret.yaml

# 3️⃣ Namespace
Write-Host "👉 Creating Namespace"
Set-Location "$ROOT\helm\allFiles"
kubectl apply -f Namespace.yaml

# 4️⃣ Application
Write-Host "👉 Creating Resource Application"
kubectl apply -f Applications.yaml

# Back to repo root
Set-Location $ROOT

Write-Host "✅ RESOURCE Helm setup completed successfully!" -ForegroundColor Green

# ▶️ RUN:
# cd <repo-root>
# .\helm-setup.ps1