# Phone Tracker System

מערכת מעקב אחר אינטראקציות בין מכשירים חשודים המבוססת על Flask ו-Neo4j.

## תיאור המערכת

המערכת מקבלת נתונים על אינטראקציות בין מכשירים כל 20 שניות ומאחסנת אותם בגרף Neo4j. המערכת מאפשרת:
- תיעוד אינטראקציות בין מכשירים
- ניתוח קשרים בין מכשירים
- מעקב אחר חיבורי Bluetooth
- בדיקת עוצמת אות וקישוריות

## דרישות מערכת

- Python 3.x
- Docker (להרצת Neo4j)
- Flask
- Neo4j Python Driver
- python-dotenv

## התקנה

1. התקנת Neo4j:
```bash
docker pull neo4j
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
```

2. שכפול פרוייקט הסימולטור:
```bash
git clone https://github.com/EnoshTsur/phone_dispatcher.git
cd phone_dispatcher

הסימולטור ישלח בקשות POST לשרת שלך כל 20 שניות.
```

3. התקנת ספריות Python:
```bash
pip install -r requirements.txt
```

4. הגדרת קובץ .env:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
```

## הפעלת המערכת

יש להפעיל את שני החלקים במקביל:

1. הרץ את השרת שלך (הקוד מהרפוזיטורי הנוכחי)
2. הרץ את הסימולטור (phone_dispatcher) שישלח נתונים לשרת

1. הפעלת השרת:
```bash
python app.py
```

השרת יעלה בכתובת `http://localhost:5000`

## API Endpoints

### POST /api/phone_tracker/interaction
יוצר אינטראקציה חדשה בין שני מכשירים.

דוגמת JSON:
```json
{
  "devices": [
    {
      "id": "device1_id",
      "brand": "Brand1",
      "model": "Model1",
      "os": "OS1",
      "location": {
        "latitude": 0.0,
        "longitude": 0.0,
        "altitude_meters": 0,
        "accuracy_meters": 0
      }
    },
    {
      "id": "device2_id",
      "brand": "Brand2",
      "model": "Model2",
      "os": "OS2",
      "location": {
        "latitude": 0.0,
        "longitude": 0.0,
        "altitude_meters": 0,
        "accuracy_meters": 0
      }
    }
  ],
  "interaction": {
    "method": "Bluetooth",
    "bluetooth_version": "5.0",
    "signal_strength_dbm": -50,
    "distance_meters": 10,
    "duration_seconds": 60,
    "timestamp": "2024-01-01T12:00:00"
  }
}
```

### GET /api/phone_tracker/bluetooth-connections
מחזיר את כל המכשירים המחוברים דרך Bluetooth ואת אורך המסלול ביניהם.

### GET /api/phone_tracker/strong-connections
מחזיר את כל המכשירים עם עוצמת אות חזקה מ-60dbm-.

### GET /api/phone_tracker/device/{device_id}/connections
סופר כמה מכשירים מחוברים למכשיר ספציפי.

### GET /api/phone_tracker/direct-connection/{device1_id}/{device2_id}
בודק אם קיים חיבור ישיר בין שני מכשירים.

### GET /api/phone_tracker/device/{device_id}/latest-interaction
מחזיר את האינטראקציה האחרונה של מכשיר ספציפי.

## מבנה הקוד

- `app.py`: הגדרות Flask והתחברות ל-Neo4j
- `phone_dispatcher_route.py`: הגדרת נתיבי API
- `phone_dispatcher_repo.py`: לוגיקת ממשק מול Neo4j
- `.env`: הגדרות התחברות ל-Neo4j

## מודל הנתונים בגרף

### Nodes
- Label: `Device`
- Properties: id, name, brand, model, os

### Relationships
- Type: `CONNECTED`
- Properties: method, bluetooth_version, signal_strength_dbm, distance_meters, duration_seconds, timestamp, locations