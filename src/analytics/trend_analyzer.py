import pandas as pd

DATA_FILE = "data/construction_monthly_metrics_numeric.csv"


def load_data():
    return pd.read_csv(DATA_FILE)


# -----------------------------------------
# Detect increasing risk trends
# -----------------------------------------
def increasing_risk_topics():

    df = load_data()

    grouped = df.groupby("topic_name")

    worsening_topics = []

    for topic, data in grouped:

        data = data.sort_values("month_index")

        risks = data["risk_index"].tolist()

        if len(risks) < 2:
            continue

        if risks[-1] > risks[0]:
            worsening_topics.append(topic)

    if not worsening_topics:
        return "No safety topics show increasing risk."

    return "Safety topics with increasing risk: " + ", ".join(worsening_topics)


# -----------------------------------------
# Detect improving safety topics
# -----------------------------------------
def improving_topics():

    df = load_data()

    grouped = df.groupby("topic_name")

    improving = []

    for topic, data in grouped:

        data = data.sort_values("month_index")

        risks = data["risk_index"].tolist()

        if len(risks) < 2:
            continue

        if risks[-1] < risks[0]:
            improving.append(topic)

    if not improving:
        return "No safety topics show improvement."

    return "Improving safety topics: " + ", ".join(improving)