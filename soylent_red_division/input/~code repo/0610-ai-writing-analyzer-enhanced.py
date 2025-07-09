
import os
import re
import difflib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define file paths and stage names
stages = [
    ("Draft", "/mnt/data/01-draft-name.md"),
    ("Refined", "/mnt/data/03 - refined-name.md"),
    ("Edited", "/mnt/data/04 - edited-name.md"),
    ("Final", "/mnt/data/05 - final-name.md"),
]

# Helper to read and preprocess text
def load_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    text_clean = re.sub(r'```.*?```', '', text, flags=re.S)
    text_clean = re.sub(r'#.*', '', text_clean)
    return text_clean.strip()

# Gather basic metrics per stage
metrics = []
texts = {}
for name, path in stages:
    txt = load_text(path)
    texts[name] = txt
    words = re.findall(r'\b\w+\b', txt)
    sentences = re.split(r'[.!?]+', txt)
    metrics.append({
        "Stage": name,
        "CharCount": len(txt),
        "WordCount": len(words),
        "AvgSentenceLen": round(sum(len(s.split()) for s in sentences if s.strip()) 
                                 / max(1, sum(1 for s in sentences if s.strip())), 1)
    })

df_metrics = pd.DataFrame(metrics)

# Analyze structural transitions and vocabulary shifts
transitions = []
for before, after in [("Draft","Refined"), ("Refined","Edited"), ("Edited","Final")]:
    t1, t2 = texts[before], texts[after]
    seq_sim = difflib.SequenceMatcher(None, t1, t2).ratio() * 100
    wc1 = len(re.findall(r'\b\w+\b', t1))
    wc2 = len(re.findall(r'\b\w+\b', t2))
    change_pct = round((wc2 - wc1) / wc1 * 100, 1) if wc1 else None
    vocab1 = set(w.lower() for w in re.findall(r'\b\w+\b', t1))
    vocab2 = set(w.lower() for w in re.findall(r'\b\w+\b', t2))
    new_vocab = len(vocab2 - vocab1)
    transitions.append({
        "Transition": f"{before} → {after}",
        "SequenceSim(%)": round(seq_sim, 1),
        "WordChange(%)": change_pct,
        "NewVocabCount": new_vocab
    })

labels = [name for name, _ in stages]
docs = [texts[name] for name in labels]
vectorizer = TfidfVectorizer(stop_words='english')
tfidf = vectorizer.fit_transform(docs)
cos_mat = cosine_similarity(tfidf)

transitions.append({
    "Transition": "Draft → Final",
    "SequenceSim(%)": None,
    "WordChange(%)": None,
    "NewVocabCount": None,
    "SemanticSim(%)": round(cos_mat[0, -1] * 100, 1)
})

df_transitions = pd.DataFrame(transitions)

print("Stage Metrics:")
print(df_metrics.to_string(index=False))
print("\nTransition Analysis (including Draft → Final semantic similarity):")
print(df_transitions.to_string(index=False))
