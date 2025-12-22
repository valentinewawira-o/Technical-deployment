from distributed import span
import streamlit as st
from datetime import date
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import base64
from pathlib import Path
import re
#page config

st.set_page_config(
    page_title="TECHNICAL ACCESSORIES SOLD ENTRY ",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🔧"
)

#backgound image






# )
st.markdown(
    """
    <style>
    /* Make all form labels inside dark panel bold and yellow */
    .panel-dark .stLabel > label {
        font-weight: bold;
        color: #FFD700;
        font-size: 16px;
    }

    <style>
    /* Fully opaque success alert */
    .stAlert.stAlertSuccess, 
    .stAlert.stAlertSuccess div[role="alert"] {
        background-color: #28a745 !important;  /* bright green */
        color: #ffffff !important;             /* white text */
        font-weight: bold !important;
        opacity: 1 !important;                 /* force full opacity */
        border-left: 6px solid #065f46 !important;
        padding: 12px 16px !important;
    }

    /* Fully opaque warning alert */
    .stAlert.stAlertWarning,
    .stAlert.stAlertWarning div[role="alert"] {
        background-color: #FF4500 !important;  /* bright orange */
        color: #ffffff !important;             /* white text */
        font-weight: bold !important;
        opacity: 1 !important;                 /* force full opacity */
        border-left: 6px solid #9c2a00 !important;
        padding: 12px 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#layout
col1, mid, col2 = st.columns([3, 0.1, 2])
#col 1 background panel-dark
st.markdown("""
    <style>
    .section-header{
        background-color: #0f172a;
        color: white;
        padding: 2px;
        border-radius: 16px;
        box-shadow: 0 10px 6px rgba(0, 0, 0, 0.1);
        height: 80%;
    }
    .section-header h2{
        margin-bottom: 4px;
        padding-left: 10px;
    }
    .section-header p{
        margin-top: -10px;
        margin-bottom: 20px;
        color: #FFFF00;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with col1:
   def add_bg_from_local(image_path: str):
    image_file=Path(image_path)
    if not image_file.exists():
        st.warning(f"Image file not found: {image_path}")
        return
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/jpg;base64,{encoded_string});
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        z-index: 0;


    }}
    </style>
    """,
        unsafe_allow_html=True
    )
    add_bg_from_local("repair img.jpg")
   st.markdown("""<div class="section-header"><h2>🛠️ Accessories Sold Entry</h2><p>Enter accessories sold during repair</p></div>""", unsafe_allow_html=True) 
   st.markdown("""<div class="panel-dark"></div>""", unsafe_allow_html=True)
   st.markdown('<span style="font-weight:bold; color:#FFD700; background-color:#1f2933; padding:2px 6px; border-radius:4px;">Select Repair Date</span>', unsafe_allow_html=True)
   repair_date = st.date_input("", date.today())
   st.markdown('<span style="font-weight:bold; color:#FFD700; background-color:#1f2933; padding:2px 6px; border-radius:4px;">Select Technician</span>', unsafe_allow_html=True)
   technician = st.selectbox("", ["Eric", "Other"])
   if technician == "Other":
        st.markdown('<span style="color:#FFD700; background-color:#1f2933; padding:2px 2px; border-radius:4px;">Technician Name</span>', unsafe_allow_html=True)
        technician = st.text_input("")
   st.markdown('<span style="font-weight:bold; color:#FFD700; background-color:#1f2933; padding:2px 6px; border-radius:4px;">Accessories Sold</span>', unsafe_allow_html=True)
   accessories = st.multiselect("",["Helmet", "Reflector", "Raincoat", "Bag", "Charger 2.0", "Charger Jasiri", "Lock"])
   prices = {
       "Helmet": 1350,
       "Reflector": 450,
       "Raincoat": 2000,
       "Bag": 4000,
       "Charger 2.0": 4550,
       "Lock": 850,
       "Charger Jasiri": 10000
       }
   st.markdown('<span style="font-weight:bold; color:#FFD700; background-color:#1f2933; padding:2px 6px; border-radius:4px;">payment_mode</span>', unsafe_allow_html=True)
   payment_mode = st.selectbox("", ["Mpesa", "Invoicing"])
       # Payment code example
   pattern = re.compile(r"\b[A-Z0-9]{7,12}\b")
   if payment_mode == "Mpesa":
    payment_code = st.text_input("Payment Code")
    if payment_code and pattern.search(payment_code):
       st.success("Payment verified")
    else:
        st.warning("Invalid payment code")
   else:
    client_type = st.selectbox("Client Type", ["Rider", "Client", "Financier"])
    client_name = st.text_input("Client Name")

   total_price = sum(prices[a] for a in accessories)
   st.markdown(
    f'<span style="font-weight:bold; color:#FFD700; background-color:#1f2933; padding:2px 6px; border-radius:4px;">total cost</span>: Ksh {total_price}',
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)
with mid:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --------------------------------------------------
# RIGHT PANEL (SUMMARY)
# --------------------------------------------------
with col2:
    st.markdown('<div class="panel-green">', unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center;'>🧾 Summary</h2>", unsafe_allow_html=True)

    st.write(f"**Repair Date:** {repair_date}")
    st.write(f"**Technician:** {technician}")
    st.write(f"**Accessories:** {', '.join(accessories) if accessories else 'None'}")
    st.write(f"**Total Price:** Ksh {total_price}")
    st.write(f"**Payment Mode:** {payment_mode}")

    if payment_mode == "Mpesa":
        st.write(f"**Payment Code:** {payment_code}")
        st.write("**Status:** Valid" if pattern.search(payment_code or "") else "**Status:** Invalid")

    if payment_mode == "Invoicing":
        st.write(f"**Client:** {client_type}")
        st.write(f"**Name:** {client_name}")

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# SUBMIT
# --------------------------------------------------
if st.button("Submit Accessories Sold"):
    if accessories and (
        payment_mode == "Invoicing"
        or (payment_mode == "Mpesa" and pattern.search(payment_code or ""))
    ):
        st.success("Accessories submitted successfully")
    else:
        st.error("Please check accessories and payment details")



