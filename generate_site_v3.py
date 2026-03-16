from pathlib import Path
from html import escape
from datetime import date
import json
import itertools
import re

# =========================
# CONFIG
# =========================
SITE_NAME = "Can I Throw This Away?"
SITE_TAGLINE = "Disposal, recycling, donation, and hazardous waste guides"
GITHUB_USERNAME = "David80023216"
REPO_NAME = "can-i-throw-this-away"
ADSENSE_PUB_ID = "8618142757434912"
GSC_VERIFICATION = "PASTE_YOUR_GSC_VERIFICATION_CODE_HERE"

BASE_URL = f"https://{GITHUB_USERNAME.lower()}.github.io/{REPO_NAME}"
BASE_PATH = f"/{REPO_NAME}"
TODAY = str(date.today())

OUT = Path("site")
OUT.mkdir(exist_ok=True)

# =========================
# DATA
# =========================
CATEGORIES = {
    "batteries": {"name": "Batteries", "icon": "🔋", "intro": "Guides for alkaline, lithium, rechargeable, button, and car batteries."},
    "paint": {"name": "Paint", "icon": "🎨", "intro": "Guides for latex, oil-based, spray paint, and paint cans."},
    "electronics": {"name": "Electronics", "icon": "📺", "intro": "TVs, laptops, printers, chargers, phones, and accessories."},
    "light-bulbs": {"name": "Light Bulbs", "icon": "💡", "intro": "LED, CFL, fluorescent, and incandescent bulb guides."},
    "books-paper": {"name": "Books and Paper", "icon": "📚", "intro": "Books, paper, magazines, cardboard, and boxes."},
    "furniture": {"name": "Furniture", "icon": "🛋️", "intro": "Couches, mattresses, chairs, tables, and dressers."},
    "chemicals": {"name": "Chemicals", "icon": "🧪", "intro": "Cleaning products, bleach, gasoline, oil, and pesticides."},
    "appliances": {"name": "Appliances", "icon": "🧰", "intro": "Microwaves, blenders, toasters, refrigerators, and more."},
}

ITEMS = [
    {"name": "AA batteries", "category": "batteries", "answer": "Recycle when possible. Avoid loose disposal if damaged.", "alt": "battery recycling drop-off"},
    {"name": "AAA batteries", "category": "batteries", "answer": "Recycle when possible and separate damaged batteries.", "alt": "battery collection point"},
    {"name": "lithium batteries", "category": "batteries", "answer": "Do not throw damaged lithium batteries into normal trash.", "alt": "special battery recycler"},
    {"name": "button batteries", "category": "batteries", "answer": "Use a battery recycling option and keep them away from children.", "alt": "battery recycling site"},
    {"name": "car batteries", "category": "batteries", "answer": "Take them to an auto parts store or hazardous waste site.", "alt": "auto battery recycling"},

    {"name": "latex paint", "category": "paint", "answer": "If fully dried, some places allow trash; liquid paint often needs special handling.", "alt": "local paint collection"},
    {"name": "oil-based paint", "category": "paint", "answer": "Usually handle as hazardous waste.", "alt": "household hazardous waste"},
    {"name": "spray paint cans", "category": "paint", "answer": "Partially full cans often need special disposal.", "alt": "hazardous waste facility"},
    {"name": "paint cans", "category": "paint", "answer": "Rules depend on whether the can is empty, dried, or still contains liquid.", "alt": "local waste program"},

    {"name": "old televisions", "category": "electronics", "answer": "Use electronics recycling when available.", "alt": "electronics recycling site"},
    {"name": "laptops", "category": "electronics", "answer": "Wipe data first, then recycle or donate.", "alt": "electronics drop-off"},
    {"name": "printers", "category": "electronics", "answer": "Use electronics recycling if your area offers it.", "alt": "printer recycling"},
    {"name": "chargers", "category": "electronics", "answer": "Bundle cords and take them to electronics recycling.", "alt": "electronics collection"},
    {"name": "phones", "category": "electronics", "answer": "Erase personal data and use donation, trade-in, or recycling.", "alt": "phone recycling program"},

    {"name": "LED bulbs", "category": "light-bulbs", "answer": "Some places allow trash, but recycling is often encouraged.", "alt": "bulb recycling"},
    {"name": "CFL bulbs", "category": "light-bulbs", "answer": "Usually should not go in normal trash because of mercury.", "alt": "hazardous waste collection"},
    {"name": "fluorescent tubes", "category": "light-bulbs", "answer": "Handle carefully and use special recycling.", "alt": "lamp recycling"},
    {"name": "incandescent bulbs", "category": "light-bulbs", "answer": "Some places allow trash; wrap first to prevent breakage.", "alt": "safe bulb disposal"},

    {"name": "books", "category": "books-paper", "answer": "Donate or resell if usable; damaged books may need trash or mixed-paper handling.", "alt": "book donation"},
    {"name": "magazines", "category": "books-paper", "answer": "Often recyclable with mixed paper if clean and dry.", "alt": "paper recycling"},
    {"name": "cardboard boxes", "category": "books-paper", "answer": "Flatten and recycle if clean.", "alt": "cardboard recycling"},
    {"name": "pizza boxes", "category": "books-paper", "answer": "Greasy sections may belong in trash depending on local rules.", "alt": "compost or trash guidance"},
    {"name": "office paper", "category": "books-paper", "answer": "Recycle if clean and dry.", "alt": "paper recycling"},

    {"name": "couches", "category": "furniture", "answer": "Donation or bulk pickup may be better than normal trash.", "alt": "bulk waste pickup"},
    {"name": "mattresses", "category": "furniture", "answer": "Often require bulk waste or specialty disposal.", "alt": "mattress recycling"},
    {"name": "chairs", "category": "furniture", "answer": "Donate if usable; otherwise use bulk collection rules.", "alt": "furniture donation"},
    {"name": "dressers", "category": "furniture", "answer": "Donation or bulk disposal may apply.", "alt": "furniture collection"},
    {"name": "tables", "category": "furniture", "answer": "Donate, sell, or use bulk waste collection.", "alt": "bulk item pickup"},

    {"name": "bleach", "category": "chemicals", "answer": "Follow local chemical disposal guidance and never mix with other products.", "alt": "hazardous waste"},
    {"name": "cleaning chemicals", "category": "chemicals", "answer": "Use hazardous waste options where required.", "alt": "local chemical collection"},
    {"name": "motor oil", "category": "chemicals", "answer": "Never dump it; use auto service or recycling collection.", "alt": "used oil recycling"},
    {"name": "gasoline", "category": "chemicals", "answer": "Treat it as hazardous waste and keep it in approved containers.", "alt": "household hazardous waste"},
    {"name": "pesticides", "category": "chemicals", "answer": "Use hazardous waste disposal and follow the label instructions.", "alt": "special waste facility"},

    {"name": "microwaves", "category": "appliances", "answer": "Often better handled as appliance or electronics recycling.", "alt": "appliance recycler"},
    {"name": "toasters", "category": "appliances", "answer": "Small appliance recycling may be preferred over trash.", "alt": "small appliance drop-off"},
    {"name": "coffee makers", "category": "appliances", "answer": "Check small-appliance recycling or donation if still working.", "alt": "appliance collection"},
    {"name": "refrigerators", "category": "appliances", "answer": "Large appliances often need scheduled pickup or certified recycling.", "alt": "bulk appliance collection"},
    {"name": "blenders", "category": "appliances", "answer": "Recycle as a small appliance when possible, or donate if still works.", "alt": "small appliance recycling"},
]

STATES = [
    "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia",
    "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
    "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey",
    "New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
    "South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"
]

# =========================
# HELPERS
# =========================
all_paths = []

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")

def site_url(path: str) -> str:
    return f"{BASE_URL}/{path}" if path else BASE_URL + "/"

def site_href(path: str) -> str:
    return f"{BASE_PATH}/{path}" if path else BASE_PATH + "/"

def write(path: str, content: str):
    file_path = OUT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    all_paths.append(path)

def breadcrumbs(crumbs):
    links = " / ".join(
        f'<a href="{site_href(url)}">{escape(name)}</a>' if url else escape(name)
        for name, url in crumbs
    )
    return f'<div class="crumbs">{links}</div>'

def card(title, text, href, label="Guide"):
    return f"""
    <a class="card" href="{href}">
      <span class="badge">{escape(label)}</span>
      <h3>{escape(title)}</h3>
      <p>{escape(text)}</p>
    </a>
    """

def page(title, description, path, body, extra_head=""):
    canonical = site_url(path)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)} | {escape(SITE_NAME)}</title>
  <meta name="description" content="{escape(description)}" />
  <meta name="robots" content="index,follow" />
  <link rel="canonical" href="{canonical}" />
  <meta name="google-site-verification" content="{escape(GSC_VERIFICATION)}" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-{ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
  <link rel="stylesheet" href="{site_href('assets/styles.css')}" />
  {extra_head}
</head>
<body>
<header class="site-header">
  <div class="wrap nav">
    <a class="logo" href="{site_href('')}">CanIThrow<span>ThisAway?</span></a>
    <nav>
      <a href="{site_href('')}">Home</a>
      <a href="{site_href('category/index.html')}">Categories</a>
      <a href="{site_href('state/index.html')}">States</a>
      <a href="{site_href('item/index.html')}">All Items</a>
      <a href="{site_href('search.html')}">Search</a>
      <a href="{site_href('about.html')}">About</a>
    </nav>
  </div>
</header>

<main class="wrap">
{body}
</main>

<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <h3>{escape(SITE_NAME)}</h3>
      <p>{escape(SITE_TAGLINE)}</p>
    </div>
    <div>
      <h4>Explore</h4>
      <a href="{site_href('category/index.html')}">Categories</a>
      <a href="{site_href('state/index.html')}">States</a>
      <a href="{site_href('item/index.html')}">All Items</a>
      <a href="{site_href('search.html')}">Search</a>
    </div>
    <div>
      <h4>Pages</h4>
      <a href="{site_href('about.html')}">About</a>
      <a href="{site_href('privacy.html')}">Privacy</a>
      <a href="{site_href('terms.html')}">Terms</a>
      <a href="{site_href('contact.html')}">Contact</a>
    </div>
  </div>
  <div class="wrap copy">© {date.today().year} {escape(SITE_NAME)}. All rights reserved.</div>
</footer>
</body>
</html>
"""

# =========================
# STYLES / ASSETS
# =========================
styles = """
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#eef2f7;color:#0f172a}
a{text-decoration:none;color:inherit}.wrap{width:min(94%,1160px);margin:0 auto}
.site-header{background:#fff;border-bottom:1px solid #dbe3ee;position:sticky;top:0;z-index:10}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:72px}
.logo{font-size:1.55rem;font-weight:800}.logo span{color:#16a34a}
nav{display:flex;gap:18px;flex-wrap:wrap}nav a{font-weight:700;color:#475569}
.hero{padding:64px 0 28px}.hero h1{font-size:clamp(2rem,5vw,3.8rem);margin:0 0 14px}.hero p{color:#475569;max-width:780px}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}.btn{display:inline-block;padding:14px 18px;border-radius:14px;font-weight:800}
.btn-primary{background:#16a34a;color:#fff}.btn-secondary{background:#fff;border:1px solid #dbe3ee}
.crumbs{font-size:.95rem;color:#64748b;margin:26px 0 10px}
.section-title{font-size:clamp(1.6rem,3vw,2.5rem);margin:0 0 10px}.section-sub{color:#475569;margin:0 0 24px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:20px 0 34px}
.card{background:#fff;border:1px solid #dbe3ee;border-radius:20px;padding:20px;box-shadow:0 12px 30px rgba(15,23,42,.06)}
.card h3{margin:8px 0;font-size:1.3rem}.card p{margin:0;color:#475569;line-height:1.7}
.badge{display:inline-block;padding:7px 10px;border-radius:999px;background:#eaf7ee;color:#177245;font-weight:800;font-size:.82rem}
.panel{background:#fff;border:1px solid #dbe3ee;border-radius:20px;padding:24px;box-shadow:0 12px 30px rgba(15,23,42,.06);margin:20px 0}
.qa{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:16px;padding:18px;margin:18px 0}
.qa strong{display:block;margin-bottom:8px;color:#166534}
.two{display:grid;grid-template-columns:1.2fr .8fr;gap:20px}
.search-box{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}.search-box input{flex:1;min-width:220px;padding:14px;border-radius:14px;border:1px solid #dbe3ee}
.search-box button{padding:14px 18px;border:none;border-radius:14px;background:#0ea5e9;color:#fff;font-weight:800}
.site-footer{background:#071330;color:#fff;margin-top:36px;padding-top:28px}.footer-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:24px}
.footer-grid h3,.footer-grid h4{margin:0 0 12px}.footer-grid p,.footer-grid a{display:block;color:#cbd5e1;margin:6px 0}.copy{padding:16px 0;border-top:1px solid rgba(255,255,255,.08);color:#94a3b8;margin-top:18px}
@media(max-width:900px){.grid,.two,.footer-grid{grid-template-columns:1fr}.nav{padding:10px 0}}
"""
write("assets/styles.css", styles)

# =========================
# HOME
# =========================
cat_cards = []
for slug, c in CATEGORIES.items():
    cat_cards.append(card(c["name"], c["intro"], site_href(f"category/{slug}.html"), "Hub"))

home = f"""
<section class="hero">
  <div class="badge">Version 3 • GitHub-only build</div>
  <h1>Simple answers for what goes in the trash, recycling, donation, or hazardous waste.</h1>
  <p>{escape(SITE_TAGLINE)}. This version uses a clean GitHub Pages-safe folder structure, so links won’t break.</p>
  <div class="actions">
    <a class="btn btn-primary" href="{site_href('category/index.html')}">Browse Categories</a>
    <a class="btn btn-secondary" href="{site_href('item/index.html')}">Browse All Items</a>
  </div>
</section>

<h2 class="section-title">Category hubs</h2>
<p class="section-sub">Start with topic hubs, then go deeper into item and state pages.</p>
<div class="grid">
  {''.join(cat_cards)}
</div>
"""
write("index.html", page("Home", SITE_TAGLINE, "index.html", home))

# =========================
# CATEGORY INDEX + PAGES
# =========================
cat_index_cards = []
for slug, c in CATEGORIES.items():
    cat_index_cards.append(card(c["name"], c["intro"], site_href(f"category/{slug}.html"), "Category"))

body = f"""
{breadcrumbs([("Home",""),("Categories",None)])}
<h1 class="section-title">Categories</h1>
<p class="section-sub">Browse the main topic hubs.</p>
<div class="grid">{''.join(cat_index_cards)}</div>
"""
write("category/index.html", page("Categories", "Browse category hubs.", "category/index.html", body))

for slug, c in CATEGORIES.items():
    related = [x for x in ITEMS if x["category"] == slug]
    cards = "".join(card(i["name"].title(), i["answer"], site_href(f"item/{slugify(i['name'])}.html"), "Guide") for i in related)
    body = f"""
    {breadcrumbs([("Home",""),("Categories","category/index.html"),(c["name"],None)])}
    <h1 class="section-title">{escape(c['icon'])} {escape(c['name'])}</h1>
    <p class="section-sub">{escape(c['intro'])}</p>
    <div class="grid">{cards}</div>
    """
    write(f"category/{slug}.html", page(c["name"], c["intro"], f"category/{slug}.html", body))

# =========================
# ITEM INDEX + ITEM PAGES
# =========================
item_cards = "".join(card(i["name"].title(), i["answer"], site_href(f"item/{slugify(i['name'])}.html"), CATEGORIES[i["category"]]["name"]) for i in ITEMS)
body = f"""
{breadcrumbs([("Home",""),("All Items",None)])}
<h1 class="section-title">All Items</h1>
<p class="section-sub">Browse every item guide.</p>
<div class="grid">{item_cards}</div>
"""
write("item/index.html", page("All Items", "Browse all item guides.", "item/index.html", body))

for i in ITEMS:
    cat = CATEGORIES[i["category"]]
    state_links = "".join(
        f'<p><a href="{site_href(f"state/{slugify(s)}/{slugify(i["name"])}.html")}">{escape(i["name"]).title()} in {escape(s)}</a></p>'
        for s in STATES[:12]
    )
    body = f"""
    {breadcrumbs([("Home",""),("All Items","item/index.html"),(i["name"].title(),None)])}
    <div class="two">
      <section class="panel">
        <h1>{escape(i["name"]).title()}</h1>
        <p>{escape(cat["name"])} guide.</p>
        <div class="qa">
          <strong>Quick answer</strong>
          <p>{escape(i["answer"])}</p>
        </div>
        <p>The safer option is often <strong>{escape(i["alt"])}</strong> instead of assuming regular trash is correct.</p>
      </section>
      <aside class="panel">
        <h3>Popular state pages</h3>
        {state_links}
      </aside>
    </div>
    """
    write(f"item/{slugify(i['name'])}.html", page(i["name"].title(), i["answer"], f"item/{slugify(i['name'])}.html", body))

# =========================
# STATE INDEX + PAGES
# =========================
state_cards = "".join(card(s, f"Disposal and recycling guides for {s}.", site_href(f"state/{slugify(s)}.html"), "State") for s in STATES)
body = f"""
{breadcrumbs([("Home",""),("States",None)])}
<h1 class="section-title">States</h1>
<p class="section-sub">Browse state hubs and item-specific pages.</p>
<div class="grid">{state_cards}</div>
"""
write("state/index.html", page("States", "Browse all state hubs.", "state/index.html", body))

for s in STATES:
    links = "".join(
        f'<p><a href="{site_href(f"state/{slugify(s)}/{slugify(i["name"])}.html")}">{escape(i["name"]).title()} in {escape(s)}</a></p>'
        for i in ITEMS[:16]
    )
    body = f"""
    {breadcrumbs([("Home",""),("States","state/index.html"),(s,None)])}
    <div class="two">
      <section class="panel">
        <h1>{escape(s)} disposal and recycling guides</h1>
        <p>Use this page as a starting point for state-based disposal searches, then verify the final rule with the local waste authority.</p>
        {links}
      </section>
      <aside class="panel">
        <h3>Categories</h3>
        {''.join(f'<p><a href="{site_href(f"category/{slug}.html")}">{escape(c["name"])}</a></p>' for slug, c in CATEGORIES.items())}
      </aside>
    </div>
    """
    write(f"state/{slugify(s)}.html", page(f"{s} disposal guides", f"Disposal and recycling guides for {s}.", f"state/{slugify(s)}.html", body))

# =========================
# STATE + ITEM PAGES
# =========================
for s, i in itertools.product(STATES, ITEMS):
    body = f"""
    {breadcrumbs([("Home",""),("States","state/index.html"),(s,f"state/{slugify(s)}.html"),(i["name"].title(),None)])}
    <section class="panel">
      <h1>How to dispose of {escape(i["name"])} in {escape(s)}</h1>
      <div class="qa">
        <strong>Quick answer</strong>
        <p>{escape(i["answer"])}</p>
      </div>
      <p>Use <strong>{escape(i["alt"])}</strong> when available. Final rules can still vary by city or county inside {escape(s)}.</p>
      <p><a class="btn btn-secondary" href="{site_href(f"item/{slugify(i['name'])}.html")}">Open general {escape(i["name"]).title()} guide</a></p>
    </section>
    """
    write(f"state/{slugify(s)}/{slugify(i['name'])}.html",
          page(f"{i['name'].title()} in {s}",
               f"General guidance for disposing of {i['name']} in {s}.",
               f"state/{slugify(s)}/{slugify(i['name'])}.html",
               body))

# =========================
# SEARCH
# =========================
search_index = []
for i in ITEMS:
    search_index.append({
        "title": i["name"].title(),
        "url": site_href(f"item/{slugify(i['name'])}.html"),
        "text": f"{i['name']} {i['answer']} {CATEGORIES[i['category']]['name']}"
    })
for s in STATES:
    search_index.append({
        "title": f"{s} disposal guides",
        "url": site_href(f"state/{slugify(s)}.html"),
        "text": f"{s} state disposal recycling guides"
    })
write("search-index.json", json.dumps(search_index, indent=2))

search_js = f"""
<script>
async function boot() {{
  const res = await fetch('{site_href("search-index.json")}');
  const data = await res.json();
  const params = new URLSearchParams(location.search);
  const q = (params.get('q') || '').toLowerCase().trim();
  const input = document.getElementById('q');
  const out = document.getElementById('results');
  input.value = q;

  function run(term) {{
    const t = term.toLowerCase().trim();
    if (!t) {{
      out.innerHTML = '<div class="panel"><p>Type a search term above.</p></div>';
      return;
    }}
    const matches = data.filter(x => x.title.toLowerCase().includes(t) || x.text.toLowerCase().includes(t)).slice(0, 60);
    out.innerHTML = matches.map(x => `<a class="card" href="${{x.url}}"><h3>${{x.title}}</h3><p>${{x.text}}</p></a>`).join('');
  }}

  document.getElementById('searchForm').addEventListener('submit', (e) => {{
    e.preventDefault();
    const v = input.value.trim();
    history.replaceState(null, '', v ? '?q=' + encodeURIComponent(v) : '');
    run(v);
  }});

  run(q);
}}
boot();
</script>
"""
body = f"""
{breadcrumbs([("Home",""),("Search",None)])}
<h1 class="section-title">Search</h1>
<form class="search-box" id="searchForm">
  <input id="q" type="text" placeholder="Search batteries, paint, Alabama, books..." />
  <button type="submit">Search</button>
</form>
<div id="results" class="grid"></div>
{search_js}
"""
write("search.html", page("Search", "Search the site.", "search.html", body))

# =========================
# SIMPLE PAGES
# =========================
def simple(title, body_html, path):
    body = f"{breadcrumbs([('Home',''),(title,None)])}<section class='panel'><h1>{escape(title)}</h1>{body_html}</section>"
    write(path, page(title, f"{title} - {SITE_NAME}", path, body))

simple("About", f"<p>{escape(SITE_NAME)} is a utility-style SEO site focused on practical disposal questions.</p>", "about.html")
simple("Contact", "<p>Email: hello@example.com</p>", "contact.html")
simple("Privacy", "<p>This site may use cookies, analytics, and advertising services including Google AdSense.</p>", "privacy.html")
simple("Terms", "<p>Replace this with your final terms of use.</p>", "terms.html")

write("404.html", page("Page Not Found", "Page not found.", "404.html",
f"{breadcrumbs([('Home',''),('Page Not Found',None)])}<section class='panel'><h1>Page Not Found</h1><p>The page you requested could not be found.</p><p><a class='btn btn-primary' href='{site_href('')}'>Go Home</a></p></section>"))

# =========================
# SUPPORT FILES
# =========================
write("ads.txt", f"google.com, pub-{ADSENSE_PUB_ID}, DIRECT, f08c47fec0942fa0\n")
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
write(".nojekyll", "")

sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in all_paths:
    sitemap.append("  <url>")
    sitemap.append(f"    <loc>{site_url(p)}</loc>")
    sitemap.append(f"    <lastmod>{TODAY}</lastmod>")
    sitemap.append("  </url>")
sitemap.append("</urlset>")
write("sitemap.xml", "\n".join(sitemap))

print(f"Built {len(all_paths)} files into {OUT.resolve()}")
from pathlib import Path
from html import escape
from datetime import date
import json
import itertools
import re

# =========================
# CONFIG
# =========================
SITE_NAME = "Can I Throw This Away?"
SITE_TAGLINE = "Disposal, recycling, donation, and hazardous waste guides"
GITHUB_USERNAME = "David80023216"
REPO_NAME = "can-i-throw-this-away"
ADSENSE_PUB_ID = "8618142757434912"
GSC_VERIFICATION = "PASTE_YOUR_GSC_VERIFICATION_CODE_HERE"

BASE_URL = f"https://{GITHUB_USERNAME.lower()}.github.io/{REPO_NAME}"
BASE_PATH = f"/{REPO_NAME}"
TODAY = str(date.today())

OUT = Path("site")
OUT.mkdir(exist_ok=True)

# =========================
# DATA
# =========================
CATEGORIES = {
    "batteries": {"name": "Batteries", "icon": "🔋", "intro": "Guides for alkaline, lithium, rechargeable, button, and car batteries."},
    "paint": {"name": "Paint", "icon": "🎨", "intro": "Guides for latex, oil-based, spray paint, and paint cans."},
    "electronics": {"name": "Electronics", "icon": "📺", "intro": "TVs, laptops, printers, chargers, phones, and accessories."},
    "light-bulbs": {"name": "Light Bulbs", "icon": "💡", "intro": "LED, CFL, fluorescent, and incandescent bulb guides."},
    "books-paper": {"name": "Books and Paper", "icon": "📚", "intro": "Books, paper, magazines, cardboard, and boxes."},
    "furniture": {"name": "Furniture", "icon": "🛋️", "intro": "Couches, mattresses, chairs, tables, and dressers."},
    "chemicals": {"name": "Chemicals", "icon": "🧪", "intro": "Cleaning products, bleach, gasoline, oil, and pesticides."},
    "appliances": {"name": "Appliances", "icon": "🧰", "intro": "Microwaves, blenders, toasters, refrigerators, and more."},
}

ITEMS = [
    {"name": "AA batteries", "category": "batteries", "answer": "Recycle when possible. Avoid loose disposal if damaged.", "alt": "battery recycling drop-off"},
    {"name": "AAA batteries", "category": "batteries", "answer": "Recycle when possible and separate damaged batteries.", "alt": "battery collection point"},
    {"name": "lithium batteries", "category": "batteries", "answer": "Do not throw damaged lithium batteries into normal trash.", "alt": "special battery recycler"},
    {"name": "button batteries", "category": "batteries", "answer": "Use a battery recycling option and keep them away from children.", "alt": "battery recycling site"},
    {"name": "car batteries", "category": "batteries", "answer": "Take them to an auto parts store or hazardous waste site.", "alt": "auto battery recycling"},

    {"name": "latex paint", "category": "paint", "answer": "If fully dried, some places allow trash; liquid paint often needs special handling.", "alt": "local paint collection"},
    {"name": "oil-based paint", "category": "paint", "answer": "Usually handle as hazardous waste.", "alt": "household hazardous waste"},
    {"name": "spray paint cans", "category": "paint", "answer": "Partially full cans often need special disposal.", "alt": "hazardous waste facility"},
    {"name": "paint cans", "category": "paint", "answer": "Rules depend on whether the can is empty, dried, or still contains liquid.", "alt": "local waste program"},

    {"name": "old televisions", "category": "electronics", "answer": "Use electronics recycling when available.", "alt": "electronics recycling site"},
    {"name": "laptops", "category": "electronics", "answer": "Wipe data first, then recycle or donate.", "alt": "electronics drop-off"},
    {"name": "printers", "category": "electronics", "answer": "Use electronics recycling if your area offers it.", "alt": "printer recycling"},
    {"name": "chargers", "category": "electronics", "answer": "Bundle cords and take them to electronics recycling.", "alt": "electronics collection"},
    {"name": "phones", "category": "electronics", "answer": "Erase personal data and use donation, trade-in, or recycling.", "alt": "phone recycling program"},

    {"name": "LED bulbs", "category": "light-bulbs", "answer": "Some places allow trash, but recycling is often encouraged.", "alt": "bulb recycling"},
    {"name": "CFL bulbs", "category": "light-bulbs", "answer": "Usually should not go in normal trash because of mercury.", "alt": "hazardous waste collection"},
    {"name": "fluorescent tubes", "category": "light-bulbs", "answer": "Handle carefully and use special recycling.", "alt": "lamp recycling"},
    {"name": "incandescent bulbs", "category": "light-bulbs", "answer": "Some places allow trash; wrap first to prevent breakage.", "alt": "safe bulb disposal"},

    {"name": "books", "category": "books-paper", "answer": "Donate or resell if usable; damaged books may need trash or mixed-paper handling.", "alt": "book donation"},
    {"name": "magazines", "category": "books-paper", "answer": "Often recyclable with mixed paper if clean and dry.", "alt": "paper recycling"},
    {"name": "cardboard boxes", "category": "books-paper", "answer": "Flatten and recycle if clean.", "alt": "cardboard recycling"},
    {"name": "pizza boxes", "category": "books-paper", "answer": "Greasy sections may belong in trash depending on local rules.", "alt": "compost or trash guidance"},
    {"name": "office paper", "category": "books-paper", "answer": "Recycle if clean and dry.", "alt": "paper recycling"},

    {"name": "couches", "category": "furniture", "answer": "Donation or bulk pickup may be better than normal trash.", "alt": "bulk waste pickup"},
    {"name": "mattresses", "category": "furniture", "answer": "Often require bulk waste or specialty disposal.", "alt": "mattress recycling"},
    {"name": "chairs", "category": "furniture", "answer": "Donate if usable; otherwise use bulk collection rules.", "alt": "furniture donation"},
    {"name": "dressers", "category": "furniture", "answer": "Donation or bulk disposal may apply.", "alt": "furniture collection"},
    {"name": "tables", "category": "furniture", "answer": "Donate, sell, or use bulk waste collection.", "alt": "bulk item pickup"},

    {"name": "bleach", "category": "chemicals", "answer": "Follow local chemical disposal guidance and never mix with other products.", "alt": "hazardous waste"},
    {"name": "cleaning chemicals", "category": "chemicals", "answer": "Use hazardous waste options where required.", "alt": "local chemical collection"},
    {"name": "motor oil", "category": "chemicals", "answer": "Never dump it; use auto service or recycling collection.", "alt": "used oil recycling"},
    {"name": "gasoline", "category": "chemicals", "answer": "Treat it as hazardous waste and keep it in approved containers.", "alt": "household hazardous waste"},
    {"name": "pesticides", "category": "chemicals", "answer": "Use hazardous waste disposal and follow the label instructions.", "alt": "special waste facility"},

    {"name": "microwaves", "category": "appliances", "answer": "Often better handled as appliance or electronics recycling.", "alt": "appliance recycler"},
    {"name": "toasters", "category": "appliances", "answer": "Small appliance recycling may be preferred over trash.", "alt": "small appliance drop-off"},
    {"name": "coffee makers", "category": "appliances", "answer": "Check small-appliance recycling or donation if still working.", "alt": "appliance collection"},
    {"name": "refrigerators", "category": "appliances", "answer": "Large appliances often need scheduled pickup or certified recycling.", "alt": "bulk appliance collection"},
    {"name": "blenders", "category": "appliances", "answer": "Recycle as a small appliance when possible, or donate if still works.", "alt": "small appliance recycling"},
]

STATES = [
    "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia",
    "Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
    "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey",
    "New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina",
    "South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"
]

# =========================
# HELPERS
# =========================
all_paths = []

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")

def site_url(path: str) -> str:
    return f"{BASE_URL}/{path}" if path else BASE_URL + "/"

def site_href(path: str) -> str:
    return f"{BASE_PATH}/{path}" if path else BASE_PATH + "/"

def write(path: str, content: str):
    file_path = OUT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    all_paths.append(path)

def breadcrumbs(crumbs):
    links = " / ".join(
        f'<a href="{site_href(url)}">{escape(name)}</a>' if url else escape(name)
        for name, url in crumbs
    )
    return f'<div class="crumbs">{links}</div>'

def card(title, text, href, label="Guide"):
    return f"""
    <a class="card" href="{href}">
      <span class="badge">{escape(label)}</span>
      <h3>{escape(title)}</h3>
      <p>{escape(text)}</p>
    </a>
    """

def page(title, description, path, body, extra_head=""):
    canonical = site_url(path)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)} | {escape(SITE_NAME)}</title>
  <meta name="description" content="{escape(description)}" />
  <meta name="robots" content="index,follow" />
  <link rel="canonical" href="{canonical}" />
  <meta name="google-site-verification" content="{escape(GSC_VERIFICATION)}" />
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-{ADSENSE_PUB_ID}" crossorigin="anonymous"></script>
  <link rel="stylesheet" href="{site_href('assets/styles.css')}" />
  {extra_head}
</head>
<body>
<header class="site-header">
  <div class="wrap nav">
    <a class="logo" href="{site_href('')}">CanIThrow<span>ThisAway?</span></a>
    <nav>
      <a href="{site_href('')}">Home</a>
      <a href="{site_href('category/index.html')}">Categories</a>
      <a href="{site_href('state/index.html')}">States</a>
      <a href="{site_href('item/index.html')}">All Items</a>
      <a href="{site_href('search.html')}">Search</a>
      <a href="{site_href('about.html')}">About</a>
    </nav>
  </div>
</header>

<main class="wrap">
{body}
</main>

<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <h3>{escape(SITE_NAME)}</h3>
      <p>{escape(SITE_TAGLINE)}</p>
    </div>
    <div>
      <h4>Explore</h4>
      <a href="{site_href('category/index.html')}">Categories</a>
      <a href="{site_href('state/index.html')}">States</a>
      <a href="{site_href('item/index.html')}">All Items</a>
      <a href="{site_href('search.html')}">Search</a>
    </div>
    <div>
      <h4>Pages</h4>
      <a href="{site_href('about.html')}">About</a>
      <a href="{site_href('privacy.html')}">Privacy</a>
      <a href="{site_href('terms.html')}">Terms</a>
      <a href="{site_href('contact.html')}">Contact</a>
    </div>
  </div>
  <div class="wrap copy">© {date.today().year} {escape(SITE_NAME)}. All rights reserved.</div>
</footer>
</body>
</html>
"""

# =========================
# STYLES / ASSETS
# =========================
styles = """
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#eef2f7;color:#0f172a}
a{text-decoration:none;color:inherit}.wrap{width:min(94%,1160px);margin:0 auto}
.site-header{background:#fff;border-bottom:1px solid #dbe3ee;position:sticky;top:0;z-index:10}
.nav{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:72px}
.logo{font-size:1.55rem;font-weight:800}.logo span{color:#16a34a}
nav{display:flex;gap:18px;flex-wrap:wrap}nav a{font-weight:700;color:#475569}
.hero{padding:64px 0 28px}.hero h1{font-size:clamp(2rem,5vw,3.8rem);margin:0 0 14px}.hero p{color:#475569;max-width:780px}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:18px}.btn{display:inline-block;padding:14px 18px;border-radius:14px;font-weight:800}
.btn-primary{background:#16a34a;color:#fff}.btn-secondary{background:#fff;border:1px solid #dbe3ee}
.crumbs{font-size:.95rem;color:#64748b;margin:26px 0 10px}
.section-title{font-size:clamp(1.6rem,3vw,2.5rem);margin:0 0 10px}.section-sub{color:#475569;margin:0 0 24px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin:20px 0 34px}
.card{background:#fff;border:1px solid #dbe3ee;border-radius:20px;padding:20px;box-shadow:0 12px 30px rgba(15,23,42,.06)}
.card h3{margin:8px 0;font-size:1.3rem}.card p{margin:0;color:#475569;line-height:1.7}
.badge{display:inline-block;padding:7px 10px;border-radius:999px;background:#eaf7ee;color:#177245;font-weight:800;font-size:.82rem}
.panel{background:#fff;border:1px solid #dbe3ee;border-radius:20px;padding:24px;box-shadow:0 12px 30px rgba(15,23,42,.06);margin:20px 0}
.qa{background:#f0fdf4;border:1px solid #bbf7d0;border-radius:16px;padding:18px;margin:18px 0}
.qa strong{display:block;margin-bottom:8px;color:#166534}
.two{display:grid;grid-template-columns:1.2fr .8fr;gap:20px}
.search-box{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}.search-box input{flex:1;min-width:220px;padding:14px;border-radius:14px;border:1px solid #dbe3ee}
.search-box button{padding:14px 18px;border:none;border-radius:14px;background:#0ea5e9;color:#fff;font-weight:800}
.site-footer{background:#071330;color:#fff;margin-top:36px;padding-top:28px}.footer-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:24px}
.footer-grid h3,.footer-grid h4{margin:0 0 12px}.footer-grid p,.footer-grid a{display:block;color:#cbd5e1;margin:6px 0}.copy{padding:16px 0;border-top:1px solid rgba(255,255,255,.08);color:#94a3b8;margin-top:18px}
@media(max-width:900px){.grid,.two,.footer-grid{grid-template-columns:1fr}.nav{padding:10px 0}}
"""
write("assets/styles.css", styles)

# =========================
# HOME
# =========================
cat_cards = []
for slug, c in CATEGORIES.items():
    cat_cards.append(card(c["name"], c["intro"], site_href(f"category/{slug}.html"), "Hub"))

home = f"""
<section class="hero">
  <div class="badge">Version 3 • GitHub-only build</div>
  <h1>Simple answers for what goes in the trash, recycling, donation, or hazardous waste.</h1>
  <p>{escape(SITE_TAGLINE)}. This version uses a clean GitHub Pages-safe folder structure, so links won’t break.</p>
  <div class="actions">
    <a class="btn btn-primary" href="{site_href('category/index.html')}">Browse Categories</a>
    <a class="btn btn-secondary" href="{site_href('item/index.html')}">Browse All Items</a>
  </div>
</section>

<h2 class="section-title">Category hubs</h2>
<p class="section-sub">Start with topic hubs, then go deeper into item and state pages.</p>
<div class="grid">
  {''.join(cat_cards)}
</div>
"""
write("index.html", page("Home", SITE_TAGLINE, "index.html", home))

# =========================
# CATEGORY INDEX + PAGES
# =========================
cat_index_cards = []
for slug, c in CATEGORIES.items():
    cat_index_cards.append(card(c["name"], c["intro"], site_href(f"category/{slug}.html"), "Category"))

body = f"""
{breadcrumbs([("Home",""),("Categories",None)])}
<h1 class="section-title">Categories</h1>
<p class="section-sub">Browse the main topic hubs.</p>
<div class="grid">{''.join(cat_index_cards)}</div>
"""
write("category/index.html", page("Categories", "Browse category hubs.", "category/index.html", body))

for slug, c in CATEGORIES.items():
    related = [x for x in ITEMS if x["category"] == slug]
    cards = "".join(card(i["name"].title(), i["answer"], site_href(f"item/{slugify(i['name'])}.html"), "Guide") for i in related)
    body = f"""
    {breadcrumbs([("Home",""),("Categories","category/index.html"),(c["name"],None)])}
    <h1 class="section-title">{escape(c['icon'])} {escape(c['name'])}</h1>
    <p class="section-sub">{escape(c['intro'])}</p>
    <div class="grid">{cards}</div>
    """
    write(f"category/{slug}.html", page(c["name"], c["intro"], f"category/{slug}.html", body))

# =========================
# ITEM INDEX + ITEM PAGES
# =========================
item_cards = "".join(card(i["name"].title(), i["answer"], site_href(f"item/{slugify(i['name'])}.html"), CATEGORIES[i["category"]]["name"]) for i in ITEMS)
body = f"""
{breadcrumbs([("Home",""),("All Items",None)])}
<h1 class="section-title">All Items</h1>
<p class="section-sub">Browse every item guide.</p>
<div class="grid">{item_cards}</div>
"""
write("item/index.html", page("All Items", "Browse all item guides.", "item/index.html", body))

for i in ITEMS:
    cat = CATEGORIES[i["category"]]
    state_links = "".join(
        f'<p><a href="{site_href(f"state/{slugify(s)}/{slugify(i["name"])}.html")}">{escape(i["name"]).title()} in {escape(s)}</a></p>'
        for s in STATES[:12]
    )
    body = f"""
    {breadcrumbs([("Home",""),("All Items","item/index.html"),(i["name"].title(),None)])}
    <div class="two">
      <section class="panel">
        <h1>{escape(i["name"]).title()}</h1>
        <p>{escape(cat["name"])} guide.</p>
        <div class="qa">
          <strong>Quick answer</strong>
          <p>{escape(i["answer"])}</p>
        </div>
        <p>The safer option is often <strong>{escape(i["alt"])}</strong> instead of assuming regular trash is correct.</p>
      </section>
      <aside class="panel">
        <h3>Popular state pages</h3>
        {state_links}
      </aside>
    </div>
    """
    write(f"item/{slugify(i['name'])}.html", page(i["name"].title(), i["answer"], f"item/{slugify(i['name'])}.html", body))

# =========================
# STATE INDEX + PAGES
# =========================
state_cards = "".join(card(s, f"Disposal and recycling guides for {s}.", site_href(f"state/{slugify(s)}.html"), "State") for s in STATES)
body = f"""
{breadcrumbs([("Home",""),("States",None)])}
<h1 class="section-title">States</h1>
<p class="section-sub">Browse state hubs and item-specific pages.</p>
<div class="grid">{state_cards}</div>
"""
write("state/index.html", page("States", "Browse all state hubs.", "state/index.html", body))

for s in STATES:
    links = "".join(
        f'<p><a href="{site_href(f"state/{slugify(s)}/{slugify(i["name"])}.html")}">{escape(i["name"]).title()} in {escape(s)}</a></p>'
        for i in ITEMS[:16]
    )
    body = f"""
    {breadcrumbs([("Home",""),("States","state/index.html"),(s,None)])}
    <div class="two">
      <section class="panel">
        <h1>{escape(s)} disposal and recycling guides</h1>
        <p>Use this page as a starting point for state-based disposal searches, then verify the final rule with the local waste authority.</p>
        {links}
      </section>
      <aside class="panel">
        <h3>Categories</h3>
        {''.join(f'<p><a href="{site_href(f"category/{slug}.html")}">{escape(c["name"])}</a></p>' for slug, c in CATEGORIES.items())}
      </aside>
    </div>
    """
    write(f"state/{slugify(s)}.html", page(f"{s} disposal guides", f"Disposal and recycling guides for {s}.", f"state/{slugify(s)}.html", body))

# =========================
# STATE + ITEM PAGES
# =========================
for s, i in itertools.product(STATES, ITEMS):
    body = f"""
    {breadcrumbs([("Home",""),("States","state/index.html"),(s,f"state/{slugify(s)}.html"),(i["name"].title(),None)])}
    <section class="panel">
      <h1>How to dispose of {escape(i["name"])} in {escape(s)}</h1>
      <div class="qa">
        <strong>Quick answer</strong>
        <p>{escape(i["answer"])}</p>
      </div>
      <p>Use <strong>{escape(i["alt"])}</strong> when available. Final rules can still vary by city or county inside {escape(s)}.</p>
      <p><a class="btn btn-secondary" href="{site_href(f"item/{slugify(i['name'])}.html")}">Open general {escape(i["name"]).title()} guide</a></p>
    </section>
    """
    write(f"state/{slugify(s)}/{slugify(i['name'])}.html",
          page(f"{i['name'].title()} in {s}",
               f"General guidance for disposing of {i['name']} in {s}.",
               f"state/{slugify(s)}/{slugify(i['name'])}.html",
               body))

# =========================
# SEARCH
# =========================
search_index = []
for i in ITEMS:
    search_index.append({
        "title": i["name"].title(),
        "url": site_href(f"item/{slugify(i['name'])}.html"),
        "text": f"{i['name']} {i['answer']} {CATEGORIES[i['category']]['name']}"
    })
for s in STATES:
    search_index.append({
        "title": f"{s} disposal guides",
        "url": site_href(f"state/{slugify(s)}.html"),
        "text": f"{s} state disposal recycling guides"
    })
write("search-index.json", json.dumps(search_index, indent=2))

search_js = f"""
<script>
async function boot() {{
  const res = await fetch('{site_href("search-index.json")}');
  const data = await res.json();
  const params = new URLSearchParams(location.search);
  const q = (params.get('q') || '').toLowerCase().trim();
  const input = document.getElementById('q');
  const out = document.getElementById('results');
  input.value = q;

  function run(term) {{
    const t = term.toLowerCase().trim();
    if (!t) {{
      out.innerHTML = '<div class="panel"><p>Type a search term above.</p></div>';
      return;
    }}
    const matches = data.filter(x => x.title.toLowerCase().includes(t) || x.text.toLowerCase().includes(t)).slice(0, 60);
    out.innerHTML = matches.map(x => `<a class="card" href="${{x.url}}"><h3>${{x.title}}</h3><p>${{x.text}}</p></a>`).join('');
  }}

  document.getElementById('searchForm').addEventListener('submit', (e) => {{
    e.preventDefault();
    const v = input.value.trim();
    history.replaceState(null, '', v ? '?q=' + encodeURIComponent(v) : '');
    run(v);
  }});

  run(q);
}}
boot();
</script>
"""
body = f"""
{breadcrumbs([("Home",""),("Search",None)])}
<h1 class="section-title">Search</h1>
<form class="search-box" id="searchForm">
  <input id="q" type="text" placeholder="Search batteries, paint, Alabama, books..." />
  <button type="submit">Search</button>
</form>
<div id="results" class="grid"></div>
{search_js}
"""
write("search.html", page("Search", "Search the site.", "search.html", body))

# =========================
# SIMPLE PAGES
# =========================
def simple(title, body_html, path):
    body = f"{breadcrumbs([('Home',''),(title,None)])}<section class='panel'><h1>{escape(title)}</h1>{body_html}</section>"
    write(path, page(title, f"{title} - {SITE_NAME}", path, body))

simple("About", f"<p>{escape(SITE_NAME)} is a utility-style SEO site focused on practical disposal questions.</p>", "about.html")
simple("Contact", "<p>Email: hello@example.com</p>", "contact.html")
simple("Privacy", "<p>This site may use cookies, analytics, and advertising services including Google AdSense.</p>", "privacy.html")
simple("Terms", "<p>Replace this with your final terms of use.</p>", "terms.html")

write("404.html", page("Page Not Found", "Page not found.", "404.html",
f"{breadcrumbs([('Home',''),('Page Not Found',None)])}<section class='panel'><h1>Page Not Found</h1><p>The page you requested could not be found.</p><p><a class='btn btn-primary' href='{site_href('')}'>Go Home</a></p></section>"))

# =========================
# SUPPORT FILES
# =========================
write("ads.txt", f"google.com, pub-{ADSENSE_PUB_ID}, DIRECT, f08c47fec0942fa0\n")
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")
write(".nojekyll", "")

sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in all_paths:
    sitemap.append("  <url>")
    sitemap.append(f"    <loc>{site_url(p)}</loc>")
    sitemap.append(f"    <lastmod>{TODAY}</lastmod>")
    sitemap.append("  </url>")
sitemap.append("</urlset>")
write("sitemap.xml", "\n".join(sitemap))

print(f"Built {len(all_paths)} files into {OUT.resolve()}")
