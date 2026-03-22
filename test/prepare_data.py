import pandas as pd
import json

with open('data/diseases.json', 'r') as f:
    dataset = json.load(f)

print(f"Loaded {len(dataset)} diseases")

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt_symptoms(symptoms: list) -> str:
    return ", ".join([s.replace('_', ' ') for s in symptoms])

def fmt_precautions(precautions: list) -> str:
    return ", ".join(precautions)

def build_document(entry: dict) -> str:
    return (
        f"{entry['Disease']} symptoms are {fmt_symptoms(entry['Symptoms'])}. "
        f"Precautions include {fmt_precautions(entry['Precautions'])}."
    )

# ── Build triplets ────────────────────────────────────────────────────────────
triplets = []

for i, entry in enumerate(dataset):
    document = build_document(entry)
    symptoms = fmt_symptoms(entry['Symptoms'])
    disease  = entry['Disease']

    # Multiple query patterns per disease
    queries = [
        f"what is {disease}",
        f"symptoms of {disease}",
        f"i have {symptoms}",
        f"precautions for {disease}",
        f"what to do if i have {symptoms}",
        f"disease with {symptoms}",
        f"how to treat {disease}",
        f"i am suffering from {symptoms}",
    ]

    # Negative — different disease
    negative = build_document(dataset[(i + 1) % len(dataset)])

    for query in queries:
        triplets.append({
            "query":    query,
            "positive": document,
            "negative": negative
        })

df = pd.DataFrame(triplets)
df.to_csv('data/disease_train.csv', index=False)

print(f"Total triplets : {len(df)}")
print(df.head(8))