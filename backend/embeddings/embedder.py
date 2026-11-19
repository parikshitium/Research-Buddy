import torch
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self,
                 model_name='all-MiniLM-L6-v2'):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = SentenceTransformer(model_name,
                                         device=self.device)
    def embed(self,texts):
        return self.model.encode(texts,
                          convert_to_numpy=True)

