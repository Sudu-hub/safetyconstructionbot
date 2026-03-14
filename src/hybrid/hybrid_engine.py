from csv_tools.baseline_queries import get_inherent_risk


def hybrid_answer(question, vectorstore, rag_function):

    q = question.lower()

    # Get CSV data
    risk = None
    if "confined space" in q:
        risk = get_inherent_risk("Confined Space")

    # Get TXT answer
    rag_answer = rag_function(vectorstore, question)

    final = f"""
Risk Score:
{risk}

Additional Context:
{rag_answer}
"""

    return final