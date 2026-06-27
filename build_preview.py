#!/usr/bin/env python3
"""Generate a static, self-contained HTML preview of the GitHub-wiki .md files.
No server needed: open preview/index.html in any browser."""
import os, re, sys, glob, html
import markdown

WIKI = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(WIKI, "preview")
os.makedirs(OUT, exist_ok=True)

def github_slug(value, sep='-'):
    value = value.strip().lower()
    value = re.sub(r'[^\w\s-]', '', value, flags=re.UNICODE)  # drop punctuation
    value = re.sub(r'\s', sep, value)                          # spaces -> hyphens (no collapse)
    return value

# pages = all .md except the special sidebar/footer partials
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
    # turn wiki links like href="Chapter-01-Tere" or "...#anchor" into ".html"
    def repl(m):
        href = m.group(1)
        if href.startswith(("http://", "https://", "#", "mailto:")):
            return m.group(0)
        base, _, anchor = href.partition("#")
        if base in page_names:
            base = base + ".html"
        elif base == "" and anchor:
            return m.group(0)  # pure in-page anchor
        new = base + (("#" + anchor) if anchor else "")
        return f'href="{new}"'
    return re.sub(r'href="([^"]+)"', repl, h)

CSS = """
:root{--fg:#1f2328;--muted:#59636e;--line:#d1d9e0;--accent:#0969da;--bg:#fff;--code:#f6f8fa;}
*{box-sizing:border-box}
body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;color:var(--fg);background:var(--bg)}
.layout{display:flex;max-width:1180px;margin:0 auto;align-items:flex-start}
.sidebar{position:sticky;top:0;flex:0 0 250px;height:100vh;overflow:auto;padding:24px 18px;border-right:1px solid var(--line);font-size:14px}
.sidebar ul{list-style:none;padding-left:12px;margin:6px 0}
.sidebar h3{margin:.2em 0}
.content{flex:1;min-width:0;padding:32px 40px;max-width:860px}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
h1,h2,h3{line-height:1.25}
h1{border-bottom:1px solid var(--line);padding-bottom:.3em}
h2{border-bottom:1px solid var(--line);padding-bottom:.3em;margin-top:1.6em}
table{border-collapse:collapse;width:100%;margin:1em 0;display:block;overflow:auto}
th,td{border:1px solid var(--line);padding:6px 13px}
th{background:var(--code)}
tr:nth-child(2n){background:#f6f8fa55}
blockquote{margin:1em 0;padding:.2em 1em;color:var(--muted);border-left:4px solid var(--line)}
code{background:var(--code);padding:.15em .4em;border-radius:6px;font-size:85%}
pre{background:var(--code);padding:14px;border-radius:8px;overflow:auto}
pre code{background:none;padding:0}
details{margin:1em 0;border:1px solid var(--line);border-radius:8px;padding:.4em 1em;background:#fbfdff}
summary{cursor:pointer;font-weight:600}
hr{border:0;border-top:1px solid var(--line);margin:2em 0}
.footer{margin-top:2em;padding-top:1em;border-top:1px solid var(--line);color:var(--muted);font-size:14px}
@media(max-width:760px){.sidebar{display:none}.content{padding:20px}}
"""

TPL = """<!doctype html><html lang="et"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Nagu Eesti</title><style>{css}</style></head>
<body><div class="layout">
<nav class="sidebar">{sidebar}</nav>
<main class="content">{body}<div class="footer">{footer}</div></main>
</div></body></html>"""

for f in md_files:
    name = os.path.splitext(os.path.basename(f))[0]
    if name in ("_Sidebar", "_Footer"):
        continue
    body = fix_links(render(open(f, encoding="utf-8").read()))
    page = TPL.format(title=name.replace("-", " "), css=CSS,
                      sidebar=fix_links(sidebar_html), body=body,
                      footer=fix_links(footer_html))
    open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8").write(page)
    if name == "Home":
        open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)

print("Built:", ", ".join(sorted(os.listdir(OUT))))
