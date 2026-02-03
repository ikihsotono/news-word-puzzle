# iOS App Skeleton (SwiftUI)

This folder contains a minimal SwiftUI structure you can paste into an Xcode project.

## Recommended Xcode setup
- Product Name: News Word Puzzle
- Organization Identifier: com.asahisenglish
- Interface: SwiftUI
- Language: Swift

## File mapping
- `AppRoot.swift` -> replace default App file
- `TodayView.swift` -> main screen
- `PuzzleView.swift` -> puzzle screen
- `ResultView.swift` -> result + link-out
- `VocabView.swift` -> saved/missed words
- `Models.swift` -> data models
- `API.swift` -> fetch puzzles JSON

## Data source
Set `apiBaseURL` in `API.swift` to the raw GitHub URL of `data/puzzles.json`.
If not set, the app falls back to the bundled sample at `Resources/puzzles.json` (add it to the Xcode target).
