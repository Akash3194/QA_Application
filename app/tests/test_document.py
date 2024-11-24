import unittest
from app.models.document import Document


class TestDocumentModel(unittest.TestCase):
    def test_table_name(self):
        self.assertEqual(Document.__tablename__, "documents")

    def test_columns(self):
        self.assertTrue(hasattr(Document, "id"))
        self.assertTrue(hasattr(Document, "title"))
        self.assertTrue(hasattr(Document, "embedding"))
        self.assertTrue(hasattr(Document, "updated_time"))

        self.assertTrue(Document.id.primary_key)
        self.assertEqual(Document.title.type.length, 255)


if __name__ == "__main__":
    unittest.main()
