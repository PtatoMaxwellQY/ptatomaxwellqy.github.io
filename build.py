#!/usr/bin/env python3
"""Build static HTML pages by injecting shared header/footer includes."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# --- Page configuration ---
PAGES = {
    "index.html": {
        "title": "OptiHK | Optical I/O from chip to package",
        "description": "OptiHK develops Optical I/O engines and photonic packaging platforms for customers building high-density AI infrastructure.",
        "body_class": "home-page",
        "bg_variant": "home",
        "active": "home",
        "extra_head": (
            '<meta property="og:title" content="OptiHK | Optical I/O from chip to package">\n'
            '    <meta property="og:description" content="Silicon photonics, low-loss interfaces, wavelength multiplexing, and advanced packaging for high-density AI systems.">\n'
            '    <meta property="og:image" content="images/banner/DSC_2979.webp">\n'
            '    <link rel="preload" as="image" href="images/banner/DSC_2979.webp">'
        ),
        "extra_styles": "",
        "footer_sensing": "Industrial metrology solutions",
        "send_cv_href": "#footer-contact-title",
        "inquiry_href": "#footer-contact-title",
        "extra_scripts": "",
    },
    "Products.html": {
        "title": "OptiHK | Products",
        "description": "OptiHK optical IO, mini sensing, and photonic automation product solutions.",
        "body_class": "product-page",
        "bg_variant": "product",
        "active": "products",
        "extra_head": "",
        "extra_styles": "",
        "footer_sensing": "Mini sensing solutions",
        "send_cv_href": "index.html#footer-contact-title",
        "inquiry_href": "index.html#footer-contact-title",
        "extra_scripts": "",
    },
    "Technology.html": {
        "title": "OptiHK | Technology",
        "description": "OptiHK silicon photonics technology platform: modulators, low-loss interfaces, multiplexing, and packaging workflows.",
        "body_class": "technology-page",
        "bg_variant": "technology",
        "active": "products",
        "extra_head": "",
        "extra_styles": "",
        "footer_sensing": "Mini sensing solutions",
        "send_cv_href": "index.html#footer-contact-title",
        "inquiry_href": "index.html#footer-contact-title",
        "extra_scripts": "",
    },
    "carrers.html": {
        "title": "OptiHK | Careers",
        "description": "Join OptiHK. Open roles in silicon photonics, optical engineering, packaging, and photonic EDA.",
        "body_class": "jobs-page",
        "bg_variant": "careers",
        "active": "careers",
        "extra_head": "",
        "extra_styles": "",
        "footer_sensing": "Mini sensing solutions",
        "send_cv_href": "index.html#footer-contact-title",
        "inquiry_href": "index.html#footer-contact-title",
        "extra_scripts": "",
    },
    "news.html": {
        "title": "OptiHK | News",
        "description": "Company announcements, technical highlights, hiring news, and event updates from OptiHK.",
        "body_class": "news-page",
        "bg_variant": "news",
        "active": "news",
        "extra_head": "",
        "extra_styles": "",
        "footer_sensing": "Mini sensing solutions",
        "send_cv_href": "index.html#footer-contact-title",
        "inquiry_href": "index.html#footer-contact-title",
        "extra_scripts": "",
    },
    "team.html": {
        "title": "OptiHK | Team",
        "description": "Meet the OptiHK team working across silicon photonics, optical sensing, CPO, and advanced packaging.",
        "body_class": "team-page",
        "bg_variant": "team",
        "active": "team",
        "extra_head": "",
        "extra_styles": "",
        "footer_sensing": "Mini sensing solutions",
        "send_cv_href": "index.html#footer-contact-title",
        "inquiry_href": "index.html#footer-contact-title",
        "extra_scripts": "",
    },
}


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote {path}")


def extract_main_content(html):
    """Extract the inner HTML of <main id="main"> from a full HTML file."""
    m = re.search(r'<main id="main">(.*?)</main>', html, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""


def extract_extra_styles(html, existing_extra):
    """Extract inline <style> block that comes after CSS links and before </head>."""
    if existing_extra:
        return existing_extra
    # Look for <style> block between last <link> and </head>
    m = re.search(
        r'(<link rel="stylesheet" href="assets/css/industrial-pages.css">)\s*(<style>.*?</style>)',
        html, re.DOTALL,
    )
    if m:
        return m.group(2)
    return ""


def extract_extra_scripts(html, existing_extra):
    """Extract page-specific inline scripts (not the standard ones)."""
    if existing_extra:
        return existing_extra
    # Get all script content before </body> that is NOT industrial-pages.js or interactive-background.js
    scripts = []
    for m in re.finditer(
        r'<script(?:\s[^>]*)?>(.*?)</script>',
        html, re.DOTALL,
    ):
        content = m.group(0)
        if "industrial-pages.js" in content or "interactive-background.js" in content:
            continue
        if content.strip() == "<script></script>":
            continue
        scripts.append(content)
    return "\n    " + "\n    ".join(scripts) if scripts else ""


def build_active_attrs(active):
    """Generate aria-current attributes for each nav link."""
    names = ["home", "products", "careers", "news", "team"]
    result = {}
    for name in names:
        if name == active:
            result[f"ACTIVE_{name.upper()}"] = ' aria-current="page"'
        else:
            result[f"ACTIVE_{name.upper()}"] = ""
    return result


def build_header(active):
    """Build header HTML with correct active nav."""
    header_tpl = read_file(ROOT / "includes" / "header.html")
    attrs = build_active_attrs(active)
    for key, val in attrs.items():
        header_tpl = header_tpl.replace("{{" + key + "}}", val)
    return header_tpl


def build_footer(sensing, send_cv, inquiry):
    """Build footer HTML with page-specific links."""
    footer_tpl = read_file(ROOT / "includes" / "footer.html")
    footer_tpl = footer_tpl.replace("{{FOOTER_SENSING}}", sensing)
    footer_tpl = footer_tpl.replace("{{SEND_CV_HREF}}", send_cv)
    footer_tpl = footer_tpl.replace("{{INQUIRY_HREF}}", inquiry)
    return footer_tpl


def build_scripts(extra_scripts):
    """Build the scripts block."""
    standard = (
        '<script src="assets/js/industrial-pages.js"></script>\n'
        '    <script src="assets/js/interactive-background.js"></script>'
    )
    if extra_scripts:
        return extra_scripts + "\n    " + standard
    return standard


def build_page(filename, cfg):
    """Build a complete HTML page."""
    print(f"Building {filename}...")

    base = read_file(ROOT / filename)
    header = build_header(cfg["active"])
    content = extract_main_content(base)
    footer = build_footer(cfg["footer_sensing"], cfg["send_cv_href"], cfg["inquiry_href"])
    scripts = build_scripts(extract_extra_scripts(base, cfg.get("extra_scripts", "")))
    extra_styles_val = extract_extra_styles(base, cfg.get("extra_styles", ""))
    extra_head = cfg.get("extra_head", "")

    # Build extra_head block
    extra_head_block = ""
    if extra_head:
        extra_head_block = "\n    " + extra_head

    # Build extra_styles block
    extra_styles_block = ""
    if extra_styles_val:
        extra_styles_block = "\n    " + extra_styles_val

    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="bright">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{cfg['title']}</title>
    <meta name="description" content="{cfg['description']}">{extra_head_block}
    <link rel="stylesheet" href="assets/css/fontawesome-all.min.css">
    <link rel="stylesheet" href="assets/css/industrial-pages.css">{extra_styles_block}
</head>
<body class="{cfg['body_class']} has-interactive-bg">
    <canvas id="bg-canvas" data-bg-variant="{cfg['bg_variant']}" aria-hidden="true"></canvas>
    <a class="skip-link" href="#main">Skip to content</a>
{header}
    <main id="main">
        {content}
    </main>
{footer}
    {scripts}
</body>
</html>"""

    write_file(ROOT / filename, html)


def main():
    print("Building OptiHK site...\n")
    for filename, cfg in PAGES.items():
        build_page(filename, cfg)
    print("\nDone. All pages rebuilt.")


if __name__ == "__main__":
    main()
