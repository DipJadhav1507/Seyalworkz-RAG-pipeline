import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form


from models import QueryRequest
from vector_store import create_vector_store
from RAG import generate_report

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    user_id: str = Form(...),
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