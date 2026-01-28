# K8s Healthcheck Reference

Reference guide for implementing health checks in Kubernetes environments.

## Core Concepts

### Dockerfile HEALTHCHECK vs K8s Probes

**Critical:** Dockerfile `HEALTHCHECK` directives are Docker-specific and **ignored by Kubernetes**.

| Feature | Scope | Purpose |
|---------|-------|---------|
| `Dockerfile HEALTHCHECK` | Docker only | Container health in Docker runtime |
| `K8s livenessProbe` | Kubernetes | Restart unhealthy pods |
| `K8s readinessProbe` | Kubernetes | Control traffic routing |

**Common misconception:** Adding `HEALTHCHECK` to Dockerfile will work in K8s. It won't.

## When to Use Health Checks

### Deployment Workloads

**Always use probes for:**
- Web services
- API servers
- Long-running processes

### Job Workloads

**Usually unnecessary for Jobs:**
- Jobs terminate with exit codes (success/failure)
- K8s monitors completion status automatically

**Use probes for Jobs when:**
- Risk of hang/deadlock exists
- Need to detect unresponsive processes

## Failure Detection Matrix

| Failure Type | Detection Without Probe | Detection With Probe |
|--------------|-------------------------|----------------------|
| OOM (Out of Memory) | Kernel kills pod → K8s detects | Same (probe not needed) |
| Crash/Exit | Exit code → K8s detects | Same (probe not needed) |
| Hang/Deadlock | Pod stays Running → undetected | Probe fails → K8s restarts |
| Memory leak (slow) | Pod stays Running → undetected | Probe timeout → K8s restarts |

**Key insight:** Probes detect problems that keep pod in "Running" state but non-functional.

## Implementation Patterns

### Python HTTP Health Server

Add background HTTP server for health checks:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress logs

def start_health_server(port=8080):
    server = HTTPServer(('', port), HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

# In main:
start_health_server(port=8080)
```

### K8s Deployment with Probe

```yaml
spec:
  containers:
  - name: app
    image: myapp:latest
    ports:
    - containerPort: 8080
    livenessProbe:
      httpGet:
        path: /health
        port: 8080
      initialDelaySeconds: 10
      periodSeconds: 30
      timeoutSeconds: 5
      failureThreshold: 3
```

### Dynamic Pod Creation (e.g., from Worker)

When worker code creates pods dynamically, probe must be set in pod spec:

```typescript
// In pod-manager.ts or similar
const podSpec = {
  containers: [{
    name: 'agent',
    image: agentImage,
    livenessProbe: {
      httpGet: {
        path: '/health',
        port: 8080
      },
      initialDelaySeconds: 10,
      periodSeconds: 30,
      timeoutSeconds: 5,
      failureThreshold: 3
    }
  }]
};
```

**Note:** Cannot configure probes via ConfigMap. Must be in pod spec.

## Probe Configuration

### Recommended Settings

| Parameter | Development | Production | Notes |
|-----------|-------------|------------|-------|
| `initialDelaySeconds` | 5-10 | 10-30 | Time for app startup |
| `periodSeconds` | 10-30 | 30-60 | Check interval |
| `timeoutSeconds` | 3-5 | 5-10 | Response timeout |
| `failureThreshold` | 2-3 | 3-5 | Failures before restart |

### Tuning Guidelines

**Short intervals (10-30s):** Use for critical services needing fast failure detection.

**Long intervals (60s+):** Use for heavy health checks or non-critical services.

**High failureThreshold (5+):** Reduce false positives from transient issues.

## Related

- K8s Probe documentation: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- Arkraft agent implementations: arkraft-agent-insight, arkraft-worker

## Session Context

Learnings from arkraft-agent-insight and arkraft-worker K8s healthcheck implementation (2026-01-28).
