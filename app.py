from flask import Flask, render_template, request, jsonify
import math
import re
from collections import Counter, defaultdict

app = Flask(__name__)

# Small built-in labeled dataset so the project works without downloading models.
TRAINING_DATA = [
    ("I love this product and it works perfectly", "positive"),
    ("The service was excellent and very helpful", "positive"),
    ("I am happy with the amazing results", "positive"),
    ("This app is fast simple and wonderful", "positive"),
    ("The experience was great and enjoyable", "positive"),
    ("I really like the clean design", "positive"),
    ("The support team solved my problem quickly", "positive"),
    ("Everything feels smooth and reliable", "positive"),
    ("The update made the application better", "positive"),
    ("I am impressed with the quality", "positive"),
    ("This is a fantastic idea", "positive"),
    ("The result is useful and accurate", "positive"),
    ("I had a pleasant experience", "positive"),
    ("The interface looks beautiful", "positive"),
    ("It saved me time and worked well", "positive"),
    ("I recommend this because it is dependable", "positive"),
    ("The feature is smart and convenient", "positive"),
    ("The response was quick and friendly", "positive"),

    ("I hate this product and it is useless", "negative"),
    ("The service was terrible and disappointing", "negative"),
    ("I am unhappy with the bad results", "negative"),
    ("This app is slow confusing and awful", "negative"),
    ("The experience was frustrating and painful", "negative"),
    ("I do not like the messy design", "negative"),
    ("The support team ignored my problem", "negative"),
    ("Everything feels broken and unreliable", "negative"),
    ("The update made the application worse", "negative"),
    ("I am disappointed with the quality", "negative"),
    ("This is a horrible idea", "negative"),
    ("The result is inaccurate and useless", "negative"),
    ("I had a bad experience", "negative"),
    ("The interface looks ugly", "negative"),
    ("It wasted my time and failed", "negative"),
    ("I would not recommend this because it is unreliable", "negative"),
    ("The feature is annoying and inconvenient", "negative"),
    ("The response was slow and rude", "negative"),

    ("The meeting starts at ten today", "neutral"),
    ("The application has three main pages", "neutral"),
    ("I opened the dashboard this morning", "neutral"),
    ("The report contains monthly statistics", "neutral"),
    ("The system stores the user profile", "neutral"),
    ("The class has a practical session", "neutral"),
    ("The software uses Python and Flask", "neutral"),
    ("The weather report says it will rain", "neutral"),
    ("The device has a six hour battery", "neutral"),
    ("The table shows values for each category", "neutral"),
    ("The project includes an interface and an API", "neutral"),
    ("I submitted the assignment on Monday", "neutral"),
    ("The server runs on port five thousand", "neutral"),
    ("This page contains a short description", "neutral"),
    ("The course has four modules", "neutral"),
    ("The user entered a sentence in the box", "neutral"),
    ("The dashboard displays recent activity", "neutral"),
    ("The model predicts one of three classes", "neutral"),
]

STOPWORDS = {
    "a", "an", "the", "is", "am", "are", "was", "were", "be", "been", "being",
    "i", "you", "he", "she", "it", "we", "they", "this", "that", "these", "those",
    "and", "or", "but", "if", "then", "than", "to", "of", "in", "on", "at", "for",
    "with", "from", "by", "as", "about", "into", "over", "after", "before", "under",
    "my", "your", "our", "their", "his", "her", "its", "me", "us", "them", "very",
    "really", "just", "so", "do", "does", "did", "not", "no", "today", "was"
}


def tokenize(text):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return [word for word in words if word not in STOPWORDS and len(word) > 1]


class ExplainableNaiveBayes:
    def __init__(self, data):
        self.labels = sorted({label for _, label in data})
        self.doc_counts = Counter()
        self.word_counts = {label: Counter() for label in self.labels}
        self.total_words = Counter()
        self.vocab = set()
        self.train(data)

    def train(self, data):
        for text, label in data:
            self.doc_counts[label] += 1
            tokens = tokenize(text)
            self.word_counts[label].update(tokens)
            self.total_words[label] += len(tokens)
            self.vocab.update(tokens)

    def word_log_probability(self, word, label):
        count = self.word_counts[label][word]
        numerator = count + 1
        denominator = self.total_words[label] + len(self.vocab)
        return math.log(numerator / denominator)

    def predict(self, text):
        tokens = tokenize(text)
        scores = {}
        total_docs = sum(self.doc_counts.values())

        for label in self.labels:
            log_prior = math.log(self.doc_counts[label] / total_docs)
            scores[label] = log_prior + sum(self.word_log_probability(t, label) for t in tokens)

        max_score = max(scores.values())
        exp_scores = {label: math.exp(score - max_score) for label, score in scores.items()}
        total = sum(exp_scores.values()) or 1.0
        probabilities = {label: value / total for label, value in exp_scores.items()}
        prediction = max(probabilities, key=probabilities.get)

        evidence = []
        for token in tokens:
            if token not in self.vocab:
                continue
            label_scores = {label: self.word_log_probability(token, label) for label in self.labels}
            best_label = max(label_scores, key=label_scores.get)
            strength = label_scores[best_label] - sorted(label_scores.values())[-2]
            evidence.append({
                "word": token,
                "supports": best_label,
                "strength": round(abs(strength), 3)
            })

        evidence.sort(key=lambda item: item["strength"], reverse=True)
        known_tokens = [t for t in tokens if t in self.vocab]

        return {
            "prediction": prediction,
            "confidence": round(probabilities[prediction] * 100, 1),
            "probabilities": {label: round(probabilities[label] * 100, 1) for label in self.labels},
            "tokens": known_tokens,
            "evidence": evidence[:6],
            "message": self.build_message(prediction)
        }

    @staticmethod
    def build_message(prediction):
        messages = {
            "positive": "The text contains language that is mostly favorable or satisfied.",
            "negative": "The text contains language that is mostly unfavorable or dissatisfied.",
            "neutral": "The text is mostly descriptive or factual without strong emotional language."
        }
        return messages[prediction]


model = ExplainableNaiveBayes(TRAINING_DATA)


@app.route("/")
def home():
    return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()
    if not text:
        return jsonify({"error": "Please enter some text to analyze."}), 400
    if len(text) > 1000:
        return jsonify({"error": "Please keep the input under 1000 characters."}), 400
    return jsonify(model.predict(text))


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "model": "Explainable Naive Bayes", "labels": model.labels})


if __name__ == "__main__":
    app.run(debug=True)
