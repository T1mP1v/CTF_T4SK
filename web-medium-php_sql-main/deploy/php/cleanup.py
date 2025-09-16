import sqlite3, time

DB_PATH = "/var/www/html/data/db.sqlite" 

def cleanup():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM scans;")
        conn.commit()
        conn.close()
        print("Table 'scans' cleaned.")
    except Exception as e:
        print(f"Error during cleanup: {e}")

while True:
    cleanup()
    time.sleep(3600)
