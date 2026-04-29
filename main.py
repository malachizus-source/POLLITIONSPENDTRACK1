import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

def connect_to_firebase():
    # משיכת פרטי ההתחברות מהסוד שהגדרנו ב-GitHub
    creds_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
    
    if not creds_json:
        print("Error: FIREBASE_SERVICE_ACCOUNT secret not found.")
        return None

    # טעינת המפתח וחיבור ל-Firebase
    creds_dict = json.loads(creds_json)
    cred = credentials.Certificate(creds_dict)
    
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

def main():
    db = connect_to_firebase()
    
    if db:
        # יצירת מסמך בדיקה באוסף שהגדרנו
        doc_ref = db.collection('politispend_expenditures').document('test_run')
        doc_ref.set({
            'status': 'Success',
            'message': 'GitHub Actions is now connected to Firebase!',
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        print("Successfully updated Firebase!")

if __name__ == "__main__":
    main()
