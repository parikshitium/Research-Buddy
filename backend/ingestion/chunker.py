def chunk(documents,
          chunk_size=200,
          overlap=50):
    chunks = []
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError('Chunk size must be greater than 0,' \
        'Overlap must not be negative,' \
        'Overlap size must not be greater than chunk size')
    for document in documents:
        words = document['text'].split()
        for start in range(0,len(words),chunk_size - overlap):
            chunk_words = words[start:start+chunk_size]
            if start > 0 and len(chunk_words) <= overlap:
                break
            chunks.append({
                'text': ' '.join(chunk_words),
                'page': document.get('page'),
                'paragraph': document.get('paragraph')
            })
    return chunks