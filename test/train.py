from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import pandas as pd
import os, warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

# ── Load triplets ─────────────────────────────────────────────────────────────
df = pd.read_csv('data/disease_train.csv')
print(f"Training on {len(df)} triplets")

train_examples = []
for _, row in df.iterrows():
    train_examples.append(InputExample(
        texts=[row['query'], row['positive'], row['negative']]
    ))

# ── Load base model ───────────────────────────────────────────────────────────
model = SentenceTransformer('all-MiniLM-L6-v2')

# ── DataLoader + Loss ─────────────────────────────────────────────────────────
train_loader = DataLoader(train_examples, batch_size=16, shuffle=True)
loss         = losses.TripletLoss(model=model)

# ── Train ─────────────────────────────────────────────────────────────────────
model.fit(
    train_objectives=[(train_loader, loss)],
    epochs=30,
    warmup_steps=50,
    output_path='disease_model',
    show_progress_bar=True
)

print("Training complete — model saved to 'disease_model/'")