import unittest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.document_repository import DocumentRepository
from app.models.document import Document


class TestDocumentRepository(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock(spec=AsyncSession)
        self.repo = DocumentRepository(db=self.mock_db)

    def tearDown(self):
        self.mock_db.reset_mock()

    async def test_add_document(self):
        # Given
        title = "Test Title"
        embeddings = "mock_embeddings"
        self.mock_db.commit = AsyncMock()
        self.mock_db.add = MagicMock()

        # When
        new_doc = await self.repo.add_document(title, embeddings)

        # Then
        self.mock_db.add.assert_called_once()
        self.mock_db.commit.assert_awaited_once()
        self.assertIsInstance(new_doc, Document)
        self.assertEqual(new_doc.title, title)
        self.assertEqual(new_doc.embedding, embeddings)

    async def test_get_document(self):
        # Given
        document_id = 1
        expected_document = Document(id=1, title="Test Title", embedding="mock_embeddings")
        mock_result = MagicMock()
        mock_result.scalars = MagicMock(return_value=iter([expected_document]))
        self.mock_db.execute = AsyncMock(return_value=mock_result)

        # When
        result = await self.repo.get_document(document_id)

        # Then
        self.mock_db.execute.assert_awaited_once()
        mock_result.scalars.assert_called_once()
        self.assertEqual(result, expected_document)


if __name__ == "__main__":
    unittest.main()
