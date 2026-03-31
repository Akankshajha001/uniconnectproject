"""
Lost & Found Service - Business logic for lost and found items
"""

from datetime import datetime
from typing import List, Dict, Optional
import random
from database.lost_found_db import add_item, get_all_items as db_get_all_items, get_item_by_id as db_get_item_by_id, update_item_status

def generate_verification_code() -> str:
    """Generate a unique 5-digit verification code"""
    return str(random.randint(10000, 99999))

def add_lost_item(item_name: str, category: str, location: str, 
                  description: str, reporter_name: str, reporter_contact: str,
                  image_path: str = None) -> Dict:
    """Add a new lost item to the database (SQLite)"""
    new_item = {
        'type': 'lost',
        'item_name': item_name,
        'category': category,
        'location': location,
        'description': description,
        'reporter_name': reporter_name,
        'reporter_contact': reporter_contact,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'open',
        'matched_with': None,
        'verification_code': generate_verification_code(),
        'image_path': image_path
    }
    new_id = add_item(new_item)
    new_item['id'] = new_id
    return new_item

def add_found_item(item_name: str, category: str, location: str,
                   description: str, reporter_name: str, reporter_contact: str,
                   image_path: str = None, secret_details: str = None,
                   color: str = None, brand: str = None) -> Dict:
    """Add a new found item to the database (SQLite)"""
    new_item = {
        'type': 'found',
        'item_name': item_name,
        'category': category,
        'location': location,
        'description': description,
        'reporter_name': reporter_name,
        'reporter_contact': reporter_contact,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'status': 'open',
        'matched_with': None,
        'verification_code': generate_verification_code(),
        'image_path': image_path,
        'secret_details': secret_details,
        'color': color,
        'brand': brand
    }
    new_id = add_item(new_item)
    new_item['id'] = new_id
    return new_item

def get_all_items() -> List[Dict]:
    """Get all lost and found items from SQLite DB"""
    return db_get_all_items()

def get_lost_items() -> List[Dict]:
    """Get only lost items from SQLite DB"""
    return [item for item in db_get_all_items() if item['type'] == 'lost']

def get_found_items() -> List[Dict]:
    """Get only found items from SQLite DB"""
    return [item for item in db_get_all_items() if item['type'] == 'found']

def get_item_by_id(item_id: int) -> Optional[Dict]:
    """Get item by ID from SQLite DB"""
    return db_get_item_by_id(item_id)

def find_potential_matches(item_type: str, category: str, location: str) -> List[Dict]:
    """
    Find potential matches for a lost or found item (SQLite DB)
    Match based on category and location
    """
    opposite_type = 'found' if item_type == 'lost' else 'lost'
    matches = []
    for item in db_get_all_items():
        if item['type'] == opposite_type and item['status'] == 'open':
            if item['category'].lower() == category.lower():
                item_copy = item.copy()
                item_copy['match_score'] = 10
                if item['location'].lower() == location.lower():
                    item_copy['match_score'] = 20
                matches.append(item_copy)
    matches.sort(key=lambda x: x['match_score'], reverse=True)
    return matches

def get_user_lost_items(user_email: str, user_name: str, category: str = None) -> List[Dict]:
    """
    Get all open lost items reported by a specific user
    Optionally filter by category
    """
    all_items = db_get_all_items()
    user_lost_items = []
    for item in all_items:
        if item['type'] == 'lost' and item['status'] == 'open':
            # Match by email or name
            if (item['reporter_contact'].lower() == user_email.lower() or 
                item['reporter_name'].lower() == user_name.lower()):
                if category is None or item['category'].lower() == category.lower():
                    user_lost_items.append(item)
    return user_lost_items

def verify_user_lost_item_otp(user_email: str, user_name: str, category: str, otp: str) -> Optional[Dict]:
    """
    Verify if user has a lost item of the given category with matching OTP
    Returns the matching lost item if found, None otherwise
    """
    user_lost_items = get_user_lost_items(user_email, user_name, category)
    for item in user_lost_items:
        if str(item.get('verification_code', '')).strip() == otp.strip():
            return item
    return None

def claim_item_with_match(found_item_id: int, lost_item_id: int, claimer_name: str, 
                          claimer_email: str = "", claimer_contact: str = "") -> bool:
    """
    Mark both found and lost items as claimed and link them
    """
    found_item = db_get_item_by_id(found_item_id)
    lost_item = db_get_item_by_id(lost_item_id)
    
    if not found_item or not lost_item:
        return False
    
    # Update both items status to claimed
    update_item_status(found_item_id, 'claimed')
    update_item_status(lost_item_id, 'claimed')
    return True

def claim_item(item_id: int, claimer_name: str, verification_detail: str = "", 
               claimer_email: str = "", claimer_contact: str = "") -> bool:
    """
    Mark an item as claimed with verification details (SQLite DB)
    Also marks any matching LOST items from the claimer as claimed
    """
    item = db_get_item_by_id(item_id)
    if not item:
        return False
    
    # Update the claimed item status
    update_item_status(item_id, 'claimed')
    
    # If this is a FOUND item being claimed, also mark claimer's LOST items of same category as claimed
    if item['type'] == 'found' and claimer_email:
        category = item['category']
        all_items = db_get_all_items()
        for lost_item in all_items:
            if (lost_item['type'] == 'lost' and 
                lost_item['status'] == 'open' and
                lost_item['category'].lower() == category.lower() and
                lost_item['reporter_contact'].lower() == claimer_email.lower()):
                # Mark the claimer's lost item as claimed too
                update_item_status(lost_item['id'], 'claimed')
    
    return True

def get_recent_items(limit: int = 10) -> List[Dict]:
    """Get most recent items from SQLite DB"""
    items = db_get_all_items()
    sorted_items = sorted(items, key=lambda x: x['date'], reverse=True)
    return sorted_items[:limit]

def search_items(query: str) -> List[Dict]:
    """Search items by name, category, or location from SQLite DB"""
    query_lower = query.lower()
    results = []
    for item in db_get_all_items():
        if (query_lower in item['item_name'].lower() or 
            query_lower in item['category'].lower() or 
            query_lower in item['location'].lower() or
            query_lower in item['description'].lower()):
            results.append(item)
    return results

def get_items_by_status(status: str) -> List[Dict]:
    """Get items filtered by status from SQLite DB"""
    return [item for item in db_get_all_items() if item['status'] == status]
