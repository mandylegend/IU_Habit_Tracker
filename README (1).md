
# 📘 Habit Tracker App - README

## 📌 Overview
The Habit Tracker App is a lightweight and user-friendly tool to help users build and maintain healthy habits. Users can create daily or weekly habits, mark completions, view progress, and analyze performance through interactive visualizations.

---

## 🚀 Features
- ✅ Add daily or weekly habits
- 📅 Mark completions easily
- 📊 View completion history and streaks
- 📈 Visual habit analytics using Plotly
- 🗃️ Data stored locally in SQLite
- 🧾 Logging of all actions and errors

---

## 🛠️ Technologies Used
- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: SQLite
- **Visualization**: Plotly, Seaborn, Matplotlib
- **Logging**: Python’s built-in `logging`

---

## 📂 Project Structure
```
├── app.py              # Main Streamlit application
├── db.py               # Database operations (SQLite)
├── habit.py            # Habit class model
├── analytics.py        # Analytics and visualizations
├── logger.py           # Logging setup
├── habits.db           # SQLite database file
├── /logs               # Log files
└── README.md           # Project readme
```

---

## 🧪 How to Run the App
1. **Clone the repository**
```bash
  git clone https://github.com/mandylegend/IU_Habit_Tracker.git
  
cd habit-tracker
```

2. **Install required packages**
```bash
pip install streamlit pandas plotly seaborn
```

3. **Run the app**
```bash
streamlit run app.py
```

---

## 🖼️ App Screenshots (seperate screenshot pdf with explantion have been attached)
- Habit creation form
- Streak visualizations
- Completion history logs

*(Include images in a folder if needed)*

---

## 🔒 Logging & Security
- All user interactions and errors are logged into timestamped files in the `/logs` folder.
- Ensures transparency and makes debugging easier.

---

## 🛠️ Future Improvements
- ⏰ Add reminder notifications
- 📱 Build mobile-friendly layout
- 🔐 User authentication for personal habit storage

---

## 📣 Credits
Developed by **Mandar More** with ❤️ using Python and Streamlit.




