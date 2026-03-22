from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os, warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

model = SentenceTransformer('disease_model')

with open('data/diseases.json', 'r') as f:
    dataset = json.load(f)

def fmt(lst: list) -> list:
    return [s.replace('_', ' ') for s in lst]

def build_document(entry: dict) -> str:
    return (
        f"{entry['Disease']} symptoms are {', '.join(fmt(entry['Symptoms']))}. "
        f"Precautions include {', '.join(entry['Precautions'])}."
    )

documents  = [build_document(e) for e in dataset]
embeddings = model.encode(documents, convert_to_numpy=True)

d     = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(np.array(embeddings, dtype=np.float32))

print(f"Index built with {len(documents)} diseases")

def answer(query: str, k: int = 1):
    query_vec = model.encode([query])
    D, I      = index.search(np.array(query_vec, dtype=np.float32), k=k)

    best      = dataset[I[0][0]]
    score     = round(1 / (1 + D[0][0]), 4)

    print(f"\nQuery       : {query}")
    print(f"Disease     : {best['Disease']}  (confidence: {score})")
    print(f"Symptoms    : {', '.join(fmt(best['Symptoms']))}")
    print(f"Precautions : {', '.join(best['Precautions'])}")
    print("-" * 60)

answer("i have continuous sneezing and watering eyes")
answer("what are precautions for allergy")
answer("i have cough and breathlessness")
answer("symptoms of diabetes")
answer("i am suffering from itching and skin rash")