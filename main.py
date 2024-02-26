import streamlit as st
import requests
import time
from datetime import datetime

CIL_LOGIN_URL = 'https://appadmin.cilantro.cafe/authpanel/login/checklogin'
CIL_PROMO_URL = 'https://appadmin.cilantro.cafe/authpanel/promocode/add'
CIL_EMAIL = "admin@cilantro.com"
CIL_PASSWORD = "admin@123"

HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4515.107 Safari/537.36"
}

# Define a function to add colored line under title
def title_with_line(title_text, line_color):
    st.markdown(f"<h1 style='color: black; border-bottom: 3px solid {line_color};'>{title_text}</h1>", unsafe_allow_html=True)


def create_promocode(promocode_names, minimum_order_amount, maximum_order_amount, maxusage, peruser_usage, start_datetime, end_datetime, amount, promocodetype, status, description):
    session = requests.session()

    # Fetch login page
    st.write("Fetching login page...")
    login_page = session.get(url=CIL_LOGIN_URL, headers=HEADER)
    st.write("Login page fetched successfully.")

    # Prepare payload for login
    payload = {
        "email": CIL_EMAIL,
        "password": CIL_PASSWORD,
        "timezone":"Africa/Cairo"
    }

    # Perform login
    st.write("Logging in...")
    login = session.post(url=CIL_LOGIN_URL, data=payload, headers=HEADER)
    st.write("Login successful.")

    # Check if login is successful
    if "Invalid email or password" in login.text:
        st.write("Error: Invalid email or password.")
        return

    # Fetch promo page
    st.write("Fetching promo page...")
    promo_page = session.get(url=CIL_PROMO_URL, headers=HEADER)
    st.write("Promo page fetched successfully.")

    for promocode_name in promocode_names:
        payload = {
            "title": f"Automated DC - {promocode_name}",
            "promocode": promocode_name,
            "vendor_id[]": [13, 12, 23, 24, 22, 20, 17],
            "subcategory_id[]": [9, 13, 32, 29, 7, 21, 25, 8, 18, 20, 4, 1, 3, 5, 6, 19, 30, 26, 22, 11, 10, 12, 2, 14, 23, 31],
            "minimum_order_amount": minimum_order_amount,
            "maximum_order_amount": maximum_order_amount,
            "maxusage": maxusage,
            "peruser_usage": peruser_usage,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime,
            "amount": amount,
            "promocodetype": promocodetype,
            "status": status,
            "description": description
        }
        # Post to the promo code creation endpoint
        create_promo = session.post(url=CIL_PROMO_URL, data=payload, headers=HEADER)

        # Check for errors in the response
        if create_promo.status_code != 200:
            st.write(f"Error creating promocode {promocode_name}: {create_promo.text}")
        else:
            st.write(f"Promocode {promocode_name} created successfully on backend.")
        time.sleep(2)

def main():
     # Set title with colored line
    title_with_line("Little Sara's promocode creator", "pink")
    st.write("Hey Little Sara, Please use this tool to create multiple promocodes with different names on the app...if you need support or have any issues reach out to Abdelgalil (01009727702) Best of luck:)")
    st.write("Enter the promo code names separated by commas:")

    promocode_names_input = st.text_input("Promo Code Names")

    minimum_order_amount = st.number_input("Minimum Order Amount", value=20)
    maximum_order_amount = st.number_input("Maximum Order Amount", value=0)
    maxusage = st.number_input("Max Usage", value=89)
    peruser_usage = st.number_input("Per User Usage", value=22)

    start_datetime = st.date_input("Start Date and Time", value=datetime.now())
    end_datetime = st.date_input("End Date and Time", value=(datetime.now()))

    amount = st.number_input("Amount", value=20)
    promocodetype = st.selectbox("Promocode Type", ["Percentage", "Fixed Amount"])
    status = st.selectbox("Status", ["Active", "Inactive"])
    description = st.text_area("Description", value="This is an automated promocode created by code made by AG")

    if st.button("Create Promo Codes"):
        promocode_names = [name.strip() for name in promocode_names_input.split(",")]
        create_promocode(promocode_names, minimum_order_amount, maximum_order_amount, maxusage, peruser_usage, start_datetime.strftime("%Y-%m-%dT%H:%M"), end_datetime.strftime("%Y-%m-%dT%H:%M"), amount, promocodetype, status, description)
        st.write("Promo codes creation process completed. Good luck :)")

if __name__ == "__main__":
    main()
