---
name: todo-kubernetes
description: Comprehensive Kubernetes deployment for todo chatbot with Minikube, Helm Charts, and AIOps tools. Use when Claude needs to work with the Phase IV Hackathon II todo kubernetes deployment for containerizing frontend and backend applications with Docker, creating Helm charts for deployment, using kubectl-ai and kagent for AI-assisted Kubernetes operations, deploying on Minikube locally, or any other Phase IV kubernetes deployment tasks.
---

# Todo Kubernetes - Phase IV

## Overview

This skill provides comprehensive guidance for deploying the Todo Chatbot on Kubernetes as part of Hackathon II Phase IV. It includes containerization with Docker, Helm chart creation, AI-assisted Kubernetes operations using kubectl-ai and kagent, and deployment on Minikube locally. The deployment follows cloud-native best practices with proper resource management and observability.

## Core Capabilities

### 1. Containerization (Docker)
- Dockerfile creation for frontend and backend applications
- Multi-stage builds for optimized images
- Environment configuration and secrets management
- Image tagging and versioning strategies
- Docker Compose for local development

### 2. Helm Chart Development
- Helm chart structure and templates
- Parameterized deployments with values.yaml
- Kubernetes resource definitions (Deployments, Services, ConfigMaps)
- Ingress configuration for external access
- Database deployment and initialization

### 3. AI-Assisted Kubernetes Operations (AIOps)
- kubectl-ai for intelligent Kubernetes operations
- Kagent for advanced cluster management
- AI-powered troubleshooting and optimization
- Intelligent resource scaling and allocation
- Automated cluster health analysis

### 4. Minikube Deployment
- Local Kubernetes cluster setup
- Resource allocation and configuration
- Service exposure and ingress setup
- Persistent volume management
- Multi-node cluster configuration

## Project Structure

### Recommended Deployment Structure
```
todo-kubernetes/
├── charts/
│   └── todo-chatbot/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── templates/
│       │   ├── deployment-frontend.yaml
│       │   ├── deployment-backend.yaml
│       │   ├── service-frontend.yaml
│       │   ├── service-backend.yaml
│       │   ├── ingress.yaml
│       │   ├── configmap.yaml
│       │   └── secret.yaml
│       └── ci/
│           └── values-dev.yaml
├── docker/
│   ├── frontend/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   └── backend/
│       └── Dockerfile
├── k8s/
│   ├── namespace.yaml
│   ├── rbac.yaml
│   ├── monitoring/
│   │   ├── prometheus.yaml
│   │   └── grafana.yaml
│   └── networking/
│       ├── ingress.yaml
│       └── network-policy.yaml
├── scripts/
│   ├── deploy.sh
│   ├── health-check.sh
│   └── backup.sh
├── specs/
│   ├── k8s-deployment.md
│   ├── helm-chart-spec.md
│   └── monitoring-strategy.md
├── CLAUDE.md
└── README.md
```

## Docker Configuration

### 1. Frontend Dockerfile
```dockerfile
# docker/frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ ./
RUN npm run build

FROM nginx:alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY docker/frontend/nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 2. Backend Dockerfile
```dockerfile
# docker/backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 3. Docker Compose for Local Development
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: .
      dockerfile: docker/frontend/Dockerfile
    ports:
      - "3000:80"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend
    restart: unless-stopped

  backend:
    build:
      context: .
      dockerfile: docker/backend/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/todo_db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: todo_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

## Helm Chart Configuration

### 1. Chart.yaml
```yaml
# charts/todo-chatbot/Chart.yaml
apiVersion: v2
name: todo-chatbot
description: A Helm chart for deploying the Todo Chatbot
type: application
version: 0.1.0
appVersion: "1.0.0"

dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
  - name: redis
    version: 18.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

### 2. Values.yaml
```yaml
# charts/todo-chatbot/values.yaml
# Frontend configuration
frontend:
  replicaCount: 2
  image:
    repository: todo-frontend
    pullPolicy: IfNotPresent
    tag: ""
  service:
    type: ClusterIP
    port: 80
  ingress:
    enabled: true
    className: nginx
    hosts:
      - host: todo.local
        paths:
          - path: /
            pathType: ImplementationSpecific
    tls: []

# Backend configuration
backend:
  replicaCount: 2
  image:
    repository: todo-backend
    pullPolicy: IfNotPresent
    tag: ""
  service:
    type: ClusterIP
    port: 8000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 250m
      memory: 256Mi

# Database configuration
postgresql:
  enabled: true
  auth:
    username: todo_user
    password: "todo_password"
    database: todo_db
  primary:
    persistence:
      enabled: true
      size: 8Gi

# Redis configuration
redis:
  enabled: true
  auth:
    enabled: false

# Global settings
global:
  domain: todo.local
```

### 3. Frontend Deployment Template
```yaml
# charts/todo-chatbot/templates/deployment-frontend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-frontend
  labels:
    {{- include "todo-chatbot.labels" . | nindent 4 }}
    app.kubernetes.io/component: frontend
spec:
  replicas: {{ .Values.frontend.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-chatbot.selectorLabels" . | nindent 6 }}
      app.kubernetes.io/component: frontend
  template:
    metadata:
      labels:
        {{- include "todo-chatbot.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: frontend
    spec:
      containers:
        - name: frontend
          image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.frontend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          env:
            - name: NEXT_PUBLIC_API_URL
              value: "http://{{ include "todo-chatbot.fullname" . }}-backend:{{ .Values.backend.service.port }}"
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
          resources:
            {{- toYaml .Values.frontend.resources | nindent 12 }}
```

### 4. Backend Deployment Template
```yaml
# charts/todo-chatbot/templates/deployment-backend.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chatbot.fullname" . }}-backend
  labels:
    {{- include "todo-chatbot.labels" . | nindent 4 }}
    app.kubernetes.io/component: backend
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-chatbot.selectorLabels" . | nindent 6 }}
      app.kubernetes.io/component: backend
  template:
    metadata:
      labels:
        {{- include "todo-chatbot.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: backend
    spec:
      containers:
        - name: backend
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "todo-chatbot.fullname" . }}-db-secret
                  key: database_url
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: {{ include "todo-chatbot.fullname" . }}-api-key
                  key: openai_api_key
          livenessProbe:
            httpGet:
              path: /health
              port: http
          readinessProbe:
            httpGet:
              path: /health
              port: http
          resources:
            {{- toYaml .Values.backend.resources | nindent 12 }}
```

## Kubernetes Deployment with Minikube

### 1. Minikube Setup
```bash
# Install and start Minikube
minikube start --cpus=4 --memory=8192 --disk-size=40g

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard
```

### 2. Deployment Commands
```bash
# Build Docker images for Minikube
eval $(minikube docker-env)
docker build -f docker/frontend/Dockerfile -t todo-frontend:latest .
docker build -f docker/backend/Dockerfile -t todo-backend:latest .

# Deploy with Helm
helm install todo-chatbot charts/todo-chatbot --values charts/todo-chatbot/values.yaml

# Verify deployment
kubectl get pods
kubectl get services
kubectl get ingress
```

## AIOps with kubectl-ai and Kagent

### 1. kubectl-ai Commands
```bash
# Deploy the todo frontend with 2 replicas
kubectl-ai "deploy the todo frontend with 2 replicas"

# Scale the backend to handle more load
kubectl-ai "scale the backend to handle more load"

# Check why the pods are failing
kubectl-ai "check why the pods are failing"

# Optimize resource allocation
kubectl-ai "optimize resource allocation for todo chatbot"

# Analyze cluster health
kubectl-ai "analyze cluster health and performance"
```

### 2. Kagent Commands
```bash
# Analyze the cluster health
kagent "analyze the cluster health"

# Optimize resource allocation
kagent "optimize resource allocation"

# Troubleshoot deployment issues
kagent "troubleshoot deployment issues with todo-chatbot"

# Monitor application performance
kagent "monitor application performance and suggest optimizations"
```

## Deployment Workflow

### 1. Pre-deployment Preparation
1. Set up Minikube cluster with appropriate resources
2. Build Docker images for frontend and backend
3. Configure Helm values for the target environment
4. Validate Helm chart templates

### 2. Deployment Process
1. Deploy database and wait for initialization
2. Deploy backend services and verify connectivity
3. Deploy frontend and configure ingress
4. Test application functionality
5. Set up monitoring and alerting

### 3. Post-deployment Validation
- Verify all pods are running and healthy
- Test application functionality through ingress
- Validate resource utilization
- Set up automated backups
- Configure monitoring dashboards

## Monitoring and Observability

### 1. Prometheus Configuration
```yaml
# k8s/monitoring/prometheus.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    rule_files:
      - "rules.yml"
    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
        - role: pod
        relabel_configs:
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
          action: keep
          regex: true
```

### 2. Grafana Dashboard
```yaml
# k8s/monitoring/grafana.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-config
data:
  todo-dashboard.json: |
    {
      "dashboard": {
        "title": "Todo Chatbot Dashboard",
        "panels": [
          {
            "title": "Application Health",
            "type": "stat",
            "targets": [
              {
                "expr": "up{job=\"todo-backend\"}",
                "legendFormat": "Backend Health"
              }
            ]
          }
        ]
      }
    }
```

## Security Best Practices

### 1. RBAC Configuration
```yaml
# k8s/rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: todo-chatbot-sa
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: todo-chatbot-role
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: todo-chatbot-rolebinding
subjects:
- kind: ServiceAccount
  name: todo-chatbot-sa
roleRef:
  kind: Role
  name: todo-chatbot-role
  apiGroup: rbac.authorization.k8s.io
```

### 2. Network Policies
```yaml
# k8s/networking/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: todo-chatbot-netpol
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: todo-chatbot
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 80
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 5432  # Database
    - protocol: TCP
      port: 443   # External API calls
```

## Development Workflow

### 1. Specification Phase
- Create detailed specs in `/specs/` directory
- Define Helm chart structure and parameters
- Document Kubernetes resource requirements
- Use Spec-Kit Plus for structured specifications

### 2. Implementation Phase
1. Create Dockerfiles for containerization
2. Build Helm charts with proper templates
3. Set up AIOps tools (kubectl-ai, Kagent)
4. Configure Minikube for local deployment
5. Test deployment process and validate

### 3. Testing Strategy
- Unit tests for Docker builds
- Helm chart validation with `helm lint`
- Integration tests for Kubernetes deployment
- Performance testing with load simulation

## Resources

### references/
- `docker_best_practices.md` - Docker containerization guidelines
- `helm_chart_guide.md` - Helm chart development and best practices
- `kubernetes_deployment_patterns.md` - K8s deployment patterns and practices
- `aiops_automation.md` - AI-assisted Kubernetes operations
- `minikube_setup_guide.md` - Minikube configuration and deployment

### assets/
- `dockerfile_templates/` - Dockerfile templates for different runtimes
- `helm_chart_templates/` - Helm chart templates and examples
- `k8s_resource_templates/` - Kubernetes resource definition templates
- `deployment_scripts/` - Automated deployment and management scripts
