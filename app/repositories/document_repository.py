from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.logging_utils import logger
from app.models.document import Document


class DocumentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_document(self, title: str, embeddings: str):
        try:
            new_doc = Document(title=title, embedding=embeddings)
            self.db.add(new_doc)
            await self.db.commit()
            await logger.info(f"Document '{title}' added successfully.")
            return new_doc
        except Exception as e:
            await logger.error(f"Failed to add document '{title}': {e}")
            raise

    async def get_document(self, document_id: int):
        result = await self.db.execute(select(Document).where(Document.id == document_id))
        return result.scalars().first()
