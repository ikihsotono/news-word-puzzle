# News Word Puzzle — MVP Spec

## Product Goals
- Daily word puzzles from economics news
- 3–5 puzzles each morning
- Focus on vocabulary growth via current events
- iOS-first (SwiftUI)

## Daily Schedule
- Run at 07:00 local time in America/Los_Angeles
- Batch generates 3–5 puzzles per day

## Content Sources (MVP)
- CNBC RSS (links + short summaries only; no full text)
- Federal Reserve RSS feeds
- BLS RSS feeds
- BEA News Release RSS
- WSJ is link-out only (no auto-fetch)

## Puzzle Rules
- Format: cloze (fill-in-the-blank)
- Source text: title + short summary
- Answers:
  - People names are not allowed
  - Company names and place names are allowed
- Difficulty:
  - Easy: common word, short length
  - Medium: domain vocabulary, mid-length
  - Hard: specialized vocabulary, longer length

## Screens
1. Today
   - 3–5 puzzles
   - progress indicator
2. Puzzle
   - cloze text
   - hint (part of speech + short context)
   - answer input
3. Result
   - explanation
   - link to original article
4. Vocab
   - saved words
   - missed words

## Data Model (MVP)
- Article
  - id, source, title, summary, url, publishedAt
- Puzzle
  - id, articleId, questionText, answer, hint, difficulty, createdAt
- UserProgress
  - puzzleId, status, attempts, solvedAt, isFavorite
