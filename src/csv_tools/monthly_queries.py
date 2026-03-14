import pandas as pd

monthly_df = pd.read_csv(
    "data/construction_monthly_metrics_numeric.csv"
)


def get_risk_index(topic, month):

    result = monthly_df[
        (monthly_df["topic_name"].str.contains(topic, case=False)) &
        (monthly_df["period_month"] == month)
    ]

    if result.empty:
        return "No data found"

    value = result.iloc[0]["risk_index"]

    return f"Risk index for {topic} in {month} is {value}"


def total_inspections(month):

    result = monthly_df[
        monthly_df["period_month"] == month
    ]

    total = result["inspections_completed"].sum()

    return f"Total inspections completed in {month}: {total}"