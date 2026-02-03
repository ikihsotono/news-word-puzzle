import SwiftUI

struct ResultView: View {
    let puzzle: Puzzle
    let isCorrect: Bool
    @Environment(\.openURL) private var openURL

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text(isCorrect ? "Correct" : "Not quite")
                .font(.largeTitle)

            Text("Answer: \(puzzle.answer)")
                .font(.headline)

            Text(puzzle.article.summary)
                .font(.body)

            Button("Read the original article") {
                if let url = URL(string: puzzle.article.url) {
                    openURL(url)
                }
            }
            .disabled(URL(string: puzzle.article.url) == nil)

            Spacer()
        }
        .padding()
        .navigationTitle("Result")
    }
}
