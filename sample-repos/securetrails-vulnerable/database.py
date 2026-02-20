import sqlite3
from datetime import datetime

DATABASE = 'database.db'

def init_db():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Trails table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trails (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            difficulty TEXT,
            created_by INTEGER
        )
    ''')
    
    # Comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trail_comments (
            id INTEGER PRIMARY KEY,
            trail_id INTEGER,
            comment TEXT,
            created_at TIMESTAMP
        )
    ''')
    
    # Insert test data
    cursor.execute('''
        INSERT OR IGNORE INTO users VALUES 
        (1, 'admin', ?, 'admin@securetrails.com', 'admin')
    ''', ('5f4dcc3b5aa765d61d8327deb882cf99',))  # MD5 of 'admin'
    
    cursor.execute('''
        INSERT OR IGNORE INTO trails VALUES 
        (1, 'Mountain Peak Trail', 'A challenging hike with great views', 'hard', 1),
        (2, 'Forest Loop', 'Easy walk through beautiful forest', 'easy', 1),
        (3, 'Valley Vista', 'Moderate hike with valley views', 'moderate', 1)
    ''')
    
    db.commit()
    db.close()

if __name__ == '__main__':
    init_db()
