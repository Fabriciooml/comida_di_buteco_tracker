# Webapp Visual Redesign — Design Spec

**Date:** 2026-04-12
**Status:** Approved

---

## Context

The app has a working dark navy/coral theme but feels unpolished — system fonts, raw hex color literals scattered across four components, no design token layer, and light-themed dialogs that don't match the dark sidebar. The goal is a full visual redesign that gives the app a coherent "Brazilian boteco" personality: warm, earthy, dark, inviting. The redesign introduces a CSS custom properties token system so the entire palette can be tuned from one place, adds Syne + DM Sans typography, and delivers a set of targeted UX improvements (branded header, redesigned cards and chips, loading state, image placeholder, SVG close icons).

---

## Design Decisions

| Decision | Choice |
|----------|--------|
| Palette | Brazilian Warmth — dark amber/terracotta/warm green |
| Typography | Syne (headings) + DM Sans (body) via Google Fonts |
| Implementation | CSS custom properties token system (no new dependencies) |
| Scope | Full redesign: all 4 components + App.vue + new style.css |

---

## Design Token System

A new `frontend/src/style.css` defines all tokens at `:root`. Imported once in `main.js`. No component uses raw hex after this change.

**Color tokens:**

```css
:root {
  --color-bg:              #1a0a00;   /* page background */
  --color-surface:         #2d1500;   /* cards, drawers, dialogs */
  --color-surface-hover:   #3d1f05;   /* hover state for surfaces */
  --color-border:          #5c3a1e;   /* borders, dividers */
  --color-accent:          #f4a261;   /* amber — primary accent */
  --color-accent-alt:      #e76f51;   /* terracotta — dish names, secondary */
  --color-text-primary:    #f0dfc0;   /* headings, bar names */
  --color-text-secondary:  #c9a882;   /* body text, descriptions */
  --color-text-muted:      #a08060;   /* meta, timestamps, counts */
  --color-vegan-bg:        #386641;
  --color-vegan-text:      #a7c957;
  --color-veg-bg:          #1a4a6b;
  --color-veg-text:        #90d0f0;
  --color-overlay:         rgba(0,0,0,0.65);
}
```

**Typography tokens:**

```css
:root {
  --font-heading: 'Syne', sans-serif;
  --font-body:    'DM Sans', sans-serif;
}
```

**Spacing/radius tokens:**

```css
:root {
  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-pill: 999px;
  --space-xs:    4px;
  --space-sm:    8px;
  --space-md:    12px;
  --space-lg:    16px;
}
```

---

## Typography

Google Fonts loaded in `index.html` via `<link>` (with `preconnect` hints):

```
Syne:wght@600;700 — headings, bar names, dialog titles, app name
DM Sans:wght@400;500;600 — all body text, labels, UI elements
```

`body` default font set to `var(--font-body)` in `style.css`. Syne applied per-element via CSS class rules.

---

## Component Changes

### `App.vue`
- Remove unscoped `<style>body { margin:0 }</style>` block (covered by `style.css`)
- Add `loading` reactive ref; wrap fetch in try/finally, set `loading = false` in finally
- Add loading overlay: full-screen `--color-bg` background with amber CSS spinner (`border-top-color: var(--color-accent)`) and "Carregando bares..." text

### `BarDrawer.vue`
- **All raw hex → tokens** throughout scoped styles
- **Branded header** inside `drawer-content`: "Comida di Buteco" in Syne amber, "Belo Horizonte" in small muted caps, separated from content by `var(--color-border)` bottom border
- **Filter chips** — pill shape (`--radius-pill`), emoji labels (`🌿 Vegano`, `🥕 Vegetariano`), smooth `0.15s` color/border transitions; separate `.vegan-chip.active` and `.vegetarian-chip.active` rules
- **Bar cards** — `position: relative`; diet badges `position: absolute` top-right; bar name in Syne at `--color-text-primary`; dish in `--color-accent-alt`; address/hours as a `card-meta` flex row with emoji icons (`📍` `🕐`) in `--color-text-muted`; `transform: translateY(-2px)` on hover

### `BarMap.vue`
- Leaflet marker colors are JS-only (CSS cannot reach them)
- Single marker: `fillColor: '#f4a261'` (amber, was coral `#e25c3b`)
- Multi-location marker: `fillColor: '#e76f51'` (terracotta, was purple `#7c3aed`)
- Marker stroke: `color: '#f0dfc0'` (warm off-white, was `#ffffff`)

### `BarDialog.vue`
- Backdrop: `--color-overlay`; dialog surface: `--color-surface` with `--color-border` border
- Bar name heading: Syne, `--color-accent`, large
- Image container: `aspect-ratio: 16/9`, `overflow: hidden`; replaces hard-coded `height: 200px`
- Image error handler (`handleImageError`): removes broken `<img>`, reveals warm placeholder (`🍺` emoji on `--color-bg`)
- Text: body in `--color-text-secondary`, labels in `--color-text-primary`
- Badges: same token-based vegan/veg styles as drawer
- SVG close icon (× path, `stroke="currentColor"`)

### `BarLocationPicker.vue`
- Full dark theme: `--color-surface` surface, `--color-border` border, `--color-overlay` backdrop
- Title in Syne amber
- Bar buttons: `--color-bg` background, hover → `--color-surface-hover` + amber border
- SVG close icon matching dialog

---

## SVG Close Icon

Replaces `✕` text in BarDialog and BarLocationPicker:

```html
<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
  <path d="M2 2L14 14M14 2L2 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
```

Button styled with `display:flex`, `28×28px`, `1px solid var(--color-border)`, `color: var(--color-text-muted)`, hover → `--color-surface-hover`.

---

## Files Changed

| File | Type of change |
|------|---------------|
| `frontend/index.html` | Add Google Fonts links, update body font |
| `frontend/src/style.css` | **New file** — token definitions + global reset |
| `frontend/src/main.js` | Import `./style.css` |
| `frontend/src/App.vue` | Remove redundant style block, add loading state |
| `frontend/src/components/BarDrawer.vue` | Branded header, chip redesign, card layout, all tokens |
| `frontend/src/components/BarMap.vue` | JS marker color values only |
| `frontend/src/components/BarDialog.vue` | Full dark theme, image container, SVG close, tokens |
| `frontend/src/components/BarLocationPicker.vue` | Full dark theme, SVG close, tokens |

Implementation order: `index.html` → `style.css` + `main.js` → `App.vue` → `BarDrawer.vue` → `BarMap.vue` → `BarDialog.vue` → `BarLocationPicker.vue` (steps 4–7 are independent).

---

## Verification

```bash
cd frontend && npm run dev
# open http://localhost:5173
```

- Throttle network in DevTools → loading spinner appears on dark background
- Map markers are amber (single) and terracotta (multi) — no purple remains
- Sidebar: branded header, pill chips with emoji, card name in Syne, dish in terracotta, meta row with icons
- BarDialog: dark surface, Syne amber bar name, 16:9 image, 🍺 placeholder on error, SVG × close
- BarLocationPicker: dark surface, Syne title, amber hover on bar buttons
- DevTools → `<html>` Computed → all `--color-*` tokens visible
- No raw hex (`#0f3460`, `#e94560`, `#fff`, `#333`, etc.) remaining in component `<style>` blocks
