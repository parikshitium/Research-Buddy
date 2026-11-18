from backend.embeddings.embedder import Embedder
from backend.generation.generator import Generator
from backend.retrieval.retriever import Retriever
from backend.retrieval.vector_store import VectorStore
from backend.pipeline import DocumentPipeline
from backend.rag_pipeline import RAGPipeline
from backend.api.routes import configure_routes
from fastapi import FastAPI
from pathlib import Path

embedder = Embedder()
vector_store = VectorStore()
index_path = Path('data/vector_store/index.faiss')
chunks_path = Path('data/vector_store/chunks.pkl')
if index_path.exists() and chunks_path.exists():
    vector_store.load(index_path, chunks_path)


generator = Generator()
doc_pipe = DocumentPipeline(embedder,
                            vector_store,
                            index_path,
                            chunks_path)
retriever = Retriever(embedder,
                      vector_store)
rag_pipe = RAGPipeline(retriever,
                       generator)

app = FastAPI()
app.include_router(configure_routes(doc_pipe,rag_pipe))

