import os
import yaml
import markdown
from pathlib import Path
from datetime import datetime
from jinja2 import Template

# Config
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "blog"
OUTPUT_DIR = BASE_DIR / "blog"
COMPONENT_OUTPUT = BASE_DIR / "components" / "blog.html"
TEMPLATE_PATH = BASE_DIR / "templates" / "blog_post.html"

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
            "content": html_content
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
        output_file = OUTPUT_DIR / f"{slug}.html"
        
        # Render Standalone Page
        final_html = template.render(
            title=meta['title'],
            date=meta['date'],
            tags=meta['tags'],
            summary=meta.get('summary', ''),
            content=data['content']
        )
        
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(final_html)
            
        # Add to list for component
        posts.append({
            "title": meta['title'],
            "date": meta['date'],
            "summary": meta.get('summary', ''),
            "tags": meta['tags'],
            "link": f"blog/{slug}.html"
        })

    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x['date'], reverse=True)
    
    # Generate Component List HTML
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
        
    print(f"Successfully generated {len(posts)} posts.")

    # 4. Update Sitemap
    try:
        from generate_sitemap import generate_sitemap
        generate_sitemap()
    except Exception as e:
        print(f"Warning: Failed to generate sitemap: {e}")

if __name__ == "__main__":
    generate_blog()
