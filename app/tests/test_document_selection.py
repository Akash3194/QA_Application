import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.document_selection import DocumentSelectionAPI


class TestDocumentSelectionAPI(unittest.TestCase):

    def setUp(self):
        self.app = FastAPI()
        self.app.include_router(DocumentSelectionAPI().router)
        self.client = TestClient(self.app)

    def test_post_document_selection_success(self):
        # Given
        endpoint = "/documents/select/"

        # When
        response = self.client.post(endpoint)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Document selection is not implemented yet."})

    def test_router_has_expected_route(self):
        # Given
        routes = [route.path for route in DocumentSelectionAPI.router.routes]

        # Then
        self.assertIn("/documents/select/", routes)

    def test_method_mapping(self):
        # Given
        routes = [route for route in DocumentSelectionAPI.router.routes if route.path == "/documents/select/"]

        # Then
        self.assertTrue(any("POST" in route.methods for route in routes))


if __name__ == "__main__":
    unittest.main()
