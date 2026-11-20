# Research Buddy

An AI-powered research assistant that lets the users upload PDF and TXT documents and ask questions about their contents.

It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents and generate context-aware answers with source citations.

## Features
- Upload PDF and TXT documents.
- Extract and chunk document text.
- Generate text embeddings using Sentence Transformers.
- Store and retrieve embeddings using FAISS.
- Ask natural language questions about the uploaded documents.
- Generate context-aware answers using Google's Gemini API.
- Display source citations with document names and page numbers.
- Maintain separate document stores for different sessions.
- Persist document indexes locally.

## Tech Stack
- **Language:** Python
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database:** FAISS
- **LLM:** Google Gemini API
- **Document Processing:** PyMuPDF

## How it works
1. Users upload PDF or TXT documents.
2. Text is extracted and divided into smaller chunks.
3. Each chunk is converted into an embedding using Sentence Transformers.
4. Embeddings and their corresponding text are stored in FAISS.
5. When a question is submitted, FAISS retrieves the most relevant chunks.
6. Retrieved context is passed to Gemini to generate an answer.
7. Answers include source citations to help users trace the information back to their documents.

## Installation and Setup

1. Clone the repository:
```bash
   git clone https://github.com/parikshitium/Research-Buddy.git
   cd Research-Buddy
   ```
2. Create a virtual environment:
```bash   
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install dependencies:
```bash   
   pip install -r requirements.txt
   ```

4. Create a .env file in the project root:
```env
   GEMINI_API_KEY=your_api_key
   API_URL=http://127.0.0.1:8000
   ```

5. Start the backend:
```bash
   python -m uvicorn backend.main:app --reload
   ```

6. Start the frontend in a separate terminal:
```bash
   streamlit run frontend/app.py
   ```

## Limitations
- Supports PDF and TXT files only.
- Scanned PDFs without extractable text are not supported.
- Answers depend on the quality and relevance of the retrieved chunks.
