#!/usr/bin/env python3
"""
Generates sitemap.xml for topdfwhousebuyers.com
Runs automatically after each blog post is generated
"""

import os
from pathlib import Path
from datetime import datetime

BASE_URL = "https://www.jasonthehousebuyer.com"

def generate_sitemap():
    urls = []
    today = datetime.now().strftime("%Y-%m-%d")

    # Main pages
    static_pages = [
        {"loc": "/", "priority": "1.0", "changefreq": "weekly"},
        {"loc": "/blog/", "priority": "0.9", "changefreq": "daily"},
    ]

    for page in static_pages:
        urls.append(f"""  <url>
    <loc>{BASE_URL}{page["loc"]}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{page["changefreq"]}</changefreq>
    <priority>{page["priority"]}</priority>
  </url>""")

    # Blog posts - scan blog directory
    blog_dir = Path("blog")
    if blog_dir.exists():
        for post_dir in sorted(blog_dir.iterdir()):
            if post_dir.is_dir() and (post_dir / "index.html").exists():
                slug = post_dir.name
                # Get file modification date
                mod_time = (post_dir / "index.html").stat().st_mtime
                mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
                urls.append(f"""  <url>
    <loc>{BASE_URL}/blog/{slug}/</loc>
    <lastmod>{mod_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''

    with open("sitemap.xml", "w") as f:
        f.write(sitemap)

    print(f"Sitemap generated with {len(urls)} URLs")
    print("Saved: sitemap.xml")

if __name__ == "__main__":
    generate_sitemap()
