from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db import get_db, init_db, Resource, User, UserRole
from shared.security import decode_access_token

app = FastAPI(title="Resource Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class ResourceCreate(BaseModel):
    title: str
    resource_name: str
    description: str
    icon: str
    status: str = "Running"
    region: str = "East US"
    created_at: Optional[datetime] = None

class ResourceResponse(BaseModel):
    id: int
    user_id: str
    icon: str
    title: str
    resource_name: str
    description: Optional[str]
    status: str
    region: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class TemplateResponse(BaseModel):
    id: int
    title: str
    resource_name: str
    description: str
    icon: str
    status: str
    region: str

# Comprehensive 70+ Azure Infrastructure & Services Templates
TEMPLATES = [
    # Networking - Core Infrastructure
    {"id": 1, "title": "Virtual Network (VNet)", "resource_name": "vnet-prod", "description": "Virtual network for cloud resources", "icon": "network", "status": "Running", "region": "East US"},
    {"id": 2, "title": "Subnet", "resource_name": "subnet-prod-001", "description": "Subnet within virtual network", "icon": "network", "status": "Running", "region": "East US"},
    {"id": 3, "title": "Network Security Group (NSG)", "resource_name": "nsg-prod", "description": "Firewall rules for network traffic", "icon": "shield", "status": "Running", "region": "East US"},
    {"id": 4, "title": "Network Interface (NIC)", "resource_name": "nic-prod-001", "description": "Network adapter for VMs", "icon": "network", "status": "Running", "region": "East US"},
    {"id": 5, "title": "Public IP Address (PIP)", "resource_name": "pip-prod-001", "description": "Public IP for internet access", "icon": "globe", "status": "Running", "region": "East US"},
    {"id": 6, "title": "Private IP Address", "resource_name": "privateip-prod-001", "description": "Private IP within VNet", "icon": "lock", "status": "Running", "region": "East US"},
    {"id": 7, "title": "Network Watcher", "resource_name": "netwatch-prod", "description": "Monitor network conditions", "icon": "activity", "status": "Running", "region": "East US"},
    {"id": 8, "title": "Route Table", "resource_name": "routetable-prod", "description": "Define network routing rules", "icon": "link", "status": "Running", "region": "East US"},
    
    # Compute - VMs & Servers
    {"id": 9, "title": "Virtual Machine", "resource_name": "vm-prod-001", "description": "IaaS compute instance", "icon": "server", "status": "Running", "region": "East US"},
    {"id": 10, "title": "VM Scale Set", "resource_name": "vmss-prod", "description": "Auto-scaling VM group", "icon": "boxes", "status": "Running", "region": "East US"},
    {"id": 11, "title": "App Service", "resource_name": "app-prod", "description": "PaaS web hosting", "icon": "globe", "status": "Running", "region": "East US"},
    {"id": 12, "title": "Azure Kubernetes Service (AKS)", "resource_name": "aks-prod", "description": "Managed Kubernetes cluster", "icon": "container", "status": "Running", "region": "East US"},
    {"id": 13, "title": "Azure Container Instances", "resource_name": "aci-prod", "description": "Serverless containers", "icon": "container", "status": "Running", "region": "East US"},
    {"id": 14, "title": "Azure Functions", "resource_name": "functions-prod", "description": "Serverless compute", "icon": "zap", "status": "Running", "region": "East US"},
    {"id": 15, "title": "App Service Plan", "resource_name": "appplan-prod", "description": "Compute resources for App Service", "icon": "server", "status": "Running", "region": "East US"},
    
    # Database & Storage
    {"id": 16, "title": "SQL Server", "resource_name": "sqlserver-prod", "description": "Managed SQL Server instance", "icon": "database", "status": "Running", "region": "East US"},
    {"id": 17, "title": "SQL Database", "resource_name": "sqldb-prod", "description": "Managed SQL database", "icon": "database", "status": "Running", "region": "East US"},
    {"id": 18, "title": "SQL Elastic Pool", "resource_name": "elasticpool-prod", "description": "Shared resource pool for databases", "icon": "database", "status": "Running", "region": "East US"},
    {"id": 19, "title": "Azure Cosmos DB", "resource_name": "cosmosdb-prod", "description": "NoSQL distributed database", "icon": "database", "status": "Running", "region": "East US"},
    {"id": 20, "title": "Storage Account", "resource_name": "storage-prod", "description": "Blob, file, queue, table storage", "icon": "hard_drive", "status": "Running", "region": "East US"},
    {"id": 21, "title": "Blob Container", "resource_name": "blob-prod", "description": "Unstructured data storage", "icon": "folder_open", "status": "Running", "region": "East US"},
    {"id": 22, "title": "File Share", "resource_name": "fileshare-prod", "description": "SMB file storage", "icon": "folder", "status": "Running", "region": "East US"},
    {"id": 23, "title": "Azure Data Lake Storage", "resource_name": "datalake-prod", "description": "Big data analytics storage", "icon": "hard_drive", "status": "Running", "region": "East US"},
    {"id": 24, "title": "PostgreSQL Database", "resource_name": "postgres-prod", "description": "Managed PostgreSQL", "icon": "database", "status": "Running", "region": "East US"},
    {"id": 25, "title": "MySQL Database", "resource_name": "mysql-prod", "description": "Managed MySQL", "icon": "database", "status": "Running", "region": "East US"},
    {"id": 26, "title": "MariaDB Database", "resource_name": "mariadb-prod", "description": "Managed MariaDB", "icon": "database", "status": "Running", "region": "East US"},
    
    # Load Balancing & CDN
    {"id": 27, "title": "Load Balancer", "resource_name": "lb-prod", "description": "Layer 4 load balancing", "icon": "network", "status": "Running", "region": "East US"},
    {"id": 28, "title": "Application Gateway", "resource_name": "appgw-prod", "description": "Layer 7 load balancing", "icon": "network", "status": "Running", "region": "East US"},
    {"id": 29, "title": "Traffic Manager", "resource_name": "trafficmgr-prod", "description": "Global DNS load balancing", "icon": "globe", "status": "Running", "region": "East US"},
    {"id": 30, "title": "Azure Front Door", "resource_name": "frontdoor-prod", "description": "Global content delivery", "icon": "globe", "status": "Running", "region": "East US"},
    {"id": 31, "title": "Content Delivery Network (CDN)", "resource_name": "cdn-prod", "description": "Global content distribution", "icon": "globe", "status": "Running", "region": "East US"},
    
    # Security & Identity
    {"id": 32, "title": "Azure Key Vault", "resource_name": "vault-prod", "description": "Secrets and key management", "icon": "key", "status": "Running", "region": "East US"},
    {"id": 33, "title": "Azure Firewall", "resource_name": "firewall-prod", "description": "Cloud firewall service", "icon": "shield", "status": "Running", "region": "East US"},
    {"id": 34, "title": "VPN Gateway", "resource_name": "vpngateway-prod", "description": "Secure VPN connection", "icon": "lock", "status": "Running", "region": "East US"},
    {"id": 35, "title": "ExpressRoute", "resource_name": "expressroute-prod", "description": "Dedicated private network", "icon": "link", "status": "Running", "region": "East US"},
    {"id": 36, "title": "Web Application Firewall (WAF)", "resource_name": "waf-prod", "description": "Application layer protection", "icon": "shield", "status": "Running", "region": "East US"},
    
    # Integration & Messaging
    {"id": 37, "title": "Service Bus", "resource_name": "servicebus-prod", "description": "Cloud messaging service", "icon": "cloud", "status": "Running", "region": "East US"},
    {"id": 38, "title": "Event Hubs", "resource_name": "eventhubs-prod", "description": "Stream processing platform", "icon": "zap", "status": "Running", "region": "East US"},
    {"id": 39, "title": "Event Grid", "resource_name": "eventgrid-prod", "description": "Event routing service", "icon": "zap", "status": "Running", "region": "East US"},
    {"id": 40, "title": "Logic Apps", "resource_name": "logicapps-prod", "description": "Workflow automation", "icon": "link", "status": "Running", "region": "East US"},
    {"id": 41, "title": "API Management", "resource_name": "apim-prod", "description": "API gateway and management", "icon": "link", "status": "Running", "region": "East US"},
    
    # Monitoring & Analytics
    {"id": 42, "title": "Application Insights", "resource_name": "insights-prod", "description": "APM and diagnostics", "icon": "activity", "status": "Running", "region": "East US"},
    {"id": 43, "title": "Azure Monitor", "resource_name": "monitor-prod", "description": "Comprehensive monitoring", "icon": "activity", "status": "Running", "region": "East US"},
    {"id": 44, "title": "Log Analytics Workspace", "resource_name": "loganalytics-prod", "description": "Log aggregation and analysis", "icon": "folder_open", "status": "Running", "region": "East US"},
    {"id": 45, "title": "Synapse Analytics", "resource_name": "synapse-prod", "description": "Enterprise data warehouse", "icon": "activity", "status": "Running", "region": "East US"},
    {"id": 46, "title": "Data Factory", "resource_name": "adf-prod", "description": "Data integration service", "icon": "box", "status": "Running", "region": "East US"},
    
    # AI & Machine Learning
    {"id": 47, "title": "Machine Learning", "resource_name": "ml-prod", "description": "ML model training and deployment", "icon": "zap", "status": "Running", "region": "East US"},
    {"id": 48, "title": "Cognitive Services", "resource_name": "cognitive-prod", "description": "AI services", "icon": "zap", "status": "Running", "region": "East US"},
    {"id": 49, "title": "Bot Service", "resource_name": "bot-prod", "description": "Intelligent bot building", "icon": "server", "status": "Running", "region": "East US"},
    {"id": 50, "title": "Translator", "resource_name": "translator-prod", "description": "Language translation", "icon": "globe", "status": "Running", "region": "East US"},
    
    # Backup & Disaster Recovery
    {"id": 51, "title": "Azure Backup", "resource_name": "backup-prod", "description": "Backup and recovery", "icon": "hard_drive", "status": "Running", "region": "East US"},
    {"id": 52, "title": "Site Recovery", "resource_name": "siterecovery-prod", "description": "Disaster recovery", "icon": "shield", "status": "Running", "region": "East US"},
    
    # DevOps & Management
    {"id": 53, "title": "Azure DevOps", "resource_name": "devops-prod", "description": "CI/CD and project management", "icon": "box", "status": "Running", "region": "East US"},
    {"id": 54, "title": "Container Registry", "resource_name": "registry-prod", "description": "Docker registry", "icon": "container", "status": "Running", "region": "East US"},
    {"id": 55, "title": "Automation Account", "resource_name": "automation-prod", "description": "Process automation", "icon": "zap", "status": "Running", "region": "East US"},
    {"id": 56, "title": "Azure Policy", "resource_name": "policy-prod", "description": "Governance and compliance", "icon": "box", "status": "Running", "region": "East US"},
    {"id": 57, "title": "Resource Group", "resource_name": "rg-prod", "description": "Resource container", "icon": "folder", "status": "Running", "region": "East US"},
    
    # Additional Infrastructure
    {"id": 58, "title": "Managed Disk", "resource_name": "disk-prod", "description": "Block storage for VMs", "icon": "hard_drive", "status": "Running", "region": "East US"},
    {"id": 59, "title": "Image (Custom)", "resource_name": "image-prod", "description": "Custom VM image", "icon": "folder_open", "status": "Running", "region": "East US"},
    {"id": 60, "title": "Snapshot", "resource_name": "snapshot-prod", "description": "Point-in-time disk backup", "icon": "hard_drive", "status": "Running", "region": "East US"},
    {"id": 61, "title": "Availability Set", "resource_name": "avset-prod", "description": "VM redundancy group", "icon": "shield", "status": "Running", "region": "East US"},
    {"id": 62, "title": "Proximity Placement Group", "resource_name": "ppg-prod", "description": "VM placement optimization", "icon": "network", "status": "Running", "region": "East US"},
    
    # Web & Search
    {"id": 63, "title": "Azure Search", "resource_name": "search-prod", "description": "Full-text search", "icon": "folder_open", "status": "Running", "region": "East US"},
    {"id": 64, "title": "Azure Static Web Apps", "resource_name": "swa-prod", "description": "Static website hosting", "icon": "globe", "status": "Running", "region": "East US"},
    {"id": 65, "title": "App Configuration", "resource_name": "appconfig-prod", "description": "Application settings management", "icon": "box", "status": "Running", "region": "East US"},
    
    # Enterprise Services
    {"id": 66, "title": "Azure Advisor", "resource_name": "advisor-prod", "description": "Best practices recommendations", "icon": "folder_open", "status": "Running", "region": "East US"},
    {"id": 67, "title": "Cost Management", "resource_name": "costmgmt-prod", "description": "Cloud spending optimization", "icon": "folder_open", "status": "Running", "region": "East US"},
    {"id": 68, "title": "Reservations (RI)", "resource_name": "reservation-prod", "description": "Compute capacity reservation", "icon": "box", "status": "Running", "region": "East US"},
    {"id": 69, "title": "Hybrid Benefit", "resource_name": "hybrid-prod", "description": "License cost optimization", "icon": "link", "status": "Running", "region": "East US"},
    {"id": 70, "title": "Spot Instances", "resource_name": "spot-prod", "description": "Discounted compute capacity", "icon": "server", "status": "Running", "region": "East US"},
]

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = authorization[7:]
    email = decode_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "Resource Service OK"}

@app.get("/api/resources/", response_model=List[ResourceResponse])
async def list_resources(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resources = db.query(Resource).all()
    return [ResourceResponse.from_orm(r) for r in resources]

@app.get("/api/resources/templates", response_model=List[TemplateResponse])
async def get_templates(current_user: User = Depends(get_current_user)):
    """Get all 70 available Azure infrastructure & services templates"""
    return TEMPLATES

@app.post("/api/resources/import-templates")
async def import_templates(template_ids: List[int], current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Import selected templates as new resources"""
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can import templates")
    
    imported = []
    for tid in template_ids:
        template = next((t for t in TEMPLATES if t["id"] == tid), None)
        if not template:
            continue
        
        resource = Resource(
            user_id=str(current_user.id),
            title=template["title"],
            resource_name=template["resource_name"],
            description=template["description"],
            icon=template["icon"],
            status=template["status"],
            region=template["region"],
            created_at=datetime.utcnow()
        )
        db.add(resource)
        imported.append(template["title"])
    
    db.commit()
    return {"message": f"Imported {len(imported)} templates", "imported": imported}

@app.post("/api/resources/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(data: ResourceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can create resources")
    
    resource = Resource(
        user_id=str(current_user.id),
        title=data.title,
        resource_name=data.resource_name,
        description=data.description,
        icon=data.icon,
        status=data.status,
        region=data.region,
        created_at=data.created_at or datetime.utcnow()
    )
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return ResourceResponse.from_orm(resource)

@app.put("/api/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, data: ResourceCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can update resources")
    
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    resource.title = data.title
    resource.resource_name = data.resource_name
    resource.description = data.description
    resource.icon = data.icon
    resource.status = data.status
    resource.region = data.region
    
    db.commit()
    db.refresh(resource)
    return ResourceResponse.from_orm(resource)

@app.delete("/api/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(resource_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete resources")
    
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db.delete(resource)
    db.commit()
