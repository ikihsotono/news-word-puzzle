# Backlog

## CNBC top news extraction
- Goal: Prefer "top" or "breaking" CNBC items for daily set.
- Approach options:
  - Use specific CNBC RSS feeds labeled "Top News" if available in the RSS index.
  - Use CNBC sitemap/section feeds (if allowed) and rank by recency + category.
  - Apply heuristic ranking: breaking flag in title, section tags, or editor-picked feeds.
- Risks:
  - RSS feed availability or terms may change.
  - Must stay within usage limits and avoid full-text reuse.
 - MVP implementation:
   - Added a CNBC "breaking" RSS candidate URL to config.
   - Added heuristic scoring in generator (keywords + rank_hint).
   - Added CNBC business/economy/finance/investing RSS candidates to config (requires verification).
