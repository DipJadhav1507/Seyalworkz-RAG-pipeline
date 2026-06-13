import pandas as pd

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_vector_store(csv_path,user_id):

    df = pd.read_csv(csv_path)

    documents = []

    for _, row in df.iterrows():

        content = "\n".join(
            [f"{col}: {row[col]}" for col in df.columns]
        )

        documents.append(
            Document(page_content=content)
        )

    db = FAISS.from_documents(
        documents,
        embedding_model
    )

    db.save_local(f"db/{user_id}")

    return True