import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# user_input = "itching, skin_rash, nodal_skin_eruptions, dischromic _patches,".split(',')
# user_input = " stomach_pain, acidity, ulcers_on_tongue, vomiting, cough".split(',')


# user_df = pd.DataFrame([user_input[:5]], columns=['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4', 'Symptom_5'])


user_input = " fatigue, cough, high_fever, breathlessness, family_history, mucoid_sputum,,,,,,,,,,,".split(',')
# user_input = " cough, high_fever, breathlessness, family_history, mucoid_sputum".split(',')

for i in range(len(user_input)):
    if user_input[i] == '':
        user_input[i] = 'None'


user_df = pd.DataFrame([user_input], columns=['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4', 'Symptom_5', 'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9', 'Symptom_10', 'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14', 'Symptom_15', 'Symptom_16', 'Symptom_17'])
# user_df = pd.DataFrame([user_input[:5]], columns=['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4', 'Symptom_5'])

df = pd.read_csv('DiseaseAndSymptoms.csv')
df.fillna('None', inplace=True)


df = df.apply(lambda x: x.str.strip())
user_df = user_df.apply(lambda x: x.str.strip())


sym_cols = ['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4', 'Symptom_5', 'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9', 'Symptom_10', 'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14', 'Symptom_15', 'Symptom_16', 'Symptom_17']

all_symptoms = pd.unique(df[sym_cols].values.ravel())

le = LabelEncoder()

le.fit(all_symptoms)

d_le = LabelEncoder()


for col in sym_cols:
    df[col] = le.transform(df[col])

# df['Symptom_1'] = le.transform(df['Symptom_1'])
# df['Symptom_2'] = le.transform(df['Symptom_2'])
# df['Symptom_3'] = le.transform(df['Symptom_3'])
# df['Symptom_4'] = le.transform(df['Symptom_4'])
# df['Symptom_5'] = le.transform(df['Symptom_5'])

df['Disease'] = d_le.fit_transform(df['Disease'])

for col in sym_cols:
    user_df[col] = le.transform(user_df[col])

# user_df['Symptom_1'] = le.transform(user_df['Symptom_1'])
# user_df['Symptom_2'] = le.transform(user_df['Symptom_2'])
# user_df['Symptom_3'] = le.transform(user_df['Symptom_3'])
# user_df['Symptom_4'] = le.transform(user_df['Symptom_4'])
# user_df['Symptom_5'] = le.transform(user_df['Symptom_5'])

X = df[sym_cols]
user_X = user_df[sym_cols]

y = df['Disease']

print(user_X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


print(X_test.head())
# print(le.inverse_transform(X_test['Symptom_1']))

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(user_X)

print(d_le.inverse_transform(y_pred))
#24 Hyperthyroidism

# from sklearn.metrics import classification_report, confusion_matrix,accuracy_score

# print("Accuracy:", accuracy_score(y_test, y_pred))

# print(classification_report(y_test, y_pred))
# print(confusion_matrix(y_test, y_pred))
