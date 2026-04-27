# Project Handoff: seanlgirgis.github.io

## Executive Summary
This repository contains the source code and content for the professional portfolio and technical blog of **Sean Luka Girgis**. It is a **Serverless Single-Page Application (SPA)** built with a custom **Python-based Static Site Generator (SSG)**. The architecture prioritizes a decoupled, data-driven approach — professional content (Resume/CV) is maintained in a single source of truth (`data/store.yaml`) and rendered into multiple formats (HTML, PDF, DOCX, Markdown). The site is live at **https://seanlgirgis.github.io**.

---

## Quick Commands (Most Common Operations)

```powershell
# Activate environment
. .\env_setter.ps1                                      # venv: C:\py_venv\resume_venv

# Add/refresh a blog post or LeetCode entry (most frequent task)
.\run_blog_refresh.ps1                                  # build_blog.py + gitq (auto-push)

# Regenerate all resume/CV formats after editing data/store.yaml
python generate.py --target all --format all

# Generate a new Learning Hub page (follow AGENTS.md rules)
# Write to: learning/{slug}.html using learning/_page-template.html

# Update sitemap after adding pages
python generate_sitemap.py

# Push to deploy (GitHub Pages — goes live on push)
git add -A && git commit -m "..." && git push
```

---

## Repository Architecture

### 1. The Decentralized Engine
Layout and content are fully separated:
- **Source Data**: `data/store.yaml` — single source of truth for all professional content (experience, skills, projects)
- **Layout Configs**: YAML files in `data/` (e.g., `resume_pdf.yaml`, `cv_docx.yaml`) define section selection and ordering
- **Renderers**: `renderers/` — Python modules for each output format (HTML, PDF, DOCX, Markdown)

### 2. Core Scripts

| Script | Role |
|--------|------|
| `generate.py` | Primary orchestrator — Resume and CV generation across all targets and formats |
| `build_blog.py` | Blog pipeline — converts `data/blog/*.md` → HTML pages, LeetCode Hub, RSS feed |
| `main.py` | Specialized DOCX generation with header stripes and complex layout |
| `generate_sitemap.py` | Regenerates `sitemap.xml` after new pages are added |
| `run_blog_refresh.ps1` | Convenience wrapper: activates env → `build_blog.py` → `gitq` (push) |
| `debug_config.py` | Debug utility for inspecting site config and render paths |
| `fix_template.py` | One-off template repair utility |

### 3. Frontend (SPA)

| File/Dir | Role |
|----------|------|
| `index.html` | Main shell — single entry point for the entire site |
| `assets/js/router.js` | Hash-based router — fetches and injects `components/` fragments into `#content-area` |
| `components/` | Generated HTML fragments loaded by the router (resume, projects, blog lists, etc.) |
| `pages/` | Additional standalone page content |
| `assets/` | Static assets — CSS, JS, images |

### 4. Learning Hub (`learning/`)
~50 standalone HTML pages for **Senior Data Engineer interview preparation**. Each page covers one AWS service or data technology with:
- 8–10 production-oriented content sections
- 6 Q&A pairs (interview-focused)
- 10–16 row quick reference cheat sheet
- Audio box

Pages are hand-generated following the strict rules in `AGENTS.md`. The template is `learning/_page-template.html` — **do not modify its CSS or class names**.

Current pages include: `aws-s3`, `aws-glue`, `aws-athena`, `aws-redshift`, `aws-kinesis`, `aws-lambda`, `aws-dynamodb`, `apache-kafka`, `apache-flink`, `apache-airflow`, and ~40 more.

---

## Environment & Setup

### Python Environment
- **Venv**: `C:\py_venv\resume_venv`
- **Activate**: `. .\env_setter.ps1`
- **Dependencies** (`requirements.txt`): `jinja2`, `markdown`, `python-docx`, `pyyaml`, `pdfkit`

### External Dependency — wkhtmltopdf
`pdfkit` is a wrapper around `wkhtmltopdf`. PDF generation **will fail** without it installed.
- Download: https://wkhtmltopdf.org/downloads.html
- Must be on system PATH, or configure path in `generate.py`

### gitq Alias
`run_blog_refresh.ps1` calls `gitq` — a custom git alias for quick add/commit/push. If `gitq` is not defined in your shell profile, either add it or replace with a standard `git add -A && git commit -m "..." && git push`.

### Deployment
Hosted on **GitHub Pages**. Deployment = push to `main`. No build step — all generated files are committed to the repo. Goes live within ~60 seconds of push.

---

## Site Sections

| Section | URL hash | Description |
|---------|----------|-------------|
| Home (Resume) | `#resume` | Targeted Data Engineering + AI Architecture resume |
| Detailed CV | `#cv` | Full career history from `store.yaml` |
| Projects | `#projects` | Flagship AI and Data Engineering projects |
| Blog | `#blog` | Technical deep dives — ML, Data Engineering, Architecture |
| LeetCode Hub | `#leetcode` | Categorized algorithmic solutions with difficulty/topic tagging |
| Learning Hub | `/learning/` | ~50 senior DE interview-prep pages |

---

## Maintenance Workflows

### Update Resume/CV
1. Edit `data/store.yaml`
2. `python generate.py --target all --format all`
3. Verify locally: open `index.html`
4. `git add -A && git commit -m "update resume" && git push`

### Add a Blog Post
1. Create `data/blog/YYYY-MM-DD-slug.md`
2. `.\run_blog_refresh.ps1` (builds + pushes)

### Add a Learning Hub Page
1. Follow all rules in `AGENTS.md` — use `learning/_page-template.html` exactly
2. Write to `learning/{slug}.html`
3. Run `python generate_sitemap.py`
4. `git add -A && git commit -m "add learning: {slug}" && git push`

### Add a LeetCode Solution
1. Add solution to the appropriate location (see `build_blog.py` for structure)
2. `.\run_blog_refresh.ps1`

### Full Site Rebuild
```powershell
. .\env_setter.ps1
python generate.py --target all --format all
python build_blog.py
python generate_sitemap.py
git add -A && git commit -m "full rebuild" && git push
```

---

## SEO Files (passive — do not delete)

| File | Purpose |
|------|---------|
| `sitemap.xml` | Generated by `generate_sitemap.py` — submit to Google Search Console |
| `robots.txt` | Search engine crawl rules |
| `rss.xml` | RSS feed — generated by `build_blog.py` |
| `BingSiteAuth.xml` | Bing Webmaster Tools verification |
| `googled5fb877a5db7013f.html` | Google Search Console verification |

---

## Maintenance Notes

- **Single source of truth**: `data/store.yaml` — all resume/CV changes start here
- **Never modify** `learning/_page-template.html` CSS or class names — all 50 pages depend on it
- **`gitq` alias**: if undefined, replace with standard git commands in `run_blog_refresh.ps1`
- **wkhtmltopdf**: required for PDF output — install separately, not in pip
- **Credentials**: none stored in repo — GitHub Pages deployment requires no secrets
- **`personal_site`** repo (`D:/Workarea/personal_site`): earlier iteration of this site — verify before archiving it

---

## Future Improvements
- Move `gitq` definition into `env_setter.ps1` so it is always available
- Add unit tests for the PDF layout to catch margin/font regressions
- Consider automated deployment via GitHub Actions instead of manual push

---
*Last reviewed and enhanced: 2026-04-27*
