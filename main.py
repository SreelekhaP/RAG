import os
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Corrected absolute package tracks resolving the workspace directory layout
from app.OCR.text_extractor import TextExtractor
from app.vector_store.rag_service import RagService
from app.models.schemas import QueryRequest, QueryResponse, DocumentResponse, IndexStatus

load_dotenv()

app = FastAPI(title="Intelligent Document Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root level document folder configuration
DOCUMENTS_DIR = Path("documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)

extractor = TextExtractor()
rag_service = RagService()
rag_service.load_index()

@app.get("/")
def home():
    return {
        "status": "online",
        "system": "Intelligent Document Analyzer Engine",
        "interactive_docs": "/docs"
    }

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a PDF.")

    file_path = DOCUMENTS_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extractor.extract_text_from_pdf(str(file_path))
    if not text.strip():
        raise HTTPException(status_code=400, detail="Extraction Engine failed to extract readable strings.")

    chunks_indexed = rag_service.create_index_from_texts([(file.filename, text)])
    
    return DocumentResponse(
        filename=file.filename,
        status="indexed",
        text_length=len(text),
        chunks_indexed=chunks_indexed
    )

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    results = rag_service.search(request.query, request.top_k)
    return QueryResponse(
        query=request.query,
        count=len(results),
        results=results
    )

@app.get("/status", response_model=IndexStatus)
def status():
    return IndexStatus(
        index_exists=os.path.exists("faiss_index"),
        vectorstore_loaded=rag_service.vectorstore is not None
    )