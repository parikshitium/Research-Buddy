
class RAGPipeline():
    def __init__(self,retriever,generator):
        self.retriever = retriever
        self.generator = generator
    def answer(self,query,top_k=3):
        chunks = self.retriever.retrieve(query,top_k)
        if not chunks:
            return 'No relevant information found in the uploaded documents.'
        context = '\n\n'.join(
            f"[S{index+1}] Source: {i['source']},"
            f"Page: {i.get('page')},Paragraph: {i.get('paragraph')}\n"
            f"Content: {i['text']}"  
            for index, i in enumerate(chunks)
        )
        sources = [{
            'id': f'S{index+1}',
            'source': i['source'],
            'page': i.get('page'),
            'paragraph': i.get('paragraph')
        }
        for index, i in enumerate(chunks)]
        prompt = f'''You are a research assistant.
                    Answer the question using only the supplied context.
                    Do not invent facts.
                    If the context doesn't contain enough information, say so.
                    Include source references in your answer.
                    Make your claims using the source IDs provided, like [S1] or [S2]

                    CONTEXT:
                    {context}

                    QUESTION:
                    {query}'''
        answer = self.generator.generate(prompt)
        response = {'response': answer, 'source': sources}
        return response