import torch
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np

# Load Pre-trained BERT Model (You can fine-tune it on bias datasets)
MODEL_NAME = "textattack/bert-base-uncased-SST-2"  # Sentiment model (use a bias-trained model)
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)

def get_bias_score(article_text):
    """Predict bias score & category using BERT."""
    inputs = tokenizer(article_text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        logits = model(**inputs).logits
    
    # Convert logits to probabilities
    probs = torch.softmax(logits, dim=1).numpy().flatten()
    bias_score = probs[1]  # Assuming label 1 = biased, label 0 = unbiased

    # Define bias categories
    if bias_score < 0.3:
        bias_category = "Unbiased"
    elif bias_score < 0.6:
        bias_category = "Moderate Bias"
    else:
        bias_category = "Highly Biased"

    # Generate explanation
    explanation = (
        "This article seems to have neutral language."
        if bias_category == "Unbiased"
        else "This article may use emotionally charged words or one-sided arguments."
    )

    return {
        "bias_score": round(float(bias_score), 2),
        "bias_category": bias_category,
        "explanation": explanation,
    }
