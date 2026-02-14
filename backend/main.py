from fastapi import FastAPI, UploadFile, File
import shutil
import os

from backend.services.pdf_service import extract_pdf_text
from backend.services.ocr_service import extract_text_from_image
from backend.services.video_service import extract_audio, transcribe_audio
from backend.services.embeddings import get_embedding
from backend.vectorstore.faiss_store import add_to_index
from backend.services.retriever import retrieve
from openai import OpenAI
from backend.config import OPENAI_API_KEY

app = FastAPI()
client = OpenAI(api_key=OPENAI_API_KEY)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = ""

    if file.filename.endswith(".pdf"):
        text = extract_pdf_text(file_path)

    elif file.filename.endswith((".png", ".jpg", ".jpeg")):
        text = extract_text_from_image(file_path)

    elif file.filename.endswith((".mp4", ".mov")):
        audio_path = extract_audio(file_path)
        text = transcribe_audio(audio_path)

    else:
        return {"error": "Unsupported file type"}

    embedding = get_embedding(text)
    add_to_index(embedding, text)

    return {"message": "File processed successfully"}

@app.post("/query")
async def query(data: dict):

    question = data.get("question")

    if not question:
        return {"answer": "No question provided"}

    contexts = retrieve(question)

    if not contexts:
        return {"answer": "No documents found. Please upload a file first."}

    prompt = f"""
    Answer based only on the context below.

    Context:
    {contexts}

    Question: {question}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"answer": response.choices[0].message.content}

