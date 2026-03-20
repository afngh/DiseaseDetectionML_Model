import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import pickle

SYM_COLS = [f'Symptom_{i}' for i in range(1, 18)]

def load_artifacts():
    model = pickle.load(open(os.path.join(BASE_DIR, 'api/model.pkl'), 'rb'))
    le    = pickle.load(open(os.path.join(BASE_DIR, 'api/le.pkl'),    'rb'))
    d_le  = pickle.load(open(os.path.join(BASE_DIR, 'api/d_le.pkl'),  'rb'))
    return model, le, d_le

def prepare_user_input(raw_input: list):
    user_input = raw_input[:]
    while len(user_input) < 17:
        user_input.append('None')
    return pd.DataFrame([user_input[:17]], columns=SYM_COLS)

def predict(raw_input: list):
    model, le, d_le = load_artifacts()
    user_df = prepare_user_input(raw_input)
    for col in SYM_COLS:
        user_df[col] = le.transform(user_df[col])
    prediction = model.predict(user_df)
    return d_le.inverse_transform(prediction)[0]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

precaution_df = pd.read_csv(os.path.join(BASE_DIR, 'api/data', 'Disease precaution.csv'))
#                            ↑ absolute path — works no matter where uvicorn runs from

class SymptomsInput(BaseModel):
    Symptom_1:  str = 'None'
    Symptom_2:  str = 'None'
    Symptom_3:  str = 'None'
    Symptom_4:  str = 'None'
    Symptom_5:  str = 'None'
    Symptom_6:  str = 'None'
    Symptom_7:  str = 'None'
    Symptom_8:  str = 'None'
    Symptom_9:  str = 'None'
    Symptom_10: str = 'None'
    Symptom_11: str = 'None'
    Symptom_12: str = 'None'
    Symptom_13: str = 'None'
    Symptom_14: str = 'None'
    Symptom_15: str = 'None'
    Symptom_16: str = 'None'
    Symptom_17: str = 'None'

@app.post("/predict")
def predict_disease(input: SymptomsInput):
    raw_input = list(input.dict().values())
    disease   = predict(raw_input)

    result = precaution_df[precaution_df['Disease'] == disease][
        ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']
    ].values

    precautions = [p for p in result[0] if pd.notna(p)] if len(result) > 0 else []

    return {"disease": disease, "precautions": precautions}
