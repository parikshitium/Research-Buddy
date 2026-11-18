from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException
from pydantic import BaseModel

router = APIRouter()

def configure_routes(document_pipeline,rag_pipeline):
    @router.post('/upload')
    async def upload_file(file: UploadFile = File(...)):
        extension = Path(file.filename).suffix.lower()
        if extension not in ['.pdf','.txt']:
            raise HTTPException(
                status_code=400,
                detail='Only PDF and TXT files are supported.'
            )
        upload_dir = Path('data/uploads')
        upload_dir.mkdir(parents=True,exist_ok=True)
        filename = f'{uuid4()}{extension}'
        file_path = upload_dir/filename
        content = await file.read()
        file_path.write_bytes(content)
        chunks_created = document_pipeline.process_document(file_path,
                                                            source_name=file.filename)
        return{
            'message': 'Document uploaded successfully',
            'filename': file.filename,
            'chunks': len(chunks_created)
        }
    @router.post('/ask')
    async def ask_question(request: QuestionRequest):
        response = rag_pipeline.answer(request.query)
        return response
    return router


class QuestionRequest(BaseModel):
    query: str