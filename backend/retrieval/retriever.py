class Retriever():
    def __init__(self,embedder,vector_store):
        self.embed = embedder
        self.vector = vector_store
    def retrieve(self,query,top_k=3):
        embedding = self.embed.embed([query])[0]
        return self.vector.search(embedding,top_k)