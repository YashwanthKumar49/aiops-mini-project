import requests
import pandas as pd
import numpy as np
from kubernetes import client, config

# -------------------------------
# Prometheus setup
# -------------------------------
PROM_URL = "http://localhost:9090/api/v1/query"
QUERY = 'sum(rate(container_cpu_usage_seconds_total[1m])) by (pod)'

def get_prometheus_data():
    response = requests.get(PROM_URL, params={'query': QUERY})
    data = response.json()['data']['result']
    metrics = {}
    for item in data:
        pod = item['metric']['pod']
        value = float(item['value'][1])
        metrics[pod] = value
    return metrics

# -------------------------------
# Anomaly detection
# -------------------------------
def detect_anomalies(metrics, threshold=2):
    df = pd.DataFrame(list(metrics.items()), columns=['pod', 'cpu'])
    mean = df['cpu'].mean()
    std = df['cpu'].std()
    df['z_score'] = (df['cpu'] - mean) / std
    anomalies = df[df['z_score'].abs() > threshold]
    return anomalies

# -------------------------------
# Kubernetes auto-remediation
# -------------------------------
config.load_kube_config()  # Load kubeconfig
v1 = client.CoreV1Api()

def restart_pod(pod_name, namespace='default'):
    print(f"🔄 Restarting pod: {pod_name}")
    try:
        v1.delete_namespaced_pod(name=pod_name, namespace=namespace)
        print(f"✅ Pod {pod_name} deleted. K8s will recreate it automatically.")
    except Exception as e:
        print(f"❌ Error restarting pod {pod_name}: {e}")

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    metrics = get_prometheus_data()
    anomalies = detect_anomalies(metrics)

    if not anomalies.empty:
        print("⚠️ Anomalies detected:")
        print(anomalies)

        # Restart anomalous pods
        for pod in anomalies['pod']:
            restart_pod(pod, namespace='kube-system')  # adjust namespace if needed
    else:
        print("✅ No anomalies detected. CPU usage normal.")
