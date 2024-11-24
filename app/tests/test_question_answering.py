import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.question_answering import QuestionAnsweringAPI, QuestionRequest


class TestQuestionAnsweringAPI(unittest.TestCase):

    def setUp(self):
        # A FastAPI app with the QuestionAnsweringAPI router included
        self.app = FastAPI()
        self.app.include_router(QuestionAnsweringAPI().router)
        self.client = TestClient(self.app)

    def test_post_question_success(self):
        # Given
        endpoint = "/qna/"
        payload = {"question": "What is FastAPI?"}

        # When
        response = self.client.post(endpoint, json=payload)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"message": "Static answer for the question."}
        )

    def test_post_question_missing_field(self):
        # Given
        endpoint = "/qna/"
        payload = {}

        # When
        response = self.client.post(endpoint, json=payload)

        # Then
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())
        self.assertIn("question", str(response.json()["detail"]))

    def test_router_has_expected_route(self):
        # Given
        routes = [route.path for route in QuestionAnsweringAPI.router.routes]

        # Then
        self.assertIn("/qna/", routes)

    def test_method_mapping(self):
        # Given
        routes = [route for route in QuestionAnsweringAPI.router.routes if route.path == "/qna/"]

        # Then
        self.assertTrue(any("POST" in route.methods for route in routes))


if __name__ == "__main__":
    unittest.main()
