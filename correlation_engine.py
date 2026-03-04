def correlate_alerts(alerts):
    grouped = {}

    for alert in alerts:
        key = (alert["system"], alert["region"], alert["host"])
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(alert)

    correlated_incidents = []

    for key, group in grouped.items():
        if len(group) > 2:  # 3+ similar alerts = correlated incident
            correlated_incidents.append({
                "system": key[0],
                "region": key[1],
                "host": key[2],
                "alert_count": len(group),
                "correlated": True
            })

    return correlated_incidents