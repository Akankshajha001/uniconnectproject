
"""
User Database - SQLite persistent user management with signup/login
Industry-standard security with bcrypt password hashing
"""

import sqlite3
from typing import Dict, Optional
import os

# Try to use bcrypt (industry standard), fallback to hashlib if not available
try:
    import bcrypt
    USE_BCRYPT = True
except ImportError:
    import hashlib 
    USE_BCRYPT = False

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def _get_conn():
    return sqlite3.connect(DB_PATH)

def _init_db():
    conn = _get_conn()
    c = conn.cursor()
    
    # Check if users table exists and has correct schema
    try:
        c.execute("SELECT id, name, roll_no, email, password_hash FROM users LIMIT 1")
    except sqlite3.OperationalError:
        c.execute("DROP TABLE IF EXISTS user_activity")
        c.execute("DROP TABLE IF EXISTS users")
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        last_login TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_activity (
        user_id INTEGER PRIMARY KEY,
        items_reported INTEGER DEFAULT 0,
        notes_uploaded INTEGER DEFAULT 0,
        notes_downloaded INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    # Add new columns if they don't exist
    try:
        c.execute('ALTER TABLE users ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE users ADD COLUMN last_login TEXT')
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

_init_db()

def hash_password(password: str) -> str:
    """Hash password using bcrypt (industry standard) or SHA256 fallback"""
    if USE_BCRYPT:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    else:
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    if USE_BCRYPT:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except ValueError:
            # Old SHA256 hash - verify with SHA256
            import hashlib
            return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed
    else:
        import hashlib
        return hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed

def signup_user(name: str, roll_no: str, email: str, password: str) -> bool:
    """Register a new user. Returns True if successful, False if user/email/roll exists."""
    conn = _get_conn()
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO users (name, roll_no, email, password_hash) VALUES (?, ?, ?, ?)''',
                  (name, roll_no, email, hash_password(password)))
        user_id = c.lastrowid
        c.execute('''INSERT INTO user_activity (user_id) VALUES (?)''', (user_id,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email_or_roll: str, password: str) -> Optional[Dict]:
    """Authenticate user by email or roll_no and password. Returns user dict if valid, else None."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''SELECT id, name, roll_no, email, password_hash FROM users WHERE email = ? OR roll_no = ?''',
              (email_or_roll, email_or_roll))
    row = c.fetchone()
    if row and verify_password(password, row[4]):
        # Update last login time
        c.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (row[0],))
        conn.commit()
        conn.close()
        return {'id': row[0], 'name': row[1], 'roll_no': row[2], 'email': row[3]}
    conn.close()
    return None

def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT id, name, roll_no, email FROM users WHERE id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {'id': row[0], 'name': row[1], 'roll_no': row[2], 'email': row[3]}
    return None

def get_user_by_email(email: str) -> Optional[Dict]:
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT id, name, roll_no, email FROM users WHERE email = ?', (email,))
    row = c.fetchone()
    conn.close()
    if row:
        return {'id': row[0], 'name': row[1], 'roll_no': row[2], 'email': row[3]}
    return None

def update_user_activity(user_id: int, activity_type: str):
    """Update user activity count in DB for a specific user_id
    
    Note: Only tracks notes_downloaded cumulatively. 
    items_reported and notes_uploaded are counted from actual database records.
    """
    if not user_id or not isinstance(user_id, (int, float)):
        return  # Skip if invalid user_id
    
    user_id = int(user_id)  # Ensure it's an integer
    
    conn = _get_conn()
    c = conn.cursor()
    
    # Ensure user_activity record exists for this user
    c.execute('INSERT OR IGNORE INTO user_activity (user_id) VALUES (?)', (user_id,))
    
    # Only track download activity (items_reported and notes_uploaded are counted from DB)
    if activity_type == 'note_downloaded':
        c.execute('UPDATE user_activity SET notes_downloaded = notes_downloaded + 1 WHERE user_id = ?', (user_id,))
    # item_reported and note_uploaded are now counted from actual database records, so we skip incrementing
    
    conn.commit()
    conn.close()

def get_all_users() -> Dict:
    """Get all users and their activity from DB"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''SELECT u.id, u.name, u.roll_no, u.email, a.items_reported, a.notes_uploaded, a.notes_downloaded
                 FROM users u LEFT JOIN user_activity a ON u.id = a.user_id''')
    rows = c.fetchall()
    conn.close()
    result = {}
    for row in rows:
        result[row[0]] = {
            'name': row[1],
            'roll_no': row[2],
            'email': row[3],
            'items_reported': row[4] or 0,
            'notes_uploaded': row[5] or 0,
            'notes_downloaded': row[6] or 0
        }
    return result
