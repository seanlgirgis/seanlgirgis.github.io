from datetime import datetime
from pathlib import Path

BASE_URL = "https://seanlgirgis.github.io"
BASE_DIR = Path(__file__).parent
BLOG_DIR = BASE_DIR / "blog"

def generate_sitemap():
    print("Generating sitemap.xml...")
    
    # Static Routes (SPA Sections)
    # Note: Search engines prefer clean URLs. Hash URLs (#about) are often ignored or treated as the same page.
    # However, listing them helps some crawlers discover content context.
    # We primarily list the root and the actual static blog pages.
    urls = [
        {
            "loc": f"{BASE_URL}/",
            "lastmod": Path(BASE_DIR / "index.html").stat().st_mtime,
            "priority": "1.0",
            "changefreq": "monthly"
        }
    ]
    # Optional additional static artifacts
    rss_file = BASE_DIR / "rss.xml"
    if rss_file.exists():
        urls.append({
            "loc": f"{BASE_URL}/rss.xml",
            "lastmod": rss_file.stat().st_mtime,
            "priority": "0.6",
            "changefreq": "weekly"
        })

    # Add Static Blog Pages
    if BLOG_DIR.exists():
        for html_file in BLOG_DIR.glob("*.html"):
            urls.append({
                "loc": f"{BASE_URL}/blog/{html_file.name}",
                "lastmod": html_file.stat().st_mtime,
                "priority": "0.8",
                "changefreq": "monthly"
            })

    # Build XML
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for url in urls:
        lastmod = datetime.fromtimestamp(url["lastmod"]).strftime("%Y-%m-%d")
        sitemap_content += '  <url>\n'
        sitemap_content += f'    <loc>{url["loc"]}</loc>\n'
        sitemap_content += f'    <lastmod>{lastmod}</lastmod>\n'
        sitemap_content += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
        sitemap_content += f'    <priority>{url["priority"]}</priority>\n'
        sitemap_content += '  </url>\n'

    sitemap_content += '</urlset>'

    # Save
    output_path = BASE_DIR / "sitemap.xml"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)
    
    print(f"Sitemap generated at {output_path} with {len(urls)} URLs.")

if __name__ == "__main__":
    generate_sitemap()
