import sqlite3

connection = sqlite3.connect("soc.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_name TEXT NOT NULL,
    severity TEXT NOT NULL,
    source_ip TEXT,
    destination_ip TEXT,
    timestamp TEXT,
    status TEXT DEFAULT 'Open',
    analyst_notes TEXT DEFAULT ''
)
""")

# Check existing columns
cursor.execute("PRAGMA table_info(alerts)")

columns = [
    column[1]
    for column in cursor.fetchall()
]

# Add status column for old database
if "status" not in columns:

    cursor.execute("""
    ALTER TABLE alerts
    ADD COLUMN status TEXT DEFAULT 'Open'
    """)

# Add analyst notes column for old database
if "analyst_notes" not in columns:

    cursor.execute("""
    ALTER TABLE alerts
    ADD COLUMN analyst_notes TEXT DEFAULT ''
    """)

connection.commit()

connection.close()

print("SOC database updated successfully.")