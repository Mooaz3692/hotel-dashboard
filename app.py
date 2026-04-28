import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Hotel System", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main {background-color: #f6f8fb;}
@media (prefers-color-scheme: dark) {
    .main {background-color: #0e1117;}
}
.card {
    padding:20px;
    border-radius:12px;
    background: rgba(255,255,255,0.9);
    box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
}
@media (prefers-color-scheme: dark) {
    .card {
        background: rgba(30,35,50,0.8);
        color:white;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='card'><h3 style='text-align:center;'>🔐 Login</h3>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if user == "admin" and pwd == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Wrong credentials")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------------- DATA ----------------
if "data" not in st.session_state:
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()

    if "Payment Type" not in df.columns:
        df["Payment Type"] = "Cash"

    st.session_state.data = df

df = st.session_state.data

# ---------------- NAV ----------------
col1, col2, col3 = st.columns([4,4,1])

with col1:
    st.markdown("### 🏨 Hotel System")

with col2:
    page = st.segmented_control(
        "",
        ["Dashboard", "Guests", "Rooms", "Payments", "Reports"],
        default="Dashboard"
    )

with col3:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ================= DASHBOARD =================
if page == "Dashboard":

    st.markdown("## Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.markdown(f"<div class='card'><h4>Bookings</h4><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><h4>Revenue</h4><h2>{int(df['RoomCharge'].sum())}</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><h4>Guests</h4><h2>{df['Guest Name'].nunique()}</h2></div>", unsafe_allow_html=True)

# ================= GUESTS =================
elif page == "Guests":

    st.markdown("## Guest Management")

    with st.expander("➕ Add Guest"):
        with st.form("add"):
            col1, col2, col3 = st.columns(3)

            guest_no = col1.text_input("Guest No")
            name = col2.text_input("Guest Name")
            nationality = col3.text_input("Nationality")

            room_no = col1.text_input("Room No")
            room_type = col2.text_input("Room Type")
            card_no = col3.text_input("Card No")

            city_ledger = col1.text_input("City Ledger")
            in_date = col2.date_input("In Date")
            out_date = col3.date_input("Out Date")

            invoice = col1.text_input("Invoice")
            invoice_no = col2.text_input("Invoice No")
            room_charge = col3.number_input("Room Charge", 0)

            guest_amount = col1.number_input("Guest Amount", 0)
            payment = col2.selectbox("Payment Type", ["Cash", "Visa"])

            if st.form_submit_button("Save"):
                new = {
                    "Guest No": guest_no,
                    "Guest Name": name,
                    "Nationality": nationality,
                    "Room No": room_no,
                    "Room Type": room_type,
                    "Card No": card_no,
                    "City Ledger": city_ledger,
                    "In Date": in_date,
                    "Out Date": out_date,
                    "Invoice": invoice,
                    "InvoiceNo.": invoice_no,
                    "RoomCharge": room_charge,
                    "GuestAmount": guest_amount,
                    "Payment Type": payment
                }

                st.session_state.data = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
                st.success("Guest Added")

    st.dataframe(st.session_state.data, use_container_width=True)

# ================= ROOMS =================
elif page == "Rooms":

    st.markdown("## 🏨 Rooms Status")

    df = st.session_state.data

    all_rooms = [str(i) for i in range(100, 121)]
    occupied_rooms = df["Room No"].dropna().astype(str).unique()

    room_data = []

    for room in all_rooms:
        if room in occupied_rooms:
            status = "🔴 Occupied"
        else:
            status = "🟢 Available"

        room_data.append({"Room No": room, "Status": status})

    rooms_df = pd.DataFrame(room_data)

    total = len(rooms_df)
    occupied = sum(rooms_df["Status"].str.contains("Occupied"))
    available = sum(rooms_df["Status"].str.contains("Available"))

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Rooms", total)
    c2.metric("Occupied", occupied)
    c3.metric("Available", available)

    st.subheader("Rooms List")
    st.dataframe(rooms_df, use_container_width=True)

# ================= PAYMENTS =================
elif page == "Payments":

    st.markdown("## 💳 Payments")

    df = st.session_state.data

    if "Payment Type" not in df.columns:
        df["Payment Type"] = "Cash"

    payment_counts = df["Payment Type"].value_counts()

    st.subheader("Payment Distribution")
    st.bar_chart(payment_counts)
    st.write(payment_counts)

# ================= REPORTS =================
elif page == "Reports":

    st.markdown("## 📄 Reports")

    df = st.session_state.data

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", int(df["RoomCharge"].sum()))
    c2.metric("Total Bookings", len(df))
    c3.metric("Avg Price", round(df["RoomCharge"].mean(), 2))

    st.subheader("Data Overview")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download Data", csv, "hotel_data.csv")
