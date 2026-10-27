from langchain.tools import tool
import csv
from datetime import date
import os 

FILE_PATH = "data/exercise_log.csv"

@tool
def log_exercise(name: str, weight: float, reps: int) -> str:
    """Log a single set of an exercise with its weight and reps. Call once for each set the user did."""

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




