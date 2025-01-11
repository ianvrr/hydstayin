import streamlit as st
import pandas as pd
import sqlite3
from data_utils import initialize_db, add_listing, get_listings
import os

# Page setup
st.set_page_config(page_title="Stay In Hyderabad", page_icon="🏠")

# Initialize the database
initialize_db()

# Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Helper function to get listing by ID
def get_listing_by_id(listing_id):
    conn = sqlite3.connect('listings.db')
    query = f"SELECT * FROM listings WHERE id = {listing_id}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Verify the image path
logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

# Check if the image file exists
if not os.path.isfile(logo_path):
    st.error("Logo image not found at: " + logo_path)

# Header with company logo and title side by side
header_html = f"""
<div style="display: flex; align-items: center; justify-content: center; gap: 20px;">
    <img src="assets/logo.png" alt="Company Logo" style="width: 150px; height: auto;">
    <h1 style='text-align: center;'>Stay In Hyderabad</h1>
</div>
"""

st.markdown(header_html, unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Finding your next PG/Hostel has never been this easy.</h2>", unsafe_allow_html=True)

# Navigation buttons
if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "show_details" not in st.session_state:
    st.session_state.show_details = False

if "current_listing_id" not in st.session_state:
    st.session_state.current_listing_id = None

col1, col2 = st.columns(2)

with col1:
    if st.button("Search Listings"):
        st.session_state.show_form = False
        st.session_state.show_details = False

with col2:
    if st.button("Post a Listing"):
        st.session_state.show_form = True
        st.session_state.show_details = False

# Ensure buttons are aligned properly
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            margin: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.show_form and not st.session_state.show_details:
    # Search Listings Section
    st.markdown("<h3 id='search' style='margin-top: 40px;'>Search Listings</h3>", unsafe_allow_html=True)

    search_query = st.text_input("Search for Location, Property Type, Amenities, etc.")
    filter_clicked = st.checkbox("Filter by Budget")

    if filter_clicked:
        budget_condition = st.selectbox("Condition", ["<", ">", "="])
        budget_amount = st.number_input("Amount (INR)", min_value=0)
        budget_range = (budget_condition, budget_amount)

    if st.button("Search"):
        if filter_clicked:
            condition, amount = budget_range
            if condition == "<":
                listings = get_listings(filter_budget=amount, filter_location=search_query)
                listings = listings[listings['budget'] < amount]
            elif condition == ">":
                listings = get_listings(filter_budget=None, filter_location=search_query)
                listings = listings[listings['budget'] > amount]
            elif condition == "=":
                listings = get_listings(filter_budget=amount, filter_location=search_query)
                listings = listings[listings['budget'] == amount]
        else:
            listings = get_listings(filter_budget=None, filter_location=search_query)

        if not isinstance(listings, pd.DataFrame) or listings.empty:
            st.write("No listings found.")
        else:
            for idx, listing in listings.iterrows():
                if st.button(f"View Details - {listing['name']}"):
                    st.session_state.current_listing_id = listing['id']
                    st.session_state.show_details = True

if st.session_state.show_details and st.session_state.current_listing_id is not None:
    # Display listing details
    listing_details = get_listing_by_id(st.session_state.current_listing_id)
    if not listing_details.empty:
        listing = listing_details.iloc[0]
        st.markdown(f"<h3>{listing['name']}</h3>", unsafe_allow_html=True)
        st.write(f"**Property Type:** {listing['property_type']}")
        st.write(f"**Size:** {listing['size']}")
        st.write(f"**Location:** {listing['location']}")
        st.write(f"**Locality:** {listing['locality']}")
        st.write(f"**Budget:** {listing['budget']}")
        st.write(f"**Amenities:** {listing['amenities']}")
        st.write(f"**Contact Number of Owner:** {listing['contact_owner']}")
        st.write(f"**Your Contact Number:** {listing['contact_user']}")

if st.session_state.show_form:
    # Post a Listing Section
    st.markdown("<h3 id='post' style='margin-top: 40px;'>Post a Listing</h3>", unsafe_allow_html=True)
    with st.form("listing_form"):
        property_name = st.text_input("Property Name *")
        your_name = st.text_input("Your Name *")
        is_owner = st.selectbox("Are you the owner? *", ["Yes", "No"])
        property_type = st.selectbox("Property Type *", ["HOSTEL", "INDEPENDENT HOME", "RESIDENTIAL APARTMENT"])
        size = st.selectbox("Size *", ["1BHK", "2BHK", "3BHK", "1RK", "Other"])
        location = st.text_input("Complete Address *")
        locality = st.text_input("Locality")
        budget = st.number_input("Expected Rent/Fee per Month *", min_value=0)
        amenities = st.multiselect("Amenities", ["WIFI", "TV", "FRIDGE", "AC", "WASHING MACHINE", "GYM"])
        contact_owner = st.text_input("Contact Number of Owner *")
        contact_user = st.text_input("Your Contact Number *")
        images = st.file_uploader("Upload Property Images", accept_multiple_files=True, type=['jpg', 'jpeg', 'png'])

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not property_name or not your_name or not is_owner or not property_type or not size or not location or not budget or not contact_owner or not contact_user:
                st.warning("Please fill out all required fields.")
            else:
                amenities_str = ", ".join(amenities)
                # Here, you'll need to handle image uploads, e.g., save them to a directory or database
                st.success("Listing added successfully!")

# Footer with © 2025 Stay In Hyderabad
footer_html = """
<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet">

<div class="footer">
    <div class="footer-left">
        <p>© 2025 Stay In Hyderabad</p>
    </div>
    <div class="footer-right">
        <div class="footer-social-icons">
            <a href="https://www.facebook.com" target="_blank" class="btn btn-outline-light btn-social mx-1"><i class="fab fa-facebook-f"></i></a>
            <a href="https://www.twitter.com" target="_blank" class="btn btn-outline-light btn-social mx-1"><i class="fab fa-twitter"></i></a>
            <a href="https://www.instagram.com" target="_blank" class="btn btn-outline-light btn-social mx-1"><i class="fab fa-instagram"></i></a>
        </div>
    </div>
</div>
"""

st.markdown(footer_html, unsafe_allow_html=True)
