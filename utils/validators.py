"""
Validators - Input validation functions with industry-standard rules
"""

import re
from typing import Tuple

# Common valid email domains
VALID_EMAIL_DOMAINS = [
    'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'live.com',
    'icloud.com', 'mail.com', 'protonmail.com', 'zoho.com', 'aol.com',
    'edu', 'ac.in', 'edu.in', 'org', 'gov.in'
]

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format with strict real email validation
    Returns: (is_valid, error_message)
    """
    if not email:
        return False, "Email cannot be empty"
    
    email = email.strip().lower()
    
    # Basic email pattern
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    # Check for valid structure
    if '..' in email:
        return False, "Email cannot contain consecutive dots"
    
    # Extract domain
    try:
        local, domain = email.rsplit('@', 1)
    except ValueError:
        return False, "Invalid email format"
    
    # Local part validation
    if len(local) < 1 or len(local) > 64:
        return False, "Email username must be between 1-64 characters"
    
    # Domain validation
    if len(domain) < 4:
        return False, "Invalid email domain"
    
    # Check if domain has valid TLD
    if '.' not in domain:
        return False, "Email must have a valid domain (e.g., gmail.com)"
    
    tld = domain.split('.')[-1]
    if len(tld) < 2:
        return False, "Invalid email domain extension"
    
    # Check for common valid domains or educational domains
    is_valid_domain = False
    for valid_domain in VALID_EMAIL_DOMAINS:
        if domain.endswith(valid_domain) or domain == valid_domain:
            is_valid_domain = True
            break
    
    # Also accept any .edu, .ac.*, .org domain
    if domain.endswith('.edu') or '.ac.' in domain or domain.endswith('.org'):
        is_valid_domain = True
    
    # Accept common email providers
    common_providers = ['gmail', 'yahoo', 'outlook', 'hotmail', 'icloud', 'protonmail']
    for provider in common_providers:
        if provider in domain:
            is_valid_domain = True
            break
    
    if not is_valid_domain:
        return False, "Please use a valid email (Gmail, Yahoo, Outlook, or educational email)"
    
    return True, ""


def validate_roll_no(roll_no: str) -> Tuple[bool, str]:
    """
    Validate roll number - must be exactly 7 digits
    Returns: (is_valid, error_message)
    """
    if not roll_no:
        return False, "Roll number cannot be empty"
    
    roll_no = roll_no.strip()
    
    # Must be exactly 7 digits
    if not roll_no.isdigit():
        return False, "Roll number must contain only digits (0-9)"
    
    if len(roll_no) != 7:
        return False, "Roll number must be exactly 7 digits"
    
    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password with strong requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    Returns: (is_valid, error_message)
    """
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 128:
        return False, "Password is too long (max 128 characters)"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter (A-Z)"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter (a-z)"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit (0-9)"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\;\'`~]', password):
        return False, "Password must contain at least one special character (!@#$%^&*)"
    
    return True, ""


def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate name (should not be empty and reasonable length)
    Returns: (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    name = name.strip()
    
    if len(name) < 2:
        return False, "Name too short (minimum 2 characters)"
    
    if len(name) > 100:
        return False, "Name too long (maximum 100 characters)"
    
    # Name should contain only letters, spaces, and common name characters
    if not re.match(r"^[a-zA-Z\s\.\-']+$", name):
        return False, "Name should contain only letters, spaces, dots, hyphens, or apostrophes"
    
    return True, ""


def validate_file_name(file_name: str) -> Tuple[bool, str]:
    """
    Validate file name format
    Returns: (is_valid, error_message)
    """
    if not file_name:
        return False, "File name cannot be empty"
    
    # Check for invalid characters
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
    for char in invalid_chars:
        if char in file_name:
            return False, f"File name contains invalid character: {char}"
    
    # Check extension
    if '.' not in file_name:
        return False, "File name should have an extension"
    
    return True, ""


def validate_description(description: str, min_length: int = 10, max_length: int = 500) -> Tuple[bool, str]:
    """
    Validate description text
    Returns: (is_valid, error_message)
    """
    if not description or not description.strip():
        return False, "Description cannot be empty"
    
    desc_length = len(description.strip())
    
    if desc_length < min_length:
        return False, f"Description too short (minimum {min_length} characters)"
    
    if desc_length > max_length:
        return False, f"Description too long (maximum {max_length} characters)"
    
    return True, ""


def validate_category(category: str, valid_categories: list) -> Tuple[bool, str]:
    """
    Validate category against a list of valid categories
    Returns: (is_valid, error_message)
    """
    if not category:
        return False, "Category cannot be empty"
    
    if category not in valid_categories:
        return False, f"Invalid category. Must be one of: {', '.join(valid_categories)}"
    
    return True, ""
