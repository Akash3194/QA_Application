import unittest
from unittest.mock import AsyncMock, MagicMock
from app.services.document_service import DocumentService
from app.repositories.document_repository import DocumentRepository


class TestDocumentService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock(spec=DocumentRepository)
        self.service = DocumentService(repo=self.mock_repo)

    def tearDown(self):
        self.mock_repo.reset_mock()

    async def test_ingest_document(self):
        # Given
        self.mock_repo.add_document = AsyncMock(
            return_value={"id": 1, "title": "Test Title", "embeddings": "mock_embeddings"})

        result = await self.service.ingest_document("Test Title", "mock_embeddings")

        self.mock_repo.add_document.assert_awaited_once_with("Test Title", "mock_embeddings")
        self.assertEqual(result, {"id": 1, "title": "Test Title", "embeddings": "mock_embeddings"})

    async def test_get_document_by_id(self):
        # Given
        self.mock_repo.get_document = AsyncMock(
            return_value={"id": 1, "title": "Test Title", "embeddings": "mock_embeddings"})

        # When
        result = await self.service.get_document_by_id(1)

        # Then
        self.mock_repo.get_document.assert_awaited_once_with(1)
        self.assertEqual(result, {"id": 1, "title": "Test Title", "embeddings": "mock_embeddings"})


if __name__ == "__main__":
    unittest.main()
