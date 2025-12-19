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

# ----------------------------
# Utility: Add image to col1 only
# ----------------------------
def add_bg_to_col1(image_path: str):
    image_file = Path(image_path)
    if not image_file.exists():
        st.warning(f"Image file not found: {image_path}")
        return
    with open(image_path, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .col1-bg {{
            background-image: url(data:image/jpg;base64,{encoded_string});
            background-size: cover;
            background-position:top center;
            border-radius: 400px;
            min-height: 30vh;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ----------------------------
# Layout: Three columns
# ----------------------------
col1, mid, col2 = st.columns([3, 0.1, 2])

# ----------------------------
# Left Column (col1) – Background + Form
# ----------------------------
with col1:
    add_bg_to_col1("repair img.jpg")
    st.markdown('<div class="col1-bg" style="padding:20px;">', unsafe_allow_html=True)

    # Header
    st.markdown("""
        <h2 style='color:white; margin-bottom:5px;'>🛠️ Accessories Sold Entry</h2>
        <p style='color:#FFD700; margin-top:0;'>Enter accessories sold during repair</p>
    """, unsafe_allow_html=True)

    # Form inputs
    st.markdown('<span style="font-weight:bold; color:#FFD700;">Select Repair Date</span>', unsafe_allow_html=True)
    repair_date = st.date_input("", date.today())

    st.markdown('<span style="font-weight:bold; color:#FFD700;">Select Technician</span>', unsafe_allow_html=True)
    technician = st.selectbox("", ["Eric", "Other"])
    if technician == "Other":
        technician = st.text_input("Technician Name")

    st.markdown('<span style="font-weight:bold; color:#FFD700;">Accessories Sold</span>', unsafe_allow_html=True)
    accessories = st.multiselect("", ["Helmet", "Reflector", "Raincoat", "Bag", "Charger 2.0", "Charger Jasiri", "Lock"])
    prices = {
        "Helmet": 1350,
        "Reflector": 450,
        "Raincoat": 2000,
        "Bag": 4000,
        "Charger 2.0": 4550,
        "Charger Jasiri": 10000
    }

    st.markdown('<span style="font-weight:bold; color:#FFD700;">Payment Mode</span>', unsafe_allow_html=True)
    payment_mode = st.selectbox("", ["Mpesa", "Invoicing/deductions"])
    pattern = re.compile(r"\b[A-Z0-9]{7,12}\b")
    payment_code = ""
    client_name = client_type = ""
    if payment_mode == "Mpesa":
        payment_code = st.text_input("Payment Code")
        if payment_code and pattern.search(payment_code):
            st.success("Payment verified")
        else:
            st.warning("Invalid payment code")
    else:
        client_type = st.selectbox("Client Type", ["Rider_bike deduction", "Client", "Financier"])
        client_name = st.text_input("Name")

    total_price = sum(prices[a] for a in accessories)
    st.markdown(f'<span style="font-weight:bold; color:#FFD700;">Total Cost:</span> Ksh {total_price}', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# Right Column (col2) – Summary
# ----------------------------
with col2:
    st.markdown("""
        <div style='background-color:#0f172a; padding:20px; border-radius:16px;'>
        <h2 style='color:#FFD700; text-align:center;'>🧾 Summary</h2>
    """, unsafe_allow_html=True)

    st.write(f"**Repair Date:** {repair_date}")
    st.write(f"**Technician:** {technician}")
    st.write(f"**Accessories:** {', '.join(accessories) if accessories else 'None'}")
    st.write(f"**Total Price:** Ksh {total_price}")
    st.write(f"**Payment Mode:** {payment_mode}")

    if payment_mode == "Mpesa":
        st.write(f"**Payment Code:** {payment_code}")
        st.write("**Status:** Valid" if pattern.search(payment_code or "") else "**Status:** Invalid")
    else:
        st.write(f"**Client Type:** {client_type}")
        st.write(f"**Client Name:** {client_name}")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
#.env
load_dotenv()

DB_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('PG_USER')}:"
    f"{os.getenv('PG_PASSWORD')}@"
    f"{os.getenv('PG_HOST')}:"
    f"{os.getenv('PG_PORT')}/"
    f"{os.getenv('PG_DATABASE')}"
)

engine = create_engine(DB_URL)
def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS accessories_sold (
        submission_id UUID,
        repair_date DATE,
        technician TEXT,
        accessory TEXT,
        price NUMERIC,
        payment_mode TEXT,
        payment_code TEXT,
        client_type TEXT,
        client_name TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    with engine.begin() as conn:
        conn.execute(text(query))
create_table()

def payment_code_exists(payment_code: str) -> bool:
    query = """
    SELECT 1
    FROM accessories_sold
    WHERE payment_code = :payment_code
    LIMIT 1
    """
    with engine.begin() as conn:
        result = conn.execute(
            text(query),
            {"payment_code": payment_code}
        ).fetchone()
    return result is not None

def save_rows_to_db(rows: list[dict]):
    df = pd.DataFrame(rows)
    df.to_sql(
        "accessories_sold",
        engine,
        if_exists="append",
        index=False
    )

if st.button("Submit Accessories Sold"):

    if not accessories:
        st.error("Please select at least one accessory.")

    elif payment_mode == "Mpesa" and not pattern.search(payment_code or ""):
        st.error("Invalid or missing Mpesa payment code.")

    elif payment_mode == "Mpesa" and payment_code_exists(payment_code):
        st.error("This payment code has already been used.")

    elif payment_mode == "Invoicing" and (not client_type or not client_name):
        st.error("Please provide both Client Type and Client Name.")

    else:
        submission_id = str(uuid.uuid4())
        rows = []

        for accessory in accessories:
            rows.append({
                "submission_id": submission_id,
                "repair_date": repair_date,
                "technician": technician,
                "accessory": accessory,
                "price": prices[accessory],
                "payment_mode": payment_mode,
                "payment_code": payment_code if payment_mode == "Mpesa" else None,
                "client_type": client_type if payment_mode == "Invoicing" else None,
                "client_name": client_name if payment_mode == "Invoicing" else None,
            })

        save_rows_to_db(rows)
        st.success("Accessories saved successfully ✅")

# #
# def safe_read_csv(path, columns):
#     if not os.path.exists(path) or os.stat(path).st_size == 0:
#         return pd.DataFrame(columns=columns)
#     return pd.read_csv(path)

# CSV_FILE = "accessories_sold.csv"
# FINAL_COLUMNS = [
#     "submission_id",
#     "repair_date",
#     "technician",
#     "accessory",
#     "price",
#     "payment_mode", 
#     "payment_code",
#     "client_type",
#     "client_name",
# ]


# def payment_code_exists(payment_code: str) -> bool:
#     if not os.path.exists(CSV_FILE):
#         return False
#     df = pd.read_csv(CSV_FILE)
#     return payment_code in df["payment_code"].astype(str).values


# def save_rows_to_csv(rows: list[dict]):
#     df = pd.DataFrame(rows)
#     if os.path.exists(CSV_FILE):
#         df.to_csv(CSV_FILE, mode="a", header=False, index=False)
#     else:
#         df.to_csv(CSV_FILE, index=False)
# # Submit Button
# # ----------------------------
# if st.button("Submit Accessories Sold"):

#     # ----------- VALIDATION -----------
#     if not accessories:
#         st.error("Please select at least one accessory.")

#     elif payment_mode == "Mpesa" and not pattern.search(payment_code or ""):
#         st.error("Invalid or missing Mpesa payment code.")

#     elif payment_mode == "Mpesa" and payment_code_exists(payment_code):
#         st.error("This payment code has already been used.")

#     elif payment_mode == "Invoicing" and (not client_type or not client_name):
#         st.error("Please provide both Client Type and Client Name for invoicing.")

#     else:
#         submission_id = str(uuid.uuid4())
#         rows = []

#         for accessory in accessories:
#             rows.append ({
#                 "submission_id": submission_id,
#                 "repair_date": repair_date,
#                 "technician": technician,
#                 "accessory": accessory,
#                 "price": prices[accessory],
#                 "payment_mode": payment_mode,
#                 "payment_code": payment_code if payment_mode == "Mpesa" else "",
#                 "client_type": client_type if payment_mode == "Invoicing" else "",
#                 "client_name": client_name if payment_mode == "Invoicing" else "",
#             })
#         save_rows_to_csv(rows)
#         st.success("Accessories saved successfully")