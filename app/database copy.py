import sqlite3
from typing import List, Dict

DB_PATH = "regulations.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS regulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            hash TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_regulations(data: List[Dict]):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for item in data:
        try:
            cur.execute("""
                INSERT INTO regulations (title, url, hash, date)
                VALUES (?, ?, ?, ?)
            """, (item["title"], item["url"], item["hash"], item["date"]))
        except sqlite3.IntegrityError:
            pass  # Já existe
    conn.commit()
    conn.close()

def get_latest():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT title, url, date FROM regulations ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    return [{"title": r[0], "url": r[1], "date": r[2]} for r in rows]