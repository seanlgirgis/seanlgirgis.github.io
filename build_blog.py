import html
import re
from datetime import datetime
from pathlib import Path

import markdown
import yaml
from jinja2 import Template

# Config
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "blog"
OUTPUT_DIR = BASE_DIR / "blog"
COMPONENT_OUTPUT = BASE_DIR / "components" / "blog.html"
LATEST_COMPONENT_OUTPUT = BASE_DIR / "components" / "latest_posts.html"
LEETCODE_COMPONENT_OUTPUT = BASE_DIR / "components" / "leetcode.html"
ARTICLES_COMPONENT_OUTPUT = BASE_DIR / "components" / "articles.html"
TEMPLATE_PATH = BASE_DIR / "templates" / "blog_post.html"
LEETCODE_CATEGORY_TEMPLATE_PATH = BASE_DIR / "templates" / "leetcode_category.html"
RSS_OUTPUT = BASE_DIR / "rss.xml"
ANNOUNCEMENTS_DIR = DATA_DIR / "announcements"
BASE_URL = "https://seanlgirgis.github.io"
DEFAULT_OG_IMAGE = "assets/img/blog/spa_flow.png"
LEETCODE_OUTPUT_DIR = OUTPUT_DIR / "leetcode"

# Stable category IDs for permanent URLs:
# /blog/leetcode/<category_id>.html
LEETCODE_CATEGORY_REGISTRY = {
    "arrays-hashing": {"label": "Arrays & Hashing", "aliases": ["arrays", "hashing"]},
    "two-pointers": {"label": "Two Pointers", "aliases": []},
    "sliding-window": {"label": "Sliding Window", "aliases": []},
    "stack-monotonic": {"label": "Stack & Monotonic Stack", "aliases": ["stack", "monotonic-stack"]},
    "heap-priority-queue": {"label": "Heap & Priority Queue", "aliases": ["heap", "priority-queue"]},
    "binary-search": {"label": "Binary Search", "aliases": []},
    "linked-list": {"label": "Linked List", "aliases": []},
    "trees": {"label": "Trees", "aliases": ["tree"]},
    "graphs": {"label": "Graphs", "aliases": ["graph"]},
    "backtracking": {"label": "Backtracking", "aliases": []},
    "dynamic-programming": {"label": "Dynamic Programming", "aliases": ["dp"]},
    "greedy": {"label": "Greedy", "aliases": []},
    "intervals": {"label": "Intervals", "aliases": []},
    "design": {"label": "Design", "aliases": ["lru", "mru", "cache-design"]},
    "simulation": {"label": "Simulation", "aliases": []},
}


def _parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return datetime.min


def _normalize_tags(tags):
    if isinstance(tags, list):
        return [str(t) for t in tags]
    return []


def _to_absolute_url(path_or_url):
    s = str(path_or_url or "").strip()
    if s.startswith("http://") or s.startswith("https://"):
        return s
    return f"{BASE_URL}/{s.lstrip('./')}"


def _extract_first_image_path(md_content):
    md_match = re.search(r"!\[[^\]]*\]\(([^)]+)\)", md_content or "")
    if md_match:
        image_path = md_match.group(1).strip()
        if image_path:
            return image_path.replace("../", "")

    html_match = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', md_content or "", re.IGNORECASE)
    if html_match:
        image_path = html_match.group(1).strip()
        if image_path:
            return image_path.replace("../", "")

    return ""


def _slugify(value):
    s = re.sub(r"[^a-z0-9]+", "-", str(value or "").strip().lower())
    return s.strip("-")


def _resolve_leetcode_category_ids(raw_values):
    alias_to_id = {}
    for category_id, cfg in LEETCODE_CATEGORY_REGISTRY.items():
        alias_to_id[category_id] = category_id
        alias_to_id[_slugify(cfg["label"])] = category_id
        for alias in cfg.get("aliases", []):
            alias_to_id[_slugify(alias)] = category_id

    out = []
    seen = set()
    for raw in raw_values:
        key = _slugify(raw)
        if not key:
            continue
        resolved = alias_to_id.get(key, key)
        if resolved not in seen:
            seen.add(resolved)
            out.append(resolved)
    return out

def render_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        # Split Frontmatter and Content
        raw = f.read()
        parts = raw.split("---", 2)
        if len(parts) < 3:
            print(f"Skipping {file_path}: Invalid Frontmatter")
            return None
        
        frontmatter = yaml.safe_load(parts[1])
        md_content = parts[2]

        # Avoid duplicate article title:
        # template already renders <h1>{{ title }}</h1>, so if markdown starts
        # with the same H1, remove that first heading only.
        fm_title = str(frontmatter.get("title", "")).strip()
        if fm_title:
            lines = md_content.lstrip("\r\n").splitlines()
            if lines and lines[0].lstrip().startswith("# "):
                first_h1 = lines[0].lstrip()[2:].strip()
                if first_h1 == fm_title:
                    md_content = "\n".join(lines[1:]).lstrip("\r\n")
        
        html_content = markdown.markdown(md_content, extensions=['fenced_code', 'codehilite'])
        
        return {
            "meta": frontmatter,
            "content": html_content,
            "raw_markdown": md_content,
        }

def generate_blog():
    # Ensure output dir exists
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    posts = []
    
    # Load Template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template_str = f.read()
        template = Template(template_str)

    # Process each MD file
    for md_file in DATA_DIR.glob("*.md"):
        print(f"Processing {md_file.name}...")
        data = render_markdown(md_file)
        if not data:
            continue
            
        meta = data['meta']
        slug = meta.get('slug', md_file.stem)
        tags = _normalize_tags(meta.get("tags", []))
        raw_lc_categories = meta.get("leetcode_categories", [])
        if isinstance(raw_lc_categories, str):
            raw_lc_categories = [raw_lc_categories]
        leetcode_category_ids = _resolve_leetcode_category_ids(raw_lc_categories)
        image = meta.get("image") or _extract_first_image_path(data["raw_markdown"]) or DEFAULT_OG_IMAGE

        posts.append({
            "title": meta['title'],
            "date": meta['date'],
            "date_obj": _parse_date(meta['date']),
            "summary": meta.get('summary', ''),
            "tags": tags,
            "slug": slug,
            "link": f"blog/{slug}.html",
            "canonical_url": f"{BASE_URL}/blog/{slug}.html",
            "image": image,
            "og_image_url": _to_absolute_url(image),
            "content": data['content'],
            "difficulty": meta.get("difficulty", ""),
            "topic": meta.get("topic", ""),
            "pattern": meta.get("pattern", ""),
            "leetcode_category_ids": leetcode_category_ids,
        })

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x["date_obj"], reverse=True)
    generated_slugs = {p["slug"] for p in posts}

    def related_posts_for(post):
        src_tags = set(t.lower() for t in post["tags"])
        candidates = []
        for other in posts:
            if other["slug"] == post["slug"]:
                continue
            overlap = len(src_tags.intersection(set(t.lower() for t in other["tags"])))
            if overlap > 0:
                candidates.append((overlap, other["date_obj"], other))
        candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
        return [c[2] for c in candidates[:3]]

    # Render each standalone page
    for post in posts:
        output_file = OUTPUT_DIR / f"{post['slug']}.html"

        final_html = template.render(
            title=post["title"],
            date=post["date"],
            tags=post["tags"],
            summary=post["summary"],
            content=post["content"],
            canonical_url=post["canonical_url"],
            og_image_url=post["og_image_url"],
            related_posts=related_posts_for(post),
        )
        
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(final_html)

    # Remove stale generated blog pages that no longer exist in data/blog.
    for html_file in OUTPUT_DIR.glob("*.html"):
        if html_file.stem not in generated_slugs:
            html_file.unlink()
    
    # Generate Blog list component
    component_html = '<div class="container"><h1>Blog</h1><div class="blog-list">'
    
    for post in posts:
        tags_html = "".join([f'<span class="tag">{t}</span>' for t in post['tags']])
        component_html += f"""
        <div class="blog-card">
            <h3><a href="{post['link']}">{post['title']}</a></h3>
            <div class="meta">{post['date']} • {tags_html}</div>
            <p>{post['summary']}</p>
            <a href="{post['link']}" class="read-more">Read Article &rarr;</a>
        </div>
        """
    
    component_html += '</div></div>'
    
    with open(COMPONENT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(component_html)

    # Generate Latest Posts component for home page
    latest_html = '<div class="container"><h2>Latest from the Blog</h2><div class="blog-list">'
    for post in posts[:3]:
        latest_html += f"""
        <div class="blog-card">
            <h3><a href="{post['link']}">{post['title']}</a></h3>
            <div class="meta">{post['date']}</div>
            <p>{post['summary']}</p>
            <a href="{post['link']}" class="read-more">Read Article &rarr;</a>
        </div>
        """
    latest_html += '</div></div>'
    with open(LATEST_COMPONENT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(latest_html)

    # Generate LeetCode hub component + stable category pages
    lc_posts = [
        p for p in posts
        if any(t.lower() == "leetcode" for t in p["tags"]) or p["slug"].startswith("lc-")
    ]
    category_to_posts = {category_id: [] for category_id in LEETCODE_CATEGORY_REGISTRY}
    for post in lc_posts:
        if post["leetcode_category_ids"]:
            for category_id in post["leetcode_category_ids"]:
                category_to_posts.setdefault(category_id, []).append(post)
        else:
            category_to_posts.setdefault("simulation", []).append(post)

    # Ensure output directory for category pages exists.
    LEETCODE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(LEETCODE_CATEGORY_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        category_template = Template(f.read())

    generated_category_files = set()
    alias_redirect_pairs = []
    for category_id, cfg in LEETCODE_CATEGORY_REGISTRY.items():
        generated_category_files.add(category_id)
        category_posts = sorted(category_to_posts.get(category_id, []), key=lambda x: x["date_obj"], reverse=True)
        output_file = LEETCODE_OUTPUT_DIR / f"{category_id}.html"
        final_html = category_template.render(
            category_label=cfg["label"],
            category_id=category_id,
            posts=category_posts,
            canonical_url=f"{BASE_URL}/blog/leetcode/{category_id}.html",
        )
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(final_html)

        for alias in cfg.get("aliases", []):
            alias_slug = _slugify(alias)
            if alias_slug and alias_slug != category_id:
                alias_redirect_pairs.append((alias_slug, category_id))
                generated_category_files.add(alias_slug)
                alias_file = LEETCODE_OUTPUT_DIR / f"{alias_slug}.html"
                alias_html = f"""<!DOCTYPE html>
<html lang="en"><head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=./{category_id}.html">
  <link rel="canonical" href="{BASE_URL}/blog/leetcode/{category_id}.html">
  <title>Redirecting...</title>
</head><body>
  <p>Redirecting to <a href="./{category_id}.html">{cfg["label"]}</a>...</p>
</body></html>"""
                with open(alias_file, "w", encoding="utf-8") as out:
                    out.write(alias_html)

    # Remove stale category pages/aliases no longer generated.
    for html_file in LEETCODE_OUTPUT_DIR.glob("*.html"):
        if html_file.stem not in generated_category_files:
            html_file.unlink()

    leetcode_html = '<div class="container"><h1>LeetCode Hub</h1><p>Persistent category pages with stable URLs. A post can appear in multiple categories.</p>'
    leetcode_html += '<h2>Categories</h2><div class="blog-list">'
    for category_id, cfg in LEETCODE_CATEGORY_REGISTRY.items():
        count = len(category_to_posts.get(category_id, []))
        leetcode_html += f"""
        <div class="blog-card">
            <h3><a href="blog/leetcode/{category_id}.html">{cfg['label']}</a></h3>
            <div class="meta">ID: {category_id}</div>
            <p>{count} solution(s)</p>
            <a href="blog/leetcode/{category_id}.html" class="read-more">Open Category &rarr;</a>
        </div>
        """
    leetcode_html += "</div>"
    if alias_redirect_pairs:
        alias_items = "".join(
            [f"<li><code>{alias}</code> → <code>{target}</code></li>" for alias, target in alias_redirect_pairs]
        )
        leetcode_html += f"<h2>Stable Alias Redirects</h2><ul>{alias_items}</ul>"

    leetcode_html += '<h2>All LeetCode Solutions</h2><div class="blog-list">'
    for post in lc_posts:
        tags_html = "".join([f'<span class="tag">{t}</span>' for t in post['tags']])
        detail_bits = [x for x in [post.get("difficulty", ""), post.get("topic", ""), post.get("pattern", "")] if x]
        detail_line = f"<div class='meta'>{' • '.join(detail_bits)}</div>" if detail_bits else ""
        cat_links = ""
        post_cat_ids = post["leetcode_category_ids"] or ["simulation"]
        cat_links = " ".join(
            [
                f'<a class="tag" href="blog/leetcode/{cid}.html">{LEETCODE_CATEGORY_REGISTRY.get(cid, {"label": cid})["label"]}</a>'
                for cid in post_cat_ids
            ]
        )
        leetcode_html += f"""
        <div class="blog-card">
            <h3><a href="{post['link']}">{post['title']}</a></h3>
            <div class="meta">{post['date']} • {tags_html}</div>
            {detail_line}
            <div class="meta">{cat_links}</div>
            <p>{post['summary']}</p>
            <a href="{post['link']}" class="read-more">Open Solution &rarr;</a>
        </div>
        """
    if not lc_posts:
        leetcode_html += "<p>No LeetCode posts yet.</p>"
    leetcode_html += "</div></div>"
    with open(LEETCODE_COMPONENT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(leetcode_html)

    # Generate Technical Articles hub component with structured sections.
    idea_posts = [
        p for p in posts
        if any(
            t.lower() in {"machine learning", "data science", "business strategy", "production ml", "ideas"}
            for t in p["tags"]
        )
    ]
    project_posts = [
        p for p in posts
        if any(
            t.lower() in {"web architecture", "architecture", "project", "spa", "serverless"}
            for t in p["tags"]
        )
    ]

    def _cards(section_posts, link_label):
        if not section_posts:
            return "<p>No posts yet.</p>"
        cards = []
        for post in section_posts[:6]:
            tags_html = "".join([f'<span class="tag">{t}</span>' for t in post['tags']])
            cards.append(
                f"""
        <div class="blog-card">
            <h3><a href="{post['link']}">{post['title']}</a></h3>
            <div class="meta">{post['date']} • {tags_html}</div>
            <p>{post['summary']}</p>
            <a href="{post['link']}" class="read-more">{link_label} &rarr;</a>
        </div>
        """
            )
        return "".join(cards)

    articles_html = f"""
<div class="container">
    <h1>Technical Articles</h1>
    <p>Organized by track so readers can quickly find solutions, ideas, and project breakdowns.</p>

    <h2>LeetCode Solutions</h2>
    <div class="blog-list">
        {_cards(lc_posts, "Open Solution")}
    </div>

    <h2>Ideas & Insights</h2>
    <div class="blog-list">
        {_cards(idea_posts, "Read Insight")}
    </div>

    <h2>Project Deep Dives</h2>
    <div class="blog-list">
        {_cards(project_posts, "Read Deep Dive")}
    </div>
</div>
"""
    with open(ARTICLES_COMPONENT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(articles_html)

    # Generate RSS feed
    rss_items = []
    for post in posts:
        pub_date = post["date_obj"].strftime("%a, %d %b %Y 00:00:00 +0000")
        rss_items.append(
            f"""<item>
  <title>{html.escape(post['title'])}</title>
  <link>{post['canonical_url']}</link>
  <guid>{post['canonical_url']}</guid>
  <pubDate>{pub_date}</pubDate>
  <description>{html.escape(post['summary'])}</description>
</item>"""
        )
    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Sean Luka Girgis Blog</title>
  <link>{BASE_URL}</link>
  <description>Technical writing on data engineering, architecture, and algorithms.</description>
  {''.join(rss_items)}
</channel>
</rss>"""
    with open(RSS_OUTPUT, "w", encoding="utf-8") as f:
        f.write(rss_xml)

    # Generate announcement snippets for social posting
    ANNOUNCEMENTS_DIR.mkdir(parents=True, exist_ok=True)
    for post in posts:
        announcement_path = ANNOUNCEMENTS_DIR / f"{post['slug']}.md"
        content = f"""# Announcement Pack: {post['title']}

## LinkedIn (Long)
New post published: **{post['title']}**

{post['summary']}

Read: {post['canonical_url']}

## LinkedIn (Short)
New article: {post['title']}
{post['canonical_url']}

## X / Twitter
New post: {post['title']}  
{post['canonical_url']}  
#DataEngineering #LeetCode #Python
"""
        with open(announcement_path, "w", encoding="utf-8") as f:
            f.write(content)
        
    print(f"Successfully generated {len(posts)} posts.")

    # 4. Update Sitemap
    try:
        from generate_sitemap import generate_sitemap
        generate_sitemap()
    except Exception as e:
        print(f"Warning: Failed to generate sitemap: {e}")

if __name__ == "__main__":
    generate_blog()
