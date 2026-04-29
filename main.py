import requests
import firebase_admin
from firebase_admin import credentials, firestore

# התחברות ל-Firebase
# וודא שהכנסת את ה-Secret ב-GitHub תחת השם FIREBASE_SERVICE_ACCOUNT
import os
import json

cred_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
if cred_json:
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
else:
    print("Error: FIREBASE_SERVICE_ACCOUNT not found.")

db = firestore.client()

def fetch_and_save_data():
    # כתובת ה-API של מאגר התרומות הממשלתי (דוגמה למאגר פעיל)
    url = "https://data.gov.il/api/3/action/datastore_search?resource_id=08638367-e9f0-4384-9022-7729676e42b8&limit=10"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # בודק אם הייתה שגיאת התחברות
        data = response.json()
        
        records = data['result']['records']
        
        for record in records:
            # אנחנו שומרים את הנתונים באוסף שנקרא donations
            doc_ref = db.collection('donations').document()
            doc_ref.set(record)
            print(f"Saved record: {record.get('שם התורם', 'Unknown')}")
            
        print("Successfully updated Firebase with new data!")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_and_save_data()
