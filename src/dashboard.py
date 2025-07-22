import streamlit as st
from streamlit_chat import message
from src.api import WaterIntakeAgent
from src.logger import log_message
from src.database import log_intake, get_intake_history
import pandas as pd
from datetime import datetime

# Get username
if "user_id" not in st.session_state:
    st.title("💧 Water Intake Tracker")
    username = st.text_input("Enter your username to continue:")
    if username:
        st.session_state.user_id = username
        st.rerun()
else:
    user_id = st.session_state.user_id

# Setup tracker state
if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

# Welcome section
if not st.session_state.tracker_started:
    st.title("💧 Water Intake Tracker")
    st.markdown("""
        Stay hydrated and healthy with your personal AI assistant!  
        Log your water intake, view history, and receive smart tips.
    """)

    if st.button("🚀 Start Tracking"):
        st.session_state.tracker_started = True
        st.rerun()

# Main Dashboard
if st.session_state.tracker_started:
    st.title(f"📊 Dashboard – {user_id}'s Hydration Tracker")

    tabs = st.tabs(["📥 Log Intake", "🤖 AI Assistant", "📈 History", "💡 Tips & Stats"])

    # Tab 1: Log Intake
    with tabs[0]:
        st.header("Log your water intake")
        quantity = st.slider("Select amount (ml)", min_value=50, max_value=1000, step=50)
        if st.button("💾 Log Intake"):
            log_intake(user_id, quantity)
            st.success(f"Logged {quantity}ml for {user_id}")

    # Tab 2: AI Assistant
    with tabs[1]:
        st.header("Chat with your Hydration Coach")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.text_input("Ask something...")
        if user_input:
            # Make sure WaterIntakeAgent has a .chat() method or replace it with .run()
            response = WaterIntakeAgent().run(user_input)
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", response))
            log_message(user_input, response)

        for i, (sender, msg) in enumerate(reversed(st.session_state.chat_history)):
            message(msg, is_user=(sender == "user"), key=f"msg_{i}")

    # Tab 3: Intake History
    with tabs[2]:
        st.header("Your Hydration History")
        raw_data = get_intake_history(user_id)
        if not raw_data:
            st.warning("No data logged yet.")
        else:
            df = pd.DataFrame(raw_data, columns=["amount", "date"])
            df["date"] = pd.to_datetime(df["date"]).dt.date
            st.dataframe(df)

            # Plot
            chart = df.groupby("date")["amount"].sum().reset_index()
            st.line_chart(chart, x="date", y="amount")

    # Tab 4: Tips and Stats
    with tabs[3]:
        st.header("Hydration Tips & Daily Goal")
        today = datetime.now().date()
        df = pd.DataFrame(get_intake_history(user_id), columns=["amount", "date"])
        df["date"] = pd.to_datetime(df["date"]).dt.date
        today_data = df[df["date"] == today]
        total_today = today_data["amount"].sum()

        goal = 2000
        remaining = goal - total_today

        col1, col2, col3 = st.columns(3)
        col1.metric("💧 Today's Intake", f"{total_today} ml")
        col2.metric("🎯 Daily Goal", f"{goal} ml")
        col3.metric("🕓 Remaining", f"{remaining if remaining > 0 else 0} ml")

        st.markdown("""
        **Tips for staying hydrated:**
        - Drink a glass of water after every bathroom break.
        - Keep a bottle near you.
        - Use reminders if you forget!
        """)
