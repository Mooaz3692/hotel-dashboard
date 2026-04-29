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

    # 🔥 بدل data.xlsx → data_new.xlsx
    df = pd.read_excel("data_new.xlsx")

    # تنظيف الأعمدة
    df.columns = df.columns.str.strip()

    # 🔥 أهم سطر في الحل كله
    df = df.loc[:, ~df.columns.duplicated()]

    # 🔥 mapping بسيط فقط
    df = df.rename(columns={
        "GuestNo": "Guest No",
        "GuestName": "Guest Name"
    })

    # التواريخ (زي ما هي)
    df["In Date"] = pd.to_datetime(df["In Date"], errors="coerce", dayfirst=True)
    df["Out Date"] = pd.to_datetime(df["Out Date"], errors="coerce", dayfirst=True)

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

    # 🔥 fix crash
    st.dataframe(st.session_state.data.reset_index(drop=True), use_container_width=True)

# ================= ROOMS =================
elif page == "Rooms":

    st.markdown("## 🏨 Rooms Status")

    df = st.session_state.data

    # 👇 سيب الجزء ده زي ما هو 100% (ما لمسناهوش)
    # ---------------- ALL ROOMS ----------------
    rooms = []

    deluxe_rooms = [
    "108","F1","F2","F3","112","114","115","117",
    "1001","1002","1003","1004","1005","1006","1007","1008",
    "1010","1011","1012","1013","1014","1015","1016","1017","1018",
    "1020","1021","1022","1023","1024","1025","1026","1027","1028",
    "1030","1032","1034",
    "2001","2002","2003","2004","2006","2007","2008","2009","2010",
    "2011","2012","2013","2015",
    "2021","2023","2025","2027","2029","2030","2032","2033","2034",
    "2035","2036","2038","2040",
    "3002","3004","3005","3006","3007","3008","3009","3010","3012",
    "3015","3016","3017","3018","3019","3020","3022","3024","3026",
    "3028","3030","3034","3036","3038","3040","3042","3044",
    "4001","4002","4003","4004","4006","4008","4012","4014","4016",
    "4018","4020","4022","4024","4026","4032","4034",
    "5004","5006","5012","5014"
]
    for r in deluxe_rooms:
        rooms.append((r, "DELUXE"))

    occupied_rooms = df["Room No"].dropna().astype(str).unique()

    room_data = []

    for room, rtype in rooms:
        status = "🔴 Occupied" if room in occupied_rooms else "🟢 Available"
        room_data.append({
            "Room No": room,
            "Type": rtype,
            "Status": status
        })

    rooms_df = pd.DataFrame(room_data)

    total = len(rooms_df)
    occupied = (rooms_df["Status"].str.contains("Occupied")).sum()
    available = (rooms_df["Status"].str.contains("Available")).sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Rooms", total)
    c2.metric("Occupied", occupied)
    c3.metric("Available", available)

    st.subheader("Rooms List")
    st.dataframe(rooms_df, use_container_width=True)

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

    # 🔥 fix crash
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "⬇️ Download Filtered Data",
        csv,
        "filtered_data.csv"
    )
