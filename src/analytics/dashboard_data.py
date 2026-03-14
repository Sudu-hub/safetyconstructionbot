import pandas as pd

DATA_FILE = "data/construction_monthly_metrics_numeric.csv"

def load_data():
    return pd.read_csv(DATA_FILE)

def risk_trend(topic):

    df = load_data()

    topic_df = df[df["topic_name"] == topic]

    return topic_df[["period_month", "risk_index"]]