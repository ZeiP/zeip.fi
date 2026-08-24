# Zeip.fi static site

This repository contains a GitHub Pages/Jekyll implementation of `www.zeip.fi`.
It replaces the Drupal site with static pages and a single language-aware writing
system.

## Content

Public content is generated from two sources:

- the current public `www.zeip.fi` Drupal site
- the extracted Drupal 7 dump in `extracted_db_dump/`

Generated Markdown lives in:

- `fi/` - Finnish static pages
- `en/` - English static pages
- `_posts/fi/` - Finnish articles
- `_posts/en/` - English articles

The blog is one maintained content system with separated public language views:

- `/fi/blogi/`
- `/en/blogi/`

Posts include front matter for language, canonical permalink, curated theme,
original tags, translation key, original URLs, and source.

## Presentation

The visual direction comes from `layout-prototype.html`, but its sample text is
not production copy. Production wording comes from the current site and the D7
articles, plus minimal localized UI labels.

Shared presentation lives in:

- `_layouts/` - page, home, blog, theme, post, redirect layouts
- `_includes/` - header, footer, language switcher, post rows, source note
- `_data/navigation.yml` - localized navigation
- `_data/themes.yml` - curated theme labels
- `assets/site.css` - styles adapted from the prototype

## Regenerating Content

To refresh generated pages, posts, redirects, feeds, and sitemap inputs:

```bash
python3 tools/generate_site.py
```

The generator fetches current public pages from `https://www.zeip.fi`, reads the
extracted D7 CSV files, and writes the Jekyll content tree.

Imported D7 scope:

- includes published `article` nodes only
- excludes comments, users, sessions, webforms, logs, cache tables, and
  unpublished nodes

## Development

Install dependencies locally:

```bash
bundle config set path vendor/bundle
bundle install
```

Build:

```bash
bundle exec jekyll build
```

Serve locally:

```bash
bundle exec jekyll serve
```

Then open `http://localhost:4000`.

## Generated Routes

The static build generates:

- `/sitemap.xml`
- `/robots.txt`
- `/fi/rss.xml`
- `/en/rss.xml`
- legacy redirect pages for known Drupal paths, article aliases, node URLs, and
  feed aliases

Important redirects include:

- `/` -> `/fi/`
- `/blog` -> `/fi/blogi/`
- `/rss.xml` -> `/fi/rss.xml`
- D7 `/artikkeli/...` and `/article/...` aliases -> canonical static articles
- D7 `/node/:id`, `/fi/node/:id`, and `/en/node/:id` -> canonical static articles

## Sensitive Files

The raw database dump and extracted database CSVs are sensitive. They include
data that should not be published as web assets or committed to a public
repository without review:

- `d7_zeipeu-beforeremoval-20260810.sql`
- `extracted_db_dump/`

Jekyll excludes these from the generated site in `_config.yml`, but repository
publishing should still treat them carefully.
