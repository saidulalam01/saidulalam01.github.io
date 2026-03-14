# Alametria Slide Config
> This file is the source of truth for all slide design decisions.
> Claude reads this before making any changes to slides or adding new case studies.

---

## How to use this file
- Every case study gets an entry below
- Each entry records: which design (01–12) + which color (01–12) was chosen
- When adding a new case study, copy the template at the bottom
- Design picker: `design-picker.html` | Color picker: `theme-picker.html`

---

## Case Study 1 — Retention Intelligence

| Property | Value |
|---|---|
| File | `retention-intelligence-slides.html` |
| Design | `01 — Classic` |
| Color | `11 — Dark Teal + Aqua` |
| Status | Locked |

### Color details
- `--bg`: `#08181a`
- `--card`: `#0f2628`
- `--accent`: `#2dd4bf`
- `--glow`: `rgba(45,212,191,0.14)`
- Bar gradient: `#2dd4bf` → `#22d3ee`
- Gold kept for: money values only

---

## Case Study 2 — Project Boomerang

| Property | Value |
|---|---|
| File | `boomerang-slides.html` |
| Design | `06 — Terminal` |
| Color | `03 — Midnight + Cyan` |
| Status | Locked |

### Color details
- `--bg`: `#09111e`
- `--card`: `#0f1e30`
- `--accent`: `#22d3ee`
- `--glow`: `rgba(34,211,238,0.14)`
- Bar gradient: `#22d3ee` → `#60a5fa`
- Gold kept for: money values only

---

## Template — New Case Study

```
## Case Study N — [Name]

| Property | Value |
|---|---|
| File | `filename-slides.html` |
| Design | `XX — Name` |
| Color | `XX — Name` |
| Status | |

### Color details
- `--bg`:
- `--card`:
- `--accent`:
- `--glow`:
```

---

## Design Reference (12 options)
| # | Name | Vibe |
|---|---|---|
| 01 | Classic | Kicker + bar + heading + stat cards |
| 02 | Split Panel | Left sidebar accent strip |
| 03 | Hero Number | Giant stat dominates |
| 04 | Minimal Lines | Rules only, clean |
| 05 | Dashboard | Metric tiles + progress bars |
| 06 | Terminal | Code/monospace |
| 07 | Executive Brief | Premium negative space |
| 08 | Editorial | Magazine bold type |
| 09 | Blueprint | Technical grid |
| 10 | Heavy Border | Brutalist-clean |
| 11 | Layered Depth | Stacked cards, 3D feel |
| 12 | Data Rows | Spreadsheet/table structure |

## Color Reference (12 options)
| # | Name | BG | Accent |
|---|---|---|---|
| 01 | Indigo + Violet | `#0f0d27` | `#a78bfa` |
| 02 | Teal + Emerald | `#0d221e` | `#34d399` |
| 03 | Midnight + Cyan | `#09111e` | `#22d3ee` |
| 04 | Obsidian + Blue | `#0d1220` | `#60a5fa` |
| 05 | Forest + Lime | `#0b1c0e` | `#86efac` |
| 06 | Charcoal + Amber | `#18120a` | `#fbbf24` |
| 07 | Deep Rose + Pink | `#1a0c16` | `#f472b6` |
| 08 | Dark Rust + Coral | `#1a0e08` | `#fb923c` |
| 09 | Slate + Ice Blue | `#0d1520` | `#bae6fd` |
| 10 | Purple + Gold | `#140d28` | `#f0a830` |
| 11 | Dark Teal + Aqua | `#08181a` | `#2dd4bf` |
| 12 | Near Black + Red | `#160c0c` | `#f87171` |
