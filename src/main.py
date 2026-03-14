from rag.txt_loader import load_txt_documents
from rag.chunker import chunk_documents
from rag.vector_store import build_vector_store, load_vector_store

from csv_tools.baseline_queries import get_inherent_risk
from csv_tools.monthly_queries import get_risk_index, total_inspections

from router.intent_router import detect_intent
from hybrid.hybrid_engine import hybrid_answer

from analytics.risk_analyzer import highest_risk_topic, topics_needing_attention
from analytics.trend_analyzer import increasing_risk_topics, improving_topics
from analytics.insight_generator import generate_safety_insight

from openai import AzureOpenAI
from config import (
    AZURE_OPENAI_KEY,
    AZURE_ENDPOINT,
    AZURE_API_VERSION,
    AZURE_CHAT_DEPLOYMENT
)

import os
import re


DATA_PATH = "data"
INDEX_PATH = "index_cache/faiss_index"


client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    azure_endpoint=AZURE_ENDPOINT,
    api_version=AZURE_API_VERSION
)


def build_index():

    print("Loading documents...")

    docs = load_txt_documents(DATA_PATH)

    print("Chunking documents...")

    texts, metadatas = chunk_documents(docs)

    print("Building vector store...")

    vectorstore = build_vector_store(texts, metadatas)

    print("Vector store created.")

    return vectorstore



def ask_rag_question(vectorstore, question):

    print("\nSearching relevant documents...\n")

    results = vectorstore.similarity_search(question, k=3)

    if not results:
        context = "No relevant context found."
    else:
        context = "\n\n".join([r.page_content for r in results])

    messages = [
        {
            "role": "system",
            "content": "You are a helpful construction safety assistant."
        },
        {
            "role": "user",
            "content": f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer clearly and cite sources if available.
"""
        }
    ]

    response = client.chat.completions.create(
        model=AZURE_CHAT_DEPLOYMENT,
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content



def handle_csv_query(question):

    q = question.lower()

    if "inherent risk" in q:

        topic = q.split("for")[-1].strip().title()

        result = get_inherent_risk(topic)

        return f"Inherent risk score for {topic} is {result}"

    elif "risk index" in q:

        topic = q.split("for")[-1].split("in")[0].strip().title()
        month = q.split("in")[-1].strip()

        result = get_risk_index(topic, month)

        return f"Risk index for {topic} in {month} is {result}"

    elif "inspections" in q:

        month = q.split("in")[-1].strip()

        result = total_inspections(month)

        return f"Total inspections in {month} = {result}"

    else:

        return "CSV query not recognized."


def handle_analytics_query(question):

    q = question.lower()

    # extract month safely
    month_match = re.search(r"\d{4}-\d{2}", question)
    month = month_match.group() if month_match else None

    if "highest risk" in q or "top risk" in q:

        result = highest_risk_topic(month)
        return result

    elif "attention" in q:

        result = topics_needing_attention(month)
        return result

    elif "increasing risk" in q or "getting worse" in q:

        return increasing_risk_topics()

    elif "improving" in q or "getting better" in q:

        return improving_topics()

    else:

        return "Analytics query not recognized."


if __name__ == "__main__":

    if not os.path.exists(INDEX_PATH):

        print("No index found. Building new vector index...\n")

        vs = build_index()

    else:

        print("Loading existing index...\n")

        vs = load_vector_store()

    while True:

        query = input("\nAsk a question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        intent = detect_intent(query)

        print("\nDetected intent:", intent)



        if intent == "ANALYTICS":

            analytics_result = handle_analytics_query(query)

            insight = generate_safety_insight(query, analytics_result)

            print("\nAI Safety Insight:\n")
            print(insight)



        elif intent == "CSV":

            answer = handle_csv_query(query)

            print("\nAnswer:\n", answer)


        elif intent == "TXT":

            answer = ask_rag_question(vs, query)

            print("\nAnswer:\n", answer)


        elif intent == "HYBRID":

            answer = hybrid_answer(query, vs, ask_rag_question)

            print("\nHybrid Answer:\n", answer)