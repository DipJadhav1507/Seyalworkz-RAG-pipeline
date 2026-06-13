import pandas as pd
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

df = pd.read_csv("data.csv")

documents = []

for _, row in df.iterrows():
    content = f"""
    Party Name: {row['Party Name']}
    Transaction Date: {row['Date']}
    Due Date: {row['Due Date']}
    Total Amount: ₹{row['Total Amount']}
    Status: {row['Status']}
    """
    
    documents.append(Document(page_content=content))

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.from_documents(
    documents,
    embedding_model
)

vectorstore.save_local("transaction_db")

print("Vector DB Created")