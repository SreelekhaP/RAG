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
intelligent_document_analyzer/
├── app/
│   ├── __init__.py            # Empty file to initialize the package
│   ├── main.py                 # FastAPI application & endpoints
│   ├── OCR/
│   │   ├── __init__.py        # Empty file
│   │   └── text_extractor.py   # PDF text layer & Tesseract OCR engine
│   ├── vector_store/
│   │   ├── __init__.py        # Empty file
│   │   └── rag_service.py      # LangChain text splitter & FAISS database
│   └── models/
│       ├── __init__.py        # Empty file
│       └── schemas.py          # Pydantic data validation models
├── documents/                  # Folder where your uploaded PDFs will save
├── faiss_index/                # Automatically generated when you upload a file
├── .env                        # Stores your local Windows Tesseract path
└── requirements.txt            # Package dependencies list
🔐 1. The Secret Key File (.env)
Your computer needs to know exactly where to look for certain applications installed on your hard drive. We keep this information inside a special, hidden text file named exactly .env (with a dot at the beginning and no file extensions at the end).

This file must sit out in the open in your main RAG folder, right next to your requirements.txt.

Copy and Paste .env Content:
Ini, TOML
# Tells our code exactly where to find Tesseract's eyes on your Windows profile
TESSERACT_CMD=C:\Users\sreel\AppData\Local\Programs\Tesseract-OCR\tesseract.exe

# Sets up the home address on your laptop where the dashboard web page will build
HOST=127.0.0.1
PORT=8000

# Names the specific open-source AI brain model we use to understand sentences
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
Why does this file matter?
TESSERACT_CMD: If this path is wrong, your project can't find its visual OCR engine. It will read digital PDFs perfectly, but the second you upload a raw smartphone photograph or a screenshot, it will lose its sight and throw an error.

HOST & PORT: This defines the exact offline digital neighborhood your web link uses. It is what allows you to type http://127.0.0.1:8000/docs into Chrome and see your beautiful dashboard.

📂 2. Meeting the Team: What Every File Does
Every folder and script inside your project has a distinct personality and a specific job to do. Here is a tour of your workspace:

The Outer Safeguards (Root Directory)
requirements.txt

In Simple Terms: The Grocery List.

Its Job: It lists all the third-party packages your computer needs to download (like FastAPI, PyMuPDF, and FAISS) so your Python code has the smart capabilities it needs to work.

.env

In Simple Terms: The Private Settings Card.

Its Job: It keeps machine-specific paths separate from your actual programming code, ensuring your setup matches your laptop perfectly.

The Brain Core (app/ Folder)
app/main.py

In Simple Terms: The Air Traffic Controller.

Its Job: This is the main gatekeeper of your app. It creates the actual webpage endpoints, welcomes you when you visit the home link, and routes your file uploads and text queries to the correct sub-folders behind the scenes.

The Security Check (app/models/ Folder)
app/models/__init__.py

In Simple Terms: The Package Label.

Its Job: This is an empty file. Its only purpose is to tap Python on the shoulder and say, "Hey, this folder is a certified code bundle! You are allowed to look inside."

app/models/schemas.py

In Simple Terms: The Form Screener.

Its Job: It double-checks data formats. For example, if you ask a question, it makes sure you typed real words for your question and a real number for how many answers you want back. If you make a typo, it intercepts the mistake before it breaks your core database.

The Eyes (app/OCR/ Folder)
app/OCR/text_extractor.py

In Simple Terms: The Smart Document Reader.

Its Job: When you upload a file, this script scans it. First, it uses PyMuPDF to quickly scrape text off digital PDFs. If it finds nothing (like in a flattened photo or screenshot), it calls Tesseract OCR to look at the pixels, decipher the shapes of letters, and transcribe them into text your code can read.

The AI Thinker (app/vector_store/ Folder)
app/vector_store/rag_service.py

In Simple Terms: The Library Cataloger.

Its Job: This is where the AI magic lives. It uses LangChain to chop long text into neat paragraphs, calls HuggingFace to turn those sentences into mathematical meaning vectors, and sets up FAISS to instantly search through thousands of paragraph blocks to pull out the precise answer to your question.

The Memory Banks (Automated Storage Folders)
documents/

In Simple Terms: The Processing Tray.

Its Job: A local landing folder where the files you upload are held so your extraction scripts can safely open and read them.

faiss_index/

In Simple Terms: The Permanent Memory Bank.

Its Job: This is where your FAISS database saves its work directly onto your hard drive. Because this folder saves binary data files, your project remembers all your documents even if you turn off your laptop, close VS Code, or restart your server!
