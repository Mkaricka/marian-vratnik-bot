from storage.json_store import load_json
from datetime import datetime, date


def parse(dt: str):
    return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")


def calculate_user_stats(user_id: str, mode: str = "all"):
    """
    mode:
    - all    -> všetky dáta
    - today  -> iba dnešok
    - month  -> aktuálny mesiac
    """

    sessions = load_json("sessions.json", {})
    data = sessions.get(user_id, [])

    total_seconds = 0
    shifts = 0
    breaks_count = 0

    today = date.today()

    for s in data:
        # neuzavretá smena sa nepočíta
        if not s.get("end"):
            continue

        try:
            start = parse(s["start"])
            end = parse(s["end"])
        except Exception:
            continue

        # FILTER PODĽA REŽIMU
        if mode == "today" and start.date() != today:
            continue

        if mode == "month":
            if start.year != today.year or start.month != today.month:
                continue

        duration = (end - start).total_seconds()

        # PRESTÁVKY
        break_time = 0
        for b in s.get("breaks", []):
            if b.get("start") and b.get("end"):
                try:
                    bs = parse(b["start"])
                    be = parse(b["end"])
                    bt = (be - bs).total_seconds()
                    if bt > 0:
                        break_time += bt
                        breaks_count += 1
                except Exception:
                    continue

        work_time = max(0, duration - break_time)
        total_seconds += work_time
        shifts += 1

    hours = round(total_seconds / 3600, 2)
    avg_shift = round(hours / shifts, 2) if shifts else 0

    return {
        "hours": hours,
        "shifts": shifts,
        "breaks": breaks_count,
        "avg_shift": avg_shift
    }
