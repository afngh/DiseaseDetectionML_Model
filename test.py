import requests

BASE_URL = "http://127.0.0.1:8000"

def test_predict(symptoms: dict):
    try:
        response = requests.post(f"{BASE_URL}/predict", json=symptoms)
        print(f"Status Code : {response.status_code}")
        try:
            print(f"Response    : {response.json()}")
        except requests.exceptions.JSONDecodeError:
            print(f"Response    : (empty body — server crashed)")
            print(f"Raw Text    : {response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error : Server not running or crashed")
        print(f"Details          : {e}")
    print("-" * 50)


print("Test 3 — All 17 Symptoms")
test_predict({
    "Symptom_1":  "vomiting",
    "Symptom_2":  "sunken_eyes",
    "Symptom_3":  "dehydration",
    "Symptom_4":  "diarrhoea",
    "Symptom_5":  "None",
    "Symptom_6":  "None",
    "Symptom_7":  "None",
    "Symptom_8":  "None",
    "Symptom_9":  "None",
    "Symptom_10": "None",
    "Symptom_11": "None",
    "Symptom_12": "None",
    "Symptom_13": "None",
    "Symptom_14": "None",
    "Symptom_15": "None",
    "Symptom_16": "None",
    "Symptom_17": "None"
})