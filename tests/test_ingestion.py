import unittest
from pathlib import Path
import tempfile
from backend.ingestion.doc_load import load_doc
from backend.ingestion.chunker import chunk
import pymupdf



class TestIngestion(unittest.TestCase):
    def test_ingestion(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir)/'sample.txt'
            file_path.write_text(
                'First paragraph.\n\nSecond paragraph.',
                encoding='utf-8'
            )
            result = load_doc(str(file_path))
            self.assertEqual(len(result),2)
            self.assertEqual(result[0]['text'],'First paragraph.')
            self.assertEqual(result[0]['paragraph'],1)
            self.assertEqual(result[1]['paragraph'],2)
    def test_error(self):
        with self.assertRaises(ValueError):
            load_doc('sample.docx')
        with self.assertRaises(FileNotFoundError):
            load_doc('samples.txt')

    def test_chunker(self):
        doc = [{
            'text': 'one two three four five six seven eight nine ten',
            'paragraph': 1
        }]
        result = chunk(doc,
                       chunk_size=6,
                       overlap=2)
        self.assertEqual(len(result),2)
        first = result[0]['text'].split()
        second = result[1]['text'].split()
        self.assertEqual(first[:2],['one','two'])
        self.assertEqual(first[-2:],second[:2])
        self.assertEqual(len(first),6)
        self.assertEqual(len(second),6)
    def test_chunk_error(self):
        doc = [{
            'text':'one two three four five six seven eight nine ten',
            'paragraph':1
        }]
        with self.assertRaises(ValueError):
            chunk(doc,
                  chunk_size=0,
                  overlap=0)
        with self.assertRaises(ValueError):
            chunk(doc,
                  chunk_size=6,
                  overlap=6)
    def test_pdf(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir)/'sample.pdf'
            pdf = pymupdf.open()
            page = pdf.new_page()
            page.insert_text((50,50),'Testing PDF extraction')
            pdf.save(file_path)
            pdf.close()
            result = load_doc(str(file_path))

            self.assertEqual(len(result),1)
            self.assertEqual(result[0]['page'],1)
            self.assertIn('Testing PDF extraction',result[0]['text'])

if __name__ == '__main__':
    unittest.main()