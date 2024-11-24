import unittest
from unittest.mock import patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db


class TestDatabase(unittest.TestCase):

    @patch("app.db.database.async_session")
    async def test_get_db(self, mock_sessionmaker):
        # Given
        mock_session = AsyncMock(spec=AsyncSession)
        mock_sessionmaker.return_value = mock_session

        # When
        async for session in get_db():
            # Then
            self.assertEqual(session, mock_session)

        mock_sessionmaker.assert_called_once()


if __name__ == "__main__":
    unittest.main()
