import Foundation

struct PuzzlePayload: Decodable {
    let generatedAt: String?
    let generatedForDate: String?
    let puzzles: [Puzzle]

    enum CodingKeys: String, CodingKey {
        case generatedAt = "generated_at"
        case generatedForDate = "generated_for_date"
        case puzzles
    }
}

struct Puzzle: Decodable, Identifiable {
    let id: String
    let questionText: String
    let answer: String
    let hint: String
    let difficulty: String
    let article: Article

    enum CodingKeys: String, CodingKey {
        case questionText
        case answer
        case hint
        case difficulty
        case article
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        questionText = try container.decode(String.self, forKey: .questionText)
        answer = try container.decode(String.self, forKey: .answer)
        hint = try container.decode(String.self, forKey: .hint)
        difficulty = try container.decode(String.self, forKey: .difficulty)
        article = try container.decode(Article.self, forKey: .article)
        id = UUID().uuidString
    }
}

struct Article: Decodable {
    let source: String
    let rankHint: String?
    let title: String
    let summary: String
    let url: String
    let published: String

    enum CodingKeys: String, CodingKey {
        case source
        case rankHint = "rank_hint"
        case title
        case summary
        case url
        case published
    }
}
