import requests
from datetime import datetime

def log_metrics():
    print(f"[{datetime.utcnow()}] Logging system metrics...")

    cluster_ips = [
        "127.0.0.1",
        "172.104.17.8",
        "173.255.230.24",
        "66.228.34.180"
    ]

    for ip in cluster_ips:
        try:
            url = f"http://{ip}:19999/api/v1/data"
            params = {
                "chart": "system.cpu",
                "after": -60,
                "format": "json"
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            print(f"{ip}: Got {len(data.get('data', []))} data points")
        except Exception as e:
            print(f"{ip}: Error fetching data: {e}")
