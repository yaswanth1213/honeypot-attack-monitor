
import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_attempts

st.set_page_config(
    page_title="Honeypot Attack Monitor",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Honeypot Attack Monitoring Dashboard")
st.caption("Cybersecurity Lab | SQLite Database")

if st.button("Refresh Dashboard"):
    st.rerun()

# Read the database
rows = get_attempts()

columns = [
    "ID", "Timestamp", "Client IP", "Username", "Event"
]

df = pd.DataFrame(rows, columns=columns)

if df.empty:
    st.info("No login attempts recorded yet.")
    st.stop()

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"], errors="coerce"
)
df["Username"] = df["Username"].fillna("Unknown")
df["Client IP"] = df["Client IP"].fillna("Unknown")

# Summary cards
c1, c2, c3 = st.columns(3)

c1.metric("Total Login Attempts", len(df))
c2.metric("Unique Client IPs", df["Client IP"].nunique())
c3.metric("Usernames Tested", df["Username"].nunique())

st.divider()

# Username statistics
left, right = st.columns(2)

with left:
    st.subheader("Most Tested Usernames")

    top_users = (
        df["Username"]
        .value_counts()
        .head(10)
        .rename_axis("Username")
        .reset_index(name="Attempts")
    )

    fig_users = px.bar(
        top_users,
        x="Username",
        y="Attempts",
        title="Login Attempts by Username"
    )

    st.plotly_chart(fig_users, use_container_width=True)

with right:
    st.subheader("Attempts Over Time")

    timed = df.dropna(subset=["Timestamp"]).copy()

    if not timed.empty:
        timeline = (
            timed.set_index("Timestamp")
            .resample("h")
            .size()
            .reset_index(name="Attempts")
        )

        fig_time = px.line(
            timeline,
            x="Timestamp",
            y="Attempts",
            markers=True,
            title="Attempts per Hour"
        )

        st.plotly_chart(fig_time, use_container_width=True)
    else:
        st.info("No valid timestamps available.")

# Recent records
st.subheader("Recent Login Attempts")

st.dataframe(
    df.sort_values(
        "Timestamp", ascending=False, na_position="last"
    ).head(20),
    use_container_width=True,
    hide_index=True
)

# Download the database records as CSV
st.download_button(
    "Download Login Records",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="honeypot_database_logs.csv",
    mime="text/csv"
)

st.caption(
    "Recorded attempts do not by themselves prove "
    "that an attack succeeded."
)
