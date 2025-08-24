import streamlit as st
from db import init_db, add_habit, get_all_habits, delete_habit, mark_completion, get_completions, habit_dataframe
import random
from analytics import filter_periodicity, longest_streak, habit_data_graph, hit_rate, skip_days
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


# Initialize DB
init_db()

# Set up Streamlit page
st.set_page_config(page_title="Habit Tracker", layout="wide")
st.title("✅ Habit Tracker")


# Sidebar menu

menu = ["Create Habit", "View Habits", "Analytics",
        "Habit Tracker Info", "Get Habits", "dataframe"]
with st.sidebar:
    st.image("D:\IU oop\Habit_tracker\habti trackker image.jpg", width=300)
    now = datetime.now()
    st.sidebar.markdown(f"📅 **Date:** `{now.strftime('%A, %d %B %Y')}`")
    st.sidebar.markdown(f"🕒 **Time:** `{now.strftime('%I:%M:%S %p')}`")
    st.markdown("### 📋 Main Navigation")

    choice = st.selectbox("Select a page:", [
                          "Create Habit", "View Habits", "Analytics", "Habit Tracker Info", "Get Habits", "dataframe", "Hit rate", "Skip days"])
st.balloons()


# def add_bg_from_url(url: str):
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("{url}");
#             background-attachment: fixed;
#             background-size: cover;
#             background-position: center;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )


# Example call
# Image is randomly sletected from internet

# add_bg_from_url("https://cdn.apollohospitals.com/health-library-prod/2021/04/shutterstock_788590396-scaled.jpg")


# --- Create Habit ---
if choice == "Create Habit":
    st.subheader("✍️ Add a New Habit")
    name = st.text_input("Enter habit name")
    periodicity = st.selectbox("Select periodicity", ['daily', 'weekly'])

    if st.button("Add Habit"):
        if name:
            try:
                add_habit(name, periodicity)
                st.success(f"Habit '{name}' added successfully.")
            except Exception as e:
                st.error(f"Error adding habit: {e}")
        else:
            st.warning("Please enter a habit name.")


# --- View Habits ---
elif choice == "View Habits":
    st.subheader("📔 Your Habits and Graphs")
    habits = get_all_habits()

    if not habits:
        st.info("No habits found.")
    else:
        for habit in habits:
            # expander for each habit
            with st.expander(f"{habit.name} ({habit.periodicity})"):
                st.markdown(f"🗓️ Created on: `{habit.created_at}`")

                # Mark completion button
                if st.button(f"✅ Mark Completed [{habit.id}]"):
                    mark_completion(habit.id)
                    st.success(f"Marked '{habit.name}' as completed.")

                # graph for habit
                st.subheader("Habit graph")
                fig = habit_data_graph(habit.id)
                if fig:
                    st.plotly_chart(fig, use_container_width=True,
                                    key=f"plot_{habit.id}")
                else:
                    st.info("No completion data available for this habit.")

                # delete habit button
                if st.button(f"🗑️ Delete Habit [{habit.id}]"):
                    delete_habit(habit.id)
                    st.success(f"Deleted habit '{habit.name}'.")

                # Fetch and display completion history
                completions = get_completions(habit.id)
                if completions:
                    st.markdown("### ✅ Completion History")
                    for c in completions:
                        st.markdown(f"- {c}")
                else:
                    st.info("No completions marked yet.")

# --- Analytics ---
elif choice == "Analytics":
    st.subheader("📈 Habit Analytics")
    habits = get_all_habits()

    if not habits:
        st.info("No habits to analyze.")
    else:
        for habit in habits:
            completions = get_completions(habit.id)
            streak = longest_streak(completions, habit.periodicity)
            st.markdown(
                f"**{habit.name}** ({habit.periodicity}) — 🔥 Longest Streak: `{streak}`")


# --- Get Habits ---
elif choice == "Get Habits":
    st.subheader("All habits in the databse")
    habits = get_all_habits()
    if not habits:
        st.info("No habits found")
    else:
        for habit in habits:
            st.markdown(
                f"- {habit.name} - ({habit.periodicity}) created on {habit.created_at}")


# --- Habit DataFrame ---
elif choice == "dataframe":
    st.subheader("Habit DataFrame")
    habits = habit_dataframe()
    if habits.empty:
        st.info("No habits found to display in DataFrame.")
    else:
        st.dataframe(habits)

# --- Hit Rate ---
elif choice == "Hit rate":
    st.subheader("🎯 Habit Hit Rate")
    habits = get_all_habits()
    if not habits:
        st.info("No habits to analyze.")
    # hit rate calculation
    else:
        for habit in habits:
            completions = get_completions(habit.id)
            if habit.periodicity == 'daily':
                total_days = (datetime.now() - datetime.strptime(
                    habit.created_at, "%Y-%m-%d %H:%M:%S")).days + 1
            else:  # weekly
                total_days = ((datetime.now() - datetime.strptime(
                    habit.created_at, "%Y-%m-%d %H:%M:%S")).days // 7) + 1

            rate = hit_rate(completions, total_days)
            st.markdown(
                f"**{habit.name}** ({habit.periodicity}) — 🎯 Hit Rate: `{rate:.2f}%`")

# --- Skip Days ---
elif choice == "Skip days":
    st.subheader("⏭️ Habit Skip Days")
    habits = get_all_habits()
    if not habits:
        st.info("No habits to analyze.")
    else:
        for habit in habits:
            completions = get_completions(habit.id)
            skips = skip_days(completions, habit.periodicity)
            st.markdown(
                f"**{habit.name}** ({habit.periodicity}) — ⏭️ Skip Days: `{skips}`")

# --- Info ---
elif choice == "Habit Tracker Info":
    st.subheader("ℹ️ Habit Tracker Information")
    st.image("https://m.media-amazon.com/images/I/91kghLn3itL.jpg", width=900)
    st.write("Note: This image is taken from internet and is not owned by me.")
    st.markdown("""
    This is a simple habit tracker app built with **Streamlit** and **SQLite**.

    ### 🔧 Features
    - Add habits with daily or weekly periodicity.
    - Mark habits as completed.
    - View all habits and completion history.
    - Analyze your progress with streak insights.

    ### 🧪 Technologies Used    
    - Streamlit (Frontend)
    - SQLite (Database)
    - Python (Backend)

    ### 🚀 How to Use
    1. Go to **Create Habit** to add a new habit.
    2. Use **View Habits** to see your habits and track them.
    3. View **Analytics** to check your streaks.
    4. Check **Habit Tracker Info** for documentation.

    ---
    Made with ❤️ by **Mandar More** 
    """)


# --- Tips ---
tips = [
    "💡 Small habits make a big difference!",
    "📈 Track daily for consistent growth.",
    "🏁 Don't break the chain!",
    "🗓️ Set reminders for daily habits.",
    "🎯 Focus on one habit at a time.",
    "📊 Use analytics to stay motivated.",
    "📝 Write down your habits to reinforce them.",
    "🤝 Share your habits with friends for accountability.",
    "⏰ Habit tracking is a marathon, not a sprint.",
    "🌱 Celebrate small wins to stay motivated.",
    "📅 Review your habits weekly to adjust goals.",
    "🔄 Consistency is key to habit formation.",
    "🧘‍♂️ Mindfulness can help in habit tracking.",
    "📚 Read about habit formation for more insights.",
    "🎉 Reward yourself for completing habits.",
    "🧩 Break down big habits into smaller steps.",
    "📖 Keep a habit journal to reflect on your progress.",
    "🕒 Track habits at the same time each day."
]
st.sidebar.markdown(f"**Tip:** {random.choice(tips)}")

# --- Sidebar Progress Bar ---
habit_count = len(get_all_habits())
st.sidebar.markdown("### 🎯 Habit Count")
st.sidebar.progress(min(habit_count / 20, 2.0))  # Assume goal = 10 habits
st.sidebar.markdown(f"**{habit_count}/20 Tracked**")


# --- Custom CSS for Sidebar ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color:#f57058;
        padding: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)
