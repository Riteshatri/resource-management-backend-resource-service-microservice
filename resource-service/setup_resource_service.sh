#!/bin/bash
set -e

# ===============================
# VARIABLES
# ===============================
VM_USER="ubuntu"
APP_NAME="resource-service"
APP_DIR="/home/$VM_USER/resource-service"
VENV_DIR="$APP_DIR/venv"
SERVICE_NAME="resource-service"
PORT="8003"

echo "👉 Starting setup for $APP_NAME"

# ===============================
# PYTHON VENV SETUP
# ===============================
cd $APP_DIR

echo "👉 Creating virtual environment"
python3 -m venv venv

echo "👉 Activating venv"
source venv/bin/activate

echo "👉 Upgrading pip"
pip install --upgrade pip

echo "👉 Installing requirements"
pip install -r requirements.txt

echo "👉 Installing gunicorn"
pip install gunicorn

deactivate

# ===============================
# SYSTEMD SERVICE CREATION
# ===============================
echo "👉 Creating systemd service"

sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=Resource Service
After=network.target

[Service]
Type=notify
User=$VM_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
EnvironmentFile=$APP_DIR/.env
ExecStart=$VENV_DIR/bin/gunicorn app.main:app \
  --workers 2 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:$PORT \
  --timeout 120
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# ===============================
# SYSTEMD COMMANDS
# ===============================
echo "👉 Reloading systemd"
sudo systemctl daemon-reload

echo "👉 Enabling service"
sudo systemctl enable $SERVICE_NAME

echo "👉 Starting service"
sudo systemctl start $SERVICE_NAME

echo "👉 Service status"
sudo systemctl status $SERVICE_NAME --no-pager

echo "✅ SETUP COMPLETED SUCCESSFULLY"






# ▶ RUN SCRIPT
# chmod +x setup_resource_service.sh
# ./setup_resource_service.sh


# DEBUG KE LIYE
# journalctl -u resource-service -f
# sudo systemctl restart resource-service
# ss -tulnp | grep 8003