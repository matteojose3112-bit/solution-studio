"""Generate a small static business microsite without executing user-supplied code."""
from html import escape
from io import BytesIO
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile


def generate_site_package(payload: dict) -> tuple[str, bytes]:
    name = str(payload.get("business_name", "")).strip()
    tagline = str(payload.get("tagline", "")).strip()
    description = str(payload.get("description", "")).strip()
    services = payload.get("services", [])
    email = str(payload.get("contact_email", "")).strip()
    color = str(payload.get("accent_color", "#7CE0B5")).strip()

    if not name or len(name) > 100:
        raise ValueError("Business name must contain 1–100 characters.")
    if not tagline or len(tagline) > 180:
        raise ValueError("Tagline must contain 1–180 characters.")
    if not description or len(description) > 800:
        raise ValueError("Description must contain 1–800 characters.")
    if not isinstance(services, list) or not 1 <= len(services) <= 6:
        raise ValueError("Add between 1 and 6 services.")
    clean_services = [str(item).strip() for item in services]
    if any(not item or len(item) > 100 for item in clean_services):
        raise ValueError("Each service must contain 1–100 characters.")
    if email and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise ValueError("Enter a valid contact email address.")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        raise ValueError("Accent color must be a six-digit hex color.")

    safe_name = escape(name)
    safe_tagline = escape(tagline)
    safe_description = escape(description)
    service_cards = "\n".join(
        f'<article class="service-card"><span>0{index}</span><h3>{escape(service)}</h3></article>'
        for index, service in enumerate(clean_services, start=1)
    )
    contact = (
        f'<a class="contact-link" href="mailto:{escape(email, quote=True)}">{escape(email)}</a>'
        if email else "<p>Add your contact email in index.html before publishing.</p>"
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{safe_description}">
  <title>{safe_name} | {safe_tagline}</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site-header"><a class="wordmark" href="#home">{safe_name}</a><a href="#contact">Get in touch</a></header>
  <main>
    <section class="hero" id="home">
      <p class="eyebrow">WELCOME</p>
      <h1>{safe_tagline}</h1>
      <p class="intro">{safe_description}</p>
      <a class="button" href="#services">Explore services</a>
    </section>
    <section class="services" id="services">
      <p class="eyebrow">WHAT WE DO</p><h2>Services built around your needs.</h2>
      <div class="service-grid">{service_cards}</div>
    </section>
    <section class="contact" id="contact">
      <p class="eyebrow">LET'S TALK</p><h2>Have a project in mind?</h2>
      {contact}
    </section>
  </main>
  <footer><span>{safe_name}</span><span>Built with Solution Studio</span></footer>
</body>
</html>
"""
    css = f""":root {{ font-family: Inter, ui-sans-serif, system-ui, sans-serif; color: #17212b; background: #f6f8f7; --accent: {color}; }}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; }}
a {{ color: inherit; text-decoration: none; }}
.site-header, footer {{ display: flex; justify-content: space-between; gap: 20px; padding: 24px max(7vw, calc((100vw - 1080px)/2)); }}
.site-header {{ border-bottom: 1px solid #17212b18; font-size: 13px; }}
.wordmark {{ font-weight: 800; }}
.hero, .services, .contact {{ max-width: 1080px; margin: auto; padding: 100px 28px; }}
.hero {{ min-height: 560px; display: flex; flex-direction: column; align-items: flex-start; justify-content: center; }}
.eyebrow {{ color: #507b68; font-size: 11px; font-weight: 800; letter-spacing: .16em; }}
h1 {{ max-width: 850px; margin: 16px 0; font-size: clamp(42px, 7vw, 78px); line-height: 1.03; letter-spacing: -.055em; }}
h2 {{ max-width: 700px; font-size: clamp(30px, 4vw, 48px); letter-spacing: -.04em; }}
.intro {{ max-width: 650px; color: #586773; font-size: 17px; line-height: 1.8; }}
.button {{ margin-top: 22px; padding: 14px 20px; border-radius: 6px; background: var(--accent); font-size: 13px; font-weight: 800; }}
.services {{ border-top: 1px solid #17212b18; }}
.service-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; margin-top: 34px; }}
.service-card {{ min-height: 150px; padding: 24px; border: 1px solid #17212b18; border-radius: 10px; background: white; }}
.service-card span {{ color: #789083; font-size: 11px; }}
.service-card h3 {{ margin-top: 28px; }}
.contact {{ border-top: 1px solid #17212b18; }}
.contact-link {{ display: inline-block; padding: 14px 18px; border-radius: 6px; background: var(--accent); font-weight: 750; }}
footer {{ border-top: 1px solid #17212b18; color: #718078; font-size: 11px; }}
@media (max-width: 600px) {{ .site-header, footer {{ padding: 20px; }} .hero, .services, .contact {{ padding: 70px 20px; }} }}
"""
    readme = f"""# {name} — Website starter

A responsive static one-page website generated with Solution Studio.

## Preview
Open index.html in a browser.

## Publish
Upload index.html and styles.css to any static host (GitHub Pages, Cloudflare Pages, Netlify or similar).

## Customize
Edit the business copy, service cards, contact email and accent color in index.html and styles.css. No build tools or paid APIs are required.
"""
    slug = re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-") or "business-site"
    archive = BytesIO()
    with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
        bundle.writestr("index.html", html)
        bundle.writestr("styles.css", css)
        bundle.writestr("README.md", readme)
    return f"{slug}-website.zip", archive.getvalue()
