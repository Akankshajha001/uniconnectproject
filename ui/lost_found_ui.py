"""
Lost & Found UI - Direct Contact + Manual Claim System
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
    claim_item
)
from database.users_db import update_user_activity
from utils.helpers import get_date_difference

# Categories and locations
CATEGORIES = ['ID Card', 'Bottle', 'Charger', 'Book', 'Umbrella', 'Keys', 
              'Phone', 'Wallet', 'Bag', 'Laptop', 'Headphones', 'Other']

LOCATIONS = ['Library', 'Cafeteria', 'Computer Lab', 'Main Building', 
             'Sports Complex', 'Auditorium', 'Parking Area', 'Garden', 
             'Hostel Area', 'Other']

def render_lost_found():
    """Main render function"""
    
    # Big Success Overlay Popup
    if st.session_state.get('show_claim_popup', False):
        popup_data = st.session_state.get('claim_popup_data', {})
        
        st.balloons()
        
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                        padding: 3rem; border-radius: 30px; color: white; text-align: center;
                        max-width: 600px; margin: 2rem auto;
                        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                        border: 5px solid white;'>
                
                <div style='font-size: 4rem; margin-bottom: 1rem;'>🎉</div>
                <h1 style='margin: 0; font-size: 2.5rem;'>ITEM CLAIMED!</h1>
                
                <p style='font-size: 1.3rem; margin: 1rem 0;'>
                    <b>{popup_data.get('category', 'Item')}</b> has been marked as claimed!
                </p>
                
                <div style='background: rgba(255,255,255,0.25); padding: 2rem; border-radius: 20px; 
                            margin: 2rem 0; border: 2px solid rgba(255,255,255,0.5);'>
                    <p style='margin: 0 0 0.5rem 0; font-size: 1rem; opacity: 0.9;'>OWNER DETAILS</p>
                    <div style='font-size: 3rem; margin: 0.5rem 0;'>👤</div>
                    <h2 style='margin: 0; font-size: 2rem;'>{popup_data.get('owner_name', '')}</h2>
                    <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-top: 1rem;'>
                        <p style='margin: 0; font-size: 1.3rem;'>📧 <b>{popup_data.get('owner_contact', '')}</b></p>
                    </div>
                </div>
                
                <p style='font-size: 1.1rem;'>Item has been resolved successfully!</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("✖  CLOSE & CONTINUE", key="close_popup", type="primary", use_container_width=True):
            st.session_state['show_claim_popup'] = False
            st.session_state['claim_popup_data'] = {}
            st.rerun()
        st.stop()
    
    # Check login
    if 'user' not in st.session_state or st.session_state.user is None:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; color: white;'>
                <h1>🔍 Lost & Found Center</h1>
            </div>
        """, unsafe_allow_html=True)
        st.error("🔒 Please login to access Lost & Found.")
        return
    
    # Header
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; color: white; margin-bottom: 1rem;'>
            <h1>🔍 Lost & Found Center</h1>
            <p style='opacity: 0.9;'>Report lost items, find your belongings, contact finders directly</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📢 Report Lost", "✅ Report Found", "🔍 Lost Items", "📦 Found Items", "✅ Claimed"
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
    """Report a lost item"""
    st.markdown("### 📢 Report a Lost Item")
    
    with st.form("report_lost_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Category *", options=CATEGORIES)
            location = st.selectbox("Last Seen Location *", options=LOCATIONS)
        
        with col2:
            user = st.session_state.user
            reporter_name = st.text_input("Your Name *", value=user.get('name', ''))
            reporter_contact = st.text_input("Contact (Email) *", value=user.get('email', ''))
        
        # ID Number for ID Card
        id_number = st.text_input(
            "ID Card Number (Required for ID Card)",
            placeholder="Enter your ID number",
            help="Required if you lost an ID Card"
        )
        
        description = st.text_area("Description *", placeholder="Describe your item - color, brand, any unique marks...", height=100)
        
        st.markdown("**📸 Photo (Optional)**")
        image_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'], key="lost_img")
        
        if st.form_submit_button("🚀 Submit Report", use_container_width=True):
            if not all([category, location, reporter_name, reporter_contact, description]):
                st.error("❌ Fill all required fields")
                return
            if category == "ID Card" and not id_number:
                st.error("❌ Enter ID Card number")
                return
            
            image_path = None
            if image_file:
                os.makedirs("uploaded_images", exist_ok=True)
                image_path = f"uploaded_images/lost_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_file.name}"
                with open(image_path, "wb") as f:
                    f.write(image_file.getbuffer())
            
            full_desc = f"[ID: {id_number}] {description}" if id_number else description
            add_lost_item(category, category, location, full_desc, reporter_name, reporter_contact, image_path)
            update_user_activity(st.session_state.user['id'], 'item_reported')
            st.success("✅ Reported successfully!")
            st.balloons()

def render_report_found():
    """Report a found item"""
    st.markdown("### ✅ Report a Found Item")
    
    with st.form("report_found_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Category *", options=CATEGORIES)
            location = st.selectbox("Found Location *", options=LOCATIONS)
        
        with col2:
            user = st.session_state.user
            reporter_name = st.text_input("Your Name *", value=user.get('name', ''))
            reporter_contact = st.text_input("Contact (Email) *", value=user.get('email', ''))
        
        phone = st.text_input("Phone Number *", placeholder="Your phone number for owner to contact you")
        
        description = st.text_area("Description *", placeholder="Describe the item - color, brand, condition...", height=100)
        
        st.markdown("**📸 Photo (Optional)**")
        image_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'], key="found_img")
        
        if st.form_submit_button("✅ Submit Report", use_container_width=True):
            if not all([category, location, reporter_name, reporter_contact, description, phone]):
                st.error("❌ Fill all required fields including phone number")
                return
            
            image_path = None
            if image_file:
                os.makedirs("uploaded_images", exist_ok=True)
                image_path = f"uploaded_images/found_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_file.name}"
                with open(image_path, "wb") as f:
                    f.write(image_file.getbuffer())
            
            # Store phone in verification_data
            import json
            verification_data = {'phone': phone}
            
            add_found_item(category, category, location, description,
                          reporter_name, reporter_contact, image_path, None, None, None,
                          verification_data)
            update_user_activity(st.session_state.user['id'], 'item_reported')
            st.success("✅ Reported successfully!")
            st.balloons()

def render_lost_items_tab():
    """Display open lost items"""
    st.markdown("### 🔍 Lost Items")
    
    filter_cat = st.selectbox("Filter", ["All"] + CATEGORIES, key="filter_lost")
    items = [i for i in get_lost_items() if i['status'] == 'open']
    
    if filter_cat != "All":
        items = [i for i in items if i['category'] == filter_cat]
    
    if not items:
        st.info("No open lost items.")
    else:
        for item in sorted(items, key=lambda x: x['date'], reverse=True):
            render_item_card(item, 'lost')

def render_found_items_tab():
    """Display open found items"""
    st.markdown("### 📦 Found Items")
    
    # Single notice at top
    st.markdown("""
        <div style='background: #e8f4fd; padding: 0.8rem 1rem; border-radius: 8px; 
                    margin-bottom: 1rem; border-left: 3px solid #2196f3; font-size: 0.9rem; color: #1565c0;'>
            🔒 To contact a finder, you must first report your lost item in the <b>"Report Lost"</b> tab (same category).
        </div>
    """, unsafe_allow_html=True)
    
    filter_cat = st.selectbox("Filter", ["All"] + CATEGORIES, key="filter_found")
    items = [i for i in get_found_items() if i['status'] == 'open']
    
    if filter_cat != "All":
        items = [i for i in items if i['category'] == filter_cat]
    
    if not items:
        st.info("No open found items.")
    else:
        for item in sorted(items, key=lambda x: x['date'], reverse=True):
            render_item_card(item, 'found')

def render_claimed_items():
    """Display claimed items"""
    st.markdown("### ✅ Claimed Items")
    
    items = [i for i in get_all_items() if i['status'] == 'claimed' and i['type'] == 'found']
    
    if not items:
        st.info("No claimed items yet.")
    else:
        for item in items:
            st.markdown(f"""
                <div style='border-left: 5px solid #28a745; padding: 1rem; 
                            background: #d4edda; border-radius: 10px; margin-bottom: 1rem;'>
                    <h4 style='margin: 0; color: #155724;'>✅ {item['category']} - CLAIMED</h4>
                    <p style='margin: 0.5rem 0; color: #155724;'>📍 {item['location']} | 📅 {item['date']}</p>
                </div>
            """, unsafe_allow_html=True)

def render_item_card(item, context):
    """Render item card"""
    user = st.session_state.user
    border = '#f44336' if item['type'] == 'lost' else '#2196f3'
    badge = '🔍 LOST' if item['type'] == 'lost' else '📦 FOUND'
    days = get_date_difference(item['date'])
    
    # Get phone from verification_data
    phone = ''
    if item.get('verification_data'):
        try:
            import json
            vdata = json.loads(item['verification_data'])
            phone = vdata.get('phone', '')
        except:
            pass
    
    # Image
    if item.get('image_path') and os.path.exists(item['image_path']):
        col_img, col_det = st.columns([1, 3])
        with col_img:
            st.image(item['image_path'], use_container_width=True)
        with col_det:
            _render_card_html(item, border, badge, days)
    else:
        _render_card_html(item, border, badge, days)
    
    # Actions based on item type
    if item['type'] == 'found':
        if item['reporter_contact'].lower() == user['email'].lower():
            # FINDER VIEW - show manual claim controls
            st.markdown("""
                <div style='background: #d4edda; padding: 1rem; border-radius: 10px; 
                            border-left: 4px solid #28a745; margin: 0.5rem 0;'>
                    <p style='margin: 0; color: #155724;'>
                        📌 <b>You found this item.</b> When the owner contacts you, verify and mark as claimed below.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Manual Claim form
            with st.expander("✅ Mark as Claimed (after owner contacts you)"):
                with st.form(f"manual_{context}_{item['id']}"):
                    st.markdown("**Enter owner details after you verified ownership:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Owner Name *", placeholder="Person who contacted you")
                    with col2:
                        contact = st.text_input("Owner Contact *", placeholder="Their phone or email")
                    
                    notes = st.text_input("How did you verify?", placeholder="e.g., Described item correctly, showed ID")
                    
                    if st.form_submit_button("✅ Approve & Mark as Claimed", type="primary", use_container_width=True):
                        if name and contact:
                            claim_item(item['id'], name, f"Verified by finder: {notes}", contact, contact)
                            st.session_state['show_claim_popup'] = True
                            st.session_state['claim_popup_data'] = {
                                'category': item['category'],
                                'owner_name': name,
                                'owner_contact': contact
                            }
                            st.rerun()
                        else:
                            st.error("Fill owner name and contact")
        else:
            # OWNER VIEW - must have a lost report in same category to contact finder
            user_lost_reports = [
                i for i in get_lost_items()
                if i['status'] == 'open'
                and i['reporter_contact'].lower() == user['email'].lower()
                and i['category'].lower() == item['category'].lower()
            ]
            
            if not user_lost_reports:
                st.markdown(f"""
                    <p style='margin: 0.3rem 0; color: #999; font-size: 0.85rem;'>
                        🔒 Report your lost <b>{item['category']}</b> first to unlock finder contact
                    </p>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"📞 Contact Finder", key=f"contact_{context}_{item['id']}"):
                    st.session_state[f'show_contact_{context}_{item["id"]}'] = True
                
                if st.session_state.get(f'show_contact_{context}_{item["id"]}', False):
                    matched_report = user_lost_reports[0]
                    st.success(f"✅ Verified — you reported a lost **{item['category']}** (Report #{matched_report['id']}, {matched_report['location']})")
                    
                    phone_line = f"📱 **{phone}**" if phone else ""
                    
                    contact_box = st.container(border=True)
                    with contact_box:
                        st.markdown("#### 📞 Finder Contact Details")
                        st.markdown("---")
                        col_a, col_b = st.columns([1, 3])
                        with col_a:
                            st.markdown("### 👤")
                        with col_b:
                            st.markdown(f"### {item['reporter_name']}")
                            st.markdown(f"📧 **{item['reporter_contact']}**")
                            if phone:
                                st.markdown(f"📱 **{phone}**")
                        st.markdown("---")
                        st.info("Contact them directly to verify your ownership and collect your item. Once verified, the finder will mark it as claimed.")
                    
                    if st.button("✖ Close", key=f"close_contact_{context}_{item['id']}"):
                        st.session_state[f'show_contact_{context}_{item["id"]}'] = False
                        st.rerun()
    
    elif item['type'] == 'lost':
        if item['reporter_contact'].lower() == user['email'].lower():
            st.info("📌 This is your lost item report.")
        else:
            st.success(f"📞 Found this? Contact: **{item['reporter_name']}** at **{item['reporter_contact']}**")

def _render_card_html(item, border, badge, days):
    st.markdown(f"""
        <div style='border-left: 5px solid {border}; padding: 1rem; 
                    background: #f8f9fa; border-radius: 10px; margin-bottom: 0.5rem;'>
            <div style='display: flex; justify-content: space-between;'>
                <h4 style='margin: 0;'>{item['category']}</h4>
                <span style='background: {border}; color: white; padding: 3px 10px; 
                            border-radius: 15px; font-size: 0.8rem;'>{badge}</span>
            </div>
            <p style='margin: 0.5rem 0; color: #666;'>📍 {item['location']} | 📅 {days} days ago</p>
            <p style='margin: 0.5rem 0;'>{item['description']}</p>
            <p style='margin: 0; color: #888; font-size: 0.9rem;'>👤 Reported by: {item['reporter_name']}</p>
        </div>
    """, unsafe_allow_html=True)
