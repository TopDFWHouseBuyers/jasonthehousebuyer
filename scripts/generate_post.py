#!/usr/bin/env python3
"""
Jason The House Buyer - Automated Blog Generator
Houston, Texas market
Runs Mon/Wed/Fri/Sat at 8am CT
"""

import os
import json
import re
import anthropic
import time
from datetime import datetime
from pathlib import Path

CITIES = [
    "Houston", "Katy", "Spring", "Sugar Land", "Humble", "Tomball",
    "Cypress", "Pasadena", "Friendswood", "Missouri City", "Pearland",
    "The Woodlands", "Conroe", "League City", "Baytown", "Rosenberg",
    "Richmond", "Jacinto City", "Crosby", "La Marque", "Texas City",
    "Deer Park", "La Porte", "Channelview", "Stafford", "Alvin",
    "Galveston", "Clute", "Lake Jackson", "Angleton"
]

CITY_TOPICS = [
    "How to Sell Your House Fast in {city}, TX - No Fees, No Repairs",
    "We Buy Houses in {city}, TX - Get a Cash Offer in 24 Hours",
    "Sell My House Fast {city} TX - The Complete Guide",
    "Cash Home Buyers in {city}, TX - What You Need to Know",
    "Selling Your {city} Home As-Is - Everything You Need to Know",
    "How to Avoid Foreclosure in {city}, TX",
    "Selling an Inherited Property in {city}, TX - A Step-by-Step Guide",
    "Selling a House During Divorce in {city}, TX",
    "Tired Landlord? How to Sell Your Rental Property in {city}, TX Fast",
    "Relocating from {city}, TX? How to Sell Your Home Fast",
]

EVERGREEN_TOPICS = [
    {"title": "Selling a House During Divorce in Texas - Everything You Need to Know", "slug": "selling-house-during-divorce-texas-houston", "keyword": "selling house during divorce Texas Houston", "category": "divorce"},
    {"title": "How to Sell Your Houston Home Fast During a Divorce", "slug": "sell-home-fast-divorce-houston", "keyword": "sell home fast divorce Houston", "category": "divorce"},
    {"title": "Texas Community Property Laws and Selling Your Houston Home", "slug": "texas-community-property-selling-houston-home", "keyword": "Texas community property selling Houston home", "category": "divorce"},
    {"title": "How to Stop Foreclosure in Houston, Texas - Your Options", "slug": "stop-foreclosure-houston-texas", "keyword": "stop foreclosure Houston Texas", "category": "foreclosure"},
    {"title": "Pre-Foreclosure in Houston - What It Means and What You Can Do", "slug": "pre-foreclosure-houston-texas", "keyword": "pre-foreclosure Houston Texas", "category": "foreclosure"},
    {"title": "Selling Your Houston Home Before Foreclosure - Is It Possible?", "slug": "sell-home-before-foreclosure-houston", "keyword": "sell home before foreclosure Houston", "category": "foreclosure"},
    {"title": "Behind on Mortgage Payments in Houston? Here Are Your Options", "slug": "behind-on-mortgage-payments-houston", "keyword": "behind on mortgage payments Houston options", "category": "foreclosure"},
    {"title": "Selling an Inherited House in Houston, Texas - A Complete Guide", "slug": "selling-inherited-house-houston-texas", "keyword": "selling inherited house Houston Texas", "category": "inheritance"},
    {"title": "How to Sell an Inherited Property in Houston During Probate", "slug": "sell-inherited-property-probate-houston", "keyword": "sell inherited property probate Houston", "category": "inheritance"},
    {"title": "What to Do With an Inherited House in Houston You Do Not Want", "slug": "inherited-house-houston-dont-want", "keyword": "inherited house Houston do not want", "category": "inheritance"},
    {"title": "What Is a Cash Home Buyer? How the Process Works in Houston", "slug": "what-is-cash-home-buyer-houston", "keyword": "what is a cash home buyer Houston", "category": "education"},
    {"title": "Cash Offer vs Traditional Sale in Houston - Which Is Better?", "slug": "cash-offer-vs-traditional-sale-houston", "keyword": "cash offer vs traditional sale Houston", "category": "education"},
    {"title": "The Real Cost of Selling a House in Houston - Fees and Hidden Costs", "slug": "real-cost-selling-house-houston", "keyword": "cost of selling a house Houston", "category": "education"},
    {"title": "How Fast Can You Sell a House in Houston? Timeline Explained", "slug": "how-fast-can-you-sell-house-houston", "keyword": "how fast can you sell a house Houston", "category": "education"},
    {"title": "Selling a House As-Is in Houston - What Sellers Need to Know", "slug": "selling-house-as-is-houston", "keyword": "selling house as-is Houston", "category": "education"},
    {"title": "Is It Better to Sell to a Cash Buyer or List With an Agent in Houston?", "slug": "cash-buyer-vs-agent-houston", "keyword": "cash buyer vs agent Houston", "category": "education"},
    {"title": "Do You Have to Pay Taxes When You Sell Your House in Texas?", "slug": "taxes-selling-house-texas-houston", "keyword": "taxes selling house Texas", "category": "education"},
    {"title": "How to Get a Fair Cash Offer on Your Houston Home", "slug": "how-to-get-fair-cash-offer-houston", "keyword": "fair cash offer Houston home", "category": "education"},
    {"title": "Selling a House With Tenants in Houston - Landlord Guide", "slug": "selling-house-with-tenants-houston", "keyword": "selling house with tenants Houston", "category": "situations"},
    {"title": "How to Sell a Hurricane or Flood Damaged Home in Houston", "slug": "sell-flood-damaged-home-houston", "keyword": "sell flood damaged home Houston", "category": "situations"},
    {"title": "Selling a House With Foundation Problems in Houston", "slug": "selling-house-foundation-problems-houston", "keyword": "selling house foundation problems Houston", "category": "situations"},
    {"title": "How to Sell a Fire-Damaged Home in Houston", "slug": "sell-fire-damaged-home-houston", "keyword": "sell fire damaged home Houston", "category": "situations"},
    {"title": "Selling a Vacant or Abandoned House in Houston", "slug": "selling-vacant-house-houston", "keyword": "selling vacant house Houston", "category": "situations"},
    {"title": "How to Sell a House With Mold in Houston", "slug": "sell-house-with-mold-houston", "keyword": "sell house with mold Houston", "category": "situations"},
    {"title": "Selling a House With Code Violations in Houston", "slug": "selling-house-code-violations-houston", "keyword": "selling house code violations Houston", "category": "situations"},
    {"title": "How to Sell a House With a Lien in Houston", "slug": "sell-house-with-lien-houston", "keyword": "sell house with lien Houston", "category": "situations"},
    {"title": "Selling Your Houston Home During Financial Hardship", "slug": "selling-home-financial-hardship-houston", "keyword": "selling home financial hardship Houston", "category": "situations"},
    {"title": "How to Sell Your Houston Home When Relocating for Work", "slug": "sell-home-relocating-houston", "keyword": "sell home relocating Houston", "category": "situations"},
    {"title": "Selling a Rental Property in Houston - What Landlords Need to Know", "slug": "selling-rental-property-houston", "keyword": "selling rental property Houston", "category": "situations"},
    {"title": "Downsizing in Houston - How to Sell Your Family Home Fast", "slug": "downsizing-houston-sell-family-home", "keyword": "downsizing Houston sell home fast", "category": "situations"},
    {"title": "Houston Real Estate Market 2025 - What Sellers Need to Know", "slug": "houston-real-estate-market-2025-sellers", "keyword": "Houston real estate market 2025 sellers", "category": "market"},
    {"title": "Is Now a Good Time to Sell Your Houston Home?", "slug": "good-time-sell-houston-home", "keyword": "good time to sell Houston home", "category": "market"},
    {"title": "Why Houston Home Prices Are Still Strong - What It Means for Sellers", "slug": "houston-home-prices-sellers", "keyword": "Houston home prices sellers", "category": "market"},
]


def get_next_topic():
    tracking_file = Path("blog/tracking.json")
    if tracking_file.exists():
        with open(tracking_file) as f:
            tracking = json.load(f)
    else:
        tracking = {"posts_written": 0, "city_index": 0, "evergreen_index": 0, "last_post": None}

    posts_written = tracking.get("posts_written", 0)

    if posts_written % 2 == 0:
        city_idx = tracking.get("city_index", 0) % len(CITIES)
        topic_template = CITY_TOPICS[posts_written % len(CITY_TOPICS)]
        city = CITIES[city_idx]
        title = topic_template.format(city=city)
        slug = f"sell-my-house-fast-{city.lower().replace(' ', '-')}-tx-{posts_written}"
        keyword = f"sell my house fast {city} TX"
        post_type = "city"
        tracking["city_index"] = (city_idx + 1) % len(CITIES)
        extra_context = f"Target city: {city}, Texas (Houston metro area). Include local context about {city} neighborhoods, the Houston area real estate market, and why sellers in {city} specifically benefit from working with a cash buyer."
    else:
        ev_idx = tracking.get("evergreen_index", 0) % len(EVERGREEN_TOPICS)
        topic = EVERGREEN_TOPICS[ev_idx]
        title = topic["title"]
        slug = topic["slug"]
        keyword = topic["keyword"]
        post_type = "evergreen"
        tracking["evergreen_index"] = (ev_idx + 1) % len(EVERGREEN_TOPICS)
        extra_context = f"Category: {topic['category']}. Write from the perspective of someone in this specific situation in the Houston, Texas area."

    tracking["posts_written"] = posts_written + 1
    tracking["last_post"] = datetime.now().isoformat()
    tracking_file.parent.mkdir(exist_ok=True)
    with open(tracking_file, "w") as f:
        json.dump(tracking, f, indent=2)

    return {"title": title, "slug": slug, "keyword": keyword, "post_type": post_type, "extra_context": extra_context}


def generate_post(topic: dict) -> dict:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""You are an expert real estate SEO content writer for Jason The House Buyer, a cash home buying company in Houston, Texas.

COMPANY INFO:
- Name: Jason The House Buyer
- Phone: 972-284-9713
- Website: https://www.jasonthehousebuyer.com
- License: TX Real Estate License #0657354
- Service area: All of Greater Houston including Houston, Katy, Spring, Sugar Land, Humble, Tomball, Cypress, Pasadena, Friendswood, Missouri City, Pearland, The Woodlands, Conroe, League City, Baytown and all surrounding areas

ASSIGNMENT:
- Title: {topic['title']}
- Primary keyword: {topic['keyword']}
- Additional context: {topic['extra_context']}
- Word count: 800-1000 words
- Include 2 call-to-action sections
- Tone: Helpful, knowledgeable, empathetic - like a trusted local Houston expert

CRITICAL REQUIREMENTS:
1. Return ONLY a JSON object - no text before or after
2. No markdown code fences
3. All apostrophes in content_html must use HTML entity &apos; or be removed
4. All double quotes inside JSON string values must be escaped with backslash
5. Keep content_html under 3000 characters total
6. Meta title under 60 characters
7. Meta description under 160 characters
8. Each CTA mentions 972-284-9713 and links to /#offer

JSON format:
{{
  "meta_title": "...",
  "meta_description": "...",
  "h1": "...",
  "intro": "2-3 sentences max",
  "content_html": "<h2>Section 1</h2><p>Content here. No apostrophes.</p><h2>Section 2</h2><p>More content.</p><h2>Section 3</h2><p>Final section.</p>",
  "word_count": 900,
  "secondary_keywords": ["keyword1", "keyword2", "keyword3"]
}}"""

    prompt_safe = prompt.encode('ascii', errors='replace').decode('ascii')

    for attempt in range(3):
        try:
            message = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt_safe}]
            )
            break
        except Exception as e:
            if 'overloaded' in str(e).lower() and attempt < 2:
                print(f"API overloaded - waiting 30 seconds before retry {attempt + 2}/3...")
                time.sleep(30)
            else:
                raise

    raw = message.content[0].text.strip()

    def clean_json(text):
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        text = text.strip()
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            text = text[start:end+1]
        return text

    try:
        return json.loads(clean_json(raw))
    except json.JSONDecodeError:
        print("JSON parse failed - retrying with minimal prompt...")
        prompt_minimal = f"""Write a real estate blog post for Jason The House Buyer about: {topic['title']}

Return ONLY this JSON with no apostrophes in content_html:
{{
  "meta_title": "Sell Your House Fast in Houston - Cash Offer",
  "meta_description": "Jason The House Buyer offers fast cash offers in Houston with no fees or repairs. Call 972-284-9713.",
  "h1": "{topic['title']}",
  "intro": "Selling your home in Houston does not have to be stressful. Jason The House Buyer makes it simple with a fair cash offer in 24 hours.",
  "content_html": "<h2>How We Buy Houses in Houston</h2><p>We buy houses throughout Greater Houston in any condition. No repairs needed, no agent fees, no closing costs. Call us at 972-284-9713 or fill out our form to get started.</p><h2>Why Houston Homeowners Choose Us</h2><p>We close in as few as 7 days on your schedule. Our process is simple: tell us about your property, get a cash offer in 24 hours, and choose your closing date.</p><h2>Get Your Free Cash Offer Today</h2><p>Ready to sell your Houston home fast? Call 972-284-9713 or visit jasonthehousebuyer.com. We serve Houston, Katy, Spring, Sugar Land, The Woodlands and all surrounding areas.</p>",
  "word_count": 150,
  "secondary_keywords": ["sell house fast Houston", "cash home buyers Houston", "we buy houses Texas"]
}}"""
        prompt_minimal_safe = prompt_minimal.encode('ascii', errors='replace').decode('ascii')
        message3 = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt_minimal_safe}]
        )
        raw3 = message3.content[0].text.strip()
        return json.loads(clean_json(raw3))


def build_html_page(post: dict, topic: dict) -> str:
    date_str = datetime.now().strftime("%B %d, %Y")
    year = datetime.now().year

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{post['meta_title']}</title>
<meta name="description" content="{post['meta_description']}">
<meta property="og:title" content="{post['meta_title']}">
<meta property="og:description" content="{post['meta_description']}">
<link rel="canonical" href="https://www.jasonthehousebuyer.com/blog/{topic['slug']}/">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{post['h1']}",
  "datePublished": "{datetime.now().isoformat()}",
  "publisher": {{
    "@type": "Organization",
    "name": "Jason The House Buyer",
    "telephone": "972-284-9713",
    "url": "https://www.jasonthehousebuyer.com"
  }}
}}
</script>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Source+Sans+3:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#f8faf8;color:#1a1f1a;font-family:'Source Sans 3',sans-serif;font-weight:300;line-height:1.6}}
.site-nav{{background:#0f1e3d;padding:16px 32px;display:flex;align-items:center;justify-content:space-between;border-bottom:3px solid #e07b20;position:sticky;top:0;z-index:100}}
.nav-logo{{color:#e07b20;font-weight:700;font-size:18px;text-decoration:none}}
.nav-logo span{{color:#fff}}
.nav-links{{display:flex;align-items:center;gap:20px}}
.nav-links a{{color:rgba(255,255,255,0.7);font-size:12px;font-weight:600;text-decoration:none;letter-spacing:0.05em;text-transform:uppercase}}
.nav-cta{{background:#e07b20;color:#fff !important;padding:9px 18px;border-radius:2px}}
.hero-blog{{background:#1a2744;padding:64px 40px;text-align:center;position:relative;overflow:hidden}}
.hero-blog::before{{content:'';position:absolute;inset:0;background:url('https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=1200&q=60') center/cover;opacity:0.15}}
.hero-blog-inner{{position:relative;z-index:1;max-width:800px;margin:0 auto}}
.hero-cat{{display:inline-block;background:rgba(224,123,32,0.2);border:1px solid rgba(224,123,32,0.4);color:#f59535;font-size:10px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;padding:5px 12px;border-radius:2px;margin-bottom:16px}}
.hero-blog h1{{font-family:'Lora',serif;font-size:clamp(26px,4vw,44px);color:#fff;font-weight:700;line-height:1.15;margin-bottom:16px}}
.hero-meta{{font-size:11px;color:rgba(255,255,255,0.5);letter-spacing:0.1em;text-transform:uppercase}}
.content-layout{{max-width:1100px;margin:0 auto;padding:48px 24px;display:grid;grid-template-columns:1fr 300px;gap:48px;align-items:start}}
@media(max-width:768px){{.content-layout{{grid-template-columns:1fr}}}}
.article-body h2{{font-family:'Lora',serif;font-size:26px;font-weight:700;color:#1a1f1a;margin:36px 0 14px;line-height:1.2}}
.article-body h3{{font-size:18px;font-weight:700;color:#1a1f1a;margin:24px 0 10px}}
.article-body p{{font-size:15px;line-height:1.9;color:#3a4a3a;margin-bottom:16px}}
.article-body ul,.article-body ol{{padding-left:22px;margin-bottom:16px}}
.article-body li{{font-size:15px;line-height:1.8;color:#3a4a3a;margin:6px 0}}
.cta-inline{{background:#0f1e3d;border-left:4px solid #e07b20;padding:24px 28px;margin:32px 0;border-radius:0 4px 4px 0}}
.cta-inline h3{{color:#e07b20;font-size:16px;font-weight:700;margin-bottom:8px}}
.cta-inline p{{color:rgba(255,255,255,0.8);font-size:14px;margin-bottom:16px;line-height:1.7}}
.cta-inline a{{display:inline-block;background:#e07b20;color:#fff;padding:12px 24px;font-weight:700;font-size:13px;text-decoration:none;border-radius:2px;letter-spacing:0.05em;text-transform:uppercase}}
.sidebar{{position:sticky;top:80px}}
.sidebar-card{{background:#fff;border:1px solid #e0d8cc;border-top:3px solid #e07b20;padding:24px;margin-bottom:20px;border-radius:0 0 4px 4px}}
.sidebar-card h3{{font-size:15px;font-weight:700;color:#1a1f1a;margin-bottom:8px}}
.sidebar-card p{{font-size:13px;color:#52675f;line-height:1.6;margin-bottom:16px}}
.sidebar-card .phone{{font-size:20px;font-weight:700;color:#e07b20;text-decoration:none;display:block;margin-bottom:12px}}
.sidebar-btn{{display:block;background:#0f1e3d;color:#fff;padding:13px;font-weight:700;font-size:12px;text-decoration:none;border-radius:2px;letter-spacing:0.06em;text-transform:uppercase;text-align:center;margin-bottom:8px}}
.sidebar-btn.orange{{background:#e07b20}}
.back-link{{display:inline-flex;align-items:center;gap:6px;color:#e07b20;text-decoration:none;font-size:12px;font-weight:600;margin-bottom:28px;letter-spacing:0.05em;text-transform:uppercase}}
footer{{background:#0f1e3d;color:rgba(255,255,255,0.5);text-align:center;padding:28px;font-size:12px;border-top:3px solid #e07b20}}
footer a{{color:#e07b20;text-decoration:none}}
</style>
</head>
<body>

<nav class="site-nav">
  <a href="/" class="nav-logo">Jason<span> The House Buyer</span></a>
  <div class="nav-links">
    <a href="/">Home</a>
    <a href="/blog/">Blog</a>
    <a href="tel:9722849713">972-284-9713</a>
    <a href="/#offer" class="nav-cta">Get Cash Offer</a>
  </div>
</nav>

<div class="hero-blog">
  <div class="hero-blog-inner">
    <div class="hero-cat">Jason The House Buyer · Houston Resource Guide</div>
    <h1>{post['h1']}</h1>
    <div class="hero-meta">Published {date_str} · Houston, Texas</div>
  </div>
</div>

<div class="content-layout">
  <div class="article-body">
    <a href="/blog/" class="back-link">Back to All Articles</a>
    <p style="font-size:16px;line-height:1.9;color:#2a3a2a;margin-bottom:24px;font-weight:400">{post['intro']}</p>
    {post['content_html']}
    <div class="cta-inline" style="margin-top:40px">
      <h3>Ready to Get Your Cash Offer in Houston?</h3>
      <p>We buy houses anywhere in Greater Houston - any condition, any situation. No fees, no repairs, no commissions. Get a fair cash offer within 24 hours.</p>
      <a href="/#offer">Get My Free Cash Offer</a>
    </div>
  </div>

  <div class="sidebar">
    <div class="sidebar-card">
      <h3>Get Your Free Cash Offer</h3>
      <p>No fees, no repairs, no commissions. We close in as few as 7 days.</p>
      <a href="tel:9722849713" class="phone">972-284-9713</a>
      <a href="/#offer" class="sidebar-btn orange">Get Cash Offer</a>
      <a href="tel:9722849713" class="sidebar-btn">Call Us Now</a>
    </div>
    <div class="sidebar-card">
      <h3>How It Works</h3>
      <p style="font-size:12px;color:#52675f;line-height:1.8;margin:0">
        <strong>1.</strong> Tell us about your property<br>
        <strong>2.</strong> Get a cash offer in 24 hours<br>
        <strong>3.</strong> Choose your closing date<br>
        <strong>4.</strong> Walk away with cash
      </p>
    </div>
  </div>
</div>

<footer>
  {year} Jason The House Buyer · <a href="/">jasonthehousebuyer.com</a> · 972-284-9713 · TX License #0657354<br>
  Serving Houston, Katy, Spring, Sugar Land, Humble, Tomball, Cypress, Pasadena, Pearland, The Woodlands and all Greater Houston areas
</footer>

</body>
</html>"""


def main():
    print(f"Starting blog generation - {datetime.now().isoformat()}")
    topic = get_next_topic()
    print(f"Topic: {topic['title']}")
    print(f"Slug: {topic['slug']}")
    print(f"Type: {topic['post_type']}")
    print("Calling Claude API...")
    post = generate_post(topic)
    print(f"Generated: {post['word_count']} words")
    html = build_html_page(post, topic)
    output_dir = Path(f"blog/{topic['slug']}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "index.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved: {output_file}")
    print(f"URL: https://www.jasonthehousebuyer.com/blog/{topic['slug']}/")
    print("Done!")


if __name__ == "__main__":
    main()
