# 🔐 Verification Code & Image Upload Features

## New Features Implemented

### 1. 🔑 5-Digit Verification Code System

#### What It Does:
- Every reported item (lost or found) gets a unique **5-digit verification code**
- Reporter receives this code immediately after reporting
- Claimer must provide this code to complete the claim
- Prevents unauthorized claims

#### How It Works:

**For Reporters:**
1. Report a lost/found item
2. Receive a unique 5-digit code (e.g., **12345**)
3. Save this code securely
4. Share only with the legitimate owner/claimer

**For Claimers:**
1. Find the item they want to claim
2. Login to the system
3. Click "Claim Item"
4. Enter the 5-digit verification code
5. Provide proof of ownership
6. Submit claim

**Security:**
- Code is randomly generated (10000-99999)
- Must match exactly to proceed
- Shown in prominent yellow/blue box after reporting
- Acts as first layer of verification

#### Visual Display:
```
🔑 Important - Save This Information!

Item ID: #4
Verification Code: 54321  (displayed in large colored box)
Status: Open

⚠️ Keep this verification code safe! 
You'll need it when someone claims your item.
```

---

### 2. 📸 Optional Image Upload

#### What It Does:
- Allows uploading photos of lost/found items
- **Completely optional** (recognizes photos may not always be available)
- Displays images in item cards for easy identification
- Stores images securely in `uploaded_images/` folder

#### Supported Formats:
- PNG
- JPG/JPEG

#### How It Works:

**During Reporting:**
1. Fill in item details
2. See "📸 Optional: Upload Image" section
3. Upload image if available (or skip)
4. Submit report

**File Storage:**
- Images saved as: `lost_YYYYMMDD_HHMMSS_filename.ext`
- Or: `found_YYYYMMDD_HHMMSS_filename.ext`
- Organized in `uploaded_images/` directory
- Unique timestamp prevents name conflicts

**Display:**
- Items with images: Show image + details side-by-side
- Items without images: Show regular text card
- Images auto-resize to fit card layout

#### Example Layout:

**With Image:**
```
┌─────────────┬──────────────────────────┐
│   [IMAGE]   │  📢 Black Wallet        │
│   Photo of  │  Category: Wallet        │
│   the item  │  Location: Library       │
│             │  Description: ...        │
└─────────────┴──────────────────────────┘
```

**Without Image:**
```
┌────────────────────────────────────────┐
│  📢 Black Wallet                       │
│  Category: Wallet | Location: Library  │
│  Description: Black leather wallet...  │
└────────────────────────────────────────┘
```

---

## Combined Verification Flow

### Complete Security Process:

1. **Login Required** ✅
   - Must be logged in to claim
   
2. **Verification Code** ✅ (NEW)
   - Enter 5-digit code from reporter
   
3. **Proof of Ownership** ✅
   - Detailed description (min 10 chars)
   
4. **Contact Verification** ✅
   - Valid phone number
   
5. **Image Reference** ✅ (NEW - if available)
   - Can compare claim details with uploaded image

### Security Layers:

```
Layer 1: Login Requirement (Must have account)
Layer 2: Verification Code (Must know secret code)
Layer 3: Detailed Proof (Must describe item specifics)
Layer 4: Contact Info (Must provide real contact)
Layer 5: Image Comparison (Optional visual verification)
```

---

## Technical Implementation

### Files Modified:

#### 1. `services/lost_found_service.py`
```python
# Added verification code generation
import random

def generate_verification_code() -> str:
    """Generate unique 5-digit code"""
    return str(random.randint(10000, 99999))

# Updated add_lost_item() and add_found_item()
# Now includes: verification_code and image_path parameters
```

#### 2. `ui/lost_found_ui.py`
```python
# Added imports
import os
from datetime import datetime

# Added image upload widget in both forms
image_file = st.file_uploader(
    "Upload image of the item (optional)",
    type=['png', 'jpg', 'jpeg']
)

# Image handling and storage
if image_file is not None:
    image_dir = "uploaded_images"
    os.makedirs(image_dir, exist_ok=True)
    image_path = os.path.join(image_dir, f"lost_{timestamp}_{filename}")
    # Save file...

# Updated item card rendering to show images
def render_item_card(item):
    if item.get('image_path'):
        # Show image + details side-by-side
    else:
        # Show regular text card

# Added verification code field in claim form
verification_code_input = st.text_input(
    "5-Digit Verification Code *",
    max_chars=5
)

# Validation
if verification_code_input != item.get('verification_code'):
    st.error("❌ Incorrect verification code!")
```

#### 3. `database/lost_found_db.py`
```python
# Updated sample data with verification codes
lost_found_items = [
    {
        'id': 1,
        # ... other fields ...
        'verification_code': '12345',
        'image_path': None
    }
]
```

---

## User Experience Examples

### Example 1: Lost Item with Photo

**Reporter (Ravi):**
1. Lost his black wallet
2. Has a photo from before he lost it
3. Reports item with photo upload
4. Receives code: **78901**
5. Posts code on campus notice board

**Claimer (Owner):**
1. Sees notice with code
2. Logs in to system
3. Searches for wallet
4. Sees photo - confirms it's his
5. Enters code: **78901**
6. Describes contents: "Has my ID, HDFC card, Rs. 200"
7. Claim approved!

### Example 2: Found Item without Photo

**Reporter (Priya):**
1. Found ID card in cafeteria
2. No camera available to take photo
3. Reports without image (optional)
4. Receives code: **45678**
5. Waits for owner to contact

**Claimer (Owner):**
1. Realizes ID is missing
2. Checks Lost & Found
3. Finds listing (no image, but description matches)
4. Contacts reporter for code
5. Enters code: **45678**
6. Describes: "Name on ID: Rohan Sharma, Roll: 12345"
7. Claim approved!

---

## Benefits

### For Reporters:
✅ **Verification code** ensures only authorized person claims  
✅ **Optional images** help legitimate owners identify items  
✅ Can skip images if not available  
✅ Extra security without complexity

### For Claimers:
✅ **Images** help confirm item before claiming  
✅ **Verification code** proves they've talked to reporter  
✅ Faster identification with visual reference  
✅ Clear proof of legitimate claim

### For System:
✅ **Two-layer verification**: code + proof of ownership  
✅ **Flexible**: works with or without images  
✅ **Scalable**: image storage organized by timestamp  
✅ **User-friendly**: optional features don't block usage

---

## Sample Data for Testing

### Test Items with Codes:

1. **Black Water Bottle** (Lost)
   - ID: #1
   - Code: **12345**
   - No image

2. **Student ID Card** (Found)
   - ID: #2
   - Code: **67890**
   - No image

3. **Laptop Charger** (Lost)
   - ID: #3
   - Code: **54321**
   - No image

### Testing Steps:

1. **Login** as any user
2. **Report new item** with/without image
3. **Note the verification code** displayed
4. **Browse items** to see image display (if uploaded)
5. **Try claiming** with wrong code → Should fail ❌
6. **Try claiming** with correct code → Should work ✅

---

## Future Enhancements (Optional)

1. **QR Code Generation**: Convert 5-digit code to QR code
2. **Image Preview**: Show thumbnail in search results
3. **Multiple Images**: Allow uploading multiple photos
4. **Image Compression**: Reduce file size automatically
5. **OCR**: Extract text from images (for ID cards, etc.)
6. **SMS Code Delivery**: Send code via SMS to reporter
7. **Code Expiry**: Make codes expire after certain days

---

## Summary

### What's New:
1. ✅ **5-digit verification codes** for all items
2. ✅ **Optional image uploads** for visual identification
3. ✅ **Smart image display** in item cards
4. ✅ **Code validation** during claims
5. ✅ **Prominent code display** after reporting

### Security Improvement:
- **Before**: Login + Proof of ownership
- **After**: Login + **Verification Code** + Proof of ownership + **Optional Image**

### Flexibility:
- Images are **completely optional**
- System works perfectly without images
- Recognizes real-world constraints (no camera, no old photos, etc.)

---

**Status:** ✅ Fully Implemented and Ready to Use  
**Date:** January 11, 2026  
**Image Storage:** `uploaded_images/` folder (auto-created)
