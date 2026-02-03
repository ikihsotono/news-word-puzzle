import Foundation

struct API {
    // Optional: set to raw GitHub URL for data/puzzles.json
    static let apiBaseURL = "https://raw.githubusercontent.com/OWNER/REPO/BRANCH/data/puzzles.json"

    static func fetchPuzzles() async throws -> PuzzlePayload {
        if let url = URL(string: apiBaseURL), apiBaseURL.contains("githubusercontent.com") {
            do {
                let (data, _) = try await URLSession.shared.data(from: url)
                return try JSONDecoder().decode(PuzzlePayload.self, from: data)
            } catch {
                // Fall back to bundled sample on failure
            }
        }
        return try loadBundled()
    }

    private static func loadBundled() throws -> PuzzlePayload {
        guard let url = Bundle.main.url(forResource: "puzzles", withExtension: "json") else {
            throw URLError(.fileDoesNotExist)
        }
        let data = try Data(contentsOf: url)
        return try JSONDecoder().decode(PuzzlePayload.self, from: data)
    }
}
