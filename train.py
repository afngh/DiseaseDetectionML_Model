# train.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────
SYM_COLS = [f'Symptom_{i}' for i in range(1, 18)]
DATA_PATH = 'data/DiseaseAndSymptoms.csv'

# ─────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────
def load_and_clean(path):
    df = pd.read_csv(path)
    df.fillna('None', inplace=True)
    df = df.apply(lambda x: x.str.strip())
    return df


def fit_encoders(df):
    all_symptoms = pd.unique(df[SYM_COLS].values.ravel())

    le = LabelEncoder()
    le.fit(all_symptoms)

    d_le = LabelEncoder()
    d_le.fit(df['Disease'])

    return le, d_le


def encode_df(df, le, d_le):
    for col in SYM_COLS:
        df[col] = le.transform(df[col])
    df['Disease'] = d_le.transform(df['Disease'])
    return df


def train_model(df):
    X = df[SYM_COLS]
    y = df['Disease']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test))
    print(f"Model Accuracy: {accuracy:.2f}")

    return model


def save_artifacts(model, le, d_le):
    pickle.dump(model, open('model.pkl', 'wb'))
    pickle.dump(le,    open('le.pkl',    'wb'))
    pickle.dump(d_le,  open('d_le.pkl',  'wb'))
    print("Saved: model.pkl, le.pkl, d_le.pkl")


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
if __name__ == '__main__':
    df              = load_and_clean(DATA_PATH)
    le, d_le        = fit_encoders(df)
    df              = encode_df(df, le, d_le)
    model           = train_model(df)
    save_artifacts(model, le, d_le)