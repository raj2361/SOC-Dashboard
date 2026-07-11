import sqlite3


connection = sqlite3.connect("soc.db")

cursor = connection.cursor()


alerts = [
    ("SSH Brute Force", "Critical", "192.168.1.50", "192.168.1.10", "2026-07-10 10:30:00"),
    ("Port Scan Detected", "High", "10.0.0.5", "192.168.1.20", "2026-07-10 10:35:00"),
    ("Multiple Failed Logins", "Medium", "192.168.1.25", "192.168.1.15", "2026-07-10 10:40:00"),
    ("Suspicious DNS Request", "Low", "192.168.1.30", "8.8.8.8", "2026-07-10 10:45:00"),
    ("Malware Detected", "Critical", "192.168.1.60", "192.168.1.5", "2026-07-10 10:50:00")
]


cursor.executemany("""
INSERT INTO alerts (
    alert_name,
    severity,
    source_ip,
    destination_ip,
    timestamp
)
VALUES (?, ?, ?, ?, ?)
""", alerts)


connection.commit()

connection.close()


print("Security alerts inserted successfully.")