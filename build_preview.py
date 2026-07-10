#!/usr/bin/env python3
"""Generate a static, self-contained HTML site from the wiki .md files.
Output goes to ./docs (GitHub Pages: Settings -> Pages -> main /docs).
Usage: python3 build_preview.py [REPO_DIR] [OUTPUT_DIR]"""
import os, re, sys, glob, html
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
    md_text = re.sub(r'<details(?![^>]*\bmarkdown=)([^>]*)>', r'<details markdown="1"\1>', md_text)
    html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc", "sane_lists", "md_in_html", "attr_list"],
        extension_configs={"toc": {"slugify": github_slug}},
    )
    # KEELETARK heading in blue, like the book
    html = re.sub(r'<h2( id="\d+-keeletark")>', r'<h2 class="keeletark"\1>', html)
    return html

def read(name):
    p = os.path.join(WIKI, name + ".md")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""

BOOKS = [  # (book title, [(file base, short label, full label), ...])
    ("E nagu Eesti", [
        ("Nagu-Eesti-01-Tere", "1 · Tere!", "1 · Tere!"),
        ("Nagu-Eesti-02-Maad-ja-keeled", "2 · Maad ja keeled", "2 · Maad ja keeled"),
        ("Nagu-Eesti-03-Kus-sa-elad", "3 · Kus sa elad?", "3 · Kus sa elad?"),
        ("Nagu-Eesti-04-Uks-ja-mitu", "4 · Üks ja mitu", "4 · Üks ja mitu"),
        ("Nagu-Eesti-05-Kuhu-sa-lahed", "5 · Kuhu sa lähed?", "5 · Kuhu sa lähed?"),
        ("Nagu-Eesti-05b-Kordamine-1-5", "Kordamine 1–5", "Kordamine 1–5"),
        ("Nagu-Eesti-06-Aastaajad", "6 · Aastaajad", "6 · Aastaajad"),
        ("Nagu-Eesti-07-Pere-ja-kodu", "7 · Pere ja kodu", "7 · Pere ja kodu"),
        ("Nagu-Eesti-08-Huvid-ja-hobid", "8 · Huvid ja hobid", "8 · Huvid ja hobid"),
        ("Nagu-Eesti-09-Hommikul-kodus", "9 · Hommikul kodus", "9 · Hommikul kodus"),
        ("Nagu-Eesti-10-Too-ja-haridus", "10 · Töö ja haridus", "10 · Töö ja haridus"),
        ("Nagu-Eesti-10b-Kordamine-6-10", "Kordamine 6–10", "Kordamine 6–10"),
        ("Nagu-Eesti-11-Lahme-poodi", "11 · Lähme poodi", "11 · Lähme poodi"),
        ("Nagu-Eesti-12-Kohvikus", "12 · Kohvikus", "12 · Kohvikus"),
        ("Nagu-Eesti-13-Üürime-korteri", "13 · Üürime korteri", "13 · Üürime korteri"),
        ("Nagu-Eesti-14-Uues-kodus", "14 · Uues kodus", "14 · Uues kodus"),
        ("Nagu-Eesti-15-Tulge-kulla", "15 · Tulge külla!", "15 · Tulge külla!"),
        ("Nagu-Eesti-16-Linnas", "16 · Linnas", "16 · Linnas"),
        ("Nagu-Eesti-17-Asju-ajamas", "17 · Asju ajamas", "17 · Asju ajamas"),
        ("Nagu-Eesti-18-Kaubamajas", "18 · Kaubamajas", "18 · Kaubamajas"),
    ]),
    ("Settle in Estonia", [
        ("Settle-01-Saame-tuttavaks", "1 · Saame tuttavaks!", "1 · Saame tuttavaks!"),
        ("Settle-02-Kuidas-palun", "2 · Kuidas palun?", "2 · Kuidas palun?"),
        ("Settle-03-Sinu-kodu", "3 · Sinu kodu", "3 · Missugune on sinu kodu?"),
        ("Settle-04-Kui-suur-on-uur", "4 · Kui suur on üür?", "4 · Kui suur on üür?"),
        ("Settle-05-Moobel-ja-kodumasinad", "5 · Mööbel ja kodumasinad", "5 · Mööbel ja kodumasinad"),
        ("Settle-06-Iseloom", "6 · Iseloom", "6 · Missugune sa oled?"),
        ("Settle-07-Perekond-ja-sugulased", "7 · Perekond ja sugulased", "7 · Perekond ja sugulased"),
        ("Settle-08-Palju-onne-tahtpaevad", "8 · Palju õnne! Tähtpäevad", "8 · Palju õnne! Tähtpäevad"),
        ("Settle-09-Valimus", "9 · Välimus", "9 · Välimus"),
        ("Settle-10-Pood-on-avatud", "10 · Pood on avatud", "10 · Pood on avatud kümnest kuueni"),
        ("Settle-11-Ilmateade", "11 · Ilmateade", "11 · Vihma ei saja. Ilmateade"),
        ("Settle-12-Minu-paev-ja-nadal", "12 · Minu päev ja nädal", "12 · Minu päev ja minu nädal"),
        ("Settle-13-Tule-mulle-kulla", "13 · Tule mulle külla!", "13 · Tule mulle külla!"),
        ("Settle-14-Kodused-tood", "14 · Kodused tööd", "14 · Mul on vaja nõusid pesta"),
        ("Settle-15-Riided-ja-jalanoud", "15 · Riided ja jalanõud", "15 · Riided ja jalanõud"),
        ("Settle-16-Riidepoes", "16 · Riidepoes", "16 · Kas ma võin proovida? Riidepoes"),
        ("Settle-17-Hobid", "17 · Hobid", "17 · Mulle meeldib joonistamine. Hobid"),
        ("Settle-18-Mida-sa-eile-tegid", "18 · Mida sa eile tegid?", "18 · Mida sa eile tegid?"),
        ("Settle-19-Soidan-rongiga", "19 · Sõidan rongiga", "19 · Sõidan rongiga Tallinnast Tartusse"),
        ("Settle-20-Ma-ei-koristanud", "20 · Ma ei koristanud", "20 · Ma ei koristanud eile tuba"),
        ("Settle-21-Vaata-seal-on-siil", "21 · Vaata, seal on siil!", "21 · Vaata, seal on siil!"),
        ("Settle-22-Uks-pilet-palun", "22 · Üks pilet palun!", "22 · Üks pilet palun! Kino, kontsert, koolitus"),
        ("Settle-23-Amet-ja-tookoht", "23 · Amet ja töökoht", "23 · Töötan restoranis kokana"),
        ("Settle-24-Curriculum-vitae", "24 · Curriculum vitae", "24 · Curriculum vitae"),
        ("Settle-25-Klaas-piima", "25 · Klaas piima", "25 · Klaas piima ja tükk kooki"),
        ("Settle-26-Mul-on-koik-korras", "26 · Mul on kõik korras!", "26 · Mul on kõik korras!"),
        ("Settle-27-Mis-sul-viga-on", "27 · Mis sul viga on?", "27 · Mis sul viga on?"),
        ("Settle-28-Mille-ule-te-kaebate", "28 · Mille üle te kaebate?", "28 · Mille üle te kaebate?"),
        ("Settle-29-Kui-ma-oleks", "29 · Kui ma oleks …", "29 · Kui ma oleks …"),
        ("Settle-30-Mida-tehakse", "30 · Mida tehakse talvel?", "30 · Mida tehakse talvel?"),
        ("Settle-31-Kordamine", "Kordamine", "Kordamine (Revision)"),
    ]),
]

def build_sidebar():
    p = ['<h3>Eesti keel · A2 Wiki</h3>',
         '<p><strong><a href="Home.html">\U0001f3e0 Home</a></strong></p>']
    for book_title, chapters in BOOKS:
        p.append(f'<p class="book"><strong>{html.escape(book_title)}</strong></p>')
        for fn, _, full in chapters:
            md = read(fn)
            heads = re.findall(r'^## (.+)$', md, flags=re.M)
            def lab(h): return html.escape(re.sub(r'^\d+\.\s*', '', h).strip())
            items = f'<li><a href="{fn}.html"><b>↗ Ava peatükk</b></a></li>'
            items += "".join(f'<li><a href="{fn}.html#{github_slug(h)}">{lab(h)}</a></li>' for h in heads)
            p.append(f'<details class="nav-chap" data-page="{fn}"><summary>{html.escape(full)}</summary><ul>{items}</ul></details>')
    p.append('<hr><p><a href="Publishing.html">How to publish</a></p>')
    return "".join(p)

sidebar_html = build_sidebar()
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
  --bg:#ffffff; --fg:#34495e; --muted:#7b8a9a; --line:#e3e6ea; --accent:#1a73e8;
  --code:#f3f4f6; --code-fg:#c7322d; --panel:#ffffff; --th-bg:#f5f6f7;
  --note-bg:#eaf3fb; --kt:#1565c0; --sidebar-bg:#fafbfc; --row:#ffffff;
}
:root[data-theme="dark"]{
  --bg:#0f1419; --fg:#e6e8eb; --muted:#9aa4ad; --line:#2a313a; --accent:#5aa2ff;
  --code:#161b22; --code-fg:#ff7b72; --panel:#161b22; --th-bg:#161b22;
  --note-bg:#122231; --kt:#79b8ff; --sidebar-bg:#0c1116; --row:#0f1419;
}
:root[data-theme="sepia"]{
  --bg:#f5f1e8; --fg:#3f3a31; --muted:#7a7060; --line:#e2d9c6; --accent:#9a6a3a;
  --code:#ece4d3; --code-fg:#b04a2f; --panel:#efe8d8; --th-bg:#ece4d3;
  --note-bg:#eef2e6; --kt:#2f6f9f; --sidebar-bg:#f1ebdc; --row:#f5f1e8;
}
*{box-sizing:border-box}
html,body{background:var(--bg)}
body{margin:0;color:var(--fg);letter-spacing:0;overflow-x:hidden;
  font-family:'Source Sans Pro','Helvetica Neue',Arial,sans-serif;
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
.layout{display:flex;max-width:1220px;margin:0 auto;align-items:flex-start}
.sidebar{position:sticky;top:0;flex:0 0 270px;height:100vh;overflow:auto;
  padding:20px 16px;border-right:1px solid var(--line);font-size:14px;background:var(--sidebar-bg)}
.sidebar h3{margin:.1em 0 .8em;font-size:16px;font-weight:700}
.sidebar p{margin:1.2em 0 .4em;font-weight:700;font-size:13.5px;color:var(--fg)}
.sidebar p.book{margin-top:1.4em;font-size:14px;color:var(--accent);border-bottom:2px solid var(--line);padding-bottom:4px}
.sidebar ul{list-style:none;padding-left:0;margin:.2em 0}
.sidebar li{margin:.12em 0;line-height:1.4}
.sidebar li a{color:var(--muted);display:block;padding:3px 8px;border-radius:6px}
.sidebar li a:hover{color:var(--accent);background:color-mix(in srgb,var(--accent) 9%,transparent);text-decoration:none}
.sidebar details.nav-chap{border:none;background:none;padding:0;margin:.15em 0}
.sidebar details.nav-chap>summary{list-style:none;cursor:pointer;font-weight:700;font-size:13.5px;
  color:var(--fg);padding:5px 8px;border-radius:6px;user-select:none}
.sidebar details.nav-chap>summary::-webkit-details-marker{display:none}
.sidebar details.nav-chap>summary::before{content:"\\25b8";display:inline-block;width:1em;margin-right:.2em;
  color:var(--muted);transition:transform .15s}
.sidebar details.nav-chap[open]>summary::before{transform:rotate(90deg)}
.sidebar details.nav-chap>summary:hover{background:color-mix(in srgb,var(--accent) 9%,transparent)}
.sidebar details.nav-chap>ul{margin:.1em 0 .5em .4em;border-left:1px solid var(--line);padding-left:.4em}
.sidebar hr{margin:1em 0}
.navsearch{width:100%;margin-bottom:12px;padding:7px 10px;border:1px solid var(--line);
  border-radius:8px;background:var(--bg);color:var(--fg);font-size:14px}
.navsearch:focus{outline:none;border-color:var(--accent)}
.content{flex:1;min-width:0;padding:36px 48px;max-width:880px}
.content p,.content figure{margin:1.2em 0}
.content ul,.content ol{line-height:1.6rem;word-spacing:.05rem}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
h1,h2,h3,h4{line-height:1.25;font-weight:700}
h1{font-size:2em;border-bottom:1px solid var(--line);padding-bottom:.3em;margin-bottom:.6em}
h2{font-size:1.5em;border-bottom:1px solid var(--line);padding-bottom:.3em;margin-top:1.8em}
h2.keeletark{color:var(--kt);border-bottom-color:var(--kt)}
h3{font-size:1.2em;margin-top:1.5em}
p,li{font-size:1rem}
table{border-collapse:collapse;width:100%;margin:1.1em 0;display:block;overflow:auto;font-size:.96em}
th,td{border:1px solid var(--line);padding:8px 14px;text-align:left;vertical-align:top}
th{background:var(--th-bg);font-weight:700}
td{background:var(--row)}
blockquote{margin:1.1em 0;padding:.7em 1em;color:var(--fg);background:var(--note-bg);
  border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:8px}
blockquote p{margin:.3em 0}
code{background:var(--code);color:var(--code-fg);padding:.12em .4em;border-radius:6px;
  font-size:.88em;font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace}
pre{background:var(--code);padding:14px;border-radius:8px;overflow:auto}
pre code{background:none;color:var(--fg);padding:0}
details{margin:1em 0;border:1px solid var(--line);border-radius:8px;padding:.5em 1em;background:var(--panel)}
summary{cursor:pointer;font-weight:600}
details.tr{background:var(--note-bg);border-style:dashed}
details.tr>summary{font-weight:600;font-size:.85em;color:var(--muted)}
details.tr>*:not(summary){font-size:.9em;font-style:italic;color:var(--muted)}
hr{border:0;border-top:1px solid var(--line);margin:2em 0}
.footer{margin-top:2.5em;padding-top:1em;border-top:1px solid var(--line);color:var(--muted);font-size:14px}
.themebar{position:fixed;top:10px;right:14px;display:flex;gap:4px;z-index:100}
.themebar button{font-size:15px;line-height:1;padding:6px 9px;border:1px solid var(--line);
  background:var(--panel);color:var(--fg);border-radius:8px;cursor:pointer}
.themebar button:hover{border-color:var(--accent)}
.themebar button.active{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent) inset}
@media(max-width:760px){.sidebar{display:none}.content{padding:20px 16px}}
"""

HEAD = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap" rel="stylesheet">
<script>
(function(){try{var t=localStorage.getItem('theme')||'light';document.documentElement.setAttribute('data-theme',t);}catch(e){}})();
function setTheme(t){document.documentElement.setAttribute('data-theme',t);try{localStorage.setItem('theme',t);}catch(e){}
 document.querySelectorAll('.themebar button').forEach(function(b){b.classList.toggle('active',b.dataset.t===t);});}
function filterNav(q){q=q.toLowerCase();document.querySelectorAll('.sidebar li').forEach(function(li){
 li.style.display=li.textContent.toLowerCase().indexOf(q)>=0?'':'none';});
 if(q){document.querySelectorAll('.sidebar details.nav-chap').forEach(function(d){d.open=true;});}}
document.addEventListener('DOMContentLoaded',function(){var t=document.documentElement.getAttribute('data-theme')||'light';
 document.querySelectorAll('.themebar button').forEach(function(b){b.classList.toggle('active',b.dataset.t===t);});
 var page=location.pathname.split('/').pop().replace('.html','');
 document.querySelectorAll('.sidebar details.nav-chap').forEach(function(d){if(d.dataset.page===page){d.open=true;}});});
</script>
"""

THEMEBAR = ('<div class="themebar">'
            '<button data-t="light" onclick="setTheme(\'light\')" title="Light">☀️</button>'
            '<button data-t="sepia" onclick="setTheme(\'sepia\')" title="Soft (eye-friendly)">\U0001f375</button>'
            '<button data-t="dark" onclick="setTheme(\'dark\')" title="Dark">\U0001f319</button>'
            '</div>')

TPL = """<!doctype html><html lang="et"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Nagu Eesti</title>{head}<style>{css}</style></head>
<body>{themebar}<div class="layout">
<nav class="sidebar"><input class="navsearch" placeholder="Filter sections…" oninput="filterNav(this.value)">{sidebar}</nav>
<main class="content">{body}<div class="footer">{footer}</div></main>
</div></body></html>"""

for f in md_files:
    name = os.path.splitext(os.path.basename(f))[0]
    if name in ("_Sidebar", "_Footer", "README"):
        continue
    body = fix_links(render(open(f, encoding="utf-8").read()))
    page = TPL.format(title=name.replace("-", " "), css=CSS, head=HEAD,
                      themebar=THEMEBAR, sidebar=fix_links(sidebar_html),
                      body=body, footer=fix_links(footer_html))
    open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8").write(page)
    if name == "Home":
        open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)

print("Built site in", OUT, ":", ", ".join(sorted(os.listdir(OUT))))
