from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

import os
import warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

# Or suppress just the HF warning
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"

# Load a pre-trained model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Example sentences to embed
sentences = [
    "Python is a high level programming language",
    "Diabetes symptoms include fatigue and frequent urination",
    "FAISS is a library for efficient similarity search",
    "Machine learning models learn patterns from data",
    "Fever is caused by infection or inflammation",
    "Neural networks are inspired by the human brain",
    "Python is widely used for machine learning and neural networks",
    "Deep learning is a subset of machine learning using neural networks",
]
# Generate embeddings (vectors)
embeddings = model.encode(sentences)

# These embeddings can now be stored in a vector database (like ChromaDB or Weaviate)
# for semantic search or other applications.

d = embeddings[0].shape[0]  

index = faiss.IndexFlatL2(d)
index.add(np.array(embeddings))

query = input('search : ')
query_embedding = model.encode([query])

D,I = index.search(np.array(query_embedding), k=2)

print(I)
print()

res = [sentences[i] for i in I[0]]
print(res)