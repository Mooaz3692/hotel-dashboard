import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Hotel Dashboard", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}
h1, h2, h3 {
    color: #1e293b;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_excel("data.xlsx")

# حل مشكلة المسافات في الأعمدة
df.columns = df.columns.str.strip()

# تحويل التواريخ
df["In Date"] = pd.to_datetime(df["In Date"], errors='coerce')
df["Out Date"] = pd.to_datetime(df["Out Date"], errors='coerce')

# ---------------- HEADER ----------------
st.title("🏨 Hotel Analytics Dashboard")

# ---------------- FILTERS ----------------
st.sidebar.header("🔎 Filters")

nationality = st.sidebar.multiselect(
    "Nationality",
    df["Nationality"].dropna().unique(),
    default=df["Nationality"].dropna().unique()
)

room_type = st.sidebar.multiselect(
    "Room Type",
    df["Room Type"].dropna().unique(),
    default=df["Room Type"].dropna().unique()
)

date_range = st.sidebar.date_input(
    "Check-in Date",
    [df["In Date"].min(), df["In Date"].max()]
)

# ---------------- FILTERING ----------------
filtered = df[
    (df["Nationality"].isin(nationality)) &
    (df["Room Type"].isin(room_type)) &
    (df["In Date"] >= pd.to_datetime(date_range[0])) &
    (df["In Date"] <= pd.to_datetime(date_range[1]))
]

# ---------------- KPIs ----------------
st.markdown("## 📊 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='card'><h3>Total Bookings</h3><h2>{len(filtered)}</h2></div>", unsafe_allow_html=True)

col2.markdown(f"<div class='card'><h3>Total Revenue</h3><h2>{int(filtered['RoomCharge'].sum())}</h2></div>", unsafe_allow_html=True)

col3.markdown(f"<div class='card'><h3>Average Price</h3><h2>{round(filtered['RoomCharge'].mean(),2)}</h2></div>", unsafe_allow_html=True)

# نحسب عدد العملاء لو العمود موجود
if "Guest Name" in filtered.columns:
    unique_guests = filtered["Guest Name"].nunique()
else:
    unique_guests = "N/A"

col4.markdown(f"<div class='card'><h3>Unique Guests</h3><h2>{unique_guests}</h2></div>", unsafe_allow_html=True)

# ---------------- CHARTS ----------------
st.markdown("## 📈 Insights")

c1, c2 = st.columns(2)

with c1:
    st.markdown("### Bookings by Nationality")
    st.bar_chart(filtered["Nationality"].value_counts())

with c2:
    st.markdown("### Revenue by Room Type")
    st.bar_chart(filtered.groupby("Room Type")["RoomCharge"].sum())

# ---------------- TABLE ----------------
st.markdown("## 📋 Booking Details")

st.dataframe(
    filtered.sort_values(by="In Date", ascending=False),
    use_container_width=True
)
