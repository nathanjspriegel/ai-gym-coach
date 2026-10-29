from langchain.tools import tool
import csv
from datetime import date
import os 
import pandas as pd

FILE_PATH = "data/exercise_log.csv"

@tool
def log_exercise(name: str, weight: float, reps: int) -> str:
    """Log a single set of an exercise with its weight and reps. 
    Call once for each set the user did. Before logging, 
    call get_exercise_names and reuse an existing name if the exercise matches one."""

    name = name.strip().title()

    exercise_data = [
        {'Date': date.today(), 'Exercise': name, 'Weight': weight, 'Reps': reps}
    ]

    file_exists = os.path.exists(FILE_PATH)
  
    with open(FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
        labels = ['Date', 'Exercise', 'Weight', 'Reps']
        writer = csv.DictWriter(file, fieldnames=labels)

        if not file_exists:
            writer.writeheader()

        writer.writerows(exercise_data)

    return f"Logged {name}: {weight} x {reps}"

@tool
def get_exercise_names() -> str:
    """Get the list of exercise names already logged. Use this before logging to reuse existing names."""

    file_exists = os.path.exists(FILE_PATH)
    if not file_exists:
        return "No exercises logged yet."
    
    with open(FILE_PATH, mode='r', newline='', encoding='utf-8') as file:
        
        
        names = set()
    
        reader = csv.DictReader(file)
        for row in reader:
            names.add(row['Exercise']) 

    return ", ".join(names)

@tool
def get_personal_record(name: str) -> str:
    """Get the user's personal record for an exercise: the heaviest weight lifted, with the reps and date of that set. 
    Use the exact name from get_exercise_names."""

    name = name.strip().title()
    
    file_exists = os.path.exists(FILE_PATH)
    if not file_exists:
        return "No exercises logged yet."
    
    df = pd.read_csv(FILE_PATH)

    exercise_rows = df[df['Exercise'] == name]

    if exercise_rows.empty:
        return f"No personal record for {name} yet."

    pr_idx = exercise_rows['Weight'].idxmax()
    pr_row = df.loc[pr_idx]

    return f"Your personal record for {name} is {pr_row['Weight']} lbs for {pr_row['Reps']} reps on {pr_row['Date']}."

@tool
def get_today() -> str:
    """Get today's date and day of the week. 
    Use this to determine dates such as 'yesterday' or 'last Friday'."""
    
    today = date.today()
    return today.strftime("%A, %Y-%m-%d")

@tool
def get_workout_history(day: str) -> str:
    """Get each set with its weight and reps for every exercise done on a given day.
    The date must be in YYYY-MM-DD format.
    Use get_today to determine dates like 'yesterday' or 'last Friday'."""

    file_exists = os.path.exists(FILE_PATH)
    if not file_exists:
        return "No exercises logged yet."

    df = pd.read_csv(FILE_PATH)

    exercise_rows = df[df['Date'] == day]
    
    if exercise_rows.empty:
        return f"No workout logged on {day}."

    day_log = []
    for _, row in exercise_rows.iterrows():
        day_log.append(f"{row['Exercise']}: {row['Weight']} lbs x {row['Reps']}")
    
    return "\n".join(day_log)

@tool
def get_exercise_progress(name: str, days: int = 30) -> str:
    """Show progress for a given exercise over a given number of days (30 default). 
    Use the exact name from get_exercise_names."""

    name = name.strip().title()

    file_exists = os.path.exists(FILE_PATH)
    if not file_exists:
        return "No exercises logged yet."
    
    df = pd.read_csv(FILE_PATH)
    df['Date'] = pd.to_datetime(df['Date'])

    date_cutoff = pd.Timestamp.today().normalize() - pd.Timedelta(days=days)

    exercise_rows = df[(df['Exercise'] == name) & (df['Date'] >= date_cutoff)]
    
    if exercise_rows.empty:
        return f"No {name} logged in the last {days} days."

    daily_best = exercise_rows.groupby('Date')['Weight'].max()

    log = []

    for day, weight in daily_best.items():
        log.append(f"{day.date()}: {weight} lbs")

    return "\n".join(log)
    








