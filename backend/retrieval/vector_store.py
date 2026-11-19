import faiss
import numpy as np
import pickle
from pathlib import Path

class VectorStore:
    def __init__(self):
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks = []
    def add(self,embeddings,chunks):
        embeddings = np.asarray(embeddings, dtype=np.float32)
        if len(embeddings) != len(chunks):
            raise ValueError('Number of embeddings must be equal to the number of chunks')
        if embeddings.ndim != 2 or embeddings.shape[1] != self.dimension:
            raise ValueError('Embedding dimension does not match the dimension of the stored vectors')
        self.index.add(embeddings)
        self.chunks.extend(chunks)
    def save(self,index_path,chunks_path):
        Path(index_path).parent.mkdir(parents=True,exist_ok=True)
        Path(chunks_path).parent.mkdir(parents=True,exist_ok=True)
        faiss.write_index(self.index,str(index_path))
        with open(chunks_path,'wb') as f:
            pickle.dump(self.chunks,f)
    def load(self,index_path,chunks_path):
        self.index = faiss.read_index(str(index_path))
        with open(chunks_path,'rb') as f:
           self.chunks = pickle.load(f)
        if self.index.ntotal != len(self.chunks):
            raise ValueError('Stored index and chunks are inconsistent')
    def search(self,query_embedding,top_k=3):
        query_embedding = np.asarray(query_embedding,dtype=np.float32)
        if query_embedding.ndim != 1 or query_embedding.size != self.dimension:
            raise ValueError('Query embedding has an incorrect dimension')
        if top_k <= 0:
            raise ValueError('top_k must be greater than 0')
        _, indices = self.index.search(query_embedding.reshape(1,-1),top_k)
        results = [self.chunks[i] for i in indices[0] if i != -1]
        return results

