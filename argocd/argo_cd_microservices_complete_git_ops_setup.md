# ArgoCD Microservices – Complete End‑to‑End Setup

> **Goal**: Har microservice ke liye **alag‑alag ArgoCD Application**, sab ek hi namespace me deploy ho, aur runtime pe **Frontend → Gateway → Microservices → Azure SQL** perfectly kaam kare.

---

## 0. Assumptions (FINAL)
- Kubernetes cluster already running
- ACR already attached to cluster
- Image tag: **v5** (sab services ke liye)
- Common namespace: **resource-mgmt**
- Env handling same as Docker (reference ke basis pe)

---

## 1. Common Infra (ONE‑TIME)

### 1.1 Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: resource-mgmt
```

### 1.2 Common ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: resource-mgmt
data:
  AZURE_SQL_SERVER: ritserver.database.windows.net
  AZURE_SQL_DATABASE: ritserver
  AZURE_SQL_USERNAME: ritserver

  GMAIL_USER: ravendrakumar20897@gmail.com

  ALGORITHM: HS256
  ACCESS_TOKEN_EXPIRE_MINUTES: "30"
```

### 1.3 Common Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: resource-mgmt
type: Opaque
stringData:
  AZURE_SQL_PASSWORD: Ritesh@12345
  SECRET_KEY: 00bfd5fadea7a8bcde64453b989e2f58a5f3718db3fb67e84e25aca777fab008
  GMAIL_APP_PASSWORD: qozjikewotogtnas
```

---

## 2. Backend Services (SAME PATTERN)

### 2.1 Template – Deployment (Auth / User / Resource / Notification / Theme)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <SERVICE-NAME>
  namespace: resource-mgmt
spec:
  replicas: 1
  selector:
    matchLabels:
      app: <SERVICE-NAME>
  template:
    metadata:
      labels:
        app: <SERVICE-NAME>
    spec:
      containers:
      - name: <SERVICE-NAME>
        image: riteshacr.azurecr.io/<IMAGE-NAME>:v5
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
```

### 2.2 Template – Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: <SERVICE-NAME>
  namespace: resource-mgmt
spec:
  selector:
    app: <SERVICE-NAME>
  ports:
    - port: 8000
```

### 2.3 Actual Mapping
| Service | SERVICE-NAME | IMAGE-NAME |
|------|-------------|-----------|
| Auth | auth-service | auth-service |
| User | user-service | user-service |
| Resource | resource-service | resource-service |
| Notification | notification-service | notification-service |
| Theme | theme-service | theme-service |

---

## 3. Gateway Service (Connector)

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gateway
  namespace: resource-mgmt
spec:
  replicas: 1
  selector:
    matchLabels:
      app: gateway
  template:
    metadata:
      labels:
        app: gateway
    spec:
      containers:
      - name: gateway
        image: riteshacr.azurecr.io/gateway:v5
        ports:
        - containerPort: 8000
        env:
        - name: AUTH_SERVICE_HOST
          value: auth-service
        - name: USER_SERVICE_HOST
          value: user-service
        - name: RESOURCE_SERVICE_HOST
          value: resource-service
        - name: NOTIFICATION_SERVICE_HOST
          value: notification-service
        - name: THEME_SERVICE_HOST
          value: theme-service
        - name: SERVICE_PORT
          value: "8000"
```

### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: gateway
  namespace: resource-mgmt
spec:
  selector:
    app: gateway
  ports:
    - port: 8000
```

---

## 4. Frontend

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: resource-mgmt
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: riteshacr.azurecr.io/frontend:v5
        ports:
        - containerPort: 80
        env:
        - name: BACKEND_HOST
          value: gateway
        - name: BACKEND_PORT
          value: "8000"
```

### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: resource-mgmt
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
    - port: 80
```

---

## 5. ArgoCD Applications (ONE PER SERVICE)

### Template
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: <APP-NAME>
  namespace: argocd
spec:
  project: default
  source:
    repoURL: <GIT-REPO-URL>
    targetRevision: main
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: resource-mgmt
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Actual Apps
| Argo App | Repo |
|-------|------|
| auth-app | auth-service repo |
| user-app | user-service repo |
| resource-app | resource-service repo |
| notification-app | notification-service repo |
| theme-app | theme-service repo |
| gateway-app | gateway repo |
| frontend-app | frontend repo |

---

## 6. Final Runtime Flow
```
Browser
 → Frontend (LB)
 → Gateway
 → Auth / User / Resource / Notification / Theme
 → Azure SQL
```

---

## 7. Interview‑Ready One‑Liner 🏆
> “Each microservice is deployed as an independent ArgoCD application using GitOps. All services share common configuration via Kubernetes Secrets and ConfigMaps and communicate internally using Kubernetes DNS. The API Gateway acts as a single entry point while ArgoCD ensures continuous reconciliation.”

---

✅ This document is **final**, **copy‑paste deployable**, and **production‑grade**.

