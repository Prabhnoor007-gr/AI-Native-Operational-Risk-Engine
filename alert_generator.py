import random
import datetime

systems = ["Payments_API", "Portfolio_Service", "Auth_Service", "Trading_Engine"]
regions = ["US-East", "US-West", "Canada-East"]
hosts = ["prod", "development", "testing"]

error_types = [
    "Database timeout",
    "Latency spike",
    "Transaction failure",
    "Authentication failure",
    "Service unavailable"
]

def generate_alert():
    alert = {
        "client": "WealthPlatform",
        "system": random.choice(systems),
        "region": random.choice(regions),
        "host": random.choice(hosts),   # NEW FIELD
        "error_type": random.choice(error_types),
        "failure_rate": random.randint(1, 50),
        "latency_ms": random.randint(100, 5000),
        "timestamp": str(datetime.datetime.now())
    }
    return alert


if __name__ == "__main__":
    print(generate_alert())

