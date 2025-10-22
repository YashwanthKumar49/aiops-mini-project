# AIOps CPU Anomaly Detection

This project monitors Kubernetes pods' CPU usage using Prometheus metrics, detects anomalies using Z-score, and automatically restarts affected pods. It’s packaged as a Docker container and runs as a Kubernetes CronJob.

## Project Structure

- `Dockerfile` → Docker image for the Python script  
- `src/cpu_anomaly.py` → Python script for anomaly detection  
- `k8s/aiops-cronjob.yaml` → Kubernetes CronJob manifest  

## Usage

### Build Docker Image
```bash
docker build -t aiops-cpu-monitor:latest .
