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
    """Get the user's personal record (heaviest weight) for an exercise. Use the exact name from get_exercise_names."""
    
    name = name.strip().title()
    
    file_exists = os.path.exists(FILE_PATH)
    if not file_exists:
        return "No exercises logged yet."
    
    df = pd.read_csv(FILE_PATH, usecols=['Exercise', 'Weight'])

    personal_record = df.loc[df['Exercise'] == name, 'Weight'].max()

    if pd.isna(personal_record):
        return f"No personal record for {name} yet"

    return f"Your personal record for {name} is {personal_record} lbs"
    






