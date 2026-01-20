from storage.json_store import load_json
from datetime import datetime


def days_between(a, b):
    da = datetime.fromisoformat(a)
    db = datetime.fromisoformat(b)
    return (db - da).days + 1


def get_absence_stats(user_id: str):
    absences = load_json("absences.json", {})
    if user_id not in absences:
        return {"pn_days": 0, "vacation_days": 0}

    a = absences[user_id]
    if not a["end"]:
        return {"pn_days": 0, "vacation_days": 0}

    days = days_between(a["from"], a["to"] or a["end"])

    if a["type"] == "PN":
        return {"pn_days": days, "vacation_days": 0}
    else:
        return {"pn_days": 0, "vacation_days": days}
