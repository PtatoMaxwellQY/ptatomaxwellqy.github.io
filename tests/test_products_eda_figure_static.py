import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ProductsEdaFigureStaticTest(unittest.TestCase):
    def read(self, name):
        return (ROOT / name).read_text(encoding="utf-8")

    def product4_markup(self):
        html = self.read("Products.html")
        return html.split('<article class="product-lane reveal-on-scroll" id="product4">', 1)[1].split("</article>", 1)[0]

    def test_eda_automation_uses_mxpic_gif_figure(self):
        markup = self.product4_markup()

        self.assertIn('class="product-image product-eda-figure"', markup)
        self.assertIn('src="images/products/mxpic_EDA.gif"', markup)
        self.assertIn('alt="MxPIC EDA photonic automation workflow preview"', markup)
        self.assertIn('width="1920"', markup)
        self.assertIn('height="982"', markup)
        self.assertNotIn('class="mxpic-mark"', markup)
        self.assertNotIn("<svg", markup)

    def test_eda_gif_has_product_specific_image_fit(self):
        css = self.read("assets/css/industrial-pages.css")

        self.assertIn(".product-eda-figure", css)
        self.assertIn(".product-eda-figure img", css)
        self.assertIn("aspect-ratio: 1920 / 982;", css)
        self.assertIn("object-fit: contain;", css)


if __name__ == "__main__":
    unittest.main()
