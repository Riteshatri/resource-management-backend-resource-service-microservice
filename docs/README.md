# Argo CD with Azure AD (Entra ID) SSO on AKS 🚀

This README provides a **complete, end-to-end guide** to configure **Argo CD** running on **Azure Kubernetes Service (AKS)** with **Azure AD (Microsoft Entra ID)** using **OIDC Single Sign-On (SSO)**.

It also covers **ALL practical access scenarios**, including:
- Argo CD exposed via **HTTP (Lab)**
- Argo CD exposed via **HTTPS (LoadBalancer / Ingress)**
- Argo CD behind a **custom domain / website**
- Common real-world mistakes & fixes

---

## 🧠 Architecture Overview

Azure Subscription  
└── AKS Cluster  
&nbsp;&nbsp;&nbsp;&nbsp;└── Argo CD  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↑ OIDC (SSO)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓  
Microsoft Entra ID (Azure AD)

Authentication → Azure AD  
Authorization → Argo CD RBAC

---

## 🎯 Objective

- Learn GitOps using Argo CD
- Integrate Azure AD SSO with Argo CD
- Understand HTTP vs HTTPS behavior
- Support all Argo CD exposure methods
- Build real-world DevOps confidence

---

## 🧰 Prerequisites

- Azure Subscription
- AKS cluster running
- kubectl configured for AKS
- Argo CD installed in namespace `argocd`
- Argo CD UI accessible (LoadBalancer / Ingress)

---

## 🟦 STEP 1: Azure AD App Registration

Azure Portal → Microsoft Entra ID → App registrations → New registration

**Details**
- Name: `argocd-aks`
- Account type: Single tenant

Redirect URI depends on how Argo CD is exposed (see scenarios below).

---

## 🟦 STEP 2: Capture App Details

From App Overview:
- Tenant ID
- Client ID

---

## 🟦 STEP 3: Create Client Secret

Certificates & secrets → New client secret  
- Name: `argocd-sso`
- Expiry: 6–12 months (lab)

⚠️ Copy the secret value immediately.

---

## 🟨 STEP 4: Configure Argo CD OIDC (argocd-cm.yaml)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  url: <ARGOCD_BASE_URL>

  oidc.config: |
    name: Azure
    issuer: https://login.microsoftonline.com/<TENANT_ID>/v2.0
    clientID: <CLIENT_ID>
    clientSecret: <CLIENT_SECRET>
    requestedScopes:
      - openid
      - profile
      - email
    requestedIDTokenClaims:
      groups:
        essential: true
```

---

## 🔴 VERY IMPORTANT: CHOOSE THE CORRECT URL (REAL-WORLD CASES)

Azure AD **STRICTLY MATCHES** the Redirect URI with Argo CD URL.

Below are **ALL PRACTICAL SCENARIOS** 👇

---

## ✅ CASE 1: Argo CD exposed via HTTP (LAB / PRACTICE)

Example:
```
http://<ARGOCD-LB-IP>:8080
```

### Azure AD Redirect URI
```
http://<ARGOCD-LB-IP>:8080/auth/callback
```

### argocd-cm.yaml
```yaml
data:
  url: http://<ARGOCD-LB-IP>:8080
```

### FLOW
User opens Argo CD (HTTP)  
→ Redirect to Azure Login (HTTPS)  
→ User logs in securely  
→ Azure redirects back to Argo CD (HTTP)  
→ LOGIN SUCCESS ✅

✔ Azure login is ALWAYS HTTPS  
✔ HTTP callback is OK for LAB  
❌ NOT recommended for production

---

## ✅ CASE 2: Argo CD via HTTPS LoadBalancer (IP based)

Example:
```
https://4.208.233.1
```

### Azure AD Redirect URI
```
https://4.208.233.1/auth/callback
```

### argocd-cm.yaml
```yaml
data:
  url: https://4.208.233.1
```

✔ Most common AKS learning setup  
✔ Works even with self-signed cert  
✔ Recommended over HTTP

---

## ✅ CASE 3: Argo CD behind Custom Domain (Website)

Example:
```
https://argocd.example.com
```

### Azure AD Redirect URI
```
https://argocd.example.com/auth/callback
```

### argocd-cm.yaml
```yaml
data:
  url: https://argocd.example.com
```

✔ BEST PRACTICE  
✔ Production-ready  
✔ Works with Ingress + cert-manager

---

## ⚠️ COMMON MISTAKES (PLEASE AVOID)

| Mistake | Result |
|------|-------|
| Redirect URI mismatch | Login loop |
| Wrong protocol (http vs https) | Azure error |
| Forgot restart | Azure button missing |
| kubectl edit on Windows | Save failure |
| No RBAC | Login but no apps |

---

## 🔄 APPLY CONFIGURATION

```bash
kubectl apply -f argocd-cm.yaml
kubectl rollout restart deployment argocd-server -n argocd
kubectl rollout restart deployment argocd-dex-server -n argocd
```

---

## 🔐 LOGIN TEST

Open Argo CD UI and confirm:
👉 **Login with Azure** button appears

---

## 🧠 INTERVIEW-READY EXPLANATION

"I integrated Argo CD with Azure AD using OIDC. The redirect URI strictly matches the external Argo CD URL, supporting HTTP for labs and HTTPS with domains for production."

---

## 👤 Author

**Ritesh Atri**  
DevOps & Kubernetes Learner  
LinkedIn: https://www.linkedin.com/in/riteshatri

---

## 🏁 CONCLUSION

This README covers **ALL real-world Argo CD access patterns** and prepares you for **production GitOps setups** using Azure AD SSO.
