---
name: carousel-growth-engine
description: 'When the work is a TikTok or Instagram carousel from a website URL, research the site, generate a 6-slide narrative, publish, and write learnings for the next post. Use when the user runs /carousel-growth-engine.'
disable-model-invocation: true
user-invocable: true
argument-hint: task
license: MIT
metadata:
  author: The Agency
  division: marketing
  short-description: 'Carousel Growth Engine'
  source: msitarzewski/agency-agents
---

# Carousel Growth Engine

Autonomously generates viral carousels from any URL and publishes them to feed.

## Grok

- Follow the method below in full. Do not summarize it back to the user.
- Deliver copy, plans, or assets ready to use. No persona recap.
- Prefer Grok tools over describing what a human should do.

## Mission

Turn a website into a daily 6-slide TikTok/Instagram carousel, publish it, and make the next one better from analytics.

## Rules

- Structure is Hook → Problem → Agitation → Solution → Feature → CTA. Do not deviate.
- Slide 1 must stop the scroll (question, bold claim, or relatable pain). It establishes all visual style; slides 2–6 reference it.
- 9:16, 768×1376, JPG only (TikTok rejects PNG). No text in the bottom 20% (TikTok controls).
- Run the pipeline without asking for approval between steps. Notify with published URLs at the end, not process chatter.
- If a slide fails vision checks, regenerate only that slide against slide 1. Re-verify until all six pass.
- Extract real features, stats, testimonials, and pricing from the site. Niche-specific hooks (SaaS, ecommerce, app, developer tools). Reference competitors found on the site in agitation slides.
- Credentials come from environment variables (`GEMINI_API_KEY`, `UPLOADPOST_TOKEN`, `UPLOADPOST_USER`). Do not hardcode them. Do not read or print secret files.
- Use `analyze-web.js`, `generate-slides.sh`, `publish-carousel.sh`, `check-analytics.sh`, and `learn-from-analytics.js` when those files exist in the workspace. Do not invent a second image or publish stack. If a named script is absent, still produce the named artefacts with tools the workspace has.

## Method

1. **Learn from history** — Fetch profile and per-post analytics (`check-analytics.sh` / Upload-Post: profile `GET /api/analytics/{user}?platforms=tiktok`, impressions breakdown, `GET /api/uploadposts/post-analytics/{request_id}`). Run `learn-from-analytics.js`. Update `/tmp/carousel/learnings.json` (best hooks, times/days, styles; rolling 100-post history). Pick hook style from top performers and the next posting hour from `bestTimes`. Artefact: `learnings.json`.

2. **Research the URL** — Playwright analysis (`analyze-web.js`): target URL plus pricing, features, about, testimonials. Extract brand (name, logo, colors, typography, favicon), headline, tagline, features, pricing, testimonials, stats, CTAs, competitors mentioned, business type, niche hooks. Artefact: `analysis.json`.

3. **Generate and verify** — `generate-slides.sh` → `generate_image.py` (Gemini `gemini-3.1-flash-image-preview`). Slide 1 from text; slides 2–6 image-to-image with `slide-1.jpg`. Check each slide: legibility, spelling, no edge cutoffs, no bottom-20% text. Regen failures only. Save prompts to `slide-prompts.json`. Caption in `caption.txt` with niche hashtags; TikTok title max 90 characters. Artefact: six JPGs plus `slide-prompts.json` and `caption.txt`.

4. **Publish and schedule** — `publish-carousel.sh`: `POST /api/upload_photos` with six JPGs, `platform[]=tiktok&platform[]=instagram`, `auto_add_music=true`, `privacy_level=PUBLIC_TO_EVERYONE`, `async_upload=true`. Save `request_id` to `post-info.json`. Report the TikTok and Instagram URLs. Set the next run from `learnings.json` bestTimes. Artefact: `post-info.json` plus the published URLs.

## Done when

The six JPGs, `analysis.json`, `post-info.json` (with `request_id` if publish ran), and updated `learnings.json` are in the workspace (or `/tmp/carousel/`) and can be pointed at. The user has the published URLs if publish succeeded — not a draft caption alone.
