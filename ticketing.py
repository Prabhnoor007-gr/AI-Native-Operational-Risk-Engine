import uuid
import datetime


def route_team(alert):
    routing_map = {
        "Payments_API": "Payments Team",
        "Portfolio_Service": "Portfolio Team",
        "Auth_Service": "Authentication Team",
        "Trading_Engine": "Trading Operations Team"
    }
    return routing_map.get(alert["system"], "General Ops Team")


def create_ticket(alert, classification):
    ticket = {
        "ticket_id": "INC-" + str(uuid.uuid4())[:8],
        "priority": classification["severity"],
        "assigned_team": route_team(alert),
        "summary": f"{alert['error_type']} detected in {alert['system']} "
                   f"({alert['region']}, {alert['host']})",
        "regulatory_risk": classification["regulatory_risk"],
        "requires_human_review": classification["requires_human_review"],
        "created_at": str(datetime.datetime.now())
    }
    return ticket

if __name__ == "__main__":
    from alert_generator import generate_alert
    from risk_engine import classify_alert

    alert = generate_alert()
    classification = classify_alert(alert)
    ticket = create_ticket(alert, classification)

    print(alert)
    print(classification)
    print(ticket)