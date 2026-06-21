import sqlite3

def update_db():
    db = sqlite3.connect("event_app.db")
    cursor = db.cursor()
    
    try:
        cursor.execute("ALTER TABLE vendors ADD COLUMN business_proof_text TEXT")
        cursor.execute("ALTER TABLE vendors ADD COLUMN business_proof_file TEXT")
        cursor.execute("ALTER TABLE vendors ADD COLUMN is_verified BOOLEAN DEFAULT 0")
        print("Added proof columns.")
    except sqlite3.OperationalError as e:
        print(f"Columns might already exist: {e}")
        
    # Mark existing mock vendors as verified so they get the green badge
    cursor.execute("UPDATE vendors SET is_verified = 1")
    db.commit()
    print("Marked existing vendors as verified.")
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    update_db()

