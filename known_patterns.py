from datetime import datetime


def is_known_benign(alert):
    # Example rule:
    # DB restart every day at 02:00 in development

    alert_time = datetime.fromisoformat(alert["timestamp"])

    if (
            alert["system"] == "Payments_API"
            and alert["host"] == "development"
            and alert_time.hour == 2
            and alert["error_type"] == "Service unavailable"
    ):
        return True

    return False