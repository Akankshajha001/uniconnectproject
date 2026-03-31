"""
Lost & Found Service - Direct Contact + Manual Claim
"""

from datetime import datetime
from typing import List, Dict, Optional
import random
import json
from database.lost_found_db import (
    add_item, get_all_items as db_get_all_items, 
    get_item_by_id as db_get_item_by_id, update_item_status
)

def generate_verification_code() -> str:
    return str(random.randint(10000, 99999))

def add_lost_item(item_name: str, category: str, location: str, 
                  description: str, reporter_name: str, reporter_contact: str,
                  image_path: str = None) -> Dict:
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
                   color: str = None, brand: str = None,
                   verification_data: Dict = None) -> Dict:
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
        'brand': brand,
        'verification_data': json.dumps(verification_data) if verification_data else None,
        'pending_claims': None
    }
    new_id = add_item(new_item)
    new_item['id'] = new_id
    return new_item

def get_all_items() -> List[Dict]:
    return db_get_all_items()

def get_lost_items() -> List[Dict]:
    return [item for item in db_get_all_items() if item['type'] == 'lost']

def get_found_items() -> List[Dict]:
    return [item for item in db_get_all_items() if item['type'] == 'found']

def get_item_by_id(item_id: int) -> Optional[Dict]:
    return db_get_item_by_id(item_id)

def claim_item(item_id: int, claimer_name: str, verification_detail: str = "", 
               claimer_email: str = "", claimer_contact: str = "") -> bool:
    item = db_get_item_by_id(item_id)
    if not item:
        return False
    
    update_item_status(item_id, 'claimed')
    
    # Also mark claimer's LOST items of same category as claimed
    if item['type'] == 'found' and claimer_email:
        category = item['category']
        all_items = db_get_all_items()
        for lost_item in all_items:
            if (lost_item['type'] == 'lost' and 
                lost_item['status'] == 'open' and
                lost_item['category'].lower() == category.lower() and
                lost_item['reporter_contact'].lower() == claimer_email.lower()):
                update_item_status(lost_item['id'], 'claimed')
    
    return True

def search_items(query: str) -> List[Dict]:
    query_lower = query.lower()
    results = []
    for item in db_get_all_items():
        if (query_lower in item['item_name'].lower() or 
            query_lower in item['category'].lower() or 
            query_lower in item['location'].lower() or
            query_lower in item['description'].lower()):
            results.append(item)
    return results
