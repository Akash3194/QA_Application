import unittest
from app.main import app


class TestMainApp(unittest.TestCase):
    def test_app_instance(self):

        # When & Then
        self.assertEqual(app.title, "Document Ingestion and Q&A API")

    def test_app_routes(self):

        # When
        routes = {route.path: route.name for route in app.routes}

        # Then
        self.assertIn("/api/documents/", routes)
        self.assertIn("/api/documents/select/", routes)
        self.assertIn("/api/qna/", routes)

        self.assertEqual(routes['/api/documents/'], 'post')
        self.assertEqual(routes['/api/documents/select/'], 'post')
        self.assertEqual(routes['/api/qna/'], 'post')


if __name__ == "__main__":
    unittest.main()
