from backend.ingestion.doc_load import load_doc
from backend.ingestion.chunker import chunk
from pathlib import Path

class DocumentPipeline():
    def __init__(self,embedder,vector_store,index_path,chunks_path):
        self.embedder = embedder
        self.vector_store = vector_store
        self.index_path = index_path
        self.chunks_path = chunks_path
    def process_document(self,path,source_name=None):
        document = load_doc(path)
        chunks = chunk(document)
        if not chunks:
            raise ValueError('No text could be extracted from the document')
        for c in chunks:
            c['source'] = source_name or Path(path).name
        data = [c['text'] for c in chunks]
        embeddings = self.embedder.embed(data)
        self.vector_store.add(embeddings,chunks)
        self.vector_store.save(self.index_path,self.chunks_path)
        return chunks