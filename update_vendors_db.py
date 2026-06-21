import sqlite3

def update_db():
    print("Updating vendors table...")
    db = sqlite3.connect("event_app.db")
    cursor = db.cursor()
    
    try:
        # Add password column if it doesnt exist
        cursor.execute("ALTER TABLE vendors ADD COLUMN password TEXT")
        print("Added password column to vendors table.")
    except sqlite3.OperationalError as e:
        print(f"Column might already exist: {e}")
        
    # Set default password for existing vendors
    cursor.execute("UPDATE vendors SET password = ?", ("vendor123",))
    db.commit()
    print("Set default password vendor123 for all existing vendors.")
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    update_db()

