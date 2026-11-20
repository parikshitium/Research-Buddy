from backend.embeddings.embedder import Embedder
from backend.generation.generator import Generator
from backend.retrieval.retriever import Retriever
from backend.retrieval.vector_store import VectorStore
from backend.pipeline import DocumentPipeline
from backend.rag_pipeline import RAGPipeline
from backend.api.routes import configure_routes
from fastapi import FastAPI
from pathlib import Path
from uuid import UUID

embedder = Embedder()
generator = Generator()
sessions = {}

def get_session(session_id):
    try:
        session_id = str(UUID(session_id))
    except (ValueError,TypeError,AttributeError):
        raise ValueError('Invalid session ID')
    if session_id not in sessions:
        session_dir = Path('data/sessions')/session_id
        session_dir.mkdir(parents=True,exist_ok=True)
        vector_store = VectorStore()
        index_path = session_dir/'index.faiss'
        chunks_path = session_dir/'chunks.pkl'

        if index_path.exists() and chunks_path.exists():
            vector_store.load(index_path,chunks_path)
        doc_pipe = DocumentPipeline(
            embedder,
            vector_store,
            index_path,chunks_path
        )
        retriever = Retriever(embedder,vector_store)
        rag_pipe = RAGPipeline(retriever,generator)
        sessions[session_id] = (doc_pipe,rag_pipe)
    return sessions[session_id]
app = FastAPI()
app.include_router(configure_routes(get_session))