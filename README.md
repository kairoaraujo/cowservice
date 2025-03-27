# Cowsay FastAPI Application

## Overview
This is a simple FastAPI application that generates cowsay messages and stores them in text files with unique hex UUIDs.

## Prerequisites
- Python 3.9+
- Docker
- Kubernetes
- Helm

## Local Development

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Application
```bash
uvicorn main:app --reload
```

## Docker Build
```bash
docker build -t cowservice .
docker run -p 8000:8000 cowservice
```

## Kubernetes Deployment

### Build Docker Image
```bash
docker build -t cowservice:latest .
```

### Deploy with Helm
```bash
helm install cowservice ./charts/cowservice
```

## API Endpoint
- POST `/generate/<name>`
  - Generates a cowsay message for the given name
  - Stores the message in a file with a hex UUID
  - Returns the generated UUID

### Example
```bash
curl -X POST http://localhost:8000/generate/World
# Returns: {"uuid": "hexuuid"}
```

## Notes
- Generated files are stored in `/data/outputs` 
- Each file is named `<hex-uuid>.txt`
- Persistent Volume Claim (PVC) is used to store generated files

# Cowsay FastAPI Application with Nginx File Serving

## Overview
This application consists of:
- A FastAPI service for generating cowsay messages
- An Nginx service to serve the generated files
- Persistent Volume Claim (PVC) for file storage

## Prerequisites
- Docker
- Kubernetes
- Helm
- Helm repositories added:
  ```bash
  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm repo update
  ```

## Deployment Steps

### 1. Install Helm Chart
```bash
helm install cowservice ./charts
```

### 2. Access Generated Files
- The Nginx service will expose files in the `/data/outputs` directory
- Files can be accessed via the Nginx service ClusterIP

## Application Workflow
1. Send a POST request to generate a file:
   ```bash
   curl -X POST http://cowsay-service:8000/generate/World
   # Returns: {"uuid": "hexuuid"}
   ```

2. Access the generated file:
   - Direct file access: `http://nginx-service/hexuuid.txt`
   - Nginx directory listing is enabled

## Kubernetes Resources Created
- Deployments:
  - Cowsay FastAPI Application
  - Nginx File Server
- Services:
  - Cowsay FastAPI Service
  - Nginx File Serving Service
- Persistent Volume Claim
- ConfigMap for Nginx configuration

## Configuration Options
Customize in `values.yaml`:
- Number of replicas
- Image tags
- Service types
- Storage size

## Notes
- Generated files are stored in a shared PVC
- Nginx serves files with directory listing enabled
- Persistent storage ensures file durability