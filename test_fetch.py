import requests

NETDATA_URL = "http://localhost:19999"

def get_cpu_usage():
    endpoint = f"{NETDATA_URL}/api/v1/data"
    params = {
        "chart": "system.cpu",
        "after": -60,  # last 60 seconds
        "format": "json"
    }
    response = requests.get(endpoint, params=params)
    data = response.json()
    print(data)

get_cpu_usage()

