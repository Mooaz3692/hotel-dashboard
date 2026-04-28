import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hotel System", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main {background-color: #f5f7fa;}
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD ----------------
if "data" not in st.session_state:
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    st.session_state.data = df

df = st.session_state.data

st.title("🏨 Hotel Management System")

# ---------------- KPIs ----------------
col1, col2, col3 = st.columns(3)

col1.markdown(f"<div class='card'><h4>Total Bookings</h4><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card'><h4>Total Revenue</h4><h2>{int(df['RoomCharge'].sum())}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card'><h4>Guests</h4><h2>{df['Guest Name'].nunique() if 'Guest Name' in df.columns else 0}</h2></div>", unsafe_allow_html=True)

# ---------------- CHARTS ----------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Bookings by Nationality")
    st.bar_chart(df["Nationality"].value_counts())

with c2:
    st.subheader("Revenue by Room Type")
    st.bar_chart(df.groupby("Room Type")["RoomCharge"].sum())

# ---------------- ADD ----------------
st.subheader("Add Guest")

with st.form("add"):
    col1, col2, col3 = st.columns(3)

    name = col1.text_input("Guest Name")
    nat = col2.text_input("Nationality")
    room = col3.text_input("Room Type")

    price = st.number_input("Room Charge", 0)

    submit = st.form_submit_button("Add Guest")

    if submit:
        new = {
            "Guest Name": name,
            "Nationality": nat,
            "Room Type": room,
            "RoomCharge": price
        }
        st.session_state.data = pd.concat([df, pd.DataFrame([new])], ignore_index=True)

# ---------------- TABLE ----------------
st.subheader("Bookings")

selected = st.selectbox("Select Record", df.index)

st.dataframe(df, use_container_width=True)

# ---------------- EDIT ----------------
st.subheader("Edit Record")

edit_row = df.loc[selected]

with st.form("edit"):
    col1, col2, col3 = st.columns(3)

    name = col1.text_input("Guest Name", edit_row.get("Guest Name", ""))
    nat = col2.text_input("Nationality", edit_row.get("Nationality", ""))
    room = col3.text_input("Room Type", edit_row.get("Room Type", ""))

    price = st.number_input("Room Charge", value=int(edit_row.get("RoomCharge", 0)))

    update = st.form_submit_button("Update")

    if update:
        st.session_state.data.loc[selected, "Guest Name"] = name
        st.session_state.data.loc[selected, "Nationality"] = nat
        st.session_state.data.loc[selected, "Room Type"] = room
        st.session_state.data.loc[selected, "RoomCharge"] = price

# ---------------- DELETE ----------------
if st.button("Delete Selected"):
    st.session_state.data = df.drop(index=selected).reset_index(drop=True)

# ---------------- DOWNLOAD ----------------
csv = df.to_csv(index=False).encode('utf-8')

st.download_button("Download Data", csv, "hotel_data.csv")
