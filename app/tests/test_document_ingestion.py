import os
import unittest
from unittest.mock import patch, MagicMock
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from app.api.document_ingestion import DocumentIngestionAPI


class TestDocumentIngestionAPI(unittest.TestCase):

    def setUp(self):
        self.app = FastAPI()
        self.app.include_router(DocumentIngestionAPI().router)
        self.client = TestClient(self.app)

    @patch("app.api.document_ingestion.DocumentService.ingest_document")
    @patch("app.api.document_ingestion.DocumentIngestionAPI.file_content_embeddings")
    def test_post_document_ingestion_success(self, mock_embeddings, mock_ingest_document):
        # Given
        mock_embeddings.return_value = "Mock embeddings"
        mock_ingest_document.return_value = MagicMock(id=1)

        # When
        with open("test.txt", "w") as file:
            file.write("This is a test file.")

        with open("test.txt", "rb") as file:
            response = self.client.post(
                "/documents/",
                files={"file": ("test.txt", file, "text/plain")},
                data={"title": "Test Document"}
            )

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {
                             "message": "Document ingested successfully",
                             "document_id": 1
                         }
                    )

    def test_post_document_ingestion_unsupported_file_type(self):
        # Given
        unsupported_file_content_type = "application/json"

        # When
        with open("test.json", "w") as file:
            file.write("{}")
        with open("test.json", "rb") as file:
            response = self.client.post(
                "/documents/",
                files={"file": ("test.json", file, unsupported_file_content_type)},
                data={"title": "Test Document"}
            )

        # Then
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertEqual(response.json(), {"detail": "Unsupported file type"})

    def test_router_has_expected_route(self):
        # Given
        routes = [route.path for route in DocumentIngestionAPI.router.routes]

        # Then
        self.assertIn("/documents/", routes)

    def test_method_mapping(self):
        # Given
        routes = [route for route in DocumentIngestionAPI.router.routes if route.path == "/documents/"]

        # Then
        self.assertTrue(any("POST" in route.methods for route in routes))

    def tearDown(self):
        test_files = ["test.txt", "test.json"]
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)


if __name__ == "__main__":
    unittest.main()
