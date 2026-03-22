import numpy as np
import pandas as pd
import json

df = pd.read_csv('data/test.csv')
preq_df = pd.read_csv('data/Disease precaution.csv')

# print(df.head())

clean_data = []

for index in range(len(df)):
    disease = df.iloc[index]['Disease']
    symptoms = []
    precautions = preq_df[preq_df['Disease'] == disease].iloc[0][1:].dropna().tolist()
    
    for i in range(1, 11):
        symptom = df.iloc[index][f'Symptom_{i}']
        if pd.notna(symptom):
            symptoms.append(symptom.strip())

    clean_data.append({
        'Disease': disease,
        'Symptoms': symptoms,
        'Precautions': precautions
    })
    

# print(df.iloc[0])

print(json.dumps(clean_data, indent=4))