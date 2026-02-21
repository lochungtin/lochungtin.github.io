#!/usr/bin/env python3
"""
generate.py — Portfolio HTML Generator
Usage:  python generate.py [data.json] [output.html]
        python generate.py                          # uses data.json -> portfolio.html
        python generate.py my_data.json             # uses my_data.json -> portfolio.html
        python generate.py my_data.json out.html    # fully custom paths
"""

import json
import sys
from html import escape
from pathlib import Path

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────


def e(text: str) -> str:
    """HTML-escape plain text (does not double-escape already-safe markup)."""
    return escape(str(text), quote=True)


def skill_bar_item(skill: dict) -> str:
    return f"""
            <div class="skill-item">
              <div class="skill-item-top">
                <span class="skill-name">{e(skill['name'])}</span>
                <span class="skill-level">{e(skill['level'])}</span>
              </div>
              <div class="skill-bar"><div class="skill-bar-fill" style="width:{int(skill['pct'])}%"></div></div>
            </div>"""


def dot_tags(items: list) -> str:
    return "\n".join(f'            <span class="skill-dot-item">{e(item)}</span>' for item in items)


def social_rows(socials: list) -> str:
    rows = []
    for s in socials:
        rows.append(
            f"""
          <a href="{e(s['url'])}" class="social-row">
            <span class="social-name">{e(s['label'])}</span>
            <span class="social-handle">{e(s['handle'])}</span>
            <span class="social-arrow">{s['arrow']}</span>
          </a>"""
        )
    return "\n".join(rows)


def education_entries(entries: list) -> str:
    blocks = []
    for entry in entries:
        tag_html = (
            f'\n          <span class="entry-tag">{e(entry["tag"])}</span>'
            if entry.get("tag")
            else ""
        )
        blocks.append(
            f"""
        <div class="entry">
          <p class="entry-year">{e(entry['years'])}</p>
          <p class="entry-title">{e(entry['degree'])}</p>
          <p class="entry-sub">{e(entry['institution'])}</p>
          <p class="entry-desc">{e(entry['description'])}</p>{tag_html}
        </div>"""
        )
    return "\n".join(blocks)


def achievement_entries(entries: list) -> str:
    blocks = []
    for entry in entries:
        blocks.append(
            f"""
        <div class="entry">
          <p class="entry-year">{e(entry['year'])}</p>
          <p class="entry-title">{e(entry['title'])}</p>
          <p class="entry-sub">{e(entry['body'])}</p>
          <p class="entry-desc">{e(entry['description'])}</p>
        </div>"""
        )
    return "\n".join(blocks)


def conference_cards(items: list) -> str:
    cards = []
    for i, item in enumerate(items, 1):
        cards.append(
            f"""
        <div class="pub-card">
          <div class="pub-number">{i:02d}</div>
          <p class="pub-type">{e(item['type'])}</p>
          <p class="pub-title">{e(item['title'])}</p>
          <p class="pub-venue">{e(item['venue'])}</p>
          <p class="pub-year">{e(item['year'])}</p>
        </div>"""
        )
    return "\n".join(cards)


def pub_cards(items: list) -> str:
    cards = []
    for i, item in enumerate(items, 1):
        cards.append(
            f"""
        <div class="pub-card">
          <div class="pub-number">{i:02d}</div>
          <p class="pub-type">{e(item['type'])}</p>
          <p class="pub-title">{e(item['title'])}</p>
          <p class="pub-venue">{e(item['venue'])}</p>
          <p class="pub-year">{e(item.get('year_doi', item.get('year', '')))}</p>
        </div>"""
        )
    return "\n".join(cards)


def experience_rows(jobs: list) -> str:
    rows = []
    for job in jobs:
        highlights_html = "\n".join(
            f'            <span class="exp-highlight">{e(h)}</span>'
            for h in job.get("highlights", [])
        )
        tags_html = "\n".join(
            f'            <span class="exp-skill-tag">{e(t)}</span>' for t in job.get("tags", [])
        )
        rows.append(
            f"""
      <div class="exp-row">
        <div class="exp-meta">
          <span class="exp-date">{e(job['date'])}</span>
          <span class="exp-type">{e(job['type'])}</span>
        </div>
        <div class="exp-body">
          <p class="exp-role">{e(job['role'])}</p>
          <p class="exp-company">{e(job['company'])}</p>
          <p class="exp-desc">{e(job['description'])}</p>
          <div class="exp-highlights">
{highlights_html}
          </div>
        </div>
        <div class="exp-side">
          <div class="exp-tag-list">
{tags_html}
          </div>
        </div>
      </div>"""
        )
    return "\n".join(rows)


def project_rows(projects: list) -> str:
    rows = []
    for i, proj in enumerate(projects, 1):
        rows.append(
            f"""
      <a href="{e(proj['url'])}" target="_blank" rel="noopener" class="project-row">
        <span class="project-num">{i:02d}</span>
        <div class="project-main">
          <span class="project-name">{e(proj['name'])}</span>
          <span class="project-sub">{e(proj['description'])}</span>
        </div>
        <span class="project-tech">{e(proj['tech'])}</span>
        <span class="project-link">&#8599;</span>
      </a>"""
        )
    return "\n".join(rows)


def about_paragraphs(paragraphs: list) -> str:
    return "<br><br>\n          ".join(e(p) for p in paragraphs)


# ─────────────────────────────────────────────
# Main generator
# ─────────────────────────────────────────────


def generate(data: dict) -> str:
    m = data["meta"]
    ab = data["about"]
    ac = data["academics"]
    exp = data["experience"]
    sk = data["skills"]
    pr = data["projects"]

    lang_count = f"{len(sk['languages']):02d} languages"
    lib_count = f"{len(sk['libraries']):02d} libraries"
    spoken_count = f"{len(sk['spoken_languages']):02d} languages"

    lang_bars = "".join(skill_bar_item(s) for s in sk["languages"])
    lib_bars = "".join(skill_bar_item(s) for s in sk["libraries"])
    spoken_bars = "".join(skill_bar_item(s) for s in sk["spoken_languages"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Portfolio &mdash; {e(m['name'])}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <!-- NAV -->
  <nav>
    <a href="#" class="nav-logo">{e(m['initials'])}</a>
    <div class="nav-links">
      <a href="#about">About</a>
      <a href="#academics">Academics</a>
      <a href="#experience">Experience</a>
      <a href="#skills">Skills</a>
      <a href="#projects">Projects</a>
    </div>
    <button class="nav-hamburger" id="hamburger" aria-label="Toggle menu">
      <span></span><span></span><span></span>
    </button>
  </nav>

  <!-- MOBILE MENU -->
  <div class="mobile-menu" id="mobileMenu">
    <a href="#about"      class="mobile-menu-item">
      <div class="mobile-menu-left"><span class="mobile-menu-num">01</span><span class="mobile-menu-label">About Me</span></div>
      <span class="mobile-menu-arrow">&#8595;</span>
    </a>
    <a href="#academics"  class="mobile-menu-item">
      <div class="mobile-menu-left"><span class="mobile-menu-num">02</span><span class="mobile-menu-label">Academics</span></div>
      <span class="mobile-menu-arrow">&#8595;</span>
    </a>
    <a href="#experience" class="mobile-menu-item">
      <div class="mobile-menu-left"><span class="mobile-menu-num">03</span><span class="mobile-menu-label">Experience</span></div>
      <span class="mobile-menu-arrow">&#8595;</span>
    </a>
    <a href="#skills"     class="mobile-menu-item">
      <div class="mobile-menu-left"><span class="mobile-menu-num">04</span><span class="mobile-menu-label">Skills</span></div>
      <span class="mobile-menu-arrow">&#8595;</span>
    </a>
    <a href="#projects"   class="mobile-menu-item">
      <div class="mobile-menu-left"><span class="mobile-menu-num">05</span><span class="mobile-menu-label">Projects</span></div>
      <span class="mobile-menu-arrow">&#8595;</span>
    </a>
  </div>

  <!-- HERO -->
  <section id="hero">
    <div class="hero-left">
      <div class="hero-dot-grid">
        <span></span><span></span><span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span><span></span><span></span>
      </div>
      <div>
        <p class="hero-tag">Portfolio &mdash; {e(m['year'])}</p>
      </div>
      <div>
        <h1 class="hero-name">{e(m['name'])}</h1>
        <p class="hero-title">{e(m['title'])}</p>
      </div>
      <p class="scroll-indicator">Scroll to explore</p>
    </div>
    <div class="hero-right">
      <div class="hero-index">
        <div class="hero-index-item"><span>01</span> About Me</div>
        <div class="hero-index-item"><span>02</span> Education</div>
        <div class="hero-index-item"><span>03</span> Achievements</div>
        <div class="hero-index-item"><span>04</span> Publications</div>
        <div class="hero-index-item"><span>05</span> Experience</div>
        <div class="hero-index-item"><span>06</span> Skills</div>
        <div class="hero-index-item"><span>07</span> Projects</div>
      </div>
      <p class="hero-bio">
        {m['bio']}
      </p>
      <div></div>
    </div>
  </section>

  <!-- ABOUT -->
  <section id="about">
    <div class="section-header">
      <div class="section-number">01</div>
      <h2 class="section-title">About Me</h2>
      <div class="section-dots"><span></span><span></span><span></span></div>
    </div>
    <div class="about-grid">
      <div class="about-col fade-in">
        <p class="about-label">Who I Am</p>
        <p class="about-body">
          {about_paragraphs(ab['paragraphs'])}
        </p>
      </div>
      <div class="about-col fade-in">
        <p class="about-label">Connect</p>
        <div class="socials">
          {social_rows(ab['socials'])}
        </div>
      </div>
    </div>
  </section>

  <!-- ACADEMICS -->
  <section id="academics">
    <div class="section-header">
      <div class="section-number">02</div>
      <h2 class="section-title">Academics</h2>
      <div class="section-dots"><span></span><span></span><span></span></div>
    </div>

    <div class="academics-body">
      <div class="academics-col fade-in">
        <div class="subsection-label">Education</div>
        {education_entries(ac['education'])}
      </div>
      <div class="academics-col fade-in">
        <div class="subsection-label">Online Certificates</div>
        {achievement_entries(ac['certificates'])}
      </div>
    </div>

    <div class="subsection-full fade-in">
      <div class="subsection-label" style="padding: 1.5rem 3rem; border-bottom: var(--line-thin);">Conference Presentations</div>
      <div class="pub-grid">
        {conference_cards(ac['conferences'])}
      </div>
    </div>

    <div class="subsection-full fade-in">
      <div class="subsection-label" style="padding: 1.5rem 3rem; border-bottom: var(--line-thin);">Publications</div>
      <div class="pub-grid">
        {pub_cards(ac['publications'])}
      </div>
    </div>
  </section>

  <!-- WORK EXPERIENCE -->
  <section id="experience">
    <div class="section-header">
      <div class="section-number">03</div>
      <h2 class="section-title">Experience</h2>
      <div class="section-dots"><span></span><span></span><span></span></div>
    </div>
    <div class="exp-list fade-in">
      {experience_rows(exp)}
    </div>
  </section>

  <!-- SKILLS -->
  <section id="skills">
    <div class="section-header">
      <div class="section-number">04</div>
      <h2 class="section-title">Skills</h2>
      <div class="section-dots"><span></span><span></span><span></span></div>
    </div>

    <div class="skills-body fade-in">

      <div class="skills-col">
        <div class="skill-category">
          <div class="skill-cat-header">
            <span class="skill-cat-name">Programming Languages</span>
            <span class="skill-cat-count">{lang_count}</span>
          </div>
          <div class="skill-items">
            {lang_bars}
          </div>
        </div>
        <div class="skill-category">
          <div class="skill-cat-header">
            <span class="skill-cat-name">ML / Data Libraries</span>
            <span class="skill-cat-count">{lib_count}</span>
          </div>
          <div class="skill-items">
            {lib_bars}
          </div>
        </div>
      </div>

      <div class="skills-col">
        <div class="skill-category">
          <div class="skill-cat-header">
            <span class="skill-cat-name">Frameworks &amp; Tools</span>
            <span class="skill-cat-count">Tags</span>
          </div>
          <div class="skill-dots-grid">
            {dot_tags(sk['tools'])}
          </div>
        </div>
        <div class="skill-category">
          <div class="skill-cat-header">
            <span class="skill-cat-name">Domain Expertise</span>
            <span class="skill-cat-count">Tags</span>
          </div>
          <div class="skill-dots-grid">
            {dot_tags(sk['domains'])}
          </div>
        </div>
        <div class="skill-category">
          <div class="skill-cat-header">
            <span class="skill-cat-name">Languages (spoken)</span>
            <span class="skill-cat-count">{spoken_count}</span>
          </div>
          <div class="skill-items">
            {spoken_bars}
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- PROJECTS -->
  <section id="projects">
    <div class="section-header">
      <div class="section-number">05</div>
      <h2 class="section-title">Projects</h2>
      <div class="section-dots"><span></span><span></span><span></span></div>
    </div>
    <div class="project-list fade-in">
      {project_rows(pr)}
    </div>
  </section>

  <!-- FOOTER -->
  <footer>
    <div class="footer-name">{e(m['name'])}.</div>
    <div class="footer-dots">
      <span></span><span></span><span></span><span></span><span></span>
    </div>
    <div class="footer-copy">&copy; {e(m['year'])} &mdash; All rights reserved</div>
  </footer>

  <script src="main.js" defer></script>
</body>
</html>"""

    return html


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────


def main():
    args = sys.argv[1:]
    data_path = Path(args[0]) if len(args) >= 1 else Path("data.json")
    output_path = Path(args[1]) if len(args) >= 2 else Path("portfolio.html")

    if not data_path.exists():
        print(f"Error: data file '{data_path}' not found.")
        sys.exit(1)

    print(f"Reading data from  : {data_path}")
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = generate(data)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Portfolio written to: {output_path}")


if __name__ == "__main__":
    main()
