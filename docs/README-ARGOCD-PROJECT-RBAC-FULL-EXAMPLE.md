# Argo CD – Application Level Segregation Using Projects & RBAC (Full Example)

## Scenario

You have **3 different applications** deployed using Argo CD and you want:

- Different users to see **only their own application**
- No visibility of other applications
- Admin users to see everything

This is achieved using **Argo CD Projects (AppProject) + RBAC**.

---

## Applications

| Application | Project |
|------------|---------|
| frontend-app | frontend-project |
| backend-app | backend-project |
| payments-app | payments-project |

---

## Architecture Flow

Azure AD Groups  
→ Argo CD RBAC Roles  
→ Argo CD Projects  
→ Applications

---

## Step 1: Create Projects (AppProject)

### frontend-project.yaml
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: frontend-project
  namespace: argocd
spec:
  sourceRepos:
    - https://github.com/example/frontend-repo.git
  destinations:
    - namespace: frontend
      server: https://kubernetes.default.svc
```

### backend-project.yaml
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: backend-project
  namespace: argocd
spec:
  sourceRepos:
    - https://github.com/example/backend-repo.git
  destinations:
    - namespace: backend
      server: https://kubernetes.default.svc
```

### payments-project.yaml
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: payments-project
  namespace: argocd
spec:
  sourceRepos:
    - https://github.com/example/payments-repo.git
  destinations:
    - namespace: payments
      server: https://kubernetes.default.svc
```

---

## Step 2: Bind Applications to Projects

### frontend-app.yaml
```yaml
spec:
  project: frontend-project
```

### backend-app.yaml
```yaml
spec:
  project: backend-project
```

### payments-app.yaml
```yaml
spec:
  project: payments-project
```

---

## Step 3: RBAC Configuration

### argocd-rbac-cm.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.default: role:readonly

  policy.csv: |
    # Admin role
    p, role:admin, applications, *, */*, allow
    p, role:admin, projects, *, *, allow

    # Frontend readonly role
    p, role:frontend-readonly, applications, list, frontend-project/*, allow
    p, role:frontend-readonly, applications, get, frontend-project/*, allow

    # Backend readonly role
    p, role:backend-readonly, applications, list, backend-project/*, allow
    p, role:backend-readonly, applications, get, backend-project/*, allow

    # Payments readonly role
    p, role:payments-readonly, applications, list, payments-project/*, allow
    p, role:payments-readonly, applications, get, payments-project/*, allow

    # Azure AD Group mappings
    g, <AZURE_AD_FRONTEND_GROUP_ID>, role:frontend-readonly
    g, <AZURE_AD_BACKEND_GROUP_ID>, role:backend-readonly
    g, <AZURE_AD_PAYMENTS_GROUP_ID>, role:payments-readonly
    g, <AZURE_AD_ADMIN_GROUP_ID>, role:admin
```

---

## Step 4: Apply Configuration

```bash
kubectl apply -f frontend-project.yaml
kubectl apply -f backend-project.yaml
kubectl apply -f payments-project.yaml

kubectl apply -f argocd-rbac-cm.yaml
kubectl rollout restart deployment argocd-server -n argocd
```

---

## Final Visibility Matrix

| User Group | Visible Project | Visible App |
|----------|----------------|-------------|
| Frontend Team | frontend-project | frontend-app |
| Backend Team | backend-project | backend-app |
| Payments Team | payments-project | payments-app |
| Admin Team | All projects | All apps |

---

## Key Rule to Remember

> Argo CD does **not** restrict access per application directly.  
> Application visibility is always controlled **via Project + RBAC**.

---

## Summary

- Projects act as **security boundaries**
- RBAC decides **who can see which project**
- Applications inherit visibility from their project
- This is the **only supported enterprise way**

---

Author: Ritesh Atri  
Focus: GitOps • Argo CD • Kubernetes • Azure AD
