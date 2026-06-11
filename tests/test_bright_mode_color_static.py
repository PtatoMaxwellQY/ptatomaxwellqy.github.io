import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SHARED_BRIGHT = {
    "--opti-bg": "#f4f8f7",
    "--opti-bg-2": "#e9f1ef",
    "--opti-surface": "#ffffff",
    "--opti-surface-2": "#eef5f3",
    "--opti-text": "#122425",
    "--opti-muted": "rgba(24, 50, 52, 0.76)",
    "--opti-faint": "rgba(24, 50, 52, 0.55)",
    "--opti-primary": "#006b73",
    "--opti-secondary": "#2d9b8b",
    "--opti-critical": "#b94b5a",
    "--opti-button-text": "#ffffff",
}

EXPECTED_HOME_BRIGHT = {
    "--color-bg": "#f4f8f7",
    "--color-bg-2": "#e9f1ef",
    "--color-surface": "#ffffff",
    "--color-surface-2": "#eef5f3",
    "--color-text": "#122425",
    "--color-muted": "rgba(24, 50, 52, 0.76)",
    "--color-faint": "rgba(24, 50, 52, 0.55)",
    "--color-primary": "#006b73",
    "--color-secondary": "#2d9b8b",
    "--color-critical": "#b94b5a",
    "--color-button-text": "#ffffff",
}

EXPECTED_DARK_TOKENS = {
    "--opti-bg": "#040807",
    "--opti-bg-2": "#081112",
    "--opti-surface": "#10191b",
    "--opti-surface-2": "#172326",
    "--opti-text": "#f6fbfa",
    "--opti-primary": "#a6e7e2",
    "--opti-secondary": "#79c4b1",
    "--opti-critical": "#d95a68",
}

EXPECTED_BACKGROUND_BRIGHT = {
    "home": ("#f4f8f7", "0, 107, 115", "#2d9b8b", "#b94b5a"),
    "product": ("#eef5f3", "45, 155, 139", "#2d9b8b", "#c05d66"),
    "technology": ("#f2f7f8", "42, 97, 150", "#5d8ed0", "#7658b8"),
    "careers": ("#f7f8f3", "142, 95, 28", "#b68436", "#b46a24"),
    "news": ("#f8f6f6", "170, 60, 78", "#b94b5a", "#cf7442"),
    "team": ("#f4f8f7", "38, 137, 124", "#006b73", "#b85a91"),
}


class BrightModeColorStaticTest(unittest.TestCase):
    def read(self, name):
        return (ROOT / name).read_text(encoding="utf-8")

    def css(self):
        return self.read("assets/css/industrial-pages.css")

    def homepage_style(self):
        html = self.read("index.html")
        return html.split("<style>", 1)[1].split("</style>", 1)[0]

    def block(self, text, selector):
        start = text.index(selector)
        brace = text.index("{", start)
        depth = 0
        for index in range(brace, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    return text[brace + 1:index]
        self.fail(f"Could not parse block for {selector}")

    def token_values(self, block):
        return {
            name: value.strip()
            for name, value in re.findall(r"(--[-\w]+):\s*([^;]+);", block)
        }

    def test_bright_tokens_are_technical_calm_and_mirrored(self):
        shared = self.token_values(self.block(self.css(), '[data-theme="bright"]'))
        home = self.token_values(self.block(self.homepage_style(), '[data-theme="bright"]'))

        for token, value in EXPECTED_SHARED_BRIGHT.items():
            with self.subTest(token=token):
                self.assertEqual(shared[token], value)

        for token, value in EXPECTED_HOME_BRIGHT.items():
            with self.subTest(token=token):
                self.assertEqual(home[token], value)

    def test_dark_shared_tokens_are_unchanged(self):
        dark = self.token_values(self.block(self.css(), ':root,\n[data-theme="dark"]'))

        for token, value in EXPECTED_DARK_TOKENS.items():
            with self.subTest(token=token):
                self.assertEqual(dark[token], value)

    def test_bright_mode_has_scoped_component_polish(self):
        css = self.css()
        home_style = self.homepage_style()

        for snippet in (
            '[data-theme="bright"] .site-header',
            '[data-theme="bright"] .product-lane h2',
            '[data-theme="bright"] .product-lane p',
            '[data-theme="bright"] .product-image img',
            '[data-theme="bright"] .tag',
            '[data-theme="bright"] .button-link:hover',
            '[data-theme="bright"] .site-footer',
            '[data-theme="bright"] .footer-contact-box',
        ):
            with self.subTest(shared_snippet=snippet):
                self.assertIn(snippet, css)

        for snippet in (
            '[data-theme="bright"] .hero',
            '[data-theme="bright"] .hero-panel',
            '[data-theme="bright"] .solution-card',
            '[data-theme="bright"] .tag',
            '[data-theme="bright"] .site-footer',
            '[data-theme="bright"] .footer-contact-box',
        ):
            with self.subTest(home_snippet=snippet):
                self.assertIn(snippet, home_style)

    def test_bright_background_palettes_are_page_specific(self):
        js = self.read("assets/js/interactive-background.js")

        for variant, (bg, line, glow, dot) in EXPECTED_BACKGROUND_BRIGHT.items():
            pattern = (
                rf"{variant}: \{{[\s\S]*?"
                rf"bright: \{{ bg: '{re.escape(bg)}', line: \[{re.escape(line)}\], "
                rf"glow: '{re.escape(glow)}', dot: '{re.escape(dot)}' \}}"
            )
            with self.subTest(variant=variant):
                self.assertRegex(js, pattern)


if __name__ == "__main__":
    unittest.main()
