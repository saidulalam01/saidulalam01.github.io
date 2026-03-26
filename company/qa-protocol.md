# QA Protocol — Portfolio Website

## Trigger
After every build (`python3 build.py`) — no exceptions.

## Checklist

### Build Verification
- [ ] `build.py` runs without errors
- [ ] `index.html` generated with expected byte size
- [ ] No Python tracebacks or warnings

### Content Accuracy
- [ ] All data.json sections render correctly
- [ ] No placeholder or Lorem Ipsum text
- [ ] Links point to correct URLs
- [ ] GitHub repo links match current public repos
- [ ] Experience dates are accurate
- [ ] Skill levels are consistent

### Visual / UI
- [ ] Dark theme renders correctly
- [ ] Light theme renders correctly
- [ ] Theme toggle works
- [ ] No text overflow or clipping
- [ ] Images load (profile, certificates, awards)
- [ ] Lightbox opens on image click
- [ ] Consistent spacing and alignment

### Responsive
- [ ] Desktop (1200px+): full layout
- [ ] Tablet (768px): grids collapse, nav works
- [ ] Phone (480px): single column, readable
- [ ] Small phone (375px): no horizontal overflow
- [ ] Hamburger menu opens/closes

### Case Studies
- [ ] Case study switcher (prev/next) works
- [ ] Iframe loads slides
- [ ] "Read Full Document" opens correct HTML
- [ ] Share buttons function (LinkedIn, WhatsApp, Copy Link)
- [ ] "More Case Studies" grid renders

### Interactions
- [ ] Smooth scroll on nav links
- [ ] Active nav highlighting on scroll
- [ ] Scroll animations trigger (fade-in, stagger)
- [ ] Contact form submits via Formspree
- [ ] Success message appears after form submit

### SEO & Meta
- [ ] `<title>` tag correct
- [ ] OG tags present and accurate
- [ ] Twitter card tags present
- [ ] Canonical URL correct
- [ ] Google Analytics script loads
- [ ] sitemap.xml up to date
- [ ] robots.txt correct

### Security
- [ ] No secrets in HTML source
- [ ] No .env values exposed
- [ ] No agent system files in public repo
- [ ] Formspree endpoint is correct (not test)

## QA Report Format
```
## QA Report: Portfolio Website — [Phase/Version]
**Date:** YYYY-MM-DD
**Tester:** [Agent name]
**Build:** index.html ([byte size])

### Results
| Check | Status | Notes |
|-------|--------|-------|
| ... | PASS/FAIL | |

### Issues Found
1. [CRITICAL/WARNING] — description

### Verdict: PASS / PASS WITH WARNINGS / FAIL
```

## File Organization
- QA artifacts → `qa/`
- Temp/debug files → `tmp/` (clean up after use)
- Never save QA files outside the project folder
