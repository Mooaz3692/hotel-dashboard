import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hotel System", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.main {background-color: #eef2f7;}

.card {
    background: white;
    padding: 18px;
    border-radius: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}

.sidebar .sidebar-content {
    background-color: #1e293b;
}

.login-card {
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>🔐 Hotel System Login</h3>", unsafe_allow_html=True)

        user = st.text_input("Username", placeholder="Enter username")
        pwd = st.text_input("Password", type="password", placeholder="Enter password")

        if st.button("Login", use_container_width=True):
            if user == "admin" and pwd == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Wrong username or password")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# ---------------- LOAD DATA ----------------
if "data" not in st.session_state:
    df = pd.read_excel("data.xlsx")
    df.columns = df.columns.str.strip()
    st.session_state.data = df

df = st.session_state.data

# ---------------- SIDEBAR ----------------
st.sidebar.title("🏨 Hotel System")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Guests", "Reports"]
)

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ================= DASHBOARD =================
if page == "Dashboard":

    st.title("📊 Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.markdown(f"<div class='card'><h4>Bookings</h4><h2>{len(df)}</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><h4>Revenue</h4><h2>{int(df['RoomCharge'].sum())}</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><h4>Guests</h4><h2>{df['Guest Name'].nunique() if 'Guest Name' in df.columns else 0}</h2></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Bookings by Nationality")
        st.bar_chart(df["Nationality"].value_counts())

    with col2:
        st.subheader("Revenue by Room Type")
        st.bar_chart(df.groupby("Room Type")["RoomCharge"].sum())

# ================= GUESTS =================
elif page == "Guests":

    st.title("👤 Guest Management")

    # ADD
    with st.expander("➕ Add Guest"):
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
                st.success("Saved successfully")

    # TABLE
    st.dataframe(df, use_container_width=True)

    # SELECT
    selected = st.selectbox("Select record", df.index)

    # EDIT
    with st.expander("✏️ Edit Guest"):
        row = df.loc[selected]

        with st.form("edit"):
            name = st.text_input("Guest Name", row.get("Guest Name", ""))
            nat = st.text_input("Nationality", row.get("Nationality", ""))
            room = st.text_input("Room Type", row.get("Room Type", ""))
            price = st.number_input("Room Charge", value=int(row.get("RoomCharge", 0)))

            if st.form_submit_button("Update"):
                st.session_state.data.loc[selected, "Guest Name"] = name
                st.session_state.data.loc[selected, "Nationality"] = nat
                st.session_state.data.loc[selected, "Room Type"] = room
                st.session_state.data.loc[selected, "RoomCharge"] = price
                st.success("Updated successfully")

    # DELETE
    if st.button("🗑 Delete Record"):
        st.session_state.data = df.drop(index=selected).reset_index(drop=True)
        st.success("Deleted")

# ================= REPORTS =================
elif page == "Reports":

    st.title("📄 Reports")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button("⬇️ Export Data", csv, "hotel_data.csv")

    st.subheader("Summary")
    st.write(df.describe())
