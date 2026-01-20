def calculate_performance(stats):
    score = 0

    if stats["hours"] >= 160:
        score += 40
    elif stats["hours"] >= 120:
        score += 25

    if stats["avg_shift"] >= 7:
        score += 20

    if stats["breaks"] < 20:
        score += 20

    score = min(score, 100)

    return score
