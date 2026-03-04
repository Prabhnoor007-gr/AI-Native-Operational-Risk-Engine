import json
import ollama


def classify_alert(alert):

    prompt = f"""
You are an AI operational risk engine for a financial trading platform.

Analyze the alert and determine:

1. Severity: P1, P2, P3, or P4
2. Regulatory risk: true or false
3. Requires human review: true or false
4. Confidence score between 0 and 1
5. Short impact summary

Alert:
{json.dumps(alert, indent=2)}

Rules:
- Production (prod) issues are more severe.
- failure_rate > 30 or latency > 3000ms in prod may be P1.
- Trading_Engine in prod may have regulatory implications.
- Non-prod issues are lower severity.
- P1 or regulatory risk must require human review.

Respond ONLY in valid JSON format like:
{{
  "severity": "P2",
  "regulatory_risk": false,
  "requires_human_review": false,
  "confidence": 0.87,
  "impact_summary": "Short explanation"
}}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
    )

    content = response["message"]["content"]

    # Extract JSON safely
    try:
        start = content.find("{")
        end = content.rfind("}") + 1
        json_str = content[start:end]
        return json.loads(json_str)
    except:
        return {
            "severity": "P3",
            "regulatory_risk": False,
            "requires_human_review": True,
            "confidence": 0.5,
            "impact_summary": "Fallback due to parsing error"
        }