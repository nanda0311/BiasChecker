import nltk
from nltk.tokenize import word_tokenize

# Ensure nltk resources are available
nltk.download('punkt')

# List of biased words (can be improved with AI)
BIAS_KEYWORDS = ["propaganda", "fake news", "misleading", "biased", "agenda"]

def detect_bias(text):
    words = word_tokenize(text.lower())
    bias_count = sum(1 for word in words if word in BIAS_KEYWORDS)
    return (bias_count / len(words)) * 100 if words else 0  # Return bias percentage

def rewrite_content(text):
    return text.replace("biased", "neutral").replace("fake news", "unverified information")

def summarize_text(text):
    sentences = text.split(".")
    return ". ".join(sentences[:2]) + "..." if len(sentences) > 2 else text
if __name__ == "__main__":
    test_text = "This is a politically charged statement with biased language."
    print("Bias Score:", detect_bias(test_text))
    print("Rewritten Content:", rewrite_content(test_text))
    print("Summary:", summarize_text(test_text))
