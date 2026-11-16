from backend.ingestion.doc_load import load_doc
from backend.ingestion.chunker import chunk
from pathlib import Path

class DocumentPipeline():
    def __init__(self,embedder,vector_store):
        self.embedder = embedder
        self.vector_store = vector_store
    def process_document(self,path):
        document = load_doc(path)
        chunks = chunk(document)
        if not chunks:
            raise ValueError('No text could be extracted from the document')
        for c in chunks:
            c['source'] = Path(path).name 
        data = [c['text'] for c in chunks]
        embeddings = self.embedder.embed(data)
        self.vector_store.add(embeddings,chunks)
        return chunks