from flask import Flask, request, jsonify
from bias_detection import get_bias_score
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze_article():
    data = request.json
    article_text = data.get("article", "").strip()

    if not article_text:
        return jsonify({"error": "No text provided"}), 400

    # Analyze bias using ML model
    bias_result = get_bias_score(article_text)

    # Generate a simple summary (first 2 sentences)
    summary = " ".join(sent_tokenize(article_text)[:2])

    return jsonify({
        "bias_score": bias_result["bias_score"],
        "bias_category": bias_result["bias_category"],
        "explanation": bias_result["explanation"],
        "summary": summary
    })

if __name__ == "__main__":
    app.run(debug=True)
