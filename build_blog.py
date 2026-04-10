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
TEMPLATE_PATH = BASE_DIR / "templates" / "blog_post.html"
RSS_OUTPUT = BASE_DIR / "rss.xml"
ANNOUNCEMENTS_DIR = DATA_DIR / "announcements"
BASE_URL = "https://seanlgirgis.github.io"
DEFAULT_OG_IMAGE = "assets/img/blog/spa_flow.png"


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
        })

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x["date_obj"], reverse=True)

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
    
    # Generate Blog list component
    component_html = '<div class="container"><h1>Blog</h1><div class="blog-list">'
    
    for post in posts:
        tags_html = "".join([f'<span class="tag">{t}</span>' for t in post['tags']])
        image_html = ""
        if post["image"]:
            image_html = f'<img class="blog-card-thumb" src="{post["image"]}" alt="{html.escape(post["title"])} thumbnail">'
        component_html += f"""
        <div class="blog-card">
            {image_html}
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

    # Generate LeetCode hub component
    lc_posts = [
        p for p in posts
        if any(t.lower() == "leetcode" for t in p["tags"]) or p["slug"].startswith("lc-")
    ]
    leetcode_html = '<div class="container"><h1>LeetCode Hub</h1><p>Structured solutions and patterns.</p><div class="blog-list">'
    for post in lc_posts:
        tags_html = "".join([f'<span class="tag">{t}</span>' for t in post['tags']])
        detail_bits = [x for x in [post.get("difficulty", ""), post.get("topic", ""), post.get("pattern", "")] if x]
        detail_line = f"<div class='meta'>{' • '.join(detail_bits)}</div>" if detail_bits else ""
        leetcode_html += f"""
        <div class="blog-card">
            <h3><a href="{post['link']}">{post['title']}</a></h3>
            <div class="meta">{post['date']} • {tags_html}</div>
            {detail_line}
            <p>{post['summary']}</p>
            <a href="{post['link']}" class="read-more">Open Solution &rarr;</a>
        </div>
        """
    if not lc_posts:
        leetcode_html += "<p>No LeetCode posts yet.</p>"
    leetcode_html += "</div></div>"
    with open(LEETCODE_COMPONENT_OUTPUT, "w", encoding="utf-8") as f:
        f.write(leetcode_html)

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
