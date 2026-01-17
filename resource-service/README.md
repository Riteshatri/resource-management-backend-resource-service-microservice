# Resource Service - Resource Management Platform

Core business logic for managing infrastructure resources and templates.

## Project Structure

```
resource-service/
├── app/
│   ├── main.py          # FastAPI application
│   └── db.py            # Database connection wrapper
├── shared/              # Shared modules (copied for independent deployment)
│   ├── db.py            # Database models and connection (Azure SQL via pymssql)
│   └── security.py      # JWT and password utilities
├── Dockerfile
├── requirements.txt
└── README.md
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_SQL_SERVER` | Azure SQL server hostname | Yes |
| `AZURE_SQL_DATABASE` | Database name | Yes |
| `AZURE_SQL_USERNAME` | Database username | Yes |
| `AZURE_SQL_PASSWORD` | Database password | Yes |
| `SECRET_KEY` | JWT signing key | Yes |

### How to Generate a Secure SECRET_KEY
1. **Python (Windows/Linux):** `python -c "import secrets; print(secrets.token_hex(32))"`
2. **Python 3 (Linux/Mac):** `python3 -c "import secrets; print(secrets.token_hex(32))"`
3. **OpenSSL:** `openssl rand -hex 32`
4. **Node.js:** `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`
5. **PowerShell (Option A):** `[Convert]::ToHexString((1..32 | ForEach-Object { [byte](Get-Random -Minimum 0 -Maximum 256) }))`
6. **PowerShell (Option B):** `-join ((1..32 | ForEach-Object { Get-Random -Min 0 -Max 256 }) | ForEach-Object { '{0:X2}' -f $_ })`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/resources/` | List user's resources |
| POST | `/api/resources/` | Create new resource |
| PUT | `/api/resources/{id}` | Update resource |
| DELETE | `/api/resources/{id}` | Delete resource |
| GET | `/api/resources/templates` | Get resource templates |
| POST | `/api/resources/import-templates` | Import templates |

## Deployment Guide

### 1. Docker Deployment

**Step 1: Create Environment File (`.env`)**
```env
AZURE_SQL_SERVER=your-server.database.windows.net
AZURE_SQL_DATABASE=your-database
AZURE_SQL_USERNAME=your-username
AZURE_SQL_PASSWORD=your-password
SECRET_KEY=your-secret-key
```

**Step 2: Build & Run**
```bash
docker build -t resource-service .

docker run -d \
  --name resource-service \
  --env-file .env \
  -p 8003:8000 \
  resource-service
```

### 2. Local Development

```bash
pip install -r requirements.txt
pip install email-validator==2.1.0

export AZURE_SQL_SERVER=your-server.database.windows.net
export AZURE_SQL_DATABASE=your-database
export AZURE_SQL_USERNAME=your-username
export AZURE_SQL_PASSWORD=your-password
export SECRET_KEY=your-secret-key
export PYTHONPATH=$(pwd)

python -m uvicorn app.main:app --host 0.0.0.0 --port 8003
```

### 3. Kubernetes

```bash
helm upgrade --install resource-service ./k8s-templates/helm/resource-service \
  -f ./k8s-templates/helm/resource-service/values-prod.yaml
```

## Database Driver

This service uses **pymssql** (FreeTDS-based) for Azure SQL connectivity. No Microsoft ODBC drivers required.

## Default Ports

- **8003** (development/external)
- **8000** (inside Docker container)
