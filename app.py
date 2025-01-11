import streamlit as st
import pandas as pd
from data_utils import initialize_db, add_listing, get_listings

# Initialize the database
initialize_db()

# App title and description
st.title("🏠 Stay In Hyderabad")
st.caption("finding your next PG/Hostel has never been this easy.")

# Sidebar navigation
st.sidebar.title("🔍 Navigation")
menu = st.sidebar.radio("Go to:", ["Search Listings", "Post a Listing"])

if menu == "Search Listings":
    st.header("Search for Listings")
    with st.expander("🔽 Add Filters"):
        location = st.text_input("Preferred Location", placeholder="Eg: Madhapur")
        budget = st.number_input("Max Budget (₹)", min_value=0, step=100)
    
    if st.button("Search"):
        results = get_listings(filter_budget=budget if budget > 0 else None, filter_location=location)
        st.subheader("Available Listings")
        if results:
            for res in results:
                with st.container():
                    st.markdown(f"### 🏠 {res[1]}")
                    st.write(f"📍 **Location:** {res[2]}")
                    st.write(f"💰 **Budget:** ₹{res[3]}")
                    st.write(f"🔧 **Amenities:** {res[4]}")
                    st.write(f"📞 **Contact:** {res[5]}")
                    st.markdown("---")
        else:
            st.warning("No listings found matching your criteria!")

elif menu == "Post a Listing":
    st.header("Post a New Listing")
    with st.form("listing_form"):
        name = st.text_input("Your Name")
        location = st.text_input("Location")
        budget = st.number_input("Budget (₹)", min_value=0, step=100)
        amenities = st.text_area("Amenities (comma-separated)", placeholder="Eg: Wi-Fi, AC, Laundry")
        contact = st.text_input("Contact Number")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if name and location and budget and contact:
                add_listing(name, location, budget, amenities, contact)
                st.success(f"Listing added successfully! Thank you, {name}.")
            else:
                st.error("All fields are required except Amenities!")

# Footer
st.markdown("---")
st.caption(" ©️ Amigo's Hostel Network 2022-2025 | Made with ❤️ using Streamlit")
