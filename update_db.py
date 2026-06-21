import sqlite3

db = sqlite3.connect("event_app.db")
cursor = db.cursor()

try:
    cursor.execute("ALTER TABLE users RENAME COLUMN email TO phone;")
    db.commit()
    print("Successfully renamed email to phone in users table.")
except sqlite3.OperationalError as e:
    print(f"Error (maybe already renamed): {e}")

cursor.close()
db.close()
