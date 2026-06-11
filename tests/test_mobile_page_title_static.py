import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MobilePageTitleStaticTest(unittest.TestCase):
    def test_shared_page_titles_wrap_on_mobile(self):
        css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        mobile = css.split("@media (max-width: 640px)", 1)[1]

        self.assertIn(".page-title {", mobile)
        self.assertIn("font-size: clamp(3rem, 17vw, 4.6rem);", mobile)
        self.assertIn("overflow-wrap: anywhere;", mobile)
        self.assertIn(".page-hero .eyebrow {", mobile)
        self.assertIn("font-size: max(1rem, calc(var(--opti-font-min) * 0.84));", mobile)
        self.assertIn("word-break: break-word;", mobile)
        self.assertIn(".page-hero .eyebrow::before {", mobile)
        self.assertIn(".page-lede {", mobile)
        self.assertIn("max-width: min(100%, 24ch);", mobile)
        self.assertIn("font-size: clamp(1.05rem, 4.8vw, 1.32rem);", mobile)
        self.assertIn(".jobs-page .page-lede,", mobile)
        self.assertIn(".product-page .page-lede,", mobile)
        self.assertIn(".job-card summary {", mobile)
        self.assertIn("width: 100%;", mobile)
        self.assertIn("flex-direction: column;", mobile)
        self.assertIn(".job-card summary > span:first-child {", mobile)
        self.assertIn("min-width: 0;", mobile)
        self.assertIn("font-size: clamp(1.2rem, 5.8vw, 1.65rem);", mobile)


if __name__ == "__main__":
    unittest.main()
