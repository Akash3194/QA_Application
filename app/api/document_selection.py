from app.api.base_api import BasePostApi  # Importing the BasePostApi class


class DocumentSelectionAPI(BasePostApi):
    ENDPOINT: str = "/documents/select/"

    @staticmethod
    async def post():
        """
        Select documents for the RAG-based Q&A process.
        """
        return {"message": "Document selection is not implemented yet."}
