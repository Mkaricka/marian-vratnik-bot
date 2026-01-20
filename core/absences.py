from datetime import datetime
from storage.json_store import load_json, save_json


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =========================
# KONTROLA AKTÍVNEJ ABSENCIE
# =========================
def has_active_absence(user_id: str) -> bool:
    absences = load_json("absences.json", {})
    return (
        user_id in absences
        and absences[user_id].get("end") is None
    )


# =========================
# SPUSTENIE ABSENCIE
# =========================
def start_absence(
    user_id: str,
    absence_type: str,
    date_from: str,
    date_to: str | None
):
    absences = load_json("absences.json", {})

    absences[user_id] = {
        "type": absence_type,          # PN | DOVOLENKA
        "from": date_from,             # plánovaný začiatok
        "to": date_to,                 # plánovaný koniec (alebo None)
        "created": now(),              # kedy bola nahlásená
        "end": None                    # reálny koniec (vyplní !koniec*)
    }

    save_json("absences.json", absences)


# =========================
# UKONČENIE ABSENCIE
# =========================
def end_absence(user_id: str):
    """
    Ukončí aktívnu absenciu a vráti jej dáta.
    Ak absencia neexistuje alebo je už ukončená → None
    """
    absences = load_json("absences.json", {})

    if user_id not in absences:
        return None

    if absences[user_id].get("end") is not None:
        return None

    absences[user_id]["end"] = now()
    save_json("absences.json", absences)

    return absences[user_id]


# =========================
# ZÍSKANIE AKTÍVNEJ ABSENCIE
# =========================
def get_active_absence(user_id: str):
    """
    Vráti aktívnu absenciu používateľa (dict) alebo None
    """
    absences = load_json("absences.json", {})

    if user_id in absences and absences[user_id].get("end") is None:
        return absences[user_id]

    return None

def get_active_absence(user_id: str):
    absences = load_json("absences.json", {})
    if user_id in absences and absences[user_id]["end"] is None:
        return absences[user_id]
    return None
