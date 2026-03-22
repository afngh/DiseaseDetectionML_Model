import pandas as pd
import json

df      = pd.read_csv('data/DiseaseAndSymptoms.csv')
preq_df = pd.read_csv('data/Disease precaution.csv')

clean_data = []

for index in range(len(df)):
    disease     = df.iloc[index]['Disease']
    symptoms    = []
    
    # Get precautions — skip if disease not found
    preq_row = preq_df[preq_df['Disease'] == disease]
    if preq_row.empty:
        continue
    precautions = preq_row.iloc[0][1:].dropna().tolist()

    # Collect symptoms
    for i in range(1, 18):
        col = f'Symptom_{i}'
        if col in df.columns:
            symptom = df.iloc[index][col]
            if pd.notna(symptom) and symptom.strip():
                symptoms.append(symptom.strip())

    # Skip duplicates
    existing = [d['Disease'] for d in clean_data]
    if disease not in existing and symptoms:
        clean_data.append({
            'Disease':     disease,
            'Symptoms':    symptoms,
            'Precautions': precautions
        })

# Save
with open('data/diseases.json', 'w') as f:
    json.dump(clean_data, f, indent=4)

print(f"Total diseases saved : {len(clean_data)}")
print(json.dumps(clean_data[:2], indent=4))