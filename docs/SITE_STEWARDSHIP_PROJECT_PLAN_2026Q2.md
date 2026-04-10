# Site Stewardship Project Plan (2026 Q2)

Owner: Sean Luka Girgis  
Steward: Codex  
Scope: `seanlgirgis.github.io`

## Vision

Build a world-class technical brand site that is:

- content-rich (LeetCode, project case studies, idea articles),
- SEO/search-friendly and indexable,
- distribution-aware (LinkedIn/X/newsletter/YouTube),
- fast, accessible, and maintainable.

## Track 1: Information Architecture

Goal: establish clear content lanes and scalable navigation.

- Add/standardize top-level content lanes:
  - Articles
  - LeetCode
  - Projects
  - Tutorials
  - Changelog/Now
- Create a LeetCode hub page with filters/taxonomy:
  - topic, difficulty, pattern, language.
- Add breadcrumbs on post pages where appropriate.

Deliverables:

- IA map doc
- LeetCode hub component/page
- Updated nav links

## Track 2: Content Production System

Goal: make publishing repeatable and consistent.

- Create templates for:
  - LeetCode solution posts
  - Idea/thought articles
  - Project case studies
- Enforce post structure:
  - summary
  - key takeaways
  - complexity (for algorithm posts)
  - downloadable assets
  - internal links + CTA
- Add a publish checklist.

Deliverables:

- `docs/content_templates/*`
- `docs/PUBLISH_CHECKLIST.md`

## Track 3: SEO & Indexing

Goal: improve discoverability and rankings.

- Add canonical URL handling for blog pages.
- Add JSON-LD schema:
  - `Article`
  - `BreadcrumbList`
  - `Person` / `WebSite`
- Ensure sitemap and robots are kept in sync per publish.
- Prepare search submission runbook:
  - Google Search Console
  - Bing Webmaster Tools
  - IndexNow ping.

Deliverables:

- SEO baseline implementation
- `docs/SEO_RUNBOOK.md`

## Track 4: Announcement & Distribution

Goal: ship every new post with multi-channel reach.

- Create per-post promotion pack:
  - LinkedIn short/long variants
  - X/Twitter post
  - newsletter snippet
- Add UTM-tagged URL generation for analytics attribution.
- Add “Latest updates” component on homepage.

Deliverables:

- `docs/distribution/POST_ANNOUNCEMENT_TEMPLATE.md`
- optional script/tooling for UTM link generation

## Track 5: YouTube Integration

Goal: connect article system to video channel growth.

- Define pipeline:
  - article -> script -> storyboard -> video -> embedded post section.
- Add “Watch version” area on relevant posts.
- Start with 2 pilot videos from high-performing posts.

Deliverables:

- `docs/video/VIDEO_PIPELINE.md`
- embedded video section pattern in blog template

## Track 6: Performance & Quality

Goal: world-class UX and reliability.

- Core Web Vitals tuning (LCP, CLS, INP).
- Accessibility pass (headings, alt text, contrast, keyboard checks).
- Image optimization pipeline and consistent code block styles.

Deliverables:

- quality checklist
- before/after metrics snapshot

## 90-Day Milestones

### Phase 1 (Weeks 1-2)

- finalize IA + templates
- implement SEO baseline + metadata standards
- create LeetCode hub scaffold

### Phase 2 (Weeks 3-6)

- publish 8-12 structured posts
- apply project case-study format
- enable announcement workflow

### Phase 3 (Weeks 7-10)

- YouTube pilot integration (2-4 videos)
- cross-channel cadence (LinkedIn + X + newsletter)

### Phase 4 (Weeks 11-12)

- perf/accessibility hardening
- analytics review and plan iteration

## KPI Dashboard (Weekly)

- indexed pages
- organic clicks and impressions
- top landing pages
- average engagement time
- CTA clicks (download/video/contact)
- publish cadence consistency

## Immediate Next 5 Tasks

1. Create content templates (`leetcode`, `idea`, `project`).
2. Create LeetCode hub page skeleton and taxonomy.
3. Implement canonical + JSON-LD on blog template.
4. Create publish checklist + distribution templates.
5. Add changelog/latest-updates block on homepage.
