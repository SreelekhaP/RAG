# Intelligent Document Analyzer Engine 🚀

A high-performance, private, and localized **Retrieval-Augmented Generation (RAG)** pipeline built to extract, index, and query unstructured text data from multi-modal documents. It natively handles selectable digital PDFs, scanned documents, and flat images (`.png`, `.jpg`, `.jpeg`) entirely offline on your local machine with zero cloud API dependencies.

---

## 🛠️ The Tech Stack

| Technology Component | Domain Layer | Key Role |
| :--- | :--- | :--- |
| **Python 3.13** | Core Engine | Base programming language environment. |
| **FastAPI** | Web Framework | Powers the asynchronous API endpoints and auto-generates Swagger UI. |
| **Uvicorn** | ASGI Web Server | Manages high-speed background server loops and hot-reloading. |
| **PyMuPDF (`fitz`)** | Document Parsing | Blazing fast textual extraction from native digital PDFs. |
| **Tesseract OCR** | Computer Vision | Transcribes text from raw pixel matrices (scans and photos). |
| **LangChain** | AI Processing | Dynamically chops text into context-aware paragraph chunks. |
| **HuggingFace** | Deep Learning | Translates plain text into dense 384-dimensional semantic vectors. |
| **FAISS (Meta AI)** | Vector Database | Stores vector matrices locally and runs lightning-fast similarity lookups. |
| **Pydantic** | Data Validation | Enforces strict API request and response data-blueprints. |

---

## 🔄 System Architecture & Flow

The system decouples web-routing interfaces from computational machine learning layers, executing operations across two clean pipelines:

1. **The Ingestion Pipeline:**
   * **Payload Intake:** Files are sent via HTTP POST to the `/upload` route.
   * **Hybrid Text Extraction:** PyMuPDF parses digital layers. If empty, the engine converts pages into images and triggers Tesseract OCR fallback loops.
   * **Contextual Chunking:** LangChain segments text into 1,000-character pieces with a 200-character overlap to retain contextual continuity.
   * **Vectorization & Indexing:** HuggingFace `all-MiniLM-L6-v2` encodes strings into numeric coordinates, and FAISS serializes them directly to local storage inside the `faiss_index/` directory.

2. **The Retrieval Pipeline:**
   * A search string is submitted to the `/query` endpoint.
   * The query string is translated into an embedding vector.
   * FAISS calculates a high-speed mathematical matrix similarity comparison (Euclidean/L2 distance) and instantly returns the top matching document snippets.

---

## 📁 Project Directory Structure

```text
RAG/
├── app/
│   ├── OCR/
│   │   ├── __init__.py
│   │   └── text_extractor.py    # Dual digital/OCR parsing logic
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic input/output schemas
│   ├── vector_store/
│   │   ├── __init__.py
│   │   └── rag_service.py       # Text splitting and local FAISS logic
│   └── main.py                  # Core FastAPI gateway routes
├── documents/                   # Upload landing storage directory
├── faiss_index/                 # Local binary database index files
├── .env                         # Windows environment binary path maps
└── requirements.txt             # Pinned project dependencies manifest
