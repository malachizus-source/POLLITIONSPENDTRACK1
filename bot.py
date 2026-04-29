import requests
import json
import os

# פונקציה למשיכת נתונים ממפתח התקציב (למשל: התקשרויות אחרונות)
def check_budget():
    # כתובת ה-API של מפתח התקציב (דוגמה להתקשרויות משרדי ממשלה)
    url = "https://next.obudget.org/api/query?q=SELECT+publisher_name,description,amount_allocated,order_date+FROM+contract_spending+ORDER+BY+order_date+DESC+LIMIT+5"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['rows']:
            for row in data['rows']:
                name = row['publisher_name']
                desc = row['description']
                amount = row['amount_allocated']
                date = row['order_date']
                
                # כאן אנחנו יוצרים את ההודעה בעברית
                message = f"📢 הוצאה חדשה זוהתה!\nמשרד: {name}\nתיאור: {desc}\nסכום: ₪{amount:,}\nתאריך: {date}"
                print(message)
                
                # כאן בעתיד תשלח את ההתראה לאפליקציה שלך (Push Notification)
                # send_push_notification(message)
                
    except Exception as e:
        print(f"שגיאה במשיכת נתונים: {e}")

if __name__ == "__main__":
    check_budget()
