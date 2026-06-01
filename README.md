# RAG
An AI-powered local search engine that securely indexes and queries text from PDFs and images offline. Using FastAPI, it extracts layout data via PyMuPDF or Tesseract OCR for scans. LangChain splits text into paragraphs, and HuggingFace embeds them into geometric vectors stored in a FAISS database for sub-second semantic retrieval.
