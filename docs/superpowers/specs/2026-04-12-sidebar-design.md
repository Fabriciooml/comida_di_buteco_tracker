# Bar List Sidebar — Design Spec

**Date:** 2026-04-12  
**Status:** Approved

## Context

The app is currently a fullscreen map with modal dialogs. There is no way to browse or search bars without clicking map markers. This feature adds a bottom drawer (mobile-first) / left sidebar (desktop) showing bars currently visible on the map, with a search bar and diet filters.

## Layout

- **Mobile (< 768px):** Bottom drawer with three snap states.
- **Desktop (≥ 768px):** Fixed left sidebar, always visible, ~300px wide. No drawer states — just the search bar, filters, and scrollable list.

## Drawer States (mobile)

| State | Height | Contents |
|-------|--------|----------|
| `collapsed` | ~60px | Drag handle + bar count (e.g. "7 bares") |
| `half` | ~50vh | Drag handle + search input + diet toggles + scrollable list |
| `full` | 100vh | Same as half, fills screen |

Transitions triggered by: tapping the handle, or swipe up/down gesture on the handle.

## Bar Card

Each item in the list displays:
- **Banner photo** (`food_image_url`) — full-width, fixed height
- **Bar name** (bold)
- **Dish · Category** (`food_name · food_category`)
- **Badges** — "vegano" (green) and/or "vegetariano" (blue), shown only when true
- **Address**
- **Working hours**

Tapping a card: sets `selectedBar` in `App.vue` (opens `BarDialog`) and flies the map to that bar's coordinates.

## Search & Filters

All filtering is client-side and reactive.

**Pipeline (applied in order):**
1. **Bounds filter** — only bars whose `[latitude, longitude]` is within the current map bounds
2. **Text search** — case-insensitive substring match against: `name`, `food_name`, `address`, `food_category`
3. **Diet toggles** — "Vegano" chip filters to `is_vegan = true`; "Vegetariano" chip filters to `is_vegetarian = true`; both can be active at the same time

Result count shown in the collapsed drawer handle and as a subtitle in the half/full states.

## Components

### New: `BarDrawer.vue`

**Props:**
- `bars: Bar[]` — full list of bars (all bars from API)
- `mapBounds: LatLngBounds | null` — current Leaflet map bounds

**Emits:**
- `bar-selected(bar: Bar)` — user tapped a card

**Internal state:**
- `drawerState: 'collapsed' | 'half' | 'full'`
- `searchQuery: string`
- `filterVegan: boolean`
- `filterVegetarian: boolean`

**Computed:**
- `visibleBars` — filtered by bounds, then text, then diet toggles

### Modified: `BarMap.vue`

- Listen to Leaflet `moveend` and `zoomend` events
- Emit `bounds-changed(bounds: LatLngBounds)` on each

### Modified: `App.vue`

- **Lift bars fetch here** — move `GET /api/bars` fetch from `BarMap.vue` to `App.vue` `onMounted`. Pass `bars` as a prop to both `BarMap` and `BarDrawer`.
- Add `mapBounds` ref (type `LatLngBounds | null`, initial `null`)
- Handle `bounds-changed` from `BarMap` → update `mapBounds`
- Handle `bar-selected` from `BarDrawer` → set `selectedBar`, call a `flyTo` method on `BarMap` via a template ref
- Render `<BarDrawer :bars="bars" :mapBounds="mapBounds" @bar-selected="onBarSelected" />`

## Backend Change

`api/routers/bars.py` — add `food_category` to the SELECT query:

```sql
SELECT id, name, latitude, longitude, food_name, food_image_url,
       food_description, food_category, is_vegan, is_vegetarian,
       address, working_hours
FROM bars WHERE latitude IS NOT NULL AND longitude IS NOT NULL
```

## Files to Modify

| File | Change |
|------|--------|
| `api/routers/bars.py` | Add `food_category` to SELECT |
| `frontend/src/App.vue` | Add `mapBounds` ref, wire `BarDrawer` |
| `frontend/src/components/BarMap.vue` | Accept `bars` prop (remove internal fetch), emit `bounds-changed`, expose `flyTo` via `defineExpose` |
| `frontend/src/components/BarDrawer.vue` | **New file** |

## Verification

1. Run backend: `uvicorn main:app --reload` — confirm `GET /api/bars` returns `food_category` field
2. Open app in browser (mobile viewport) — confirm drawer shows at bottom with handle
3. Pan/zoom map — confirm list updates to show only visible bars
4. Type in search box — confirm filters by name, food, address, category
5. Toggle vegan/vegetarian chips — confirm list filters correctly
6. Tap a bar card — confirm `BarDialog` opens and map flies to that bar
7. Resize to desktop width — confirm drawer becomes a left sidebar
