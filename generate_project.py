#!/usr/bin/env python3
"""
generate_project.py — Project Post Page Generator
Reads a JSON file and outputs a project.html faithful to the portfolio
design system (style.css + project.css).

Usage:
    python generate_project.py                              # project_data.json -> project.html
    python generate_project.py my_project.json             # -> project.html
    python generate_project.py my_project.json output.html # fully custom

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JSON SCHEMA REFERENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{
  "meta": {
    "nav_logo":      "YN.",
    "portfolio_url": "portfolio.html",
    "title_prefix":  "Project",       // plain text before the italic word
    "title_italic":  "Alpha",         // rendered in DM Serif italic
    "number":        "05",
    "tagline":       "One-sentence hook.",
    "status":        "In Progress",
    "year":          "2024",
    "role":          "Lead Developer",
    "stack":         "Python · PyTorch",
    "tags":          ["Machine Learning", "NLP"],
    "links": [
      { "label": "GitHub ↗", "url": "https://..." }
    ],
    "prev_project": { "label": "← Prev", "url": "#" },   // optional
    "next_project": { "label": "Next →", "url": "#" }    // optional
  },

  "sections": [
    {
      "id":    "overview",
      "title": "Overview",
      "blocks": [ ...block objects... ]
    }
  ]
}

━━ BLOCK TYPES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

paragraph
  "style":  "body" (default) | "lead" (larger intro text)
  "text":   "Plain text content."

image
  "src":     "path/to/image.png"  (empty string → placeholder shown)
  "alt":     "Description for screen readers"
  "label":   "Fig. 1"             (optional, shown bold before caption)
  "caption": "Caption text."      (optional)

callout
  "stats": [{ "num": "94.2%", "label": "Accuracy" }, ...]
  Renders a bordered grid of big key stats. 1–4 stats look best.

quote
  "text":  "The quoted text."
  "cite":  "— Author Name"  (optional)

bullet_list
  "style": "simple" (dash markers) | "boxed" (bordered rows)
  "title": "Optional heading above the list"   (optional)
  "items": ["Item one.", "Item two."]

numbered_list
  "style": "simple"  — inline mono numbers, plain list
           "steps"   — big ghost numbers, title + description per item
           "boxed"   — bordered rows with number column
           "next"    — the auto-numbered "what's next" style
  "title": "Optional heading above the list"   (optional)
  "items": strings for simple/boxed/next
           objects { "title": "...", "text": "..." } for steps

code
  "lang":     "Python"         (shown in header bar)
  "filename": "model.py"       (optional, shown right of header)
  "code":     "..."            (raw code string; use \n for newlines)

table
  "headers": ["Col A", "Col B", "Col C"]
  "rows": [
    { "cells": ["val", "val", "val"], "highlight": false },
    { "cells": ["**bold**", "val"],   "highlight": true  }
  ]
  Cells support **bold** wrapping.

challenges
  "items": [{ "title": "Challenge title.", "text": "Explanation." }]
  Renders bordered cards with a dot marker.
"""

import json
import re
import sys
from html import escape
from pathlib import Path


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def e(text: str) -> str:
    """HTML-escape plain text."""
    return escape(str(text), quote=True)


def bold(text: str) -> str:
    """Replace **word** with <strong>word</strong>, then escape the rest."""
    parts = re.split(r'\*\*(.+?)\*\*', str(text))
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append(f'<strong>{e(part)}</strong>')
        else:
            out.append(e(part))
    return ''.join(out)


# ─────────────────────────────────────────────
# Block renderers
# ─────────────────────────────────────────────

def render_paragraph(block: dict) -> str:
    style = block.get('style', 'body')
    cls = ' class="lead"' if style == 'lead' else ''
    return f'<p{cls}>{e(block["text"])}</p>\n'


def render_image(block: dict) -> str:
    src     = block.get('src', '')
    alt     = block.get('alt', '')
    caption = block.get('caption', '')
    label   = block.get('label', '')

    if src:
        img_html = f'<img src="{e(src)}" alt="{e(alt)}">'
    else:
        # Placeholder
        img_html = (
            '<div class="proj-figure-placeholder">'
            '<div class="proj-figure-icon">'
            '<span></span><span></span><span></span><span></span>'
            '</div>'
            f'<p class="proj-figure-caption-text">{e(alt) or "Image placeholder"}</p>'
            '</div>'
        )

    caption_html = ''
    if caption or label:
        label_part = f'<strong>{e(label)}</strong> — ' if label else ''
        caption_html = (
            f'<p class="proj-image-caption">{label_part}{e(caption)}</p>'
        )

    return (
        '<div class="proj-image">\n'
        f'  {img_html}\n'
        f'  {caption_html}\n'
        '</div>\n'
    )


def render_callout(block: dict) -> str:
    stats = block.get('stats', [])
    cols = max(1, len(stats))
    # Override grid columns dynamically via inline style
    inner_style = f'grid-template-columns: repeat({cols}, 1fr);'
    items_html = ''
    for stat in stats:
        items_html += (
            '<div class="proj-stat">'
            f'<span class="proj-stat-num">{e(stat["num"])}</span>'
            f'<span class="proj-stat-label">{e(stat["label"])}</span>'
            '</div>'
        )
    return (
        '<div class="proj-callout">\n'
        f'  <div class="proj-callout-inner" style="{inner_style}">\n'
        f'    {items_html}\n'
        '  </div>\n'
        '</div>\n'
    )


def render_quote(block: dict) -> str:
    cite_html = ''
    if block.get('cite'):
        cite_html = f'<cite>{e(block["cite"])}</cite>'
    return (
        '<blockquote class="proj-quote">\n'
        f'  {e(block["text"])}\n'
        f'  {cite_html}\n'
        '</blockquote>\n'
    )


def render_bullet_list(block: dict) -> str:
    style = block.get('style', 'simple')
    items = block.get('items', [])
    title_html = _block_title(block.get('title', ''))

    css_class = {
        'simple': 'proj-list--simple',
        'boxed':  'proj-list--boxed',
    }.get(style, 'proj-list--simple')

    lis = ''.join(f'<li>{e(item)}</li>\n' for item in items)
    return (
        f'{title_html}'
        f'<ul class="{css_class}">\n'
        f'{lis}'
        '</ul>\n'
    )


def render_numbered_list(block: dict) -> str:
    style = block.get('style', 'simple')
    items = block.get('items', [])
    title_html = _block_title(block.get('title', ''))

    if style == 'steps':
        # Items must be dicts with title + text
        rows = ''
        for i, item in enumerate(items, 1):
            t = item if isinstance(item, dict) else {'title': str(item), 'text': ''}
            rows += (
                '<div class="proj-step">'
                f'<div class="proj-step-num">{i}</div>'
                '<div class="proj-step-body">'
                f'<strong>{e(t.get("title", ""))}</strong>'
                f'<p>{e(t.get("text", ""))}</p>'
                '</div>'
                '</div>\n'
            )
        return (
            f'{title_html}'
            '<div class="proj-steps">\n'
            f'{rows}'
            '</div>\n'
        )

    elif style == 'next':
        lis = ''.join(
            f'<li data-n="{str(i).zfill(2)}">{e(item)}</li>\n'
            for i, item in enumerate(items, 1)
        )
        return (
            f'{title_html}'
            '<ul class="proj-next-list">\n'
            f'{lis}'
            '</ul>\n'
        )

    elif style == 'boxed':
        lis = ''.join(
            f'<li>{bold(item) if isinstance(item, str) else bold(item.get("text", ""))}</li>\n'
            for item in items
        )
        return (
            f'{title_html}'
            '<ol class="proj-numbered--boxed">\n'
            f'{lis}'
            '</ol>\n'
        )

    else:  # simple
        lis = ''.join(
            f'<li>{bold(item) if isinstance(item, str) else bold(item.get("text", ""))}</li>\n'
            for item in items
        )
        return (
            f'{title_html}'
            '<ol class="proj-numbered--simple">\n'
            f'{lis}'
            '</ol>\n'
        )


def render_code(block: dict) -> str:
    lang     = block.get('lang', '')
    filename = block.get('filename', '')
    code     = block.get('code', '')
    return (
        '<div class="proj-code-block">\n'
        '  <div class="proj-code-header">'
        f'<span class="proj-code-lang">{e(lang)}</span>'
        f'<span class="proj-code-file">{e(filename)}</span>'
        '</div>\n'
        f'  <pre class="proj-code"><code>{e(code)}</code></pre>\n'
        '</div>\n'
    )


def render_table(block: dict) -> str:
    headers = block.get('headers', [])
    rows    = block.get('rows', [])

    th_html = ''.join(f'<th>{e(h)}</th>' for h in headers)
    rows_html = ''
    for row in rows:
        cells    = row.get('cells', [])
        highlight = row.get('highlight', False)
        tr_class = ' class="proj-table-highlight"' if highlight else ''
        tds = ''.join(f'<td>{bold(c)}</td>' for c in cells)
        rows_html += f'<tr{tr_class}>{tds}</tr>\n'

    return (
        '<div class="proj-table-wrap">\n'
        '  <table class="proj-table">\n'
        f'    <thead><tr>{th_html}</tr></thead>\n'
        f'    <tbody>\n{rows_html}    </tbody>\n'
        '  </table>\n'
        '</div>\n'
    )


def render_challenges(block: dict) -> str:
    items = block.get('items', [])
    cards = ''
    for item in items:
        cards += (
            '<div class="proj-challenge">'
            '<div class="proj-challenge-header">'
            '<span class="proj-challenge-dot"></span>'
            f'<strong>{e(item.get("title", ""))}</strong>'
            '</div>'
            f'<p>{e(item.get("text", ""))}</p>'
            '</div>\n'
        )
    return (
        '<div class="proj-challenges">\n'
        f'{cards}'
        '</div>\n'
    )


def _block_title(title: str) -> str:
    if not title:
        return ''
    return f'<p class="proj-block-title">{e(title)}</p>\n'


# Map type strings to renderer functions
RENDERERS = {
    'paragraph':     render_paragraph,
    'image':         render_image,
    'callout':       render_callout,
    'quote':         render_quote,
    'bullet_list':   render_bullet_list,
    'numbered_list': render_numbered_list,
    'code':          render_code,
    'table':         render_table,
    'challenges':    render_challenges,
}


def render_block(block: dict) -> str:
    btype = block.get('type', '')
    renderer = RENDERERS.get(btype)
    if renderer is None:
        return f'<!-- unknown block type: {e(btype)} -->\n'
    return renderer(block)


# ─────────────────────────────────────────────
# Page builders
# ─────────────────────────────────────────────

def build_nav(meta: dict, sections: list) -> str:
    logo = e(meta.get('nav_logo', 'YN.'))
    portfolio = e(meta.get('portfolio_url', 'portfolio.html'))

    mobile_items = ''
    for i, sec in enumerate(sections, 1):
        sid   = e(sec.get('id', ''))
        title = e(sec.get('title', ''))
        num   = str(i).zfill(2)
        mobile_items += (
            f'    <a href="#{sid}" class="mobile-menu-item">\n'
            f'      <div class="mobile-menu-left">'
            f'<span class="mobile-menu-num">{num}</span>'
            f'<span class="mobile-menu-label">{title}</span></div>\n'
            f'      <span class="mobile-menu-arrow">&#8595;</span>\n'
            f'    </a>\n'
        )

    return f"""  <!-- NAV -->
  <nav>
    <a href="{portfolio}" class="nav-logo">{logo}</a>
    <div class="nav-links">
      <a href="{portfolio}#about">About</a>
      <a href="{portfolio}#academics">Academics</a>
      <a href="{portfolio}#experience">Experience</a>
      <a href="{portfolio}#skills">Skills</a>
      <a href="{portfolio}#projects">Projects</a>
    </div>
    <button class="nav-hamburger" id="hamburger" aria-label="Toggle menu">
      <span></span><span></span><span></span>
    </button>
  </nav>

  <!-- MOBILE MENU -->
  <div class="mobile-menu" id="mobileMenu">
{mobile_items}  </div>"""


def build_header(meta: dict) -> str:
    portfolio   = e(meta.get('portfolio_url', 'portfolio.html'))
    prefix      = e(meta.get('title_prefix', ''))
    italic      = e(meta.get('title_italic', ''))
    number      = e(meta.get('number', '01'))
    tagline     = e(meta.get('tagline', ''))
    status      = e(meta.get('status', ''))
    year        = e(meta.get('year', ''))
    role        = e(meta.get('role', ''))
    stack       = e(meta.get('stack', ''))
    tags        = meta.get('tags', [])
    links       = meta.get('links', [])

    tags_html  = ''.join(f'<span class="proj-tag">{e(t)}</span>' for t in tags)
    links_html = ''.join(
        f'<a href="{e(l["url"])}" class="proj-ext-link" target="_blank" rel="noopener">{e(l["label"])}</a>'
        for l in links
    )

    return f"""  <!-- PROJECT HEADER -->
  <header class="proj-header">
    <div class="proj-header-meta">
      <a href="{portfolio}#projects" class="proj-back">← All Projects</a>
      <div class="proj-meta-block">
        <div class="proj-meta-row">
          <span class="proj-meta-label">Status</span>
          <span class="proj-meta-value proj-status-badge">{status}</span>
        </div>
        <div class="proj-meta-row">
          <span class="proj-meta-label">Year</span>
          <span class="proj-meta-value">{year}</span>
        </div>
        <div class="proj-meta-row">
          <span class="proj-meta-label">Role</span>
          <span class="proj-meta-value">{role}</span>
        </div>
        <div class="proj-meta-row">
          <span class="proj-meta-label">Stack</span>
          <span class="proj-meta-value">{stack}</span>
        </div>
        <div class="proj-meta-row">
          <span class="proj-meta-label">Links</span>
          <div class="proj-link-group">{links_html}</div>
        </div>
      </div>
      <div class="proj-dot-cluster">
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span>
      </div>
    </div>
    <div class="proj-header-title">
      <p class="proj-number">{number} / Project</p>
      <h1 class="proj-title">{prefix}<br><em>{italic}</em></h1>
      <p class="proj-tagline">{tagline}</p>
      <div class="proj-tag-row">{tags_html}</div>
    </div>
  </header>"""


def build_toc(sections: list) -> str:
    items_html = ''
    for i, sec in enumerate(sections, 1):
        num   = str(i).zfill(2)
        sid   = e(sec.get('id', ''))
        title = e(sec.get('title', ''))
        items_html += (
            f'<a href="#{sid}" class="proj-toc-item">'
            f'<span class="proj-toc-num">{num}</span> {title}'
            '</a>'
        )
    return f"""  <!-- TABLE OF CONTENTS -->
  <nav class="proj-toc" id="toc">
    <button class="proj-toc-toggle" id="tocToggle" aria-label="Toggle contents">
      <span class="proj-toc-toggle-label">Contents</span>
      <span class="proj-toc-toggle-arrow">&#8595;</span>
    </button>
    <div class="proj-toc-links" id="tocLinks">{items_html}</div>
  </nav>"""


def build_sidebar(sections: list) -> str:
    links_html = ''
    for sec in sections:
        sid   = e(sec.get('id', ''))
        title = e(sec.get('title', ''))
        links_html += (
            f'<a href="#{sid}" class="proj-sidebar-link" data-section="{sid}">{title}</a>\n'
        )
    return f"""    <aside class="proj-sidebar" id="sidebar">
      <p class="proj-sidebar-label">On this page</p>
      {links_html}
    </aside>"""


def build_sections(sections: list) -> str:
    html = ''
    for i, sec in enumerate(sections, 1):
        num    = str(i).zfill(2)
        sid    = e(sec.get('id', f'section-{i}'))
        title  = e(sec.get('title', ''))
        blocks = sec.get('blocks', [])

        blocks_html = ''.join(render_block(b) for b in blocks)

        html += f"""      <section class="proj-section" id="{sid}">
        <div class="proj-section-header">
          <span class="proj-section-num">{num}</span>
          <h2 class="proj-section-title">{title}</h2>
        </div>
        <div class="proj-content">
{blocks_html}        </div>
      </section>\n"""
    return html


def build_footer(meta: dict) -> str:
    portfolio = e(meta.get('portfolio_url', 'portfolio.html'))
    prev = meta.get('prev_project')
    nxt  = meta.get('next_project')
    prev_html = f'<a href="{e(prev["url"])}" class="proj-footer-sibling">{e(prev["label"])}</a>' if prev else ''
    next_html = f'<a href="{e(nxt["url"])}"  class="proj-footer-sibling">{e(nxt["label"])}</a>'  if nxt  else ''
    return f"""  <footer class="proj-footer">
    <div class="proj-footer-inner">
      <a href="{portfolio}#projects" class="proj-footer-back">← Back to Projects</a>
      <div class="footer-dots">
        <span></span><span></span><span></span><span></span><span></span>
      </div>
      <div class="proj-footer-nav">
        {prev_html}
        {next_html}
      </div>
    </div>
  </footer>"""


# ─────────────────────────────────────────────
# Document assembly
# ─────────────────────────────────────────────

def generate(data: dict) -> str:
    meta     = data.get('meta', {})
    sections = data.get('sections', [])

    prefix = e(meta.get('title_prefix', ''))
    italic = e(meta.get('title_italic', ''))
    full_title = f'{prefix} {italic}'.strip()
    nav_logo   = e(meta.get('nav_logo', 'YN.'))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{full_title} — {nav_logo.rstrip('.')}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  <link rel="stylesheet" href="project.css">
</head>
<body>

{build_nav(meta, sections)}

{build_header(meta)}

{build_toc(sections)}

  <!-- BODY -->
  <main class="proj-body">
{build_sidebar(sections)}
    <article class="proj-article">
{build_sections(sections)}
    </article>
  </main>

{build_footer(meta)}

  <script src="project.js" defer></script>
</body>
</html>"""
    return html


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

def main():
    args        = sys.argv[1:]
    data_path   = Path(args[0]) if len(args) >= 1 else Path('project_data.json')
    output_path = Path(args[1]) if len(args) >= 2 else Path('project.html')

    if not data_path.exists():
        print(f"Error: '{data_path}' not found.")
        sys.exit(1)

    print(f"Reading data from  : {data_path}")
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html = generate(data)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Page written to    : {output_path}")


if __name__ == '__main__':
    main()
