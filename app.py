import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hotel System", layout="wide")

# ---------------- THEME FIX ----------------
st.markdown("""
<style>

/* Background */
.main {
    background-color: #f6f8fb;
}

/* Dark mode fix */
@media (prefers-color-scheme: dark) {
    .main {
        background-color: #0e1117;
    }
}

/* Navbar */
.navbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:12px 20px;
    border-radius:10px;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    margin-bottom:20px;
}

@media (prefers-color-scheme: dark) {
    .navbar {
        background: rgba(20,25,35,0.7);
    }
}

/* Cards */
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

/* Buttons */
button {
    border-radius:8px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("""
        <div class='card'>
        <h3 style='text-align:center;'>🔐 Login</h3>
        """, unsafe_allow_html=True)

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
    st.session_state.data = df

df = st.session_state.data

# ---------------- NAVBAR ----------------
col1, col2, col3 = st.columns([4,3,1])

with col1:
    st.markdown("### 🏨 Hotel System")

with col2:
    page = st.segmented_control(
        "",
        ["Dashboard", "Guests", "Reports"]
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

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Bookings by Nationality")
        st.bar_chart(df["Nationality"].value_counts())

    with col2:
        st.subheader("Revenue by Room Type")
        st.bar_chart(df.groupby("Room Type")["RoomCharge"].sum())

# ================= GUESTS =================
elif page == "Guests":

    st.markdown("## Guests")

    with st.expander("Add Guest"):
        with st.form("add"):
            name = st.text_input("Guest Name")
            nat = st.text_input("Nationality")
            room = st.text_input("Room Type")
            price = st.number_input("Room Charge", 0)

            if st.form_submit_button("Save"):
                new = {
                    "Guest Name": name,
                    "Nationality": nat,
                    "Room Type": room,
                    "RoomCharge": price
                }
                st.session_state.data = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
                st.success("Saved")

    st.dataframe(df, use_container_width=True)

# ================= REPORTS =================
elif page == "Reports":

    st.markdown("## Reports")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data", csv, "hotel_data.csv")
