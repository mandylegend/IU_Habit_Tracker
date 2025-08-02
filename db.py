import sqlite3
from datetime import datetime
from habit import Habit
import pandas as pd
from logger import logging

db = "habits.db"

def db_connection():
    return sqlite3.connect(db)

# Initialize the database
# Set up log directory

logging.info("Setting up database connection.")
def init_db():
    try:
        with db_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    periodicity TEXT NOT NULL,
                    created_at TEXT
                );
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER,
                    completion_date TEXT,
                    FOREIGN KEY(habit_id) REFERENCES habits(id)
                );
            ''')
        logging.info("Database initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")

# CRUD operations
logging.info("Defining CRUD operations for habits.")
def add_habit(name, periodicity):
    try:
        with db_connection() as conn:
            conn.execute(
                "INSERT INTO habits (name, periodicity, created_at) VALUES (?, ?, ?)",
                (name, periodicity, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
        logging.info(f"Habit '{name}' added successfully.")
    except Exception as e:
        logging.error(f"Error adding habit '{name}': {e}")


logging.info("Defining function to get all habits.")
def get_all_habits():
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, periodicity, created_at FROM habits")
    rows = cursor.fetchall()
    conn.close()
    return [Habit(name=row[1], periodicity=row[2], created_at=row[3], habit_id=row[0]) for row in rows]


logging.info("Defining function to delete a habit.")
def delete_habit(habit_id):
    try:
        with db_connection() as conn:
            conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
            conn.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
            conn.commit()
        logging.info(f"Habit with ID {habit_id} deleted successfully.")
    except Exception as e:
        logging.error(f"Error deleting habit with ID {habit_id}: {e}")


logging.info("Defining function to mark completion of a habit.")
def mark_completion(habit_id):
    try:
        with db_connection() as conn:
            conn.execute(
                "INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)",
                (habit_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()
        logging.info(f"Completion marked for habit ID {habit_id}.")
    except Exception as e:
        logging.error(f"Error marking completion for habit ID {habit_id}: {e}")


logging.info("Defining function to mark completion of a habit.")
def get_completions(habit_id):
    try:
        with db_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT completion_date FROM completions WHERE habit_id=? ORDER BY completion_date",
                (habit_id,)
            )
            completions = [row[0] for row in cur.fetchall()]
        logging.info(f"Fetched completions for habit ID {habit_id}.")
        return completions
    except Exception as e:
        logging.error(f"Error fetching completions for habit ID {habit_id}: {e}")
        return []

# dataframe function to get habits in a DataFrame format
logging.info("Defining function to get habits in a DataFrame format.")
def habit_dataframe():
    habits = get_all_habits()
    data = {
        "ID": [habit.id for habit in habits],
        "Name": [habit.name for habit in habits],   
        "Periodicity": [habit.periodicity for habit in habits],
        "Created At": [habit.created_at for habit in habits]

    }
    return pd.DataFrame(data)

logging.info("The database module is ready for use.")
logging.info("Database operations have been defined successfully.")
