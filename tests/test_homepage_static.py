import re
import unittest
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

    def test_homepage_surfaces_proof_points_and_product_pathways(self):
        for proof_point in (">110G", "210 Gbps @ &lt;1 Vpp", "&lt;0.9 dB", "Dense mux"):
            self.assertIn(proof_point, self.html)

        for pathway in (
            "Co-Packaged Optical Engine",
            "Integrated Photonic Sensor",
            "Advanced Photonic Packaging",
        ):
            self.assertIn(pathway, self.html)

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
        self.assertIn('data-theme="dark"', self.html)
        self.assertIn('href="assets/css/industrial-pages.css"', self.html)
        self.assertIn('class="theme-selector"', self.html)
        self.assertIn('data-theme-choice="bright"', self.html)
        self.assertIn('data-theme-choice="dark"', self.html)
        self.assertIn('Bright', self.html)
        self.assertIn('Dark', self.html)
        self.assertIn('[data-theme="bright"]', self.html)
        self.assertIn('--color-bg: #f4f7f6;', self.html)
        self.assertIn('--color-primary: #006d77;', self.html)
        self.assertIn('--color-bg: #050808;', self.html)
        self.assertIn('--color-primary: #9ad8d8;', self.html)
        self.assertIn("setTheme(choice)", self.html)

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

    def test_homepage_has_fixed_main_slogan_and_separate_slide_caption(self):
        self.assertIn("Optical IO solution for cluster AI computations", self.html)
        self.assertIn('id="main-slogan"', self.html)
        self.assertIn("<span>Optical IO solution</span>", self.html)
        self.assertIn("<span>for cluster AI</span>", self.html)
        self.assertIn("<span>computations</span>", self.html)
        self.assertIn('id="slide-caption-title"', self.html)
        self.assertIn("Advanced packaging", self.html)
        self.assertIn("Clean architecture", self.html)
        self.assertNotIn("title.textContent = slide.title", self.html)
        self.assertNotIn("desc.textContent = slide.description", self.html)
        self.assertIn('href="#contact">Contact US</a>', self.html)
        self.assertNotIn(">Start inquiry</a>", self.html)

    def test_homepage_hero_is_short_enough_to_show_metrics_early(self):
        self.assertIn("min-height: clamp(18rem, 35vh, 23.5rem);", self.html)
        self.assertIn("font-size: clamp(2rem, 3.1vw, 3.8rem);", self.html)
        self.assertIn("padding: clamp(var(--space-5), 4vh, var(--space-8)) 0 var(--space-5);", self.html)


if __name__ == "__main__":
    unittest.main()
