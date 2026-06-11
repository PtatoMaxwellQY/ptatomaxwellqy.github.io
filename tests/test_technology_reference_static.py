import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TechnologyReferenceStaticTest(unittest.TestCase):
    def test_technology_page_file_remains_but_is_not_linked(self):
        self.assertTrue((ROOT / "Technology.html").is_file())
        for page in ROOT.glob("*.html"):
            with self.subTest(page=page.name):
                html = page.read_text(encoding="utf-8")
                self.assertNotIn("Technology.html", html)


if __name__ == "__main__":
    unittest.main()
