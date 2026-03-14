import pandas as pd

DATA_FILE = "data/construction_monthly_metrics_numeric.csv"


def load_data():
    df = pd.read_csv(DATA_FILE)
    return df


# -----------------------------------------
# Highest Risk Topic
# -----------------------------------------
def highest_risk_topic(month):

    df = load_data()

    # filter month
    month_df = df[df["period_month"] == month]

    if month_df.empty:
        return f"No data available for {month}"

    # find max risk
    row = month_df.loc[month_df["risk_index"].idxmax()]

    topic = row["topic_name"]
    risk = row["risk_index"]

    return f"Highest risk topic in {month} is '{topic}' with risk index {risk}"


# -----------------------------------------
# Topics needing attention
# -----------------------------------------
def topics_needing_attention(month):

    df = load_data()

    month_df = df[df["period_month"] == month]

    if month_df.empty:
        return f"No data available for {month}"

    # threshold risk
    risky = month_df[month_df["risk_index"] > 90]

    if risky.empty:
        return f"No high-risk topics found in {month}"

    topics = risky["topic_name"].tolist()

    return f"Topics needing attention in {month}: {', '.join(topics)}"