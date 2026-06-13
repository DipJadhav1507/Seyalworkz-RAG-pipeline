import os
from dotenv import load_dotenv
from groq import Groq

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_report(user_id,query):

    db = FAISS.load_local(
        f"db/{user_id}",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(
        search_kwargs={"k":20}
    )

    docs = retriever.invoke(query)

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a Financial Intelligence Assistant.

User Query:
{query}

Financial Data:
{context}

Generate:

1. Executive Summary
2. Revenue Opportunities
3. Profit Improvement Suggestions
4. Risk Analysis
5. Action Items
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content