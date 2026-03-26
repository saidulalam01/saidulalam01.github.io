#!/usr/bin/env python3
"""
build.py — Generates index.html from data.json.
Pure Python, zero external dependencies.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data.json"
OUTPUT_FILE = ROOT / "index.html"

# ── SVG icon constants ───────────────────────────────────────────────────────

SVG_SUN = '<svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'

SVG_MOON = '<svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'

SVG_GITHUB = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>'

SVG_GITHUB_26 = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>'

SVG_LINKEDIN_26 = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>'

SVG_EMAIL = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>'

# Project card SVG icons by key
PROJECT_ICONS = {
    "code": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    "document": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
    "layers": '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
}

CONTACT_ICONS = {
    "linkedin": SVG_LINKEDIN_26,
    "github": SVG_GITHUB_26,
}


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ── Section renderers ────────────────────────────────────────────────────────

def render_head(d):
    m = d["meta"]
    og = m["og"]
    tw = m["twitter"]
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={m['ga_id']}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{m['ga_id']}');
  </script>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
  <title>{m['title']}</title>
  <meta name="description" content="{m['description']}">
  <meta name="keywords" content="{m['keywords']}">
  <meta name="author" content="{m['author']}">
  <meta name="google-site-verification" content="{m['google_verification']}" />
  <link rel="canonical" href="{m['canonical_url']}">

  <!-- Open Graph / Social sharing -->
  <meta property="og:type" content="{og['type']}">
  <meta property="og:title" content="{og['title']}">
  <meta property="og:description" content="{og['description']}">
  <meta property="og:url" content="{og['url']}">
  <meta property="og:site_name" content="{og['site_name']}">
  <meta property="og:image" content="{og['image']}">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="{tw['card']}">
  <meta name="twitter:title" content="{tw['title']}">
  <meta name="twitter:description" content="{tw['description']}">
  <meta name="twitter:image" content="{tw['image']}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="stylesheet" href="style.css">
</head>
<body>"""


def render_nav(d):
    nav = d["nav"]
    links = "\n".join(f'        <a href="#{lnk.lower().replace(" ", "-")}">{lnk}</a>' for lnk in nav["links"])
    mobile_links = "\n".join(f'    <a href="#{lnk.lower().replace(" ", "-")}">{lnk}</a>' for lnk in nav["links"])
    return f"""
  <!-- Navigation -->
  <nav class="nav" id="nav">
    <div class="nav-inner">
      <a href="#hero" class="nav-logo">{nav['logo']}<span class="logo-line"></span></a>
      <div class="nav-links" id="navLinks">
{links}
      </div>
      <div class="nav-actions">
        <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme">
          {SVG_SUN}
          {SVG_MOON}
        </button>
        <button class="nav-hamburger" id="hamburger" aria-label="Toggle menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </nav>

  <!-- Mobile Menu -->
  <div class="mobile-menu" id="mobileMenu">
{mobile_links}
  </div>

  <!-- Lightbox Modal -->
  <div class="lightbox" id="lightbox">
    <button class="lb-close" id="lbClose" aria-label="Close">&times;</button>
    <img src="" alt="" class="lb-img" id="lbImg">
  </div>
"""


def render_hero(d):
    h = d["hero"]
    float_cards = ""
    for i, fc in enumerate(h["float_cards"], 1):
        float_cards += f"""        <div class="hero-float-card float-{i}">
          <span class="float-icon">{fc['icon']}</span> {fc['text']}
        </div>\n"""

    stats_parts = []
    for j, s in enumerate(h["quick_stats"]):
        if j > 0:
            stats_parts.append('          <div class="qs-divider"></div>')
        stats_parts.append(f'          <div class="qs"><span class="qs-num">{s["num"]}</span><span class="qs-label">{s["label"]}</span></div>')
    stats_html = "\n".join(stats_parts)

    return f"""
  <!-- Hero -->
  <section class="hero" id="hero">
    <div class="hero-bg-glow"></div>
    <div class="container hero-grid">
      <div class="hero-content">
        <div class="hero-badge">{h['badge']}</div>
        <h1>{h['headline_pre']}<span class="text-gradient">{h['headline_highlight']}</span>{h['headline_post']}</h1>
        <p class="hero-sub">
          {h['sub']}
        </p>
        <div class="hero-cta">
          <a href="{h['cta_primary']['href']}" class="btn btn-primary">{h['cta_primary']['text']}</a>
          <a href="{h['cta_secondary']['href']}" class="btn btn-ghost">{h['cta_secondary']['text']}</a>
        </div>
        <div class="hero-quick-stats">
{stats_html}
        </div>
      </div>
      <div class="hero-photo-wrap">
        <div class="hero-photo-ring">
          <img src="{h['photo']}" alt="{h['photo_alt']}" class="hero-photo">
        </div>
{float_cards.rstrip()}
      </div>
    </div>
    <div class="hero-quote">
      <p>"{h['quote']}"</p>
    </div>
  </section>"""


def render_about(d):
    a = d["about"]
    paragraphs = "\n".join(f"          <p>\n            {p}\n          </p>" for p in a["paragraphs"])

    info_cards = ""
    for ic in a["info_cards"]:
        sub_line = f'\n              <span class="info-sub">{ic["sub"]}</span>' if ic.get("sub") else ""
        info_cards += f"""          <div class="info-card">
            <div class="info-icon">{ic['icon']}</div>
            <div>
              <span class="info-label">{ic['label']}</span>
              <span class="info-value">{ic['value']}</span>{sub_line}
            </div>
          </div>\n"""

    return f"""
  <!-- About -->
  <section class="section" id="about">
    <div class="container">
      <span class="section-label">{a['section_label']}</span>
      <h2 class="section-title">{a['section_title']}</h2>
      <div class="about-layout">
        <div class="about-text">
{paragraphs}
        </div>
        <div class="about-info-cards">
{info_cards.rstrip()}
        </div>
      </div>
    </div>
  </section>"""


def render_experience(d):
    exp = d["experience"]
    items_html = ""
    for item in exp["items"]:
        active_class = " active" if item.get("active") else ""
        bullets = "\n".join(f"              <li>{b}</li>" for b in item["bullets"])
        tags = "".join(f"<span>{t}</span>" for t in item["tags"])
        items_html += f"""
        <div class="exp-item">
          <div class="exp-marker">
            <div class="exp-dot{active_class}"></div>
            <div class="exp-line"></div>
          </div>
          <div class="exp-card">
            <div class="exp-top">
              <div>
                <h3>{item['title']}</h3>
                {'<a href="' + item['company_url'] + '" target="_blank" class="exp-company exp-company-link">' + item['company'] + '</a>' if item.get('company_url') else '<span class="exp-company">' + item['company'] + '</span>'}
              </div>
              <span class="exp-date">{item['date']}</span>
            </div>
            <ul class="exp-bullets">
{bullets}
            </ul>
            <div class="exp-tags">
              {tags}
            </div>
          </div>
        </div>
"""

    return f"""
  <!-- Experience -->
  <section class="section section-alt" id="experience">
    <div class="container">
      <span class="section-label">{exp['section_label']}</span>
      <h2 class="section-title">{exp['section_title']}</h2>
      <div class="exp-timeline">
{items_html}
      </div>
    </div>
  </section>"""


def render_projects(d):
    proj = d["projects"]
    feat = proj["featured"]

    # Featured project outcomes
    outcomes = ""
    for o in feat["outcomes"]:
        outcomes += f"""              <div class="pf-outcome">
                <span class="pf-outcome-num">{o['num']}</span>
                <span class="pf-outcome-text">{o['text']}</span>
              </div>\n"""

    feat_tech = "".join(f"<span>{t}</span>" for t in feat["tech"])

    # Project cards
    cards = ""
    for card in proj["cards"]:
        icon_svg = PROJECT_ICONS.get(card["icon"], PROJECT_ICONS["code"])
        card_tech = "".join(f"<span>{t}</span>" for t in card["tech"])
        cards += f"""        <div class="project-card">
          <div class="pc-icon">
            {icon_svg}
          </div>
          <h3>{card['title']}</h3>
          <p>
            {card['description']}
          </p>
          <div class="pc-tech">
            {card_tech}
          </div>
          <a href="{card['github_url']}" target="_blank" class="pc-link">Source Code &rarr;</a>
        </div>

"""

    # Portfolio items
    portfolio = ""
    for po in proj["portfolio"]:
        if po.get("url"):
            portfolio += f"""          <a href="{po['url']}" target="_blank" class="po-item">
            <span class="po-icon">{po['icon']}</span>
            <div>
              <strong>{po['title']}</strong>
              <p>{po['description']}</p>
            </div>
            <span class="po-arrow">&rarr;</span>
          </a>\n"""
        else:
            portfolio += f"""          <div class="po-item">
            <span class="po-icon">{po['icon']}</span>
            <div>
              <strong>{po['title']}</strong>
              <p>{po['description']}</p>
            </div>
          </div>\n"""

    return f"""
  <!-- Projects -->
  <section class="section" id="projects">
    <div class="container">
      <span class="section-label">{proj['section_label']}</span>
      <h2 class="section-title">{proj['section_title']}</h2>

      <!-- Featured: Insight Agent -->
      <div class="project-featured">
        <div class="pf-badge">{feat['badge']}</div>
        <div class="pf-grid">
          <div class="pf-info">
            <h3>{feat['title']}</h3>
            <p>
              {feat['description']}
            </p>
            <div class="pf-outcomes">
{outcomes.rstrip()}
            </div>
            <div class="pf-tech">
              {feat_tech}
            </div>
            <a href="{feat['github_url']}" target="_blank" class="btn btn-sm">
              {SVG_GITHUB}
              View on GitHub
            </a>
          </div>
        </div>
      </div>

      <!-- Other projects -->
      <div class="projects-row">
{cards.rstrip()}
      </div>

      <!-- Other portfolio work -->
      <div class="portfolio-other">
        <h3>Other Portfolio Work</h3>
        <div class="po-grid">
{portfolio.rstrip()}
        </div>
      </div>
    </div>
  </section>"""


def render_case_studies(d):
    """Case studies shell — content populated by script.js from CS_DATA."""
    return """
  <!-- Case Studies -->
  <section class="section section-alt" id="case-studies">
    <div class="container">
      <span class="section-label">Deep dives</span>
      <h2 class="section-title">Case Studies</h2>

      <div class="cs-grid">

        <!-- ── Featured card ── -->
        <div class="cs-featured">
          <div class="cs-featured-slides">
            <iframe
              id="csIframe"
              src="case-studies/alametria/retention-intelligence-slides.html"
              class="cs-featured-iframe"
              title="Retention Intelligence Slides"
              loading="lazy"
              allowfullscreen
            ></iframe>
          </div>
          <div class="cs-featured-bar">
            <div class="cs-featured-meta">
              <span class="cs-badge" id="csBadge">Case Study</span>
              <span class="cs-badge-sub" id="csBadgeSub">Prop Trading &middot; 2026</span>
            </div>
            <div class="cs-featured-bottom">
              <div>
                <h3 class="cs-featured-title" id="csTitle">Retention Intelligence &mdash; Alametria</h3>
                <p class="cs-featured-desc" id="csDesc">581,000 users. One retention label hiding 10 behaviors. $10.2M combined impact &mdash; from the existing user base alone.</p>
              </div>
              <div class="cs-nav-arrows">
                <button class="cs-arrow-btn" id="csPrev" aria-label="Previous case">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 19l-7-7 7-7"/></svg>
                  Prev Case
                </button>
                <button class="cs-arrow-btn" id="csNext" aria-label="Next case">
                  Next Case
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- ── Sidebar card ── -->
        <div class="cs-doc-card">
          <div class="cs-doc-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5.586a1 1 0 0 1 .707.293l5.414 5.414a1 1 0 0 1 .293.707V19a2 2 0 0 1-2 2z"/></svg>
          </div>
          <h3 class="cs-doc-title" id="csDocTitle">What's Inside</h3>
          <p class="cs-doc-desc" id="csDocDesc">Full methodology, framework, and results. 21 pages covering the complete analytical process from raw transaction data to $10.2M in measurable impact.</p>
          <ul class="cs-checklist" id="csChecklist">
            <li>
              <span class="cs-check"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg></span>
              Behavioral Lifecycle Framework
            </li>
            <li>
              <span class="cs-check"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg></span>
              10-Segment Classification Model
            </li>
            <li>
              <span class="cs-check"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg></span>
              Results &amp; $10.2M Impact Analysis
            </li>
            <li>
              <span class="cs-check"><svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg></span>
              SQL Methodology &amp; Data Sources
            </li>
          </ul>
          <div class="cs-doc-actions">
            <a href="case-studies/alametria/retention-intelligence-casestudy.html" target="_blank" class="cs-doc-btn" id="csReadBtn">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
              Read Full Document
            </a>
            <div class="cs-share-wrap">
              <button class="cs-dl-btn" id="csShareBtn">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
                Share
              </button>
              <div class="cs-share-menu" id="csShareMenu">
                <button class="cs-share-item" onclick="csOpenLinkedIn()">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg>
                  Share on LinkedIn
                </button>
                <button class="cs-share-item" onclick="csOpenWhatsApp()">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
                  Share on WhatsApp
                </button>
                <button class="cs-share-item" onclick="csCopyLink()">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                  <span id="csCopyText">Copy Link</span>
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- ── More Case Studies ── populated by JS ── -->
      <div class="cs-more" id="csMore"></div>

    </div>
  </section>"""


def render_achievements(d):
    ach = d["achievements"]
    certs = d["certifications"]

    items_html = ""
    for item in ach["items"]:
        classes = "ach-card"
        if item.get("featured"):
            classes += " ach-featured"
        if item.get("small"):
            classes += " ach-small"

        img_html = ""
        if item.get("image"):
            if item.get("small"):
                img_html = f'          <img src="{item["image"]}" alt="{item.get("image_alt", "")}" class="ach-img-small clickable-img" data-full="{item["image"]}">\n'
            else:
                img_html = f'          <img src="{item["image"]}" alt="{item.get("image_alt", "")}" class="ach-img clickable-img" data-full="{item["image"]}">\n'

        items_html += f"""        <div class="{classes}">
{img_html}          <div class="ach-info">
            <span class="ach-type">{item['type']}</span>
            <h3>{item['title']}</h3>
            <p>
              {item['description']}
            </p>
          </div>
        </div>

"""

    # Certifications
    cert_cards = ""
    for c in certs["items"]:
        cert_cards += f"""          <div class="cert-card clickable-img" data-full="{c['image']}">
            <img src="{c['image']}" alt="{c['image_alt']}" class="cert-img">
            <div>
              <strong>{c['name']}</strong>
              <span>{c['issuer']}</span>
            </div>
          </div>\n"""

    return f"""
  <!-- Achievements -->
  <section class="section section-alt" id="achievements">
    <div class="container">
      <span class="section-label">{ach['section_label']}</span>
      <h2 class="section-title">{ach['section_title']}</h2>
      <div class="ach-grid">

{items_html.rstrip()}
      </div>

      <!-- Certifications -->
      <div class="certs-section">
        <h3>{certs['title']}</h3>
        <div class="certs-grid">
{cert_cards.rstrip()}
        </div>
      </div>
    </div>
  </section>"""


def render_skills(d):
    sk = d["skills"]
    groups_html = ""
    for g in sk["groups"]:
        domain_class = " domain" if g.get("domain") else ""
        pills = ""
        for p in g["pills"]:
            level_html = f'<span class="pill-level {p["level"]}"></span>' if p.get("level") else ""
            pills += f"            <div class=\"pill\">{level_html}{p['name']}</div>\n"
        groups_html += f"""        <div class="skill-group">
          <h3>{g['name']}</h3>
          <div class="skill-pills{domain_class}">
{pills.rstrip()}
          </div>
        </div>

"""

    legend_items = " ".join(
        f'<span><span class="pill-level {l["level"]}"></span> {l["label"]}</span>'
        for l in sk["legend"]
    )

    return f"""
  <!-- Skills -->
  <section class="section" id="skills">
    <div class="container">
      <span class="section-label">{sk['section_label']}</span>
      <h2 class="section-title">{sk['section_title']}</h2>
      <div class="skills-layout">

{groups_html.rstrip()}

      </div>
      <div class="skill-legend">
        {legend_items}
      </div>
    </div>
  </section>"""


def render_contact(d):
    c = d["contact"]
    circles = ""
    for s in c["socials"]:
        icon_svg = CONTACT_ICONS.get(s["icon"], "")
        circles += f"""        <a href="{s['url']}" target="_blank" class="contact-circle" aria-label="{s['label']}">
          <div class="cc-ring">
            {icon_svg}
          </div>
          <span class="cc-label">{s['label']}</span>
        </a>\n"""

    return f"""
  <!-- Contact -->
  <section class="section section-alt" id="contact">
    <div class="container contact-container">
      <span class="section-label">{c['section_label']}</span>
      <h2 class="section-title">{c['section_title']}</h2>
      <p class="contact-desc">
        {c['description']}
      </p>
      <form class="contact-form" action="{c['formspree_endpoint']}" method="POST" id="contactForm">
        <div class="form-row">
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" name="name" placeholder="Your name" required>
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" placeholder="your@email.com" required>
          </div>
        </div>
        <div class="form-group">
          <label for="subject">Subject</label>
          <input type="text" id="subject" name="subject" placeholder="What's this about?">
        </div>
        <div class="form-group">
          <label for="message">Message</label>
          <textarea id="message" name="message" rows="5" placeholder="Your message..." required></textarea>
        </div>
        <button type="submit" class="form-submit">Send Message</button>
        <div class="form-success" id="formSuccess">Message sent! I'll get back to you soon.</div>
      </form>
      <div class="contact-divider">or find me on</div>
      <div class="contact-circles">
{circles.rstrip()}
      </div>
    </div>
  </section>"""


def render_footer(d):
    f = d["footer"]
    links = "\n".join(
        f'        <a href="{lnk["url"]}" target="_blank">{lnk["label"]}</a>'
        if not lnk["url"].startswith("mailto:")
        else f'        <a href="{lnk["url"]}">{lnk["label"]}</a>'
        for lnk in f["links"]
    )
    return f"""
  <!-- Footer -->
  <footer class="footer">
    <div class="container footer-inner">
      <span>&copy; {f['copyright']}</span>
      <div class="footer-links">
{links}
      </div>
    </div>
  </footer>

  <script src="script.js"></script>
  <script src="https://rahat-bot-api.vercel.app/widget.js" defer></script>
</body>
</html>
"""


def build():
    data = load_data()
    parts = [
        render_head(data),
        render_nav(data),
        render_hero(data),
        render_about(data),
        render_experience(data),
        render_projects(data),
        render_case_studies(data),
        render_achievements(data),
        render_skills(data),
        render_contact(data),
        render_footer(data),
    ]
    html = "\n".join(parts)
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"Built {OUTPUT_FILE} ({len(html)} bytes)")
    return True


if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"Build failed: {e}", file=sys.stderr)
        sys.exit(1)
