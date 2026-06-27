#!/usr/bin/env python3
"""Generate a static, self-contained HTML site from the wiki .md files.
Output goes to ./docs (GitHub Pages: Settings -> Pages -> main /docs).
Usage: python3 build_preview.py [REPO_DIR] [OUTPUT_DIR]
No server needed: open docs/index.html in any browser."""
import os, re, sys, glob
import markdown

WIKI = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(WIKI, sys.argv[2] if len(sys.argv) > 2 else "docs")
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, ".nojekyll"), "w").close()

def github_slug(value, sep='-'):
    value = value.strip().lower()
    value = re.sub(r'[^\w\s-]', '', value, flags=re.UNICODE)
    value = re.sub(r'\s', sep, value)
    return value

md_files = [f for f in glob.glob(os.path.join(WIKI, "*.md"))]
page_names = {os.path.splitext(os.path.basename(f))[0] for f in md_files}

def render(md_text):
    md_text = md_text.replace("<details>", '<details markdown="1">')
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "sane_lists", "md_in_html", "attr_list"],
        extension_configs={"toc": {"slugify": github_slug}},
    )

def read(name):
    p = os.path.join(WIKI, name + ".md")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

sidebar_html = render(read("_Sidebar")) if read("_Sidebar") else ""
footer_html = render(read("_Footer")) if read("_Footer") else ""

def fix_links(h):
    def repl(m):
        href = m.group(1)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        base, _, anchor = href.partition("#")
        if base.endswith(".md"):
            base = base[:-3]
        if base in page_names:
            base = base + ".html"
        elif base == "" and anchor:
            return m.group(0)
        new = base + (("#" + anchor) if anchor else "")
        return f'href="{new}"'
    return re.sub(r'href="([^"]+)"', repl, h)

CSS = """
:root{
  --bg:#ffffff; --fg:#1f2328; --muted:#59636e; --line:#d1d9e0; --accent:#0969da;
  --code:#f6f8fa; --panel:#fbfdff; --stripe:#f6f8fa; --sidebar-bg:#ffffff;
}
:root[data-theme="dark"]{
  --bg:#0d1117; --fg:#e6edf3; --muted:#9198a1; --line:#30363d; --accent:#4493f8;
  --code:#161b22; --panel:#161b22; --stripe:#12161d; --sidebar-bg:#0d1117;
}
:root[data-theme="sepia"]{
  --bg:#f4ecd8; --fg:#5b4636; --muted:#7d6b58; --line:#ddcdb0; --accent:#9a6a3a;
  --code:#ece0c8; --panel:#efe6d0; --stripe:#efe6cf; --sidebar-bg:#f1e7cf;
}
*{box-sizing:border-box}
html,body{background:var(--bg)}
body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;color:var(--fg)}
.layout{display:flex;max-width:1180px;margin:0 auto;align-items:flex-start}
.sidebar{position:sticky;top:0;flex:0 0 250px;height:100vh;overflow:auto;padding:24px 18px;border-right:1px solid var(--line);font-size:14px;background:var(--sidebar-bg)}
.sidebar h3{margin:.2em 0 .6em}
.sidebar p{margin:1.1em 0 .3em;font-size:13px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}
.sidebar p strong{color:var(--muted)}
.sidebar ul{list-style:none;padding-left:0;margin:.2em 0}
.sidebar li{margin:.28em 0;line-height:1.35}
.content{flex:1;min-width:0;padding:32px 40px;max-width:860px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
h1,h2,h3{line-height:1.25}
h1{border-bottom:1px solid var(--line);padding-bottom:.3em}
h2{border-bottom:1px solid var(--line);padding-bottom:.3em;margin-top:1.6em}
table{border-collapse:collapse;width:100%;margin:1em 0;display:block;overflow:auto}
th,td{border:1px solid var(--line);padding:6px 13px}
th{background:var(--code)}
tr:nth-child(2n){background:var(--stripe)}
blockquote{margin:1em 0;padding:.2em 1em;color:var(--muted);border-left:4px solid var(--line)}
code{background:var(--code);padding:.15em .4em;border-radius:6px;font-size:85%}
pre{background:var(--code);padding:14px;border-radius:8px;overflow:auto}
pre code{background:none;padding:0}
details{margin:1em 0;border:1px solid var(--line);border-radius:8px;padding:.4em 1em;background:var(--panel)}
summary{cursor:pointer;font-weight:600}
hr{border:0;border-top:1px solid var(--line);margin:2em 0}
.footer{margin-top:2em;padding-top:1em;border-top:1px solid var(--line);color:var(--muted);font-size:14px}
.themebar{position:fixed;top:10px;right:14px;display:flex;gap:4px;z-index:100}
.themebar button{font-size:15px;line-height:1;padding:6px 9px;border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:8px;cursor:pointer}
.themebar button:hover{border-color:var(--accent)}
.themebar button.active{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent) inset}
@media(max-width:760px){.sidebar{display:none}.content{padding:20px 16px}}
"""

HEAD_JS = """
<script>
(function(){try{var t=localStorage.getItem('theme')||'light';document.documentElement.setAttribute('data-theme',t);}catch(e){}})();
function setTheme(t){document.documentElement.setAttribute('data-theme',t);try{localStorage.setItem('theme',t);}catch(e){}
 document.querySelectorAll('.themebar button').forEach(function(b){b.classList.toggle('active',b.dataset.t===t);});}
document.addEventListener('DOMContentLoaded',function(){var t=document.documentElement.getAttribute('data-theme')||'light';
 document.querySelectorAll('.themebar button').forEach(function(b){b.classList.toggle('active',b.dataset.t===t);});});
</script>
"""

THEMEBAR = ('<div class="themebar">'
            '<button data-t="light" onclick="setTheme(\'light\')" title="Light">☀️</button>'
            '<button data-t="sepia" onclick="setTheme(\'sepia\')" title="Soft (eye-friendly)">\U0001f375</button>'
            '<button data-t="dark" onclick="setTheme(\'dark\')" title="Dark">\U0001f319</button>'
            '</div>')

TPL = """<!doctype html><html lang="et"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Nagu Eesti</title><style>{css}</style>{headjs}</head>
<body>{themebar}<div class="layout">
<nav class="sidebar">{sidebar}</nav>
<main class="content">{body}<div class="footer">{footer}</div></main>
</div></body></html>"""

for f in md_files:
    name = os.path.splitext(os.path.basename(f))[0]
    if name in ("_Sidebar", "_Footer", "README"):
        continue
    body = fix_links(render(open(f, encoding="utf-8").read()))
    page = TPL.format(title=name.replace("-", " "), css=CSS, headjs=HEAD_JS,
                      themebar=THEMEBAR, sidebar=fix_links(sidebar_html),
                      body=body, footer=fix_links(footer_html))
    open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8").write(page)
    if name == "Home":
        open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)

print("Built site in", OUT, ":", ", ".join(sorted(os.listdir(OUT))))
