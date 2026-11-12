import pymupdf
from .chunker import chunk
from pathlib import Path

def load_doc(data):
    extension = Path(data).suffix.lower()
    try:
        if extension == '.txt':
            text = data
        elif extension == '.pdf':
            with pymupdf.open(data) as doc:
                text = []
                for page_num,page in enumerate(doc, start=1):
                    content = page.get_text()
                    text.append({
                        'page': page_num,
                        'text': content
                    })
                return text
        else:
            raise ValueError('Not a txt or pdf file')
        with open(text,'r',encoding='utf-8') as f:
            content = f.read()
            content = content.split('\n\n')
            words = []
            for page_num, para in enumerate(content,start=1):
                if not para:
                    continue
                words.append({
                    'paragraph': page_num,
                    'text': para.strip()
                })
            return words
    except FileNotFoundError:
        raise FileNotFoundError(f'{data} does not exist')
if __name__ == '__main__':
    text = '../../'+input('Your file: ').strip()
    docs = load_doc(text)
    result = chunk(docs)
    print(result)