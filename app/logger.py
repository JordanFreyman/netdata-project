"""Log metrics from each cluster machine by querying Netdata API endpoints."""

from datetime import datetime, timezone
import urllib.parse
import requests

from app.models import db, MetricLogs


def log_metrics():
    """Fetch and log CPU, memory, disk, and network usage from cluster nodes."""
    print(f"[{datetime.now(timezone.utc)}] Logging system metrics...")

    cluster_ips = [
        "127.0.0.1",
        "172.104.17.8",
        "173.255.230.24",
        "66.228.34.180",
        "66.175.210.204"
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
                    "format": "json",
                    "options": "absolute,dimension_names"
                }
                response = requests.get(url, params=params, timeout=5)
                response.raise_for_status()

                json_data = response.json()
                rows = json_data.get("data", [])
                dim_names = json_data.get("labels", [])[1:]

                print(f"{ip} - {metric_name} dimensions: {dim_names}")

                if metric_name in ["memory", "disk"]:
                    if "used" in dim_names:
                        used_index = dim_names.index("used")
                        values = [
                            row[used_index + 1]
                            for row in rows
                            if len(row) > used_index + 1
                        ]
                        avg = sum(values) / len(values) if values else None
                    else:
                        print(f"{ip} - 'used' not found in dimensions for {metric_name}. Got: {dim_names}")
                        avg = None
                else:
                    values = [sum(row[1:]) for row in rows if len(row) > 1]
                    avg = sum(values) / len(values) if values else None

                unit = {
                    "cpu": "%",
                    "memory": "MiB",
                    "disk": "GiB",
                    "network": "KiB/s"
                }.get(metric_name, "")

                print(f"{ip} - {metric_name.capitalize()}: {avg:.2f} {unit} (from {len(rows)} points)")

                metrics[metric_name] = avg

            except requests.RequestException as err:
                print(f"{ip}: Error fetching {metric_name} data: {err}")
                metrics[metric_name] = None

        if all(value is None for value in metrics.values()):
            print(f"{ip} No valid metrics fetched — skipping logging.")
            continue

        log = MetricLogs(
            machine_name=ip,
            cpu_usage=metrics.get("cpu"),
            memory_usage=metrics.get("memory"),
            disk_usage=metrics.get("disk"),
            network_usage=metrics.get("network")
        )
        db.session.add(log)

    db.session.commit()


if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        log_metrics()
