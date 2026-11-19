
class RAGPipeline:
    def __init__(self,retriever,generator):
        self.retriever = retriever
        self.generator = generator
    def answer(self,query,top_k=3):
        chunks = self.retriever.retrieve(query,top_k)
        if not chunks:
            return {
                'response':'No relevant information found in the uploaded documents.',
                'source':[]
            }
        context = '\n\n'.join(
            f"[S{index+1}] Source: {item['source']}, "
            f"Page: {item.get('page')}, "
            f"Paragraph: {item.get('paragraph')}\n"
            f"Content: {item['text']}"  
            for index, item in enumerate(chunks)
        )
        sources = [{
            'id': f'S{index+1}',
            'source': item['source'],
            'page': item.get('page'),
            'paragraph': item.get('paragraph')
        }
        for index, item in enumerate(chunks)]
        prompt = f'''You are a research assistant.
                    Answer the question using only the supplied context.
                    Do not invent facts.
                    If the context doesn't contain enough information, say so.
                    Cite factual claims using the supplied source IDs like [S1] or [S2].
                    Do not cite sources that do not support the claim.

                    CONTEXT:
                    {context}

                    QUESTION:
                    {query}'''
        answer = self.generator.generate(prompt)
        response = {'response': answer, 'source': sources}
        return response