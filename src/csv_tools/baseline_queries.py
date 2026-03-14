import pandas as pd

baseline_df = pd.read_csv(
    "data/construction_topic_baselines_numeric.csv"
)


def get_inherent_risk(topic):

    result = baseline_df[
        baseline_df["topic_name"].str.contains(topic, case=False)
    ]

    if result.empty:
        return "Topic not found"

    score = result.iloc[0]["inherent_risk_score"]

    return f"Inherent risk score for {topic} is {score}"


def get_severity_score(topic):

    result = baseline_df[
        baseline_df["topic_name"].str.contains(topic, case=False)
    ]

    if result.empty:
        return "Topic not found"

    score = result.iloc[0]["severity_potential_score"]

    return f"Severity potential score for {topic} is {score}"