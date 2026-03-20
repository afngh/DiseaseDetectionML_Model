import pandas as pd
import pickle

SYM_COLS = [f'Symptom_{i}' for i in range(1, 18)]

def load_artifacts():
    model = pickle.load(open('model.pkl', 'rb'))
    le    = pickle.load(open('le.pkl',    'rb'))
    d_le  = pickle.load(open('d_le.pkl',  'rb'))
    return model, le, d_le


def prepare_user_input(raw_input: list):
    user_input = raw_input
    while len(user_input) < 17:
        user_input.append('None')

    user_df = pd.DataFrame([user_input[:17]], columns=SYM_COLS)
    return user_df


def predict(raw_input: list):
    model, le, d_le = load_artifacts()

    user_df = prepare_user_input(raw_input)

    for col in SYM_COLS:
        user_df[col] = le.transform(user_df[col])

    prediction = model.predict(user_df)
    disease    = d_le.inverse_transform(prediction)

    return disease[0]
