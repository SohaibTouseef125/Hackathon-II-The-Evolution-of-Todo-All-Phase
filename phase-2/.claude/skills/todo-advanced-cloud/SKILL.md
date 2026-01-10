---
name: todo-advanced-cloud
description: Comprehensive advanced cloud deployment for todo chatbot with Kafka, Dapr, and production-grade Kubernetes. Use when Claude needs to work with the Phase V Hackathon II todo advanced cloud deployment for implementing advanced features like recurring tasks and due date reminders, setting up event-driven architecture with Kafka and Dapr, deploying on production-grade Kubernetes (GKE/AKS), or any other Phase V advanced cloud deployment tasks.
---

# Todo Advanced Cloud - Phase V

## Overview

This skill provides comprehensive guidance for deploying the Todo Chatbot on production-grade cloud infrastructure as part of Hackathon II Phase V. It includes advanced features like recurring tasks and due date reminders, event-driven architecture with Kafka and Dapr, and deployment on cloud Kubernetes platforms like GKE/AKS. The deployment incorporates cloud-native patterns with proper observability, security, and scalability.

## Core Capabilities

### 1. Advanced Feature Implementation
- Recurring tasks with auto-rescheduling
- Due dates and time-based reminders
- Priority and tag/categorization system
- Search and filter functionality
- Sort tasks by various criteria

### 2. Event-Driven Architecture (Kafka)
- Kafka cluster setup and configuration
- Topic design for task events (task-events, reminders, task-updates)
- Producer implementation for task operations
- Consumer services for notifications and recurring tasks
- Event schema design and management

### 3. Dapr Integration (Distributed App Runtime)
- Dapr pub/sub for Kafka abstraction
- State management with PostgreSQL
- Service invocation for inter-service communication
- Bindings for scheduled triggers (cron)
- Secrets management with cloud providers
- Distributed tracing and observability

### 4. Production-Grade Kubernetes Deployment
- GKE/AKS cluster setup and configuration
- Multi-zone deployment for high availability
- Horizontal Pod Autoscaling (HPA) and Vertical Pod Autoscaling (VPA)
- Advanced networking with service mesh (Istio)
- Production monitoring and alerting

## Project Structure

### Recommended Production Structure
```
todo-advanced-cloud/
├── charts/
│   └── todo-enterprise/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-prod.yaml
│       ├── templates/
│       │   ├── kafka/
│       │   │   ├── zookeeper.yaml
│       │   │   ├── kafka-broker.yaml
│       │   │   └── topics.yaml
│       │   ├── dapr/
│       │   │   ├── components.yaml
│       │   │   └── configuration.yaml
│       │   ├── todo-chatbot/
│       │   │   ├── deployment-frontend.yaml
│       │   │   ├── deployment-backend.yaml
│       │   │   ├── deployment-notifications.yaml
│       │   │   ├── deployment-recurring-tasks.yaml
│       │   │   └── services.yaml
│       │   └── monitoring/
│       │       ├── prometheus.yaml
│       │       ├── grafana.yaml
│       │       └── alertmanager.yaml
│       └── files/
│           └── kafka/
│               └── topic-config.json
├── k8s/
│   ├── namespaces.yaml
│   ├── rbac/
│   │   ├── service-accounts.yaml
│   │   ├── roles.yaml
│   │   └── role-bindings.yaml
│   ├── networking/
│   │   ├── ingress.yaml
│   │   ├── istio-gateway.yaml
│   │   └── virtual-services.yaml
│   ├── monitoring/
│   │   ├── service-monitors.yaml
│   │   └── prometheus-rules.yaml
│   └── security/
│       ├── network-policies.yaml
│       └── pod-security-policies.yaml
├── kafka/
│   ├── schemas/
│   │   ├── task-event.avsc
│   │   └── reminder-event.avsc
│   ├── producers/
│   │   └── task-producer.py
│   └── consumers/
│       ├── notification-consumer.py
│       └── recurring-task-consumer.py
├── dapr/
│   ├── components/
│   │   ├── pubsub.yaml
│   │   ├── statestore.yaml
│   │   ├── bindings.yaml
│   │   └── secrets.yaml
│   └── config/
│       └── config.yaml
├── specs/
│   ├── advanced-features.md
│   ├── kafka-architecture.md
│   ├── dapr-integration.md
│   └── cloud-deployment.md
├── scripts/
│   ├── deploy-prod.sh
│   ├── backup.sh
│   ├── health-check.sh
│   └── migrate.sh
├── CLAUDE.md
└── README.md
```

## Advanced Feature Implementation

### 1. Recurring Tasks Service
```python
# kafka/consumers/recurring-task-consumer.py
from kafka import KafkaConsumer
import json
from datetime import datetime, timedelta
import psycopg2
import logging

class RecurringTaskConsumer:
    def __init__(self, bootstrap_servers, db_config):
        self.consumer = KafkaConsumer(
            'recurring-tasks',
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.db_config = db_config
        self.logger = logging.getLogger(__name__)

    def process_recurring_task(self, task_data):
        """Process a recurring task and create next occurrence"""
        try:
            # Connect to database
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()

            # Get the original task
            original_task_id = task_data['original_task_id']
            cursor.execute("""
                SELECT title, description, user_id, recurrence_pattern
                FROM tasks
                WHERE id = %s
            """, (original_task_id,))

            original_task = cursor.fetchone()
            if not original_task:
                self.logger.error(f"Original task {original_task_id} not found")
                return

            title, description, user_id, recurrence_pattern = original_task

            # Calculate next occurrence based on pattern
            next_occurrence = self.calculate_next_occurrence(
                recurrence_pattern,
                datetime.utcnow()
            )

            # Create new task instance
            cursor.execute("""
                INSERT INTO tasks (title, description, user_id, due_date, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (title, description, user_id, next_occurrence, datetime.utcnow()))

            new_task_id = cursor.fetchone()[0]
            conn.commit()

            # Publish event for notification
            # (This would typically send to a Kafka producer)
            self.logger.info(f"Created recurring task {new_task_id} from {original_task_id}")

        except Exception as e:
            self.logger.error(f"Error processing recurring task: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def calculate_next_occurrence(self, pattern, current_date):
        """Calculate next occurrence based on recurrence pattern"""
        if pattern == 'daily':
            return current_date + timedelta(days=1)
        elif pattern == 'weekly':
            return current_date + timedelta(weeks=1)
        elif pattern == 'monthly':
            # Simple monthly calculation (same day next month)
            next_month = current_date.month + 1
            next_year = current_date.year
            if next_month > 12:
                next_month = 1
                next_year += 1

            try:
                return current_date.replace(year=next_year, month=next_month)
            except ValueError:
                # Handle days that don't exist in shorter months
                # e.g., Jan 31 -> Feb 31 (doesn't exist)
                return current_date.replace(year=next_year, month=next_month, day=28)

        # Default to next day for unknown patterns
        return current_date + timedelta(days=1)

    def run(self):
        """Main consumer loop"""
        self.logger.info("Starting recurring task consumer...")
        for message in self.consumer:
            try:
                task_data = message.value
                self.process_recurring_task(task_data)
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
```

### 2. Reminder/Notification Service
```python
# kafka/consumers/notification-consumer.py
from kafka import KafkaConsumer
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

class NotificationConsumer:
    def __init__(self, bootstrap_servers, email_config):
        self.consumer = KafkaConsumer(
            'reminders',
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.email_config = email_config
        self.logger = logging.getLogger(__name__)

    def send_reminder(self, reminder_data):
        """Send reminder notification to user"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = reminder_data['user_email']
            msg['Subject'] = f"Todo Reminder: {reminder_data['title']}"

            body = f"""
            Hi there,

            This is a reminder for your task: {reminder_data['title']}

            Due Date: {reminder_data['due_at']}
            Description: {reminder_data.get('description', 'No description')}

            Please complete this task soon!

            Best regards,
            Todo App
            """

            msg.attach(MIMEText(body, 'plain'))

            # Send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            text = msg.as_string()
            server.sendmail(self.email_config['from_email'], reminder_data['user_email'], text)
            server.quit()

            self.logger.info(f"Reminder sent to {reminder_data['user_email']} for task {reminder_data['task_id']}")

        except Exception as e:
            self.logger.error(f"Error sending reminder: {e}")

    def run(self):
        """Main consumer loop"""
        self.logger.info("Starting notification consumer...")
        for message in self.consumer:
            try:
                reminder_data = message.value
                self.send_reminder(reminder_data)
            except Exception as e:
                self.logger.error(f"Error processing reminder: {e}")
```

## Kafka Event Architecture

### 1. Task Event Schema
```json
// kafka/schemas/task-event.avsc
{
  "type": "record",
  "name": "TaskEvent",
  "namespace": "com.todo",
  "fields": [
    {
      "name": "event_type",
      "type": "string",
      "doc": "Type of event: created, updated, completed, deleted"
    },
    {
      "name": "task_id",
      "type": "int",
      "doc": "The task ID"
    },
    {
      "name": "task_data",
      "type": {
        "type": "record",
        "name": "Task",
        "fields": [
          {"name": "title", "type": "string"},
          {"name": "description", "type": ["null", "string"], "default": null},
          {"name": "completed", "type": "boolean", "default": false},
          {"name": "due_date", "type": ["null", "string"], "default": null},
          {"name": "priority", "type": ["null", "string"], "default": null},
          {"name": "tags", "type": {"type": "array", "items": "string"}, "default": []}
        ]
      }
    },
    {
      "name": "user_id",
      "type": "string",
      "doc": "User who performed action"
    },
    {
      "name": "timestamp",
      "type": "string",
      "doc": "When event occurred"
    }
  ]
}
```

### 2. Reminder Event Schema
```json
// kafka/schemas/reminder-event.avsc
{
  "type": "record",
  "name": "ReminderEvent",
  "namespace": "com.todo",
  "fields": [
    {
      "name": "task_id",
      "type": "int",
      "doc": "The task ID"
    },
    {
      "name": "title",
      "type": "string",
      "doc": "Task title for notification"
    },
    {
      "name": "due_at",
      "type": "string",
      "doc": "When task is due"
    },
    {
      "name": "remind_at",
      "type": "string",
      "doc": "When to send reminder"
    },
    {
      "name": "user_id",
      "type": "string",
      "doc": "User to notify"
    },
    {
      "name": "user_email",
      "type": "string",
      "doc": "User's email for notification"
    }
  ]
}
```

## Dapr Integration

### 1. Dapr Components Configuration
```yaml
# dapr/components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka:9092"
    - name: consumerGroup
      value: "todo-service"
    - name: authRequired
      value: "false"
```

```yaml
# dapr/components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgresql-state
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      value: "host=postgres user=postgres password=pgPassword123! port=5432 database=todo"
    - name: actorStateStore
      value: "true"
```

```yaml
# dapr/components/bindings.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: cron-binding
spec:
  type: bindings.cron
  version: v1
  metadata:
    - name: schedule
      value: "@every 1m"  # Check for reminders every minute
```

```yaml
# dapr/components/secrets.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
spec:
  type: secretstores.kubernetes
  version: v1
```

### 2. Dapr Application Integration
```python
# backend/dapr_integration.py
import httpx
import json
from typing import Dict, Any

class DaprIntegration:
    def __init__(self, dapr_http_port: int = 3500):
        self.dapr_http_port = dapr_http_port
        self.dapr_url = f"http://localhost:{dapr_http_port}"

    async def publish_event(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """Publish event via Dapr pub/sub"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.dapr_url}/v1.0/publish/kafka-pubsub/{topic}",
                    json=event_data,
                    headers={"Content-Type": "application/json"}
                )
                return response.status_code == 200
        except Exception as e:
            print(f"Error publishing event: {e}")
            return False

    async def save_state(self, key: str, value: Any) -> bool:
        """Save state via Dapr state management"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.dapr_url}/v1.0/state/postgresql-state",
                    json=[{
                        "key": key,
                        "value": json.dumps(value)
                    }],
                    headers={"Content-Type": "application/json"}
                )
                return response.status_code == 200
        except Exception as e:
            print(f"Error saving state: {e}")
            return False

    async def get_state(self, key: str) -> Any:
        """Get state via Dapr state management"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.dapr_url}/v1.0/state/postgresql-state/{key}"
                )
                if response.status_code == 200:
                    return json.loads(response.text)
                return None
        except Exception as e:
            print(f"Error getting state: {e}")
            return None

    async def invoke_service(self, app_id: str, method: str, data: Any = None) -> Any:
        """Invoke service via Dapr service invocation"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.dapr_url}/v1.0/invoke/{app_id}/method/{method}"
                if data:
                    response = await client.post(
                        url,
                        json=data,
                        headers={"Content-Type": "application/json"}
                    )
                else:
                    response = await client.get(url)

                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Error invoking service: {e}")
            return None
```

## Production-Grade Kubernetes Configuration

### 1. Horizontal Pod Autoscaler
```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-frontend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-frontend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  minReplicas: 3
  maxReplicas: 15
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65
  - type: Pods
    pods:
      metric:
        name: kafka_consumer_lag
      target:
        type: AverageValue
        averageValue: "100"
```

### 2. Istio Service Mesh Configuration
```yaml
# k8s/networking/istio-gateway.yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: todo-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "todo.example.com"
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: todo-virtualservice
spec:
  hosts:
  - "todo.example.com"
  gateways:
  - todo-gateway
  http:
  - match:
    - uri:
        prefix: /api
    route:
    - destination:
        host: todo-backend
        port:
          number: 8000
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: todo-frontend
        port:
          number: 80
```

### 3. Production Monitoring
```yaml
# k8s/monitoring/service-monitors.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: todo-backend-monitor
  labels:
    app: todo-backend
spec:
  selector:
    matchLabels:
      app: todo-backend
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: todo-alerts
spec:
  groups:
  - name: todo.rules
    rules:
    - alert: TodoBackendDown
      expr: up{job="todo-backend"} == 0
      for: 2m
      labels:
        severity: critical
      annotations:
        summary: "Todo Backend is down"
        description: "Todo Backend has been down for more than 2 minutes"
```

## Cloud-Specific Deployments

### 1. GKE Setup
```bash
# scripts/deploy-gke.sh
#!/bin/bash

# Create GKE cluster
gcloud container clusters create todo-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --machine-type=e2-standard-4 \
    --enable-autoscaling \
    --min-nodes=3 \
    --max-nodes=10 \
    --enable-autorepair \
    --enable-autoupgrade

# Get cluster credentials
gcloud container clusters get-credentials todo-cluster --zone=us-central1-a

# Enable Istio on the cluster
gcloud container fleet mesh update --project=PROJECT_ID --enable-autorelay
```

### 2. AKS Setup
```bash
# scripts/deploy-aks.sh
#!/bin/bash

# Create AKS cluster
az aks create \
    --resource-group todo-rg \
    --name todo-cluster \
    --node-count 3 \
    --node-vm-size Standard_D4s_v3 \
    --enable-cluster-autoscaler \
    --min-count 3 \
    --max-count 10 \
    --enable-addons monitoring \
    --generate-ssh-keys

# Get cluster credentials
az aks get-credentials --resource-group todo-rg --name todo-cluster
```

## Security and Compliance

### 1. Network Security
```yaml
# k8s/security/network-policies.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: todo-frontend-netpol
spec:
  podSelector:
    matchLabels:
      app: todo-frontend
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
      port: 8000  # Backend service
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: todo-backend-netpol
spec:
  podSelector:
    matchLabels:
      app: todo-backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: todo-frontend
    - podSelector:
        matchLabels:
          app: todo-notifications
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 5432  # Database
    - protocol: TCP
      port: 9092  # Kafka
```

### 2. Pod Security Standards
```yaml
# k8s/security/pod-security-policies.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted-todo
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
      - min: 1
        max: 65535
```

## Development Workflow

### 1. Specification Phase
- Create detailed specs in `/specs/` directory
- Define advanced feature requirements and acceptance criteria
- Document Kafka topic schemas and event flows
- Plan Dapr component configurations
- Use Spec-Kit Plus for structured specifications

### 2. Implementation Phase
1. Implement advanced features (recurring tasks, reminders, etc.)
2. Set up Kafka cluster and topic configurations
3. Integrate Dapr for event-driven architecture
4. Configure production-grade Kubernetes deployments
5. Set up monitoring, alerting, and security

### 3. Testing Strategy
- Unit tests for advanced feature logic
- Integration tests for Kafka event flows
- End-to-end tests for Dapr integrations
- Chaos engineering for resilience testing
- Performance testing with realistic load patterns

## Resources

### references/
- `advanced_feature_patterns.md` - Advanced feature implementation patterns
- `kafka_architecture_guide.md` - Kafka event-driven architecture patterns
- `dapr_integration_patterns.md` - Dapr integration best practices
- `cloud_deployment_strategies.md` - Production cloud deployment strategies
- `security_best_practices.md` - Security and compliance guidelines

### assets/
- `kafka_schema_templates/` - Kafka event schema templates
- `dapr_component_templates/` - Dapr component configuration templates
- `cloud_deployment_templates/` - Cloud platform deployment templates
- `monitoring_dashboard_templates/` - Monitoring and alerting templates
