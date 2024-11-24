from fastapi import FastAPI
from app.api.document_ingestion import DocumentIngestionAPI
from app.api.document_selection import DocumentSelectionAPI
from app.api.question_answering import QuestionAnsweringAPI
from app.db.database import init_db

app = FastAPI(title="Document Ingestion and Q&A API")

@app.on_event("startup")
async def startup_event():
    await init_db()

app.include_router(DocumentIngestionAPI().router, prefix="/api", tags=["Document Ingestion"])
app.include_router(DocumentSelectionAPI().router, prefix="/api", tags=["Document Selection"])
app.include_router(QuestionAnsweringAPI().router, prefix="/api", tags=["Q&A"])
