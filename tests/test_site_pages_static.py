import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGES = ("Products.html", "Technology.html", "carrers.html", "news.html", "team.html")


class SitePagesStaticTest(unittest.TestCase):
    def read(self, name):
        return (ROOT / name).read_text(encoding="utf-8")

    def test_non_home_pages_load_shared_industrial_style(self):
        for page in PAGES:
            with self.subTest(page=page):
                self.assertIn('href="assets/css/industrial-pages.css"', self.read(page))
                self.assertIn('src="assets/js/industrial-pages.js"', self.read(page))
                self.assertNotIn('href="assets/css/main.css"', self.read(page))
                self.assertNotIn('href="assets/css/noscript.css"', self.read(page))

    def test_non_home_pages_use_homepage_header_functions(self):
        for page in PAGES:
            with self.subTest(page=page):
                html = self.read(page)
                self.assertIn('<header class="site-header">', html)
                self.assertIn('class="nav-shell"', html)
                self.assertIn('class="desktop-nav"', html)
                self.assertNotIn('<header id="header"', html)
                self.assertNotIn('id="page-wrapper"', html)
                self.assertIn('data-theme="dark"', html)
                self.assertIn('class="theme-selector"', html)
                self.assertIn('data-theme-choice="bright"', html)
                self.assertIn('data-theme-choice="dark"', html)

    def test_non_home_pages_use_homepage_logo_mark(self):
        for page in PAGES:
            with self.subTest(page=page):
                html = self.read(page)
                header = html.split('<header class="site-header">', 1)[1].split('</header>', 1)[0]
                self.assertIn('<span class="brand-mark" aria-hidden="true">', header)
                self.assertIn('<svg viewBox="0 0 32 32"', header)
                self.assertIn('stroke-linecap="square"', header)
                self.assertIn('<img class="theme-logo" src="./images/optihk_dark.png"', header)
                self.assertIn('data-logo-bright="./images/optihk_bright.png"', header)
                self.assertIn('data-logo-dark="./images/optihk_dark.png"', header)
                self.assertNotIn(">IO</span>", header)
                self.assertNotIn("Silicon photonics</span>", header)

    def test_legacy_header_inline_overrides_are_removed(self):
        for page in PAGES:
            with self.subTest(page=page):
                html = self.read(page)
                self.assertNotIn("header.style.backgroundColor", html)
                self.assertNotIn("style.borderBottom", html)

    def test_products_page_keeps_interactive_background_animation(self):
        html = self.read("Products.html")
        self.assertIn('<canvas id="bg-canvas"></canvas>', html)
        self.assertIn("requestAnimationFrame(animate)", html)
        self.assertIn("window.addEventListener('mousemove', onMouseMove)", html)
        self.assertIn("const LINE_COLOR = '#84bda0';", html)

    def test_products_page_uses_compressed_product_images(self):
        css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        self.assertIn("aspect-ratio: 16 / 7;", css)
        self.assertIn("height: clamp(8.5rem, 14vw, 16rem);", css)
        self.assertIn("--product-image-scale: 1;", css)
        self.assertIn(".product-lane:not(#product4) .product-image img", css)
        self.assertIn("width: calc(100% * var(--product-image-scale));", css)
        self.assertIn("grid-template-columns: 2.6rem minmax(0, 0.88fr) minmax(24rem, 1.12fr);", css)
        self.assertIn("padding: 0.65rem 0.75rem;", css)
        self.assertIn("font-size: clamp(1.05rem, 1vw, 1.28rem);", css)

    def test_products_page_main_text_is_larger(self):
        css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        self.assertIn(".product-page .page-lede,", css)
        self.assertIn(".product-page .product-lane p,", css)
        self.assertIn(".product-page .delivery-flow p", css)
        self.assertIn("font-size: calc(1em + 2pt);", css)

    def test_products_page_has_product_first_lanes_and_mxpic(self):
        html = self.read("Products.html")
        self.assertIn('class="product-lane reveal-on-scroll"', html)
        self.assertIn("Optical IO solutions", html)
        self.assertIn("Mini sensing solutions", html)
        self.assertIn("Photonic Automation solutions", html)
        self.assertIn("Co-packaged Optics OE Engine", html)
        self.assertIn("D8-1600G SiPh transmitter", html)
        self.assertIn("SiPh spectrometers", html)
        self.assertIn("MxPIC EDA tools", html)
        self.assertIn('class="mxpic-mark"', html)
        self.assertIn('href="index.html#contact"', html)
        self.assertNotIn('class="lane-specs"', html)
        self.assertNotIn("<dt>Interface</dt>", html)
        self.assertNotIn("<dt>Stage</dt>", html)
        self.assertNotIn("<dt>Use</dt>", html)
        self.assertNotIn("Co-Packaged Optical Engine", html)
        self.assertNotIn("Integrated Photonic Sensor", html)
        self.assertNotIn("Advanced Photonic Packaging", html)
        self.assertNotIn("MxPIC Photonic EDA Suite", html)

    def test_products_page_keeps_clean_reconstructed_product_experience(self):
        html = self.read("Products.html")
        css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        for text in (
            'class="delivery-flow reveal-on-scroll"',
            "Prototype to packaged module",
        ):
            self.assertIn(text, html)
        for removed in (
            "Chip to package to layout",
            "Bandwidth pressure",
            "Measurement pressure",
            "Match the lane to the program phase",
            'class="evidence-strip"',
            'class="product-signal-panel"',
            'class="portfolio-map reveal-on-scroll"',
            'class="product-fit-matrix reveal-on-scroll"',
        ):
            self.assertNotIn(removed, html)
        for selector in (
            ".delivery-flow",
            ".product-lane::before",
        ):
            self.assertIn(selector, css)
        for removed_selector in (
            ".product-signal-panel",
            ".portfolio-map",
            ".product-fit-matrix",
            ".fit-table",
            ".evidence-strip",
        ):
            self.assertNotIn(removed_selector, css)

    def test_technology_page_has_capability_map_and_process_band(self):
        html = self.read("Technology.html")
        for text in (
            "Product-first capability map",
            "MxPIC EDA Flow",
            "Architecture",
            "Simulation / design",
            "Package integration",
            "Validation",
        ):
            self.assertIn(text, html)
        self.assertIn("process-band", html)
        self.assertIn('class="capability-map"', html)
        self.assertNotIn('class="evidence-strip"', html)
        self.assertNotIn("Photonic circuit architecture", html)
        self.assertNotIn("Driver, receiver, and control interfaces", html)
        self.assertNotIn("Low-loss optical and thermal integration", html)
        self.assertNotIn("MxPIC design flow</span>", html)

    def test_jobs_page_has_filters_and_stronger_cv_path(self):
        html = self.read("carrers.html")
        self.assertIn("filter-bar", html)
        self.assertIn('data-filter-group="jobs"', html)
        self.assertIn('data-filter-target="pic"', html)
        self.assertIn('data-filter-item', html)
        self.assertIn('href="index.html#contact">Send CV / introduction</a>', html)

    def test_team_page_groups_people_and_normalizes_portraits(self):
        html = self.read("team.html")
        self.assertIn("Leadership", html)
        self.assertIn("Engineering contributors", html)
        self.assertIn('class="team-section-label"', html)
        css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        self.assertIn("object-position: center top;", css)
        self.assertIn("min-height: 8.5rem;", css)

    def test_news_page_has_polished_newsroom_layout(self):
        html = self.read("news.html")
        self.assertIn('class="featured-news reveal-on-scroll"', html)
        self.assertIn('class="news-grid"', html)
        self.assertIn("Company", html)
        self.assertIn("Technology", html)
        self.assertIn("Careers", html)

    def test_shared_interactions_support_filters_and_theme_persistence(self):
        js = (ROOT / "assets/js/industrial-pages.js").read_text(encoding="utf-8")
        self.assertIn("localStorage.setItem('optihk-theme'", js)
        self.assertIn("data-filter-group", js)
        self.assertIn("data-filter-item", js)
        self.assertIn("prefers-reduced-motion", js)

    def test_pages_use_clean_company_chrome_copy(self):
        for page in PAGES:
            with self.subTest(page=page):
                html = self.read(page)
                self.assertIn("Copyright &copy; 2026 OptiHK. All Rights Reserved.", html)
                self.assertNotIn("Copyright 穢", html)
                self.assertNotIn("OptiHK 繚", html)

    def test_shared_industrial_style_exposes_homepage_tokens(self):
        css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        self.assertIn("--opti-bg: #050808;", css)
        self.assertIn("--opti-primary: #9ad8d8;", css)
        self.assertIn("--opti-secondary: #84bda0;", css)
        self.assertIn("border-radius: 4px;", css)
        self.assertIn('[data-theme="bright"]', css)
        self.assertIn(".theme-selector", css)
        self.assertIn('border-bottom: 0 !important;', css)

    def test_subpage_titles_match_homepage_scale_and_position(self):
        css = (ROOT / "assets/css/industrial-pages.css").read_text(encoding="utf-8")
        self.assertIn("min-height: clamp(18rem, 35vh, 23.5rem);", css)
        self.assertIn("padding: clamp(1.25rem, 4vh, 2rem) 0 1.25rem;", css)
        self.assertIn("align-content: start;", css)
        self.assertIn("font-size: clamp(2rem, 3.1vw, 3.8rem);", css)
        self.assertIn("max-width: 16ch;", css)


if __name__ == "__main__":
    unittest.main()
