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
        if len(content) > 20*1024*1024:
            raise HTTPException(
                status_code=400,
                detail=f'{file.filename} exceeds the maximum file size of 20 MB'
            )
        if not content:
            raise HTTPException(
                status_code=400,
                detail=f'{file.filename} cannot be empty'
            )
        file_path.write_bytes(content)
        try:
            chunks_created = document_pipeline.process_document(
                file_path,
                source_name=file.filename
            )
            return{
                'message': 'Document uploaded successfully',
                'filename': file.filename,
                'chunks': len(chunks_created)
            }
        except ValueError as e:
            file_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception:
            file_path.unlink(missing_ok=True)
            raise HTTPException(
                status_code=500,
                detail='An unexpected error has occurred while processing'
            )
    @router.post('/ask')
    async def ask_question(request: QuestionRequest):
        response = rag_pipeline.answer(request.query)
        return response
    return router


class QuestionRequest(BaseModel):
    query: str


@router.get('/health')
async def health_check():
    return {'status': 'healthy'}