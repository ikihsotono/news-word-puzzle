import SwiftUI
import SafariServices

struct ResultView: View {
    let puzzle: Puzzle
    let isCorrect: Bool
    @State private var showSafari = false

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text(isCorrect ? "Correct" : "Not quite")
                .font(.largeTitle)

            Text("Answer: \(puzzle.answer)")
                .font(.headline)

            Text(puzzle.article.summary)
                .font(.body)

            Button("Read the original article") {
                showSafari = true
            }

            Spacer()
        }
        .padding()
        .navigationTitle("Result")
        .sheet(isPresented: $showSafari) {
            SafariView(url: URL(string: puzzle.article.url)!)
        }
    }
}

struct SafariView: UIViewControllerRepresentable {
    let url: URL

    func makeUIViewController(context: Context) -> SFSafariViewController {
        SFSafariViewController(url: url)
    }

    func updateUIViewController(_ uiViewController: SFSafariViewController, context: Context) {
    }
}
