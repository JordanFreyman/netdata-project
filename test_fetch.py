"""Fetch CPU metrics from Netdata API for testing."""
import requests

NETDATA_URL = "http://localhost:19999"

def get_cpu_usage():
    """Make a request to the Netdata API and print CPU usage data."""
    endpoint = f"{NETDATA_URL}/api/v1/data"
    params = {
        "chart": "system.cpu",
        "after": -60,  # last 60 seconds
        "format": "json"
    }
    response = requests.get(endpoint, params=params, timeout=5)
    data = response.json()
    print(data)

get_cpu_usage()
