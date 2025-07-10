# app.py (Final Version)

import nltk
from flask import Flask, request, jsonify
from flask_cors import CORS
from sentence_transformers import SentenceTransformer, util

# --- INITIALIZATION ---

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)

# Load a pre-trained sentence-transformer model.
print("Loading semantic analysis model...")
model = SentenceTransformer('paraphrase-albert-small-v2')
print("Model loaded.")

# --- NEW: Robustly check for and download all required NLTK data ---
print("Checking for NLTK resources...")
required_resources = ['punkt', 'punkt_tab']
for resource in required_resources:
    try:
        # The path for tokenizers is standard
        nltk.data.find(f'tokenizers/{resource}')
    except LookupError:
        print(f"NLTK resource '{resource}' not found. Downloading...")
        nltk.download(resource)
        print(f"'{resource}' downloaded.")
print("NLTK resources are ready.")


# --- HELPER FUNCTIONS (The accurate versions) ---

def count_words(text):
    return len(text.strip().split()) if text else 0

def count_sentences_accurate(text):
    if not text:
        return 0
    # Use NLTK for accurate sentence tokenization
    return len(nltk.sent_tokenize(text))

def count_paragraphs(text):
    if not text or not text.strip():
        return 0
    # Split by one or more newlines, and filter out empty paragraphs
    return len([p for p in text.split('\n') if p.strip()])

def calculate_word_retention(original, modified):
    original_words = set(original.lower().replace(r'[^\w\s]', '').split())
    modified_words = set(modified.lower().replace(r'[^\w\s]', '').split())
    if not original_words:
        return 0
    retained_count = len(original_words.intersection(modified_words))
    return (retained_count / len(original_words)) * 100

def calculate_semantic_change_accurate(text1, text2):
    """Calculates semantic change using sentence embeddings and cosine similarity."""
    if not text1 or not text2:
        return 100.0 # 100% change if one document is empty

    # Encode texts into semantic vectors (embeddings)
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)

    # Calculate cosine similarity between the two vectors
    cosine_scores = util.cos_sim(embedding1, embedding2)
    
    # Similarity is a value from -1 to 1. We'll normalize it to 0-1 for simplicity.
    similarity = (cosine_scores.item() + 1) / 2
    
    # Change is the inverse of similarity
    change_percentage = (1 - similarity) * 100
    return change_percentage

def analyze_checkpoint(doc1, doc2):
    """Analyzes a single transition between two documents."""
    words1, words2 = count_words(doc1), count_words(doc2)
    sentences1, sentences2 = count_sentences_accurate(doc1), count_sentences_accurate(doc2)
    paragraphs1, paragraphs2 = count_paragraphs(doc1), count_paragraphs(doc2)

    return {
        "metrics": {
            "words": {"from": words1, "to": words2, "delta": words2 - words1},
            "sentences": {"from": sentences1, "to": sentences2, "delta": sentences2 - sentences1},
            "paragraphs": {"from": paragraphs1, "to": paragraphs2, "delta": paragraphs2 - paragraphs1},
            "retention": calculate_word_retention(doc1, doc2),
            "semanticChange": calculate_semantic_change_accurate(doc1, doc2)
        }
    }

# --- API ENDPOINT (Updated to your preference) ---
@app.route('/authenticity', methods=['POST'])
def analyze():
    """The main API endpoint that the frontend will call."""
    data = request.get_json()
    docs = [
        data.get('doc1', ''),
        data.get('doc2', ''),
        data.get('doc3', ''),
        data.get('doc4', '')
    ]
    labels = ['AI Draft', 'AI Refined', 'Human Edited', 'Final Version']
    
    analyses = []
    for i in range(3):
        analysis_result = analyze_checkpoint(docs[i], docs[i + 1])
        analysis_result["from"] = labels[i]
        analysis_result["to"] = labels[i + 1]
        analyses.append(analysis_result)

    return jsonify(analyses)

# --- RUN THE APP ---
if __name__ == '__main__':
    # Makes the server available on your local network
    app.run(host='0.0.0.0', port=5000)
