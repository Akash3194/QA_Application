import time

from fastapi import Depends, UploadFile, File, Form, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.logging_utils import logger
from app.services.document_service import DocumentService
from app.repositories.document_repository import DocumentRepository
from app.api.base_api import BasePostApi
import asyncio


class DocumentIngestionAPI(BasePostApi):
    ENDPOINT: str = "/documents/"

    @staticmethod
    async def post(
            title: str = Form(...),
            file: UploadFile = File(...),  # File upload field
            db: AsyncSession = Depends(get_db)
    ):
        """
        Ingest a new document into the system.
        Offload the file extraction to a background thread to avoid blocking.
        """

        loop = asyncio.get_event_loop()
        try:
            embeddings = await loop.run_in_executor(None,
                                                    DocumentIngestionAPI.file_content_embeddings,
                                                    file)

            service = DocumentService(DocumentRepository(db))
            document = await service.ingest_document(title, embeddings)
            return {"message": "Document ingested successfully", "document_id": document.id}
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=str(e)
            )
        except Exception as e:
            await logger.error(f"Unexpected error during ingestion: {e}")
            raise HTTPException(status_code=500, detail="Something bad happened.")

    @staticmethod
    def file_content_embeddings(file: UploadFile):
        """Extract content from the uploaded file.

        For this example, it handles PDF files and plain text files.
        """

        if file.content_type == "application/pdf":
            DocumentIngestionAPI.extract_pdf_text(file)
        elif file.content_type == "text/plain":
            time.sleep(2)  # Adding time.sleep here because, method to vectorize it is not added
        else:
            raise ValueError("Unsupported file type. Provide .txt file.")

        return "Some mock content."

    @staticmethod
    def extract_pdf_text(file: UploadFile):
        """Extract text from a PDF file."""

        # Adding time.sleep here because, method to vectorize it is not added
        time.sleep(2)
