import unittest
from backend.embeddings.embedder import Embedder
from backend.retrieval.vector_store import VectorStore
from backend.pipeline import DocumentPipeline
from backend.retrieval.retriever import Retriever


class TestDocumentPipeline(unittest.TestCase):
    def setUp(self):
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.pipeline = DocumentPipeline(embedder=self.embedder,
                                         vector_store=self.vector_store)
        self.retriever = Retriever(self.embedder,
                                    self.vector_store)
    def test_processing_txt(self):
        path = 'data/samples/sample.txt'
        chunks = self.pipeline.process_document(path)
        self.assertGreater(len(chunks),0)
        self.assertTrue(all(c['source'] == 'sample.txt' for c in chunks))
        self.assertGreater(self.vector_store.index.ntotal,0)
    def test_processing_pdf(self):
        path = 'data/samples/sample.pdf'
        chunks = self.pipeline.process_document(path)
        self.assertGreater(len(chunks),0)
        self.assertTrue(all(c['source'] == 'sample.pdf' for c in chunks))
        self.assertTrue(all(c['page'] is not None and c['page'] > 0 for c in chunks))
    def test_more_docs(self):
        txt = self.pipeline.process_document('data/samples/sample.txt')
        pdf = self.pipeline.process_document('data/samples/sample.pdf')
        results = self.retriever.retrieve(query='Explain artificial intelligence, text embeddings and retrieval augmented generation',
                                top_k=self.vector_store.index.ntotal)
        self.assertEqual(len(results),len(txt)+len(pdf))
        sources = {c['source'] for c in results}
        self.assertEqual(sources,{'sample.txt','sample.pdf'})