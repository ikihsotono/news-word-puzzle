import SwiftUI

struct PuzzleView: View {
    let puzzle: Puzzle
    @State private var input = ""
    @State private var isCorrect: Bool? = nil

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text(puzzle.questionText)
                .font(.title3)

            Text("Hint: \(puzzle.hint)")
                .foregroundColor(.secondary)

            TextField("Type your answer", text: $input)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .autocapitalization(.none)
                .disableAutocorrection(true)

            Button("Check") {
                let normalized = input.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
                isCorrect = (normalized == puzzle.answer.lowercased())
            }

            if let isCorrect {
                NavigationLink(destination: ResultView(puzzle: puzzle, isCorrect: isCorrect)) {
                    Text("See result")
                }
            }

            Spacer()
        }
        .padding()
        .navigationTitle("Puzzle")
    }
}
