import streamlit as st
import pandas as pd

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

# ---------------- LOAD DATA ----------------
if "data" not in st.session_state:

    # 🔥 نقرأ الشيت الجديد
    df = pd.read_excel("data_new.xls")

    df.columns = df.columns.str.strip()

    # 🔥 Mapping للأسماء الجديدة
    df = df.rename(columns={
        "GuestNo": "Guest No",
        "GuestName": "Guest Name",
        "CheckInTime": "Check In",
        "CheckOutTime": "Check Out"
    })

    # 🔥 تحويل التواريخ
    df["In Date"] = pd.to_datetime(df["In Date"], errors="coerce", dayfirst=True)
    df["Out Date"] = pd.to_datetime(df["Out Date"], errors="coerce", dayfirst=True)

    # Payment fallback
    if "Payment Type" not in df.columns:
        df["Payment Type"] = "Cash"

    st.session_state.data = df

df = st.session_state.data

# ---------------- NAV ----------------
col1, col2 = st.columns([4,4])

with col1:
    st.image("logo.jpeg", width=180)
    st.markdown("### 🏨 Hotel System")

with col2:
    page = st.segmented_control(
        "",
        ["Dashboard", "Guests", "Rooms", "Payments", "Reports"],
        default="Dashboard"
    )

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

    occupied_rooms = df["Room No"].dropna().astype(str).unique()

    total_rooms = 21  # زي ما انت عامل قبل كده

    occupied = len(occupied_rooms)
    available = total_rooms - occupied

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Rooms", total_rooms)
    c2.metric("Occupied", occupied)
    c3.metric("Available", available)

# ================= PAYMENTS =================
elif page == "Payments":

    st.markdown("## 💳 Payments")

    payment_counts = df["Payment Type"].value_counts()

    st.bar_chart(payment_counts)
    st.write(payment_counts)

# ================= REPORTS =================
elif page == "Reports":

    st.markdown("## 📄 Reports")

    col1, col2 = st.columns(2)

    start_date = col1.date_input("From Date")
    end_date = col2.date_input("To Date")

    filtered_df = df.copy()

    if start_date and end_date:
        filtered_df = df[
            (df["In Date"].notna()) &
            (df["In Date"] >= pd.to_datetime(start_date)) &
            (df["In Date"] <= pd.to_datetime(end_date))
        ]

    st.subheader("Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇️ Download Filtered Data",
        csv,
        "filtered_data.csv"
    )
