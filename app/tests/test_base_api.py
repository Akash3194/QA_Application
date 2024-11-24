import unittest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.api.base_api import BaseGetApi, BasePostApi


class TestGetApi(BaseGetApi):
    """A test class to test BaseGetApi"""

    ENDPOINT = "/test-get/"

    @staticmethod
    async def get():
        return {"message": "GET request successful"}


class TestPostApi(BasePostApi):
    """A test class to test BasePostApi"""

    ENDPOINT = "/test-post/"

    @staticmethod
    async def post():
        return {"message": "POST request successful"}


class TestBaseApi(unittest.TestCase):

    def setUp(self):
        self.app = FastAPI()
        self.app.include_router(TestGetApi().router)
        self.app.include_router(TestPostApi().router)
        self.client = TestClient(self.app)

    def test_base_get_api(self):
        # Given
        endpoint = "/test-get/"

        # When
        response = self.client.get(endpoint)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "GET request successful"})

    def test_base_post_api(self):
        # Given
        endpoint = "/test-post/"

        # When
        response = self.client.post(endpoint)

        # Then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "POST request successful"})

    def test_base_api_missing_endpoint(self):
        # Given
        class InvalidGetApi(BaseGetApi):

            @staticmethod
            async def get():
                return {"message": "Invalid"}

        class InvalidPostApi(BasePostApi):

            @staticmethod
            async def post():
                return {"message": "Invalid"}

        # When & Then
        with self.assertRaises(ValueError) as get_context:
            InvalidGetApi()

        with self.assertRaises(ValueError) as post_context:
            InvalidPostApi()

        self.assertIn("must define a valid 'ENDPOINT'", str(get_context.exception))
        self.assertIn("must define a valid 'ENDPOINT'", str(post_context.exception))

    def test_base_api_missing_handler(self):
        # Given
        class InvalidGetApi(BaseGetApi):
            ENDPOINT = "/invalid-get/"

        class InvalidPostApi(BasePostApi):
            ENDPOINT = "/invalid-post/"

        # When & Then
        with self.assertRaises(TypeError) as get_context:
            InvalidGetApi()

        with self.assertRaises(TypeError) as post_context:
            InvalidPostApi()

        self.assertIn("Can't instantiate abstract class ",
                      str(get_context.exception))
        self.assertIn("Can't instantiate abstract class ",
                      str(post_context.exception))

    def test_router_has_expected_routes(self):

        # When
        get_routes = [route.path for route in TestGetApi.router.routes]
        post_routes = [route.path for route in TestPostApi.router.routes]

        # Then
        self.assertIn("/test-get/", get_routes)
        self.assertIn("/test-post/", post_routes)

        get_methods = [method for route in TestGetApi.router.routes for method in route.methods]
        post_methods = [method for route in TestPostApi.router.routes for method in route.methods]

        self.assertIn("GET", get_methods)
        self.assertIn("POST", post_methods)


if __name__ == "__main__":
    unittest.main()
