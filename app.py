import os

from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from models import QueryRequest
from vector_store import create_vector_store
from rag import generate_report

app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR,exist_ok=True)
os.makedirs("db",exist_ok=True)

@app.get("/")
def home():

    return {
        "status":"running"
    }

@app.post("/upload")

async def upload_csv(
    user_id:str,
    file:UploadFile = File(...)
):

    filepath = f"{UPLOAD_DIR}/{user_id}.csv"

    with open(filepath,"wb") as f:
        f.write(await file.read())

    create_vector_store(
        filepath,
        user_id
    )

    return {
        "message":"Vector DB Created"
    }

@app.post("/analyze")

def analyze(request:QueryRequest):

    report = generate_report(
        request.user_id,
        request.query
    )

    return {
        "report":report
    }