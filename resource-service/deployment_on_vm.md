# Resource Service - Deployment on Ubuntu VM

> **Resource Management Service** | Port 8003 | CRUD operations for resources

---

## Method 1: Deploy Directly on VM

### Step 1: Connect to Backend VM

```bash
ssh user@your-backend-vm-ip

# Example:
# ssh ritesh@20.123.45.67
```

### Step 2: Install System Dependencies

```bash
# Update package list
sudo apt update

# Install required packages (Python 3.12 comes with Ubuntu 24.04)
sudo apt install -y build-essential python3.12 python3.12-venv python3-pip freetds-dev freetds-bin git

# Verify Python version
python3 --version
# Should show: Python 3.12.x
```

### Step 3: Clone Resource Service Repository

```bash
cd /home/user
git clone <your-resource-service-repo-url>
cd resource-service
```

### Step 4: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in prompt
```

### Step 5: Install Python Dependencies

```bash
# Make sure (venv) is active!
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Create Environment Configuration

```bash
nano .env
```

**Add this content:**
```env
# Azure SQL Database
AZURE_SQL_SERVER=ritserver.database.windows.net
AZURE_SQL_DATABASE=ritserver
AZURE_SQL_USERNAME=ritesh
AZURE_SQL_PASSWORD=your_password_here

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this
# To generate a new key, run one of these:
# Windows (Python): python -c "import secrets; print(secrets.token_hex(32))"
# Linux/Mac (Python 3): python3 -c "import secrets; print(secrets.token_hex(32))"
# PowerShell: -join ((1..32 | ForEach-Object { Get-Random -Min 0 -Max 256 }) | ForEach-Object { '{0:X2}' -f $_ })
ALGORITHM=HS256
```

**Save:** `Ctrl+S` then `Ctrl+X`

### Step 7: Test Resource Service Manually

```bash
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003
OR
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --env-file .env
```

**Expected Output:**
```
Using AZURE SQL database: ritserver.database.windows.net/ritserver
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
INFO:     Started server process
INFO:     Application startup complete.
```

**Test it:**
```bash
# In another terminal
curl http://localhost:8003/health
# Should return: {"status":"healthy"}
```

If working, press `Ctrl+C` to stop.

### Step 8: Install Gunicorn

```bash
source venv/bin/activate
pip install gunicorn
```

### Step 9: Create Systemd Service

```bash
sudo nano /etc/systemd/system/resource-service.service
```

**Add this content:**
```ini
[Unit]
Description=Resource Service
After=network.target

[Service]
Type=notify
User=user
WorkingDirectory=/home/user/resource-service
Environment="PATH=/home/user/resource-service/venv/bin"
EnvironmentFile=/home/user/resource-service/.env
ExecStart=/home/user/resource-service/venv/bin/gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8003 --timeout 120
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Important:** Replace `user` with your actual username!

**Save:** `Ctrl+S` then `Ctrl+X`

### Step 10: Start and Enable Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable resource-service

# Start service
sudo systemctl start resource-service

# Check status
sudo systemctl status resource-service
```

**Expected Output:**
```
● resource-service.service - Resource Service
   Loaded: loaded (/etc/systemd/system/resource-service.service; enabled)
   Active: active (running) since ...
```

### Step 11: Configure Firewall

```bash
# Allow port 8003
sudo ufw allow 8003/tcp

# Check firewall status
sudo ufw status
```

### Step 12: Test External Access

```bash
curl http://YOUR-BACKEND-VM-IP:8003/health
# Should return: {"status":"healthy"}
```

**Resource Service Deployment Complete!**

---

## Method 2: Build Locally, Deploy to VM

### Step 1: Prepare Code Locally

On your local Windows machine:

```powershell
cd E:\path\to\resource-service
```

### Step 2: Create Environment File Locally

```powershell
notepad .env
```

**Add this content:**
```env
# Azure SQL Database
AZURE_SQL_SERVER=ritserver.database.windows.net
AZURE_SQL_DATABASE=ritserver
AZURE_SQL_USERNAME=ritesh
AZURE_SQL_PASSWORD=your_password_here

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this
# To generate a new key, run one of these:
# Windows (Python): python -c "import secrets; print(secrets.token_hex(32))"
# Linux/Mac (Python 3): python3 -c "import secrets; print(secrets.token_hex(32))"
# PowerShell: -join ((1..32 | ForEach-Object { Get-Random -Min 0 -Max 256 }) | ForEach-Object { '{0:X2}' -f $_ })
ALGORITHM=HS256
```

**Save and close.**

### Step 3: Transfer Code to VM

**Using SCP (from Windows PowerShell)**
```powershell
scp -r "E:\path\to\resource-service" user@vm-ip:"~/"
```

### Step 4: Connect to VM

```bash
ssh user@your-backend-vm-ip
```

### Step 5: Install System Dependencies

```bash
# Update package list
sudo apt update

# Install required packages
sudo apt install -y build-essential python3 python3-venv python3-pip freetds-dev freetds-bin

# Verify Python version
python3 --version
# Should show: Python 3.12.x
```

### Step 6: Create Virtual Environment

```bash
# Navigate to resource-service folder
cd /home/user/resource-service

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in prompt
```

### Step 7: Install Python Dependencies

```bash
# Make sure (venv) is active!
pip install --upgrade pip
pip install -r requirements.txt
# pip install fastapi uvicorn sqlalchemy pymssql python-jose[cryptography] pydantic pydantic-settings python-dotenv gunicorn
```

### Step 8: Test Resource Service Manually

```bash
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003
OR
python -m uvicorn app.main:app --host 0.0.0.0 --port 8003 --env-file .env
```

**Expected Output:**
```
Using AZURE SQL database: ritserver.database.windows.net/ritserver
INFO:     Uvicorn running on http://0.0.0.0:8003
```

**Test it:**
```bash
# In another terminal
curl http://localhost:8003/health
# Should return: {"status":"healthy"}
```

If working, press `Ctrl+C` to stop.

### Step 8-B : Install Gunicorn

```bash
source venv/bin/activate
pip install gunicorn
```

### Step 9: Create Systemd Service

```bash
sudo nano /etc/systemd/system/resource-service.service
```

**Add this content:**
```ini
[Unit]
Description=Resource Service
After=network.target

[Service]
Type=notify
User=user
WorkingDirectory=/home/user/resource-service
Environment="PATH=/home/user/resource-service/venv/bin"
EnvironmentFile=/home/user/resource-service/.env
ExecStart=/home/user/resource-service/venv/bin/gunicorn app.main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8003 --timeout 120
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Important:** Replace `user` with your actual username!

**Save:** `Ctrl+S` then `Ctrl+X`

### Step 10: Start and Enable Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable resource-service

# Start service
sudo systemctl start resource-service

# Check status
sudo systemctl status resource-service
```

**Expected Output:**
```
● resource-service.service - Resource Service
   Loaded: loaded (/etc/systemd/system/resource-service.service; enabled)
   Active: active (running) since ...
```

### Step 11: Configure Firewall

```bash
# Allow port 8003
sudo ufw allow 8003/tcp

# Check firewall status
sudo ufw status
```

### Step 12: Test External Access

```bash
curl http://YOUR-BACKEND-VM-IP:8003/health
# Should return: {"status":"healthy"}
```

**Resource Service Deployment Complete!**

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/resources/` | GET | List all resources |
| `/api/resources/` | POST | Create new resource |
| `/api/resources/{id}` | GET | Get resource by ID |
| `/api/resources/{id}` | PUT | Update resource |
| `/api/resources/{id}` | DELETE | Delete resource |
| `/api/resources/templates` | GET | Get resource templates |
| `/api/resources/import-templates` | POST | Import templates |

---

## Resource Priority

Resources have priority levels:
- **High** - Red badge
- **Medium** - Amber badge (default)
- **Low** - Green badge

---

## Troubleshooting

### Service won't start
```bash
# Check logs
sudo journalctl -u resource-service -f
```

### Database connection failed
```bash
# Test Azure SQL connection
python3 -c "import pymssql; conn = pymssql.connect('ritserver.database.windows.net', 'ritesh', 'password', 'ritserver'); print('Connected!')"
```

### Azure SQL firewall blocking
```
Azure Portal → SQL Server → Networking → Add your VM's public IP
```

### Restart service after changes
```bash
sudo systemctl restart resource-service
sudo systemctl status resource-service
```

---

## Swagger Documentation

Access API docs at: `http://YOUR-VM-IP:8003/docs`

---

**Resource Service v5.0.0** | Port 8003
