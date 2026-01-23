# Argo CD RBAC – In‑Depth Explanation (Admin, Readonly & Default Users)

## Overview

This document explains **why three different RBAC YAML configurations are used in Argo CD**, what each file does, and **how access control works when users log in via Azure AD (Entra ID)**.

Your setup follows **enterprise-grade GitOps security practices**:
- Azure AD handles **authentication** (who the user is)
- Argo CD RBAC handles **authorization** (what the user can do)

---

## Why RBAC is Required in Argo CD

By default, Argo CD allows users to authenticate, but **does not automatically grant permissions** to view or manage applications.

Without RBAC:
- Users can log in
- But may see **no applications**
- Or may get **more access than intended**

RBAC ensures:
- Only the right users see the right applications
- Only authorized users can deploy or change workloads
- GitOps access is auditable and secure

---

## The Three RBAC Scenarios Explained

You created **three logical access levels**, implemented via RBAC:

1. **Admin Users**
2. **Readonly Users**
3. **Users with no group mapping**

Each level is intentional and solves a real-world requirement.

---

## 1. Admin RBAC (`argocd-rbac-admin.yaml`)

### Why this exists

Admin users are responsible for:
- Managing applications
- Performing deployments
- Handling rollbacks
- Managing repositories, clusters, and projects

They need **full control** over Argo CD.

### What this YAML does

- Grants **complete administrative access**
- Maps a specific Azure AD group (e.g. `argocd-admins`) to the `admin` role

### Capabilities

Admin users can:
- Create, edit, delete applications
- Perform manual syncs
- Enable/disable auto-sync
- Rollback deployments
- Add/remove repositories and clusters
- Manage projects and settings

This matches how **SRE / Platform teams** operate in real organizations.

---

## 2. Readonly RBAC (`argocd-rbac-users.yaml`)

### Why this exists

Not everyone should be able to deploy.

Common readonly users:
- QA teams
- Managers
- Security & audit teams
- Stakeholders

They need **visibility**, not control.

### What this YAML does

- Grants read-only access to applications
- Allows users to:
  - List applications
  - View application details
  - Inspect manifests and status
- Blocks any action that could modify the system

### Capabilities

Readonly users can:
- Log in via Azure AD
- View applications and health
- Inspect YAML and resources

Readonly users **cannot**:
- Sync
- Rollback
- Edit or delete applications
- Add repos or clusters

This ensures **zero risk** while maintaining transparency.

---

## 3. Default / No-Group Users

### Why this exists

This is a **security safety net**.

If a user:
- Exists in Azure AD
- But is not part of any Argo CD RBAC group

Then they should **not see or access Argo CD applications**.

### What happens for these users

- Login succeeds
- Argo CD UI opens
- No applications are visible

This prevents:
- Accidental exposure
- Unauthorized access
- Over-permissioning

This is a **best practice in enterprise IAM**.

---

## How These Three YAMLs Work Together

```text
Azure AD
   |
   | (Authentication)
   v
Argo CD
   |
   | (RBAC Authorization)
   v
Admin / Readonly / No Access
```

- Azure AD proves identity
- Argo CD RBAC decides permissions
- Access is based on **group membership**

---

## Real-World Enterprise Mapping

| Azure AD Group | Argo CD Role | Typical Users |
|--------------|-------------|---------------|
| argocd-admins | Admin | SRE / Platform Team |
| argocd-readonly | Readonly | QA / Managers |
| No group | No Access | General users |

---

## Key Takeaways

- Authentication and authorization are separate concerns
- RBAC prevents accidental or malicious changes
- Group-based access scales cleanly
- This model is used in real production GitOps setups

---

## Final Result

Your Argo CD setup is now:
- Secure
- Scalable
- Audit-friendly
- Enterprise-ready

This is **not a lab-only setup** — this is how real teams operate GitOps platforms.

---

**Author:** Ritesh Atri  
**Focus:** GitOps • Kubernetes • Argo CD • Azure

&nbsp;
&nbsp;
&nbsp;
&nbsp;
&nbsp;

# Argo CD RBAC – Complete In-Depth Permission Reference (Cheat Sheet)

## Purpose of this Document Mentioned Below

This README is a **deep, line-by-line RBAC reference** for Argo CD.

It explains:
- Every RBAC rule you commonly use
- What each line **allows**
- What each line **blocks**
- How to safely combine permissions

You can treat this as:
- A **design guide**
- A **cheat sheet**
- A **custom RBAC builder reference**

---

## RBAC Basics (Very Important)

Argo CD RBAC rules follow this format:

```
p, <role>, <resource>, <action>, <scope>, allow
```

### Meaning:
- **role** → logical permission group (admin, readonly, custom)
- **resource** → what is being accessed
- **action** → what operation is allowed
- **scope** → where it applies
- **allow** → permission grant

---

## Default Role

### `policy.default: role:readonly`

### What it does:
- Applies to users **not mapped** to any Azure AD group
- Acts as a security fallback

### What it allows:
- Nothing by default

### What it blocks:
- App listing
- App access
- Any modification

---

## Applications Permissions (Most Important)

### `applications, list`

Allows:
- Application list visibility in UI

Blocks:
- Viewing application details
- Any changes

Used for:
- Dashboard visibility

---

### `applications, get`

Allows:
- Open application
- View YAML
- View status & history

Blocks:
- Sync
- Rollback
- Edit
- Delete

Used for:
- Read-only inspection

---

### `applications, sync`

Allows:
- Manual sync

Blocks:
- App deletion
- Repo changes

Used for:
- Operators who deploy but don’t manage config

---

### `applications, delete`

Allows:
- Delete application

Blocks:
- Nothing related to deletion

Used for:
- Admins only

---

### `applications, *`

Allows:
- All application actions

Blocks:
- Nothing

Used for:
- Platform admins

---

## Repository Permissions

### `repositories, get`

Allows:
- View repo list

Blocks:
- Add/remove repos

---

### `repositories, *`

Allows:
- Add/edit/remove Git repositories

Used for:
- Platform admins

---

## Cluster Permissions

### `clusters, get`

Allows:
- View registered clusters

---

### `clusters, *`

Allows:
- Add/remove Kubernetes clusters

Used for:
- Infra / SRE teams

---

## Project Permissions

### `projects, get`

Allows:
- View Argo CD projects

---

### `projects, *`

Allows:
- Create/edit/delete projects

Used for:
- Admin users

---

## Logs & Exec

### `logs, get`

Allows:
- View pod logs

---

### `exec, create`

Allows:
- Exec into pods via Argo CD

Security Note:
- Should be admin-only

---

## Group Mapping Rules

### `g, <GROUP_ID>, role:admin`

Effect:
- All members of the Azure AD group become admins

---

### `g, <GROUP_ID>, role:readonly`

Effect:
- Group members get view-only access

---

## Common Role Patterns

### Readonly Role

```
applications, list
applications, get
```

### Sync-Only Role

```
applications, list
applications, get
applications, sync
```

### Full Admin Role

```
applications, *
repositories, *
clusters, *
projects, *
```

---

## Security Best Practices

- Keep `policy.default` as readonly
- Use Azure AD groups, never individual users
- Grant minimum required permissions
- Restart Argo CD server after RBAC changes
- Always test with non-admin user first

---

## Final Notes

RBAC in Argo CD is **composable**.

Each line:
- Adds power
- Never removes power

Design permissions carefully.

---

**Author:** Ritesh Atri  
**Focus:** Argo CD • Kubernetes • GitOps • Azure AD





&nbsp;&nbsp;
&nbsp;&nbsp;
&nbsp;&nbsp;
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
https://51.104.152.250
```

### Azure AD Redirect URI
```
https://51.104.152.250/auth/callback
```

### argocd-cm.yaml
```yaml
data:
  url: https://51.104.152.250
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


&nbsp;&nbsp;
&nbsp;&nbsp;
&nbsp;&nbsp;
&nbsp;&nbsp;
&nbsp;&nbsp;
&nbsp;&nbsp;
&nbsp;&nbsp;
  
  
  




# Argo CD with Azure AD (Entra ID) SSO on AKS 🚀

This document provides a complete, end-to-end guide to configure **Argo CD** running on **Azure Kubernetes Service (AKS)** with **Azure AD (Microsoft Entra ID)** using **OIDC Single Sign-On (SSO)**.

The goal is to allow Azure AD users to log in to Argo CD using their Azure credentials, without creating local Argo CD users.

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
- Avoid local users and passwords
- Enable centralized authentication
- Build enterprise-grade GitOps knowledge

---

## 🧰 Prerequisites

- Azure Subscription
- AKS cluster running
- kubectl configured for AKS
- Argo CD installed in namespace `argocd`
- Argo CD UI accessible (LoadBalancer or Ingress)

Example:
https://4.208.233.1

---

## 🟦 Step 1: Azure AD App Registration

1. Azure Portal → Microsoft Entra ID
2. App registrations → New registration

**Details**
- Name: `argocd-aks`
- Account type: Single tenant
- Redirect URI (Web):
  https://4.208.233.1/auth/callback

Click **Register**.

---

## 🟦 Step 2: Capture App Details

From Overview page:
- Tenant ID
- Client ID

---

## 🟦 Step 3: Create Client Secret

Certificates & secrets → New client secret  
- Name: `argocd-sso`
- Expiry: 6–12 months

⚠️ Copy the secret value immediately.

---

## 🟦 Step 4: (Recommended) Azure AD Groups

Create:
- argocd-admins
- argocd-readonly

Add users and note **Object IDs**.

---

## 🟨 Step 5: Configure Argo CD OIDC

Create file **argocd-cm.yaml**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  url: https://4.208.233.1

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

Replace placeholders with actual values.

---

## 🟨 Step 6: Apply Configuration

```bash
kubectl apply -f argocd-cm.yaml
```

---

## 🔄 Step 7: Restart Argo CD

```bash
kubectl rollout restart deployment argocd-server -n argocd
kubectl rollout restart deployment argocd-dex-server -n argocd
```

---

## 🟩 Step 8: Verify

```bash
kubectl get cm argocd-cm -n argocd -o yaml
```

Ensure `oidc.config` and `url` are present.

---

## 🔐 Step 9: Login Test

Open:
https://4.208.233.1

You should see **Login with Azure**.

---

## 🧠 Common Issues

| Issue | Resolution |
|-----|-----------|
| Login loop | Check redirect URI |
| Azure button missing | Restart Argo CD |
| kubectl edit fails | Use kubectl apply |
| No apps visible | Configure RBAC |

---

## 🧠 Interview-Ready Statement

"I integrated Argo CD with Azure AD using OIDC. Authentication is handled by Azure AD and authorization via Argo CD RBAC mapped to Azure AD groups."

---

## 👤 Author

**Ritesh Atri**  
DevOps & Kubernetes Learner  
LinkedIn: https://www.linkedin.com/in/riteshatri

---

## 🏁 Conclusion

This setup demonstrates a real-world GitOps authentication model using AKS, Argo CD, and Azure AD SSO.
