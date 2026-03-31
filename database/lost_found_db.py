
"""
Lost & Found Database - SQLite persistent storage
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), 'lost_found.db')

def _get_conn():
    return sqlite3.connect(DB_PATH)

def _init_db():
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lost_found_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        item_name TEXT,
        category TEXT,
        location TEXT,
        description TEXT,
        reporter_name TEXT,
        reporter_contact TEXT,
        date TEXT,
        status TEXT,
        matched_with INTEGER,
        verification_code TEXT,
        image_path TEXT,
        secret_details TEXT,
        color TEXT,
        brand TEXT
    )''')
    # Add new columns if they don't exist (for existing databases)
    try:
        c.execute('ALTER TABLE lost_found_items ADD COLUMN secret_details TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    try:
        c.execute('ALTER TABLE lost_found_items ADD COLUMN color TEXT')
    except sqlite3.OperationalError:
        pass
    try:
        c.execute('ALTER TABLE lost_found_items ADD COLUMN brand TEXT')
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

_init_db()

def add_item(item: Dict) -> int:
    """Add a lost or found item to the database. Returns new item id."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO lost_found_items (
        type, item_name, category, location, description, reporter_name, reporter_contact, date, status, matched_with, verification_code, image_path, secret_details, color, brand
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        item['type'], item['item_name'], item['category'], item['location'], item['description'],
        item['reporter_name'], item['reporter_contact'], item.get('date', datetime.now().strftime('%Y-%m-%d')),
        item.get('status', 'open'), item.get('matched_with'), item.get('verification_code'), item.get('image_path'),
        item.get('secret_details'), item.get('color'), item.get('brand')
    ))
    item_id = c.lastrowid
    conn.commit()
    conn.close()
    return item_id

def get_all_items() -> List[Dict]:
    """Get all lost and found items from the database."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM lost_found_items')
    rows = c.fetchall()
    conn.close()
    keys = ['id', 'type', 'item_name', 'category', 'location', 'description', 'reporter_name', 'reporter_contact', 'date', 'status', 'matched_with', 'verification_code', 'image_path', 'secret_details', 'color', 'brand']
    return [dict(zip(keys, row)) for row in rows]

def get_item_by_id(item_id: int) -> Optional[Dict]:
    """Get a single item by id."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM lost_found_items WHERE id = ?', (item_id,))
    row = c.fetchone()
    conn.close()
    if row:
        keys = ['id', 'type', 'item_name', 'category', 'location', 'description', 'reporter_name', 'reporter_contact', 'date', 'status', 'matched_with', 'verification_code', 'image_path', 'secret_details', 'color', 'brand']
        return dict(zip(keys, row))
    return None

def update_item_status(item_id: int, status: str, matched_with: Optional[int] = None):
    """Update the status and optionally matched_with for an item."""
    conn = _get_conn()
    c = conn.cursor()
    if matched_with is not None:
        c.execute('UPDATE lost_found_items SET status = ?, matched_with = ? WHERE id = ?', (status, matched_with, item_id))
    else:
        c.execute('UPDATE lost_found_items SET status = ? WHERE id = ?', (status, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id: int):
    """Delete an item from the database."""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('DELETE FROM lost_found_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

def get_items_count() -> int:
    """Get total count of items in database"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM lost_found_items')
    count = c.fetchone()[0]
    conn.close()
    return count

def get_claimed_count() -> int:
    """Get count of claimed items"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM lost_found_items WHERE status = 'claimed'")
    count = c.fetchone()[0]
    conn.close()
    return count
