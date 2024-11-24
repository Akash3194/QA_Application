from fastapi import APIRouter
from abc import ABC, abstractmethod


class BaseApi:
    router = APIRouter()
    ENDPOINT: str = ''
    METHOD: str = ''

    def __init__(self):
        self.__register_route()

    @classmethod
    def __register_route(cls):
        if not hasattr(cls, 'ENDPOINT') or not getattr(cls, 'ENDPOINT'):
            raise ValueError(f"{cls.__name__} must define a valid 'ENDPOINT'.")

        if not hasattr(cls, 'METHOD') or not getattr(cls, 'METHOD'):
            raise ValueError(f"{cls.__name__} must define a valid 'METHOD'")

        if not hasattr(cls, cls.METHOD.lower()):
            raise ValueError(f"{cls.__name__} must define a '{cls.METHOD.lower()}' method.")

        cls.router.add_api_route(
            path=cls.ENDPOINT,
            endpoint=getattr(cls, cls.METHOD.lower()),
            methods=[cls.METHOD]
        )


class BaseGetApi(ABC, BaseApi):
    ENDPOINT: str = ''
    METHOD: str = 'GET'

    @staticmethod
    @abstractmethod
    async def get(*args, **kwargs):
        """Must be implemented in subclasses."""


class BasePostApi(ABC, BaseApi):
    ENDPOINT: str = ''
    METHOD: str = 'POST'

    @staticmethod
    @abstractmethod
    async def post(*args, **kwargs):
        """Must be implemented in subclasses."""

