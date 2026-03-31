"""
Lost & Found UI - User interface for lost and found items
Secret Details + Verification System
"""

import streamlit as st
import os
from datetime import datetime
from services.lost_found_service import (
    add_lost_item,
    add_found_item,
    get_all_items,
    get_lost_items,
    get_found_items,
    find_potential_matches,
    claim_item,
    search_items
)
from database.users_db import update_user_activity
from utils.helpers import format_date, get_date_difference, truncate_text
from utils.validators import validate_name, validate_description

# Categories for items
CATEGORIES = ['ID Card', 'Bottle', 'Charger', 'Book', 'Umbrella', 'Keys', 
              'Phone', 'Wallet', 'Bag', 'Laptop', 'Headphones', 'Other']

# Common locations on campus
LOCATIONS = ['Library', 'Cafeteria', 'Computer Lab', 'Main Building', 
             'Sports Complex', 'Auditorium', 'Parking Area', 'Garden', 
             'Hostel Area', 'Other']

def show_claim_success_popup(finder_name, finder_contact, item_category):
    """Show big success message for successful claim - using Streamlit components"""
    # This function is now empty - popup is handled inline in render_lost_found
    pass

def render_lost_found():
    """Main render function for Lost & Found section"""
    
    # Check for claim success popup - using simple Streamlit components
    if st.session_state.get('show_claim_popup', False):
        popup_data = st.session_state.get('claim_popup_data', {})
        finder_name = popup_data.get('finder_name', '')
        finder_contact = popup_data.get('finder_contact', '')
        item_category = popup_data.get('category', '')
        
        st.balloons()
        
        # Big success message
        st.success("🎉 **CLAIM SUCCESSFUL!**")
        
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                        padding: 2rem; border-radius: 20px; color: white; text-align: center;
                        margin: 1rem 0; box-shadow: 0 10px 40px rgba(0,0,0,0.2);'>
                <h2 style='margin: 0;'>Your {item_category} claim has been verified!</h2>
                <div style='background: rgba(255,255,255,0.2); padding: 1.5rem; border-radius: 15px; margin: 1.5rem 0;'>
                    <h3 style='margin: 0;'>📞 Contact the Finder</h3>
                    <p style='font-size: 1.5rem; margin: 0.5rem 0; font-weight: bold;'>{finder_name}</p>
                    <p style='font-size: 1.2rem; margin: 0;'>📧 {finder_contact}</p>
                </div>
                <p>Contact them to arrange pickup of your item!</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        
        # Close button - prominent and clickable
        if st.button("✖ CLOSE & CONTINUE", key="close_popup_btn", type="primary", use_container_width=True):
            st.session_state['show_claim_popup'] = False
            st.session_state['claim_popup_data'] = {}
            st.rerun()
        
        st.stop()
    
    # Check if user is logged in
    if 'user' not in st.session_state or st.session_state.user is None:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; color: white; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 2rem;'>
                <h1 style='margin: 0; font-size: 2.5rem;'>🔍 Lost & Found Center</h1>
                <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;'>
                    Help reunite items with their owners
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.error("🔒 Please login from the sidebar to access the Lost & Found section.")
        return
    
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; color: white; 
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2.5rem;'>🔍 Lost & Found Center</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;'>
                Help reunite items with their owners
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Action Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📢 Report Lost", 
        "✅ Report Found", 
        "🔍 Lost Items",
        "📦 Found Items",
        "✅ Claimed"
    ])
    
    with tab1:
        render_report_lost()
    
    with tab2:
        render_report_found()
    
    with tab3:
        render_lost_items_tab()
    
    with tab4:
        render_found_items_tab()
    
    with tab5:
        render_claimed_items()

def render_report_lost():
    """Form to report a lost item with optional image"""
    st.markdown("### 📢 Report a Lost Item")
    st.info("ℹ️ Provide details about your lost item. Add a photo if available for better identification.")
    
    with st.form("report_lost_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Category *", options=CATEGORIES)
            location = st.selectbox("Last Seen Location *", options=LOCATIONS)
        
        with col2:
            user = st.session_state.user
            reporter_name = st.text_input("Your Name *", value=user.get('name', ''))
            reporter_contact = st.text_input("Contact (Email/Phone) *", value=user.get('email', ''))
        
        description = st.text_area(
            "Description *",
            placeholder="Describe your item: color, brand, distinguishing features...",
            height=100
        )
        
        # Optional image upload
        st.markdown("**📸 Upload Photo (Optional)**")
        image_file = st.file_uploader(
            "Upload image of the item",
            type=['png', 'jpg', 'jpeg'],
            help="A photo helps others identify your item",
            key="lost_image"
        )
        
        submit = st.form_submit_button("🚀 Submit Lost Item Report", use_container_width=True)
        
        if submit:
            if not all([category, location, reporter_name, reporter_contact, description]):
                st.error("❌ Please fill all required fields")
            else:
                name_valid, name_error = validate_name(reporter_name)
                if not name_valid:
                    st.error(f"❌ {name_error}")
                    return
                
                # Handle image upload
                image_path = None
                if image_file:
                    image_dir = "uploaded_images"
                    os.makedirs(image_dir, exist_ok=True)
                    image_path = os.path.join(image_dir, f"lost_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_file.name}")
                    with open(image_path, "wb") as f:
                        f.write(image_file.getbuffer())
                
                item = add_lost_item(
                    item_name=category,
                    category=category,
                    location=location,
                    description=description,
                    reporter_name=reporter_name,
                    reporter_contact=reporter_contact,
                    image_path=image_path
                )
                
                update_user_activity(st.session_state.user['id'], 'item_reported')
                st.success("✅ Lost item reported successfully!")
                st.balloons()

def render_report_found():
    """Form to report a found item with SECRET DETAILS and optional image"""
    st.markdown("### ✅ Report a Found Item")
    
    st.markdown("""
        <div style='background: #fff3cd; padding: 1rem; border-radius: 10px; margin: 1rem 0;
                    border-left: 4px solid #ffc107;'>
            <p style='margin: 0; color: #856404;'>
                🔐 <strong>Secret Details:</strong> Enter details that only the true owner would know.
                These are HIDDEN from public and used to verify ownership.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("report_found_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Category *", options=CATEGORIES)
            location = st.selectbox("Found Location *", options=LOCATIONS)
        
        with col2:
            user = st.session_state.user
            reporter_name = st.text_input("Your Name *", value=user.get('name', ''))
            reporter_contact = st.text_input("Contact (Email/Phone) *", value=user.get('email', ''))
        
        description = st.text_area(
            "Public Description",
            placeholder="Brief description (e.g., 'Phone found near library')",
            height=60
        )
        
        # Optional image upload
        st.markdown("**📸 Upload Photo (Optional)**")
        image_file = st.file_uploader(
            "Upload image of the found item",
            type=['png', 'jpg', 'jpeg'],
            help="Photo helps owner identify their item",
            key="found_image"
        )
        
        st.markdown("---")
        st.markdown("### 🔐 Secret Verification Details (Hidden from Public)")
        
        col3, col4 = st.columns(2)
        with col3:
            color = st.text_input("Color *", placeholder="e.g., Blue, Black with silver")
        with col4:
            brand = st.text_input("Brand/Model", placeholder="e.g., Samsung, Nike")
        
        secret_details = st.text_area(
            "Secret Details *",
            placeholder="Unique marks, scratches, stickers, what's inside...",
            height=100
        )
        
        submit = st.form_submit_button("✅ Submit Found Item Report", use_container_width=True)
        
        if submit:
            if not all([category, location, reporter_name, reporter_contact, color, secret_details]):
                st.error("❌ Please fill all required fields including secret details")
            else:
                name_valid, name_error = validate_name(reporter_name)
                if not name_valid:
                    st.error(f"❌ {name_error}")
                    return
                
                # Handle image upload
                image_path = None
                if image_file:
                    image_dir = "uploaded_images"
                    os.makedirs(image_dir, exist_ok=True)
                    image_path = os.path.join(image_dir, f"found_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_file.name}")
                    with open(image_path, "wb") as f:
                        f.write(image_file.getbuffer())
                
                item = add_found_item(
                    item_name=category,
                    category=category,
                    location=location,
                    description=description or f"{category} found at {location}",
                    reporter_name=reporter_name,
                    reporter_contact=reporter_contact,
                    image_path=image_path,
                    secret_details=secret_details,
                    color=color,
                    brand=brand
                )
                
                update_user_activity(st.session_state.user['id'], 'item_reported')
                st.success("✅ Found item reported successfully!")
                st.balloons()

def render_lost_items_tab():
    """Display only OPEN LOST items (not claimed)"""
    st.markdown("### 🔍 Lost Items (Open)")
    st.info("These items are still being searched for. If you found any, contact the owner!")
    
    filter_category = st.selectbox("Filter by Category", ["All"] + CATEGORIES, key="filter_cat_lost")
    
    items = get_lost_items()
    # Only show OPEN items (not claimed)
    items = [item for item in items if item['status'] == 'open']
    
    if filter_category != "All":
        items = [item for item in items if item['category'] == filter_category]
    
    if not items:
        st.info("No open lost items found.")
    else:
        st.success(f"Showing {len(items)} lost item(s)")
        items_sorted = sorted(items, key=lambda x: x['date'], reverse=True)
        for item in items_sorted:
            render_item_card(item, context='lost')

def render_found_items_tab():
    """Display only OPEN FOUND items (not claimed)"""
    st.markdown("### 📦 Found Items (Open)")
    st.info("These items were found and waiting for owners to claim them!")
    
    filter_category = st.selectbox("Filter by Category", ["All"] + CATEGORIES, key="filter_cat_found")
    
    items = get_found_items()
    # Only show OPEN items (not claimed)
    items = [item for item in items if item['status'] == 'open']
    
    if filter_category != "All":
        items = [item for item in items if item['category'] == filter_category]
    
    if not items:
        st.info("No open found items. All items have been claimed!")
    else:
        st.success(f"Showing {len(items)} found item(s) waiting for owners")
        items_sorted = sorted(items, key=lambda x: x['date'], reverse=True)
        for item in items_sorted:
            render_item_card(item, context='found')

def render_claimed_items():
    """Display only CLAIMED items - show only FOUND items to avoid duplicates"""
    st.markdown("### ✅ Claimed Items (Resolved)")
    
    items = get_all_items()
    # Only show FOUND items that are claimed (to avoid showing both Lost+Found duplicates)
    claimed_items = [item for item in items if item['status'] == 'claimed' and item['type'] == 'found']
    
    if not claimed_items:
        st.info("No claimed items yet.")
    else:
        st.success(f"Showing {len(claimed_items)} resolved item(s)")
        for item in claimed_items:
            render_claimed_card(item)

def render_claimed_card(item):
    """Simple card for claimed items"""
    st.markdown(f"""
        <div style='border-left: 5px solid #28a745; padding: 1rem; 
                    background: #d4edda; border-radius: 10px; margin-bottom: 1rem;'>
            <h4 style='margin: 0; color: #155724;'>✅ {item['category']} - CLAIMED</h4>
            <p style='margin: 0.5rem 0; color: #155724;'>
                📍 {item['location']} | 📅 {item['date']}
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_item_card(item, context='default'):
    """Render item card with claim functionality"""
    user = st.session_state.user
    
    # Determine styling
    if item['type'] == 'lost':
        border_color = '#f44336'
        status_badge = '🔍 LOST'
    else:
        border_color = '#2196f3'
        status_badge = '📦 FOUND'
    
    days_ago = get_date_difference(item['date'])
    
    # Show image if available
    if item.get('image_path') and os.path.exists(item['image_path']):
        col_img, col_details = st.columns([1, 3])
        with col_img:
            st.image(item['image_path'], use_container_width=True)
        with col_details:
            render_card_content(item, border_color, status_badge, days_ago)
    else:
        render_card_content(item, border_color, status_badge, days_ago)
    
    # Actions based on item type
    if item['type'] == 'found':
        # FOUND item - show claim button or finder controls
        if item['reporter_contact'].lower() == user['email'].lower():
            # User is the FINDER - show manual approve option
            st.info("📌 You found this item. Waiting for owner to claim.")
            render_finder_controls(item, context)
        else:
            # User is NOT the finder - can claim
            if st.button(f"🏆 Claim This Item", key=f"claim_{context}_{item['id']}"):
                st.session_state[f'claiming_{context}_{item["id"]}'] = True
            
            if st.session_state.get(f'claiming_{context}_{item["id"]}', False):
                render_claim_form(item, context, user)
    
    elif item['type'] == 'lost':
        # LOST item
        if item['reporter_contact'].lower() == user['email'].lower():
            st.info("📌 This is your lost item report. Wait for someone to find it.")
        else:
            st.success(f"📞 Found this item? Contact: **{item['reporter_name']}** at **{item['reporter_contact']}**")

def render_card_content(item, border_color, status_badge, days_ago):
    """Render the card content"""
    st.markdown(f"""
        <div style='border-left: 5px solid {border_color}; padding: 1rem; 
                    background: #f8f9fa; border-radius: 10px; margin-bottom: 0.5rem;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <h4 style='margin: 0; color: #333;'>{item['category']}</h4>
                <span style='background: {border_color}; color: white; padding: 3px 10px; 
                            border-radius: 15px; font-size: 0.8rem;'>{status_badge}</span>
            </div>
            <p style='margin: 0.5rem 0; color: #666;'>
                📍 <strong>Location:</strong> {item['location']} | 📅 {days_ago} days ago
            </p>
            <p style='margin: 0.5rem 0; color: #444;'>{item['description']}</p>
            <p style='margin: 0.5rem 0; color: #888; font-size: 0.9rem;'>
                👤 <strong>Reported by:</strong> {item['reporter_name']} | 📧 {item['reporter_contact']}
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_finder_controls(item, context):
    """Controls for the finder to manually approve claims"""
    st.markdown("---")
    st.markdown("**🔧 Finder Controls:**")
    
    with st.expander("📋 Manually Approve Claim (if auto-verification failed)"):
        st.warning("⚠️ Use this only if the owner contacted you and verified ownership but auto-claim failed (spelling mistakes, etc.)")
        
        with st.form(f"manual_approve_{context}_{item['id']}"):
            claimer_name = st.text_input("Owner's Name *", placeholder="Name of the person claiming")
            claimer_contact = st.text_input("Owner's Contact *", placeholder="Their email or phone")
            reason = st.text_area("Verification Notes", placeholder="How did you verify ownership?")
            
            approve = st.form_submit_button("✅ Approve & Mark as Claimed", type="primary")
            
            if approve:
                if not claimer_name or not claimer_contact:
                    st.error("Please fill owner's name and contact")
                else:
                    success = claim_item(
                        item_id=item['id'],
                        claimer_name=claimer_name,
                        verification_detail=f"Manual approval by finder. Notes: {reason}",
                        claimer_email=claimer_contact,
                        claimer_contact=claimer_contact
                    )
                    if success:
                        st.success("✅ Item marked as claimed!")
                        st.balloons()
                        import time
                        time.sleep(2)
                        st.rerun()

def render_claim_form(item, context, user):
    """Render the claim verification form"""
    
    st.markdown("""
        <div style='background: #fff3cd; padding: 1rem; border-radius: 10px; margin: 1rem 0;
                    border-left: 4px solid #ffc107;'>
            <h4 style='margin: 0; color: #856404;'>🔐 Verify Your Ownership</h4>
            <p style='margin: 0.5rem 0 0 0; color: #856404;'>
                Describe your item in detail to prove ownership.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form(f"claim_form_{context}_{item['id']}"):
        st.markdown(f"**Claiming as:** {user['name']} ({user['email']})")
        
        col1, col2 = st.columns(2)
        with col1:
            claim_color = st.text_input("What color is your item? *", placeholder="e.g., Blue, Black")
        with col2:
            claim_brand = st.text_input("Brand/Model?", placeholder="e.g., Samsung, Nike")
        
        claim_details = st.text_area(
            "Describe unique features *",
            placeholder="Scratches, stickers, what's inside...",
            height=100
        )
        
        contact = st.text_input("Your Contact Number *", placeholder="Phone number")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("✅ Submit Claim", type="primary", use_container_width=True)
        with col2:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if cancel:
            st.session_state[f'claiming_{context}_{item["id"]}'] = False
            st.rerun()
        
        if submitted:
            if not claim_color or not claim_details or not contact:
                st.error("❌ Please fill all required fields!")
                return
            
            # Compare with finder's secret details
            item_color = (item.get('color') or '').lower().strip()
            claim_color_lower = claim_color.lower().strip()
            
            # Check color match
            color_match = False
            if item_color and claim_color_lower:
                if item_color in claim_color_lower or claim_color_lower in item_color:
                    color_match = True
                item_words = set(item_color.split())
                claim_words = set(claim_color_lower.split())
                if item_words & claim_words:
                    color_match = True
            
            if not color_match and item_color:
                st.error("❌ Color doesn't match! Please verify you have the right item.")
                st.warning(f"💡 If you're sure this is your item, contact the finder directly: **{item['reporter_name']}** at **{item['reporter_contact']}**")
                st.info("The finder can manually approve your claim if you verify ownership to them.")
                return
            
            # Mark as claimed
            success = claim_item(
                item_id=item['id'],
                claimer_name=user['name'],
                verification_detail=f"Color: {claim_color}, Brand: {claim_brand}, Details: {claim_details}",
                claimer_email=user['email'],
                claimer_contact=contact
            )
            
            if success:
                # Show popup
                st.session_state['show_claim_popup'] = True
                st.session_state['claim_popup_data'] = {
                    'finder_name': item['reporter_name'],
                    'finder_contact': item['reporter_contact'],
                    'category': item['category']
                }
                update_user_activity(user['id'], 'claim_item')
                st.session_state[f'claiming_{context}_{item["id"]}'] = False
                st.rerun()
            else:
                st.error("❌ Failed to submit claim. Please try again.")
