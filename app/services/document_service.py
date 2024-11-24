from app.logging_utils import logger
from app.repositories.document_repository import DocumentRepository


class DocumentService:
    def __init__(self, repo: DocumentRepository):
        self.repo = repo

    async def ingest_document(self, title: str, embeddings: str):
        try:
            document = await self.repo.add_document(title, embeddings)
            await logger.info(f"Document '{title}' ingested successfully.")
            return document
        except Exception as e:
            await logger.error(f"Failed to ingest document '{title}': {e}")
            raise

    async def get_document_by_id(self, document_id: int):
        return await self.repo.get_document(document_id)
