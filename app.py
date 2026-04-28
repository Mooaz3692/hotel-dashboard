import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hotel System", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main {background-color: #f8fafc;}
.card {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}
button {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
if "data" not in st.session_state:
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    st.session_state.data = df

df = st.session_state.data

st.title("🏨 Hotel Management System")

# ---------------- KPIs ----------------
col1, col2, col3 = st.columns(3)
col1.metric("Bookings", len(df))
col2.metric("Revenue", int(df["RoomCharge"].sum()))
col3.metric("Guests", df["Guest Name"].nunique() if "Guest Name" in df.columns else 0)

# ---------------- ADD FORM ----------------
st.subheader("➕ Add Guest")

with st.form("add_form"):
    name = st.text_input("Guest Name")
    nationality = st.text_input("Nationality")
    room = st.text_input("Room Type")
    price = st.number_input("Room Charge", 0)

    submitted = st.form_submit_button("Add")

    if submitted:
        new_row = {
            "Guest Name": name,
            "Nationality": nationality,
            "Room Type": room,
            "RoomCharge": price
        }
        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([new_row])],
            ignore_index=True
        )
        st.success("Guest added successfully!")

# ---------------- TABLE ----------------
st.subheader("📋 Data")

selected_row = st.selectbox(
    "Select Guest to Edit/Delete",
    df.index
)

st.dataframe(df, use_container_width=True)

# ---------------- ACTIONS ----------------
col1, col2, col3 = st.columns(3)

# DELETE
if col1.button("🗑 Delete"):
    st.session_state.data = df.drop(index=selected_row).reset_index(drop=True)
    st.success("Deleted!")

# EDIT
if col2.button("✏️ Edit (Demo)"):
    st.warning("Edit simulated فقط 👀")

# DOWNLOAD
csv = df.to_csv(index=False).encode('utf-8')
col3.download_button(
    "⬇️ Download Data",
    csv,
    "hotel_data.csv",
    "text/csv"
)
