import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class JoinUsStaticTest(unittest.TestCase):
    def read_join_page(self):
        return (ROOT / "join_us.html").read_text(encoding="utf-8")

    def read_css(self):
        return (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")

    def test_join_us_page_uses_shared_industrial_chrome(self):
        html = self.read_join_page()
        self.assertIn('<html lang="en" data-theme="dark">', html)
        self.assertIn('<body class="join-page">', html)
        self.assertIn('href="assets/css/industrial-pages.css"', html)
        self.assertIn('src="assets/js/industrial-pages.js"', html)
        self.assertIn('<header class="site-header">', html)
        self.assertIn('class="theme-selector"', html)
        self.assertIn('id="mobile-menu"', html)
        self.assertIn('Copyright &copy; 2026 OptiHK. All Rights Reserved.', html)

    def test_join_us_page_contains_planned_sections_and_ctas(self):
        html = self.read_join_page()
        for text in (
            "Start your journey at the photonic hardware frontier.",
            "Why OptiHK",
            "Values we work by",
            "How the team works",
            "Open role tracks",
            "Build what compact optical systems need next.",
        ):
            self.assertIn(text, html)
        self.assertIn('src="./images/banner/DSC_2976.webp"', html)
        self.assertNotIn("images/poeple/Join_us.png", html)
        self.assertEqual(html.count('class="join-value-card reveal-on-scroll"'), 6)
        self.assertEqual(html.count('class="join-work-card reveal-on-scroll"'), 6)
        self.assertEqual(html.count('class="join-role-card reveal-on-scroll"'), 5)
        self.assertIn('href="carrers.html"', html)
        self.assertIn('href="index.html#footer-contact-title"', html)

    def test_join_us_styles_are_scoped(self):
        css = self.read_css()
        for selector in (
            ".join-page .join-hero",
            ".join-page .join-values-grid",
            ".join-page .join-work-grid",
            ".join-page .join-role-grid",
            ".join-page .join-final-cta",
        ):
            self.assertIn(selector, css)


if __name__ == "__main__":
    unittest.main()
