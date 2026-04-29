import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# התחברות ל-Firebase באמצעות ה-Secret שהגדרת
cred_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')

if cred_json:
    try:
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()

        # יצירת נתון בדיקה פשוט
        data = {
            "name": "Test User",
            "message": "Hello from GitHub Actions!",
            "status": "Success"
        }

        # שמירה ב-Firebase באוסף שנקרא 'test_connection'
        db.collection('test_connection').add(data)
        print("✅ Success! Data sent to Firebase.")

    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print("❌ Error: FIREBASE_SERVICE_ACCOUNT secret not found.")
