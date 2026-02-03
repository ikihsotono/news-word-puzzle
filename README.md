# NewsWordPuzzle

MVP for a daily, auto-generated word puzzle app focused on economics news.

## Goals
- Daily update at 07:00 PST
- 3–5 puzzles generated from RSS sources (CNBC + public agencies)
- WSJ as link-out only (SFSafariViewController)
- AI-generated cloze questions, quality-focused
- People names are not allowed as answers

## Repos / Folders
- `ios/` SwiftUI app (Xcode project goes here)
- `backend/` scheduled fetch + AI generation + API
- `docs/` specs, prompts, and API contract

## Next steps
- Create iOS app project in `ios/` via Xcode
- Choose backend: Firebase (fast/free tier) recommended
- Define API contract and data model

