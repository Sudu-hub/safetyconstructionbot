def detect_intent(question):

    q = question.lower()

    analytics_keywords = [
        "highest risk",
        "most dangerous",
        "needs attention",
        "top risk"
    ]

    csv_keywords = [
        "risk score",
        "risk index",
        "inspections"
    ]

    txt_keywords = [
        "owner",
        "who",
        "governance"
    ]

    if any(word in q for word in analytics_keywords):
        return "ANALYTICS"

    if any(word in q for word in csv_keywords):
        return "CSV"

    if any(word in q for word in txt_keywords):
        return "TXT"

    return "TXT"