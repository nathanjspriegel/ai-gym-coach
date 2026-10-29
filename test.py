import pandas as pd

df = pd.read_csv("data/exercise_log.csv")

exercise_rows = df[df['Exercise'] == 'Barbell Bench Press']
daily_best = exercise_rows.groupby('Date')['Weight'].max()
print(daily_best)