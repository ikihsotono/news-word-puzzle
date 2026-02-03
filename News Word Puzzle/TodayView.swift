import SwiftUI

struct TodayView: View {
    @State private var payload: PuzzlePayload?
    @State private var isLoading = false
    @State private var errorMessage: String?

    var body: some View {
        NavigationView {
            Group {
                if isLoading {
                    ProgressView("Loading puzzles...")
                } else if let errorMessage {
                    VStack(spacing: 12) {
                        Text("Could not load puzzles")
                            .font(.headline)
                        Text(errorMessage)
                            .font(.footnote)
                            .foregroundColor(.secondary)
                        Button("Retry") {
                            Task { await load() }
                        }
                    }
                } else if let payload {
                    List {
                        Section(header: Text("Today")) {
                            ForEach(payload.puzzles) { puzzle in
                                NavigationLink(destination: PuzzleView(puzzle: puzzle)) {
                                    VStack(alignment: .leading, spacing: 6) {
                                        Text(puzzle.questionText)
                                            .font(.headline)
                                        Text("Difficulty: \(puzzle.difficulty.capitalized)")
                                            .font(.caption)
                                            .foregroundColor(.secondary)
                                    }
                                }
                            }
                        }
                    }
                    .refreshable {
                        await load()
                    }
                } else {
                    Text("No puzzles yet")
                        .foregroundColor(.secondary)
                }
            }
            .navigationTitle("News Word Puzzle")
        }
        .task {
            await load()
        }
    }

    private func load() async {
        isLoading = true
        errorMessage = nil
        do {
            payload = try await API.fetchPuzzles()
        } catch {
            errorMessage = error.localizedDescription
        }
        isLoading = false
    }
}
