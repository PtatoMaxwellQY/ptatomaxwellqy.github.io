import unittest
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SHARED_BRIGHT = {
    "--opti-bg": "#F1FAEE",
    "--opti-bg-2": "#EEF8F8",
    "--opti-surface": "#FEFEFD",
    "--opti-surface-2": "#E6F0F1",
    "--opti-text": "#2B2D42",
    "--opti-muted": "rgba(69, 88, 100, 0.76)",
    "--opti-faint": "rgba(88, 108, 122, 0.55)",
    "--opti-primary": "#006D77",
    "--opti-secondary": "#457B9D",
    "--opti-critical": "#E63946",
    "--opti-button-text": "#FEFEFD",
}

EXPECTED_DARK_TOKENS = {
    "--opti-bg": "#09090D",
    "--opti-bg-2": "#11121A",
    "--opti-surface": "#1A1B28",
    "--opti-surface-2": "#222435",
    "--opti-text": "#F6FBFC",
    "--opti-primary": "#A8DADC",
    "--opti-secondary": "#66A7AD",
    "--opti-critical": "#E63946",
}

EXPECTED_HOME_THEME_ALIASES = {
    "--color-bg": "var(--opti-bg)",
    "--color-bg-2": "var(--opti-bg-2)",
    "--color-surface": "var(--opti-surface)",
    "--color-surface-2": "var(--opti-surface-2)",
    "--color-text": "var(--opti-text)",
    "--color-muted": "var(--opti-muted)",
    "--color-faint": "var(--opti-faint)",
    "--color-primary": "var(--opti-primary)",
    "--color-secondary": "var(--opti-secondary)",
    "--color-critical": "var(--opti-critical)",
    "--color-button-text": "var(--opti-button-text)",
}

EXPECTED_BACKGROUND_BRIGHT = {
    "home": ("0, 109, 119", "#457B9D", "#E63946"),
    "product": ("69, 123, 157", "#006D77", "#D90429"),
    "technology": ("88, 108, 122", "#457B9D", "#006D77"),
    "careers": ("174, 3, 33", "#006D77", "#457B9D"),
    "news": ("14, 165, 233", "#38BDF8", "#0284C7"),
    "team": ("51, 138, 146", "#006D77", "#66A7AD"),
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
        home = self.token_values(self.block(self.homepage_style(), ":root"))

        for token, value in EXPECTED_SHARED_BRIGHT.items():
            with self.subTest(token=token):
                self.assertEqual(shared[token], value)

        for token, value in EXPECTED_HOME_THEME_ALIASES.items():
            with self.subTest(token=token):
                self.assertEqual(home[token], value)

    def test_dark_shared_tokens_follow_color_system(self):
        dark = self.token_values(self.block(self.css(), ':root,\n[data-theme="dark"]'))

        for token, value in EXPECTED_DARK_TOKENS.items():
            with self.subTest(token=token):
                self.assertEqual(dark[token], value)

    def test_page_backgrounds_use_solid_theme_color_without_wash_layers(self):
        css = self.css()
        home_style = self.homepage_style()

        for disallowed in ("--opti-wash", "--opti-accent-wash"):
            with self.subTest(shared_disallowed=disallowed):
                self.assertNotIn(disallowed, css)

        for disallowed in ("--body-wash", "--body-accent-wash"):
            with self.subTest(home_disallowed=disallowed):
                self.assertNotIn(disallowed, home_style)

        self.assertIn("background: var(--opti-bg);", self.block(css, "body {"))
        self.assertIn("background: var(--color-bg);", self.block(home_style, "body {"))

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

        self.assertNotIn('[data-theme="bright"] {\n            --color-bg:', home_style)
        self.assertNotIn('[data-theme="dark"] {\n            --color-bg:', home_style)

    def test_interactive_background_uses_shared_theme_background(self):
        js = self.read("assets/js/interactive-background.js")

        self.assertIn("getPropertyValue('--opti-bg')", js)
        self.assertIn("bg: themeBackground(),", js)
        self.assertNotRegex(js, r"(dark|bright): \{ bg: '#")

        for variant, (line, glow, dot) in EXPECTED_BACKGROUND_BRIGHT.items():
            pattern = (
                rf"{variant}: \{{[\s\S]*?"
                rf"bright: \{{ line: \[{re.escape(line)}\], "
                rf"glow: '{re.escape(glow)}', dot: '{re.escape(dot)}' \}}"
            )
            with self.subTest(variant=variant):
                self.assertRegex(js, pattern)


if __name__ == "__main__":
    unittest.main()
