import unittest
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PAGES = {
    "index.html": "home",
    "Products.html": "product",
    "Technology.html": "technology",
    "carrers.html": "careers",
    "news.html": "news",
    "team.html": "team",
}


class InteractiveBackgroundStaticTest(unittest.TestCase):
    def read(self, name):
        return (ROOT / name).read_text(encoding="utf-8")

    def read_background_js(self):
        return self.read("assets/js/interactive-background.js")

    def background_variants(self):
        js = self.read_background_js()
        pattern = re.compile(
            r"(?P<name>home|product|technology|careers|news|team): \{\s+"
            r"count: (?P<count>\d+),\s+"
            r"distance: (?P<distance>\d+),.*?"
            r"dark: \{ line: \[(?P<dark_line>[^\]]+)\], glow: '[^']+', dot: '(?P<dark_dot>[^']+)' \},\s+"
            r"bright: \{ line: \[(?P<bright_line>[^\]]+)\], glow: '[^']+', dot: '(?P<bright_dot>[^']+)' \}",
            re.S,
        )
        return {
            match.group("name"): {
                "count": int(match.group("count")),
                "distance": int(match.group("distance")),
                "dark_line": match.group("dark_line"),
                "dark_dot": match.group("dark_dot"),
                "bright_line": match.group("bright_line"),
                "bright_dot": match.group("bright_dot"),
            }
            for match in pattern.finditer(js)
        }

    def test_all_public_pages_include_variant_background_canvas(self):
        for page, variant in PAGES.items():
            with self.subTest(page=page):
                html = self.read(page)
                canvas = f'<canvas id="bg-canvas" data-bg-variant="{variant}" aria-hidden="true"></canvas>'
                self.assertIn(canvas, html)
                self.assertIn('src="assets/js/interactive-background.js"', html)
                self.assertLess(html.index(canvas), html.index('<a class="skip-link"'))

    def test_background_animation_is_shared_not_inline_product_code(self):
        product_html = self.read("Products.html")
        background_js = self.read("assets/js/interactive-background.js")

        self.assertNotIn("const LINE_COLOR", product_html)
        self.assertNotIn("requestAnimationFrame(animate)", product_html)
        self.assertIn("data-bg-variant", background_js)
        self.assertIn("requestAnimationFrame(animate)", background_js)
        self.assertIn("document.addEventListener('pointermove', onPointerMove, { passive: true });", background_js)
        self.assertIn("canvas.addEventListener('pointermove', onPointerMove, { passive: true });", background_js)
        self.assertIn("window.addEventListener('mousemove', onPointerMove, { passive: true });", background_js)
        self.assertIn("prefers-reduced-motion: reduce", background_js)
        self.assertIn("var frameInterval = reducedMotion ? 1000 / 24 : 0;", background_js)
        self.assertIn("var lastFrameTime = 0;", background_js)
        self.assertIn("phase: Math.random() * Math.PI * 2", background_js)
        self.assertIn("var idleFlow = reducedMotion ? 0.018 : 0.026;", background_js)
        self.assertIn("particle.vx += Math.cos(time * 0.72 + particle.phase)", background_js)
        self.assertNotIn("if (!reducedMotion) {\n        animate();\n    }", background_js)
        self.assertIn("animate();", background_js)
        self.assertIn("if (reducedMotion && width && height)", background_js)
        self.assertIn("updateParticles();", background_js)
        self.assertIn("draw();", background_js)

    def test_canvas_layering_is_shared_across_background_pages(self):
        css = self.read("assets/css/industrial-pages.css")

        self.assertIn(".has-interactive-bg main,", css)
        self.assertIn(".has-interactive-bg .site-header,", css)
        self.assertIn(".has-interactive-bg .site-footer", css)
        self.assertIn("#bg-canvas", css)
        self.assertIn("pointer-events: auto;", css)

    def test_background_variants_are_denser_and_page_specific(self):
        variants = self.background_variants()

        self.assertEqual(set(variants), set(PAGES.values()))

        minimums = {
            "home": (112, 150),
            "product": (156, 166),
            "technology": (140, 160),
            "careers": (124, 154),
            "news": (112, 148),
            "team": (128, 154),
        }
        for variant, (min_count, min_distance) in minimums.items():
            with self.subTest(variant=variant):
                self.assertGreaterEqual(variants[variant]["count"], min_count)
                self.assertGreaterEqual(variants[variant]["distance"], min_distance)

        for key in ("dark_line", "dark_dot", "bright_line", "bright_dot"):
            values = [variant[key] for variant in variants.values()]
            with self.subTest(color_key=key):
                self.assertEqual(len(values), len(set(values)))


if __name__ == "__main__":
    unittest.main()
