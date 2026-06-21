import psycopg2
import os

def init_db(db_url=None):
    print("Initializing PostgreSQL Database...")
    if db_url is None:
        db_url = os.environ.get("DATABASE_URL")
    
    if not db_url:
        print("DATABASE_URL environment variable is missing!")
        return

    try:
        db = psycopg2.connect(db_url)
        cursor = db.cursor()

        # Drop existing tables for a clean slate during initialization
        cursor.execute("DROP TABLE IF EXISTS bookings, vendor_reviews, vendors, tasks, expenses, timeline, guests, events, users CASCADE;")

        # 1. Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                phone TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        # 2. Events Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                budget REAL NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # 3. Expenses Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id SERIAL PRIMARY KEY,
                category TEXT NOT NULL,
                item TEXT NOT NULL,
                amount REAL NOT NULL,
                event_id INTEGER,
                vendor_id INTEGER,
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
        """)

        # 4. Tasks Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                event_id INTEGER,
                description TEXT NOT NULL,
                is_done BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
        """)

        # 5. Vendors Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendors (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                rating REAL DEFAULT 0.0,
                description TEXT,
                image_url TEXT,
                email TEXT,
                phone TEXT,
                password TEXT,
                business_proof_text TEXT,
                business_proof_file TEXT,
                is_verified INTEGER DEFAULT 0
            )
        """)

        # 6. Vendor Reviews Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendor_reviews (
                id SERIAL PRIMARY KEY,
                vendor_id INTEGER,
                user_id INTEGER,
                rating INTEGER,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 7. Bookings Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                event_id INTEGER,
                vendor_id INTEGER,
                total_amount REAL,
                advance_paid REAL DEFAULT 0,
                status TEXT DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 8. Guests Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guests (
                id SERIAL PRIMARY KEY,
                event_id INTEGER,
                name TEXT,
                status TEXT DEFAULT 'Confirmed',
                notes TEXT
            )
        """)

        # 9. Timeline Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timeline (
                id SERIAL PRIMARY KEY,
                event_id INTEGER,
                time TEXT,
                activity TEXT,
                notes TEXT
            )
        """)

        # Insert Vendor Data
        vendor_data = [
            # Photographers
            ("Aura Studio", "Photography", 15000, 4.9, "Cinematic wedding photography and creative portraits.", "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&q=80&w=300", "contact@aurastudio.com", "+91 98765 43210"),
            ("SnapPixel", "Photography", 8500, 4.7, "Budget-friendly event coverage with high-quality digital delivery.", "https://images.unsplash.com/photo-1542038784456-1ea8e935640e?auto=format&fit=crop&q=80&w=300", "info@snappixel.in", "+91 91234 56789"),
            
            # Decorators
            ("Neon Bloom", "Decoration", 25000, 4.8, "Modern floral arrangements and neon-themed event styling.", "https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&q=80&w=300", "hello@neonbloom.com", "+91 99887 76655"),
            ("Royal Decor", "Decoration", 45000, 5.0, "Luxury stage setups and traditional Indian wedding themes.", "https://images.unsplash.com/photo-1469334031218-e382a71b716b?auto=format&fit=crop&q=80&w=300", "royal@decor.com", "+91 90000 11111"),
            
            # Catering
            ("Spice Route", "Catering", 500, 4.6, "Per-plate authentic multi-cuisine buffet services.", "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&q=80&w=300", "spice@route.com", "+91 88888 77777"),
            ("Gourmet Gala", "Catering", 1200, 4.9, "Premium fine-dining experience for corporate events.", "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&q=80&w=300", "gala@gourmet.com", "+91 77777 66666"),
            
            # Music/Entertainment
            ("DJ Vibe", "Music", 12000, 4.7, "Professional DJ services with sound and lighting included.", "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&q=80&w=300", "dj@vibe.com", "+91 99999 00000"),
            ("Melody Band", "Music", 35000, 4.8, "Live acoustic band for intimate gatherings and weddings.", "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&q=80&w=300", "melody@band.com", "+91 98888 77777"),

            # Venues
            ("Grand Palace", "Venue", 150000, 4.9, "Palatial venue for grand weddings and large scale corporate events.", "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&q=80&w=300", "events@grandpalace.com", "+91 91111 22222"),
            ("Green Garden", "Venue", 50000, 4.5, "Beautiful outdoor lawn perfect for summer weddings and parties.", "https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&q=80&w=300", "info@greengarden.com", "+91 92222 33333"),

            # Makeup Artists
            ("Glow Up", "Makeup", 12000, 4.8, "Professional bridal makeup and styling for all skin types.", "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&q=80&w=300", "glow@upmakeup.com", "+91 93333 44444"),
            ("Artistry by Ana", "Makeup", 8000, 4.6, "Specialized in minimalist and elegant party makeup looks.", "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&q=80&w=300", "ana@artistry.com", "+91 94444 55555"),

            # Invitations
            ("Paper Craft", "Invitations", 100, 4.7, "Custom designed luxury wedding cards and digital invites.", "https://images.unsplash.com/photo-1544928147-79a2dbc1f389?auto=format&fit=crop&q=80&w=300", "design@papercraft.com", "+91 95555 66666"),

            # Transportation
            ("Luxury Rides", "Transportation", 20000, 4.8, "Premium fleet of luxury cars for bridal arrivals and guest transit.", "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&q=80&w=300", "rides@luxury.com", "+91 96666 77777")
        ]

        # Use %s for psycopg2 parameter substitution
        cursor.executemany(
            "INSERT INTO vendors (name, category, price, rating, description, image_url, email, phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            vendor_data
        )

        db.commit()
        print("✅ Database initialized successfully with PostgreSQL!")
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_db()
