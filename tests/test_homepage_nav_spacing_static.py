import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HomepageNavSpacingStaticTest(unittest.TestCase):
    def test_homepage_does_not_override_shared_nav_spacing(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        style = html.split("<style>", 1)[1].split("</style>", 1)[0]

        for selector in (
            ".nav-shell {",
            ".brand {",
            ".brand-mark {",
            ".brand-mark svg {",
            ".desktop-nav {",
            ".desktop-nav a {",
            ".theme-selector {",
            ".theme-selector button {",
        ):
            with self.subTest(selector=selector):
                self.assertNotIn(selector, style)

        shared_css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        self.assertIn(".nav-shell {", shared_css)
        self.assertIn(".desktop-nav {", shared_css)


if __name__ == "__main__":
    unittest.main()
