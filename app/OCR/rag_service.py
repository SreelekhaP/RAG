import os
from typing import List, Dict, Any, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class RagService:
    def __init__(self, index_path: str = "faiss_index"):
        self.index_path = index_path
        self.vectorstore = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        # Pulls a lightweight, locally executing embedding pipeline
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def _build_documents(self, items: List[Tuple[str, str]]) -> List[Document]:
        docs = []
        for filename, text in items:
            base_doc = Document(page_content=text, metadata={"filename": filename})
            chunks = self.text_splitter.split_documents([base_doc])
            docs.extend(chunks)
        return docs

    def create_index_from_texts(self, items: List[Tuple[str, str]]) -> int:
        documents = self._build_documents(items)
        if not documents:
            return 0
        self.vectorstore = FAISS.from_documents(documents, self.embeddings)
        self.vectorstore.save_local(self.index_path)
        return len(documents)

    def load_index(self) -> bool:
        if not os.path.exists(self.index_path):
            return False
        try:
            self.vectorstore = FAISS.load_local(
                self.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return True
        except Exception:
            return False

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if self.vectorstore is None:
            if not self.load_index():
                return []
                
        results = self.vectorstore.similarity_search_with_score(query, k=top_k)
        response = []
        for doc, score in results:
            response.append({
                "content": doc.page_content,
                "score": float(score),
                "metadata": doc.metadata
            })
        return response
