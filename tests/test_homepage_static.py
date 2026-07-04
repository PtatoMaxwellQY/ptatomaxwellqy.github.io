import re
import unittest
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HomepageStaticTest(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_homepage_has_customer_partner_industrial_positioning(self):
        self.assertIn("<title>OptiHK | Optical I/O from chip to package</title>", self.html)
        self.assertRegex(
            self.html,
            r'<meta name="description" content="[^"]*Optical I/O[^"]*customers[^"]*"',
        )
        self.assertIn("Optical I/O from chip to package", self.html)
        self.assertIn("Built for customers and partners developing high-density AI infrastructure", self.html)

    def test_homepage_surfaces_product_pathways_without_removed_metrics(self):
        for pathway in (
            "Co-Packaged Optical Engine",
            "Integrated Photonic Sensor",
            "Advanced Photonic Packaging",
        ):
            self.assertIn(pathway, self.html)

        for removed in (
            "Faster Data by the Numbers",
            "High bandwidth modulator.",
            'aria-label="Technical proof points"',
            'id="faster-data"',
        ):
            self.assertNotIn(removed, self.html)

    def test_homepage_removes_placeholders_and_keeps_contact_endpoint(self):
        for placeholder in ("untitled", "(000) 000-0000", 'href="#"'):
            self.assertNotIn(placeholder, self.html)

        self.assertIn('action="/api/contact"', self.html)
        self.assertIn('name="cv"', self.html)
        self.assertIn("Partnership / product inquiry", self.html)

    def test_carousel_controls_have_correct_accessible_labels(self):
        self.assertRegex(
            self.html,
            r'<button[^>]+class="carousel-arrow prev"[^>]+aria-label="Previous slide"',
        )
        self.assertRegex(
            self.html,
            r'<button[^>]+class="carousel-arrow next"[^>]+aria-label="Next slide"',
        )

    def test_visual_companion_artifacts_are_ignored(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertTrue(
            re.search(r"(?m)^\.superpowers/$", gitignore),
            ".superpowers/ should be ignored so visual companion files stay out of commits",
        )

    def test_homepage_has_bright_dark_theme_selector(self):
        shared_css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        shared_js = (ROOT / "assets/js/industrial-pages.js").read_text(encoding="utf-8")
        self.assertIn('[data-theme="dark"]', shared_css)
        self.assertIn('href="assets/css/industrial-pages.css"', self.html)
        self.assertIn('id="theme-toggle"', self.html)
        self.assertIn('aria-label="Toggle color mode"', self.html)
        self.assertNotIn('--color-bg: #', self.html)
        self.assertNotIn('--color-primary: #', self.html)
        self.assertIn("setTheme(current === 'bright' ? 'dark' : 'bright', true)", shared_js)

    def test_homepage_header_has_simplified_tabs_and_shared_mark(self):
        self.assertIn('<span class="brand-mark" aria-hidden="true">', self.html)
        self.assertIn('<svg viewBox="0 0 32 32"', self.html)
        self.assertIn('<img class="theme-logo" src="./images/optihk_dark.png"', self.html)
        self.assertIn('data-logo-bright="./images/optihk_bright.png"', self.html)
        self.assertIn('data-logo-dark="./images/optihk_dark.png"', self.html)
        self.assertNotIn('<span class="brand-text">Silicon photonics</span>', self.html)
        self.assertNotIn('class="nav-cta"', self.html)
        header = self.html.split('<header class="site-header">', 1)[1].split('</header>', 1)[0]
        self.assertNotIn('href="#contact"', header)
        self.assertNotIn(">Contact</a>", header)

    def test_homepage_dark_nav_active_state_stays_readable(self):
        self.assertIn("body.home-page .desktop-nav a[aria-current=\"page\"]", self.html)
        self.assertIn("color: var(--color-text);", self.html)
        self.assertNotIn("color: var(--color-surface);\n            text-shadow: 0 1px 4px", self.html)

    def test_homepage_header_styles_are_shared(self):
        shared_css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        self.assertNotIn("\n        .site-header {", self.html)
        self.assertNotIn("\n        .desktop-nav {", self.html)
        self.assertNotIn("\n        .theme-selector {", self.html)
        self.assertIn(".site-header {", shared_css)
        self.assertIn(".desktop-nav {", shared_css)
        self.assertIn("font-size: calc(0.75rem + 2pt);", shared_css)

    def test_homepage_hero_does_not_include_platform_engine_panel(self):
        self.assertNotIn('class="hero-panel"', self.html)
        self.assertNotIn('aria-label="Platform focus"', self.html)
        self.assertNotIn("<span>Platform</span>", self.html)
        self.assertNotIn("<span>Optical engine</span>", self.html)

    def test_homepage_has_updated_main_slogan_with_colorful_photonic_ics(self):
        self.assertIn("Advancing the future with Photonic ICs", self.html)
        self.assertIn('id="main-slogan"', self.html)
        self.assertIn('<span class="slogan-line">Advancing the future with</span>', self.html)
        self.assertIn('<span class="colorful-phrase">Photonic ICs</span>', self.html)
        self.assertIn('font-family: Calibri, "Segoe UI", Arial, sans-serif;', self.html)
        self.assertIn("max-width: 24ch;", self.html)
        self.assertIn("white-space: nowrap;", self.html)
        self.assertIn("background: linear-gradient(90deg, #004e89 0%, #006d77 34%, #1d4ed8 68%, #0f766e 100%);", self.html)
        self.assertIn("font-style: italic;", self.html)
        self.assertIn("font-weight: 900;", self.html)
        self.assertIn('[data-theme="dark"] .hero h1 .colorful-phrase', self.html)
        self.assertIn("background: linear-gradient(90deg, #41BFD5 0%, #824FD2 100%);", self.html)
        self.assertIn("text-shadow: 0 0 36px rgba(65, 191, 213, 0.34), 0 0 54px rgba(130, 79, 210, 0.3);", self.html)
        self.assertIn("Optics to the world", self.html)
        self.assertNotIn("Optical IO solution for cluster AI computations", self.html)
        self.assertNotIn("Silicon photonics for AI systems", self.html)
        self.assertNotIn("Large AI needs a cleaner path than copper and power-hungry SERDES.", self.html)
        self.assertNotIn("Electrical reach, package density, and thermal pressure are becoming system-level limits.", self.html)

    def test_homepage_why_optihk_has_four_strength_sections(self):
        self.assertIn('class="why-grid reveal-on-scroll"', self.html)
        self.assertIn('aria-label="OptiHK strengths"', self.html)

        for title in (
            "Advanced Technology",
            "Professional Team",
            "Rich Funding Source",
            "Solid Industrial Collaboration",
        ):
            with self.subTest(title=title):
                self.assertIn(f"<h3>{title}</h3>", self.html)

        self.assertEqual(self.html.count('class="why-card"'), 4)
        self.assertIn(".why-grid", self.html)
        self.assertIn(".why-card h3", self.html)

    def test_homepage_section_labels_use_consistent_calibri_style(self):
        shared_css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        self.assertIn("--opti-display: Calibri, Arial, sans-serif;", shared_css)
        self.assertIn("font-family: Calibri, Arial, sans-serif;", shared_css)
        self.assertIn("--font-display: Calibri, Arial, sans-serif;", self.html)
        self.assertIn("font-family: Calibri, Arial, sans-serif;", self.html)
        self.assertIn(".hero-copy > .eyebrow {\n            font-size: var(--opti-font-section-title);", self.html)
        self.assertIn("letter-spacing: 0.08em;", self.html)

    def test_homepage_hero_is_short_enough_to_show_metrics_early(self):
        self.assertIn("min-height: clamp(18rem, 35vh, 23.5rem);", self.html)
        self.assertIn("font-size: clamp(2rem, 3.1vw, 3.8rem);", self.html)
        self.assertIn("padding: clamp(var(--space-5), 4vh, var(--space-8)) 0 var(--space-5);", self.html)


if __name__ == "__main__":
    unittest.main()
