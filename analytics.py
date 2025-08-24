from datetime import datetime
import pandas as pd
import plotly.express as px
from db import get_completions

def filter_periodicity(habits, periodicity):
    return [habit for habit in habits if habit.periodicity == periodicity]

def longest_streak(completions, periodicity):
    if not completions:
        return 0

    dates = sorted([datetime.strptime(c, "%Y-%m-%d %H:%M:%S") for c in completions])
    streak = 1
    max_streak = 1

    gap = 1 if periodicity == 'daily' else 7

    for i in range(1, len(dates)):
        d = (dates[i] - dates[i - 1]).days
        if d <= gap:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1
    return max_streak

def habit_data_graph(habit_id):
    completion = get_completions(habit_id)
    if not completion:
        return None
    
    df = pd.DataFrame(completion, columns=['completion_date'])
    df['completion_date'] = pd.to_datetime(df['completion_date'])
    df = df.groupby(df["completion_date"].dt.date).size().reset_index(name='count')

    fig = px.bar(df, x="completion_date", y="count", title="Habit Completion History", labels={"completion_date": "Date", "count": "Completions"})
    return fig

