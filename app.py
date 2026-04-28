import streamlit as st
import pandas as pd

# قراءة الداتا
df = pd.read_excel("data.xlsx")

st.title("🏨 Hotel Dashboard")

# تحويل التواريخ (مهم)
df["In Date"] = pd.to_datetime(df["In Date"])
df["Out Date"] = pd.to_datetime(df["Out Date"])

# ---------------- KPIs ----------------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("عدد الحجوزات", len(df))
col2.metric("إجمالي الإيراد", int(df["RoomCharge"].sum()))
col3.metric("متوسط السعر", round(df["RoomCharge"].mean(), 2))

# ---------------- Filters ----------------
st.sidebar.header("🔎 Filters")

nationality = st.sidebar.multiselect(
    "الجنسية",
    df["Nationality"].dropna().unique(),
    default=df["Nationality"].dropna().unique()
)

room_type = st.sidebar.multiselect(
    "نوع الغرفة",
    df["Room Type"].dropna().unique(),
    default=df["Room Type"].dropna().unique()
)

date_range = st.sidebar.date_input(
    "تاريخ الدخول",
    [df["In Date"].min(), df["In Date"].max()]
)

# ---------------- Filtering ----------------
filtered = df[
    (df["Nationality"].isin(nationality)) &
    (df["Room Type"].isin(room_type)) &
    (df["In Date"] >= pd.to_datetime(date_range[0])) &
    (df["In Date"] <= pd.to_datetime(date_range[1]))
]

# ---------------- Table ----------------
st.subheader("📋 البيانات")

st.dataframe(filtered, use_container_width=True)

# ---------------- Charts ----------------
st.subheader("📈 تحليلات")

st.write("الحجوزات حسب الجنسية")
st.bar_chart(filtered["Nationality"].value_counts())

st.write("الحجوزات حسب نوع الغرفة")
st.bar_chart(filtered["Room Type"].value_counts())

st.write("الإيراد حسب نوع الغرفة")
st.bar_chart(filtered.groupby("Room Type")["RoomCharge"].sum())