import io
import tempfile
import unittest
from pathlib import Path

from backend import SubmissionStore


class SubmissionStoreTest(unittest.TestCase):
    def test_submission_data_is_stored_in_dated_name_folder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            store = SubmissionStore(root)

            submission_id = store.save_submission(
                {
                    "name": "Ada Wong",
                    "title": "Photonics Engineer",
                    "email": "ada@example.com",
                    "message": "I would like to learn more about OptiHK.",
                },
                "ada_cv.pdf",
                io.BytesIO(b"%PDF-1.4 cv bytes"),
            )

            submission_dir = root / "20260527" / "Ada_Wong"
            cv_path = submission_dir / "upload_CV" / "ada_cv.pdf"
            info_path = submission_dir / f"{submission_id}.txt"

            self.assertTrue(submission_dir.exists())
            self.assertEqual(cv_path.read_bytes(), b"%PDF-1.4 cv bytes")
            info_text = info_path.read_text(encoding="utf-8")
            self.assertIn("Name: Ada Wong", info_text)
            self.assertIn("Title: Photonics Engineer", info_text)
            self.assertIn("Email: ada@example.com", info_text)
            self.assertIn("Message: I would like to learn more about OptiHK.", info_text)


if __name__ == "__main__":
    unittest.main()
