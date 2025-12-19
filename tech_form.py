import pip
import streamlit as st
from datetime import date
import base64
from pathlib import Path
import re
import pandas as pd
import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="TECHNICAL ACCESSORIES SOLD ENTRY",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🔧"
)

#add background image to cover full page
def add_bg_from_local(image_path: str):
    image_file = Path(image_path)
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
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
add_bg_from_local("repair img.jpg")
#add intro text
st.markdown("""
    <div style='background-color:#0f172a; padding:100px; border-radius:150px;'>
    <h2 style='color:#FFD700; text-align:center;'>🛠️ Accessories Sold Entry</h2>
""", unsafe_allow_html=True)
#ysing a dark background write all the accessories and their prices
st.markdown("""
    <div style='background-color:#0f172a; padding:10px; border-radius:16px;'>
    <h3 style='color:#FFD700; text-align:left;'>Available Accessories and Prices:</h3>
    <ul style='color:white;'>
        <li>Helmet - kes 1,350</li>
        <li>Reflector - kes 450</li>
        <li>Raincoat - kes 2,000</li>
        <li>Bag - kes 4,000</li>
        <li>Charger 2.0 - kes 4,550</li>
        <li>Charger Jasiri - kes 10,000</li>
    </ul>
    </div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)  # Add space after intro section
# ----------------------------


