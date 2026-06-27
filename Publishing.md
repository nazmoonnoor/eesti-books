# How to publish this as a GitHub Wiki

These `.md` files use **GitHub Wiki** conventions (a `Home.md` landing page, a `_Sidebar.md` for navigation, a `_Footer.md`, and `[[Page-Name]]`-style links). Here is how to get them online.

## Option A — GitHub Wiki (what we chose)

1. Create a repository on GitHub, e.g. `nagu-eesti`.
2. On the repo page, click the **Wiki** tab → **Create the first page** → Save (this initialises the wiki repo). 
3. Clone the wiki repo locally:
   ```bash
   git clone https://github.com/<your-username>/nagu-eesti.wiki.git
   ```
4. Copy every `.md` file from this `wiki/` folder into the cloned `nagu-eesti.wiki` folder.
5. Commit and push:
   ```bash
   cd nagu-eesti.wiki
   git add .
   git commit -m "Add Chapter 1"
   git push
   ```
6. Your wiki is live at `https://github.com/<your-username>/nagu-eesti/wiki`.

> Page file names map to URLs: `Chapter-01-Tere.md` → `.../wiki/Chapter-01-Tere`. Keep the hyphens.

## Option B — Also run it as a GitHub **Pages** site

GitHub Wiki and GitHub Pages are different things. If you later want a styled website with the same content, copy these files into a normal repo and enable **Settings → Pages**. The internal links (`Chapter-01-Tere`) work in both, and a light Jekyll theme can be added without changing the Markdown. Just ask and I'll set that up.

## Naming convention going forward

- One page per chapter: `Chapter-02-...`, `Chapter-03-...`, etc.
- Update `Home.md` (chapter table) and `_Sidebar.md` (nav) each time a chapter is added.
