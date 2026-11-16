import faiss
import numpy as np
import pickle
from pathlib import Path

class VectorStore():
    def __init__(self):
        self.index = faiss.IndexFlatL2(384)
        self.chunks = []
        self.dimension = 384
    def add(self,embeddings,chunks):
        embeddings = np.asarray(embeddings, dtype=np.float32)
        self.index.add(embeddings)
        self.chunks.extend(chunks)
    def save(self,index_path,chunks_path):
        Path(index_path).parent.mkdir(parents=True,exist_ok=True)
        Path(chunks_path).parent.mkdir(parents=True,exist_ok=True)
        faiss.write_index(self.index,index_path)
        with open(chunks_path,'wb') as f:
            pickle.dump(self.chunks,f)
    def load(self,index_path,chunks_path):
        self.index = faiss.read_index(index_path)
        with open(chunks_path,'rb') as f:
           self.chunks = pickle.load(f)
    def search(self,query_embedding,top_k=3):
        query_embedding = np.asarray(query_embedding,dtype=np.float32)
        distances, indices = self.index.search(query_embedding.reshape(1,-1),top_k)
        results = [self.chunks[i] for i in indices[0] if i != -1]
        return results

