# Jason The House Buyer — Houston Website & Blog Automation

## What This Does

This repository powers the automated blog system for [jasonthehousebuyer.com](https://www.jasonthehousebuyer.com).

**Every Monday and Thursday at 8am CT**, GitHub Actions automatically:
1. Picks the next topic from the queue (80+ topics covering Houston cities, divorce, foreclosure, inheritance, flood damage, education, and more)
2. Calls Claude AI to write a 1,200-word SEO-optimized blog post
3. Builds a complete HTML page with proper meta tags and schema markup
4. Updates the sitemap
5. Commits to this repo
6. Netlify automatically deploys it to the live site

## Houston-Specific Topics

- **30 Houston area cities** — Houston, Katy, Spring, Sugar Land, Humble, Tomball, Cypress, Pasadena, Friendswood, Missouri City, Pearland, The Woodlands, Conroe, League City, Baytown, Rosenberg, Richmond + more
- **Flood/Hurricane damage** — unique to Houston market
- **Foreclosure** — Harris County specific guidance
- **Divorce** — Texas community property laws
- **Inheritance** — Houston probate process
- **Cash buyer education** — Houston market context
- **Specific situations** — tenants, foundation, fire, mold, liens, vacant, hardship, relocation, downsizing, rentals

## Setup

### 1. Add Anthropic API key to GitHub Secrets
1. Repo → **Settings → Secrets and variables → Actions**
2. **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: your Claude API key
5. Save

### 2. Connect to Netlify
1. Netlify → **Add new site → Import from GitHub**
2. Select this repo
3. Build command: (empty)
4. Publish directory: `.`
5. Deploy

### 3. Point jasonthehousebuyer.com DNS to Netlify

### 4. That's it — posts run every Monday and Thursday automatically

## File Structure

```
/
├── index.html                    ← Main website
├── sitemap.xml                   ← Auto-updated after each post
├── blog/
│   ├── index.html                ← Blog listing page
│   ├── tracking.json             ← Tracks post history
│   └── [slug]/index.html         ← Each generated post
├── scripts/
│   ├── generate_post.py          ← Blog generator
│   └── generate_sitemap.py       ← Sitemap updater
└── .github/workflows/
    └── generate-blog.yml         ← Automation schedule
```
