from app.api.base_api import BasePostApi
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class QuestionAnsweringAPI(BasePostApi):
    ENDPOINT: str = "/qna/"

    @staticmethod
    async def post(request: QuestionRequest):
        """
        Answer a user query using a static response (RAG not implemented yet).
        """
        question = request.question
        return {"message": f"Static answer for the question."}
