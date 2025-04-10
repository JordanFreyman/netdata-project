import requests
from datetime import datetime
from app.models import db, MetricLogs
import urllib.parse
def log_metrics():
    print(f"[{datetime.utcnow()}] Logging system metrics...")

    cluster_ips = [
        "127.0.0.1",
        "172.104.17.8",
        "173.255.230.24",
        "66.228.34.180"
    ]

    charts = {
        "cpu": "system.cpu",
        "memory": "system.ram",
        "disk": "disk_space./",
        "network": "system.net"
    }

    for ip in cluster_ips:
        print(f"\n--- {ip} ---")
        metrics = {}

        for metric_name, chart in charts.items():
                try:
                    encoded_chart = urllib.parse.quote(chart)
                    url = f"http://{ip}:19999/api/v1/data"
                    params = {
                        "chart": encoded_chart,
                        "after": -60,
                        "format": "json"
                    }
                    response = requests.get(url, params=params, timeout=5)
                    response.raise_for_status()
                    json_data = response.json()
                    rows = json_data.get("data", [])

                    values = [sum(row[1:]) for row in rows if len(row) > 1]
                    avg = sum(values) / len(values) if values else None

                    print(f"{metric_name.capitalize()}: Retrieved {len(rows)} points, avg={avg}")
                    metrics[metric_name] = avg
                except Exception as e:
                    print(f"{ip}: Error fetching data: {e}")
                    metrics[metric_name] = None
        log = MetricLogs(
            machine_name=ip,
            cpu_usage=metrics.get("cpu"),
            memory_usage=metrics.get("memory"),
            disk_usage=metrics.get("disk"),
            network_usage=metrics.get("network")
        )
        db.session.add(log)

    db.session.commit()
