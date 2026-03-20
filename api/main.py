from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from predict import predict

app = FastAPI()

precaution_df = pd.read_csv('data/Disease precaution.csv')

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
    raw_input = list()
    for symptom in input.dict().values():
        raw_input.append(symptom)

    disease = predict(raw_input)

    # Get precautions
    result = precaution_df[precaution_df['Disease'] == disease][
        ['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']
    ].values

    precautions = [p for p in result[0] if pd.notna(p)] if len(result) > 0 else []

    return {
        "disease": disease,
        "precautions": precautions
    }