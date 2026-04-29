import os
import json
import requests
import firebase_admin
from firebase_admin import credentials, firestore

def connect_to_firebase():
    creds_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
    if not creds_json:
        return None
    creds_dict = json.loads(creds_json)
    cred = credentials.Certificate(creds_dict)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()

def fetch_political_data():
    # כתובת ה-API של מאגר הנתונים הממשלתי - תרומות למפלגות
    url = "https://data.gov.il/api/3/action/datastore_search?resource_id=1910d656-6f81-4e0e-972a-60586e3f28d8&limit=10"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['result']['records']
        return []
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def main():
    db = connect_to_firebase()
    if not db:
        print("Firebase connection failed")
        return

    print("Fetching data from Gov API...")
    data = fetch_political_data()
    
    for record in data:
        # יצירת מזהה ייחודי כדי שלא נשמור את אותה תרומה פעמיים
        doc_id = f"don_{record.get('_id')}"
        doc_ref = db.collection('politispend_expenditures').document(doc_id)
        
        # שמירת הנתונים
        doc_ref.set({
            'candidate_name': record.get('CandidateName'),
            'party_name': record.get('PartyName'),
            'amount': record.get('Amount'),
            'donor_name': record.get('DonorName'),
            'date': record.get('Date'),
            'last_updated': firestore.SERVER_TIMESTAMP
        })
        print(f"Saved: {record.get('DonorName')} donated to {record.get('CandidateName')}")

if __name__ == "__main__":
    main()
