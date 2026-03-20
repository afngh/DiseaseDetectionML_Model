import pandas as pd
import numpy as np

df = pd.read_csv('Disease precaution.csv')

def get_precautions(disease : str):
    precautions = df[df['Disease'] == disease][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']].values
    return {
        'Disease': disease,
        'Precautions': precautions[0] if len(precautions) > 0 else []
    }
