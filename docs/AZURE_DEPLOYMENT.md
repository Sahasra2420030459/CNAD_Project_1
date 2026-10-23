# Azure Cloud Production Deployment Guide

> [!IMPORTANT]
> This guide is for deploying the platform to Microsoft Azure. Per project safety rules, **do not execute these commands or provision cloud resources without explicit user approval**, as Azure charges may apply.

---

## 1. Cloud Architecture Overview

| Component | Target Azure Service | SKU / Configuration |
| :--- | :--- | :--- |
| **Frontend UI** | Azure Static Web Apps | Free / Standard Tier |
| **Backend REST API** | Azure App Service (Linux) | B1 (Basic) / P1V2 (Production) |
| **Worker Engine** | Azure Container Apps | Consumption (Serverless, KEDA queue autoscaling) |
| **Database** | Azure Database for MySQL Flexible Server | Burstable B1ms / General Purpose |
| **Object Storage** | Azure Blob Storage | Standard LRS (Hot Access Tier) |
| **Async Messaging** | Azure Queue Storage | Standard Queue Storage |

---

## 2. Infrastructure Setup (Azure CLI)

### 2.1 Set Variables
```bash
RESOURCE_GROUP="rg-videoplatform-prod"
LOCATION="eastus"
STORAGE_ACCOUNT="stvideoplatform$RANDOM"
MYSQL_SERVER="mysql-videoplatform-$RANDOM"
APP_SERVICE_PLAN="asp-videoplatform"
BACKEND_APP="app-videoplatform-api-$RANDOM"
CONTAINER_APP_ENV="cae-videoplatform"
CONTAINER_WORKER="worker-videoplatform"
ACR_NAME="acrvideoplatform$RANDOM"
```

### 2.2 Create Resource Group
```bash
az group create --name $RESOURCE_GROUP --location $LOCATION
```

### 2.3 Provision Azure Storage (Blob + Queue)
```bash
# Create storage account
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS

# Retrieve connection string
CONNECTION_STRING=$(az storage account show-connection-string \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --output tsv)

# Create Blob Container for videos
az storage container create \
  --name video-processing \
  --connection-string "$CONNECTION_STRING" \
  --public-access off

# Create Queue for async jobs
az storage queue create \
  --name video-compression-jobs \
  --connection-string "$CONNECTION_STRING"
```

### 2.4 Provision Azure Database for MySQL Flexible Server
```bash
az mysql flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name $MYSQL_SERVER \
  --location $LOCATION \
  --admin-user cloudadmin \
  --admin-password "P@ssw0rdCloudSecure2026!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 8.0 \
  --storage-size 32

# Allow Azure Services to access MySQL
az mysql flexible-server firewall-rule create \
  --resource-group $RESOURCE_GROUP \
  --name $MYSQL_SERVER \
  --rule-name AllowAllAzureIPs \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Create application database
az mysql flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $MYSQL_SERVER \
  --database-name videoplatform
```

### 2.5 Provision Azure Container Registry (ACR)
```bash
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# Login to registry
az acr login --name $ACR_NAME
```

---

## 3. Deploying the Backend API (Azure App Service)

```bash
# Build and tag backend image
docker build -t $ACR_NAME.azurecr.io/videoplatform-backend:latest ./backend
docker push $ACR_NAME.azurecr.io/videoplatform-backend:latest

# Create App Service Plan (Linux)
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --is-linux \
  --sku B1

# Create App Service with Container
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $BACKEND_APP \
  --deployment-container-image-name $ACR_NAME.azurecr.io/videoplatform-backend:latest

# Configure App Service Environment Variables
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $BACKEND_APP \
  --settings \
    SPRING_PROFILES_ACTIVE=azure \
    DB_HOST="${MYSQL_SERVER}.mysql.database.azure.com" \
    DB_PORT=3306 \
    DB_NAME="videoplatform" \
    DB_USERNAME="cloudadmin" \
    DB_PASSWORD="P@ssw0rdCloudSecure2026!" \
    DB_USE_SSL="true" \
    STORAGE_TYPE="azure" \
    AZURE_STORAGE_CONNECTION_STRING="$CONNECTION_STRING" \
    AZURE_BLOB_CONTAINER_NAME="video-processing" \
    QUEUE_TYPE="azure" \
    AZURE_QUEUE_NAME="video-compression-jobs" \
    JWT_SECRET="YourProductionGrade256BitSecretKeyHereMustBeKeptSecret12345"
```

---

## 4. Deploying the Worker (Azure Container Apps with KEDA Queue Autoscaling)

The worker container includes OpenJDK and FFmpeg. We deploy it as an Azure Container App that can scale to 0 when the queue is idle, and scale out up to 10 instances when batches of videos arrive.

```bash
# Build and tag worker image
docker build -t $ACR_NAME.azurecr.io/videoplatform-worker:latest ./worker
docker push $ACR_NAME.azurecr.io/videoplatform-worker:latest

# Create Container Apps Environment
az containerapp env create \
  --name $CONTAINER_APP_ENV \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Get ACR credentials
ACR_PASS=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Deploy Container App with KEDA Azure Queue Autoscaling
az containerapp create \
  --name $CONTAINER_WORKER \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_APP_ENV \
  --image $ACR_NAME.azurecr.io/videoplatform-worker:latest \
  --registry-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_NAME \
  --registry-password "$ACR_PASS" \
  --min-replicas 0 \
  --max-replicas 10 \
  --scale-rule-name "queue-based-autoscaling" \
  --scale-rule-type "azure-queue" \
  --scale-rule-metadata \
    queueName="video-compression-jobs" \
    queueLength="2" \
  --scale-rule-auth "connection=$CONNECTION_STRING" \
  --env-vars \
    SPRING_PROFILES_ACTIVE=azure \
    DB_HOST="${MYSQL_SERVER}.mysql.database.azure.com" \
    DB_PORT=3306 \
    DB_NAME="videoplatform" \
    DB_USERNAME="cloudadmin" \
    DB_PASSWORD="P@ssw0rdCloudSecure2026!" \
    DB_USE_SSL="true" \
    STORAGE_TYPE="azure" \
    AZURE_STORAGE_CONNECTION_STRING="$CONNECTION_STRING" \
    AZURE_BLOB_CONTAINER_NAME="video-processing" \
    QUEUE_TYPE="azure" \
    AZURE_QUEUE_NAME="video-compression-jobs" \
    WORKER_FFMPEG_SIMULATION_MODE="false"
```

---

## 5. Deploying Frontend (Azure Static Web Apps)

1. Commit your repository to GitHub.
2. In the Azure Portal or via Azure CLI:
```bash
az staticwebapp create \
  --name "swa-videoplatform-web" \
  --resource-group $RESOURCE_GROUP \
  --source "https://github.com/YourUsername/cnad_project" \
  --location $LOCATION \
  --branch main \
  --app-location "/frontend" \
  --output-location "build"
```
3. Set the environment variable `REACT_APP_API_BASE_URL` in Azure Static Web Apps Configuration to:
   `https://<YOUR_APP_SERVICE_NAME>.azurewebsites.net/api`
