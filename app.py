import streamlit as st
import pandas as pd

FILE_PATH = "data/exercise_log.csv"

st.title("AI Gym Coach")
st.write("Choose exercise from the dropdown to view progress")

df = pd.read_csv(FILE_PATH)
df['Date'] = pd.to_datetime(df['Date'])

exercise_names = df['Exercise'].unique()

exercise = st.selectbox("Pick an exercise", exercise_names)
days = st.select_slider("Time range (days)", [7, 30, 90, 365, 'All-Time'])

if days == 'All-Time':
    exercise_rows = df[df['Exercise'] == exercise]
else:
    date_cutoff = pd.Timestamp.today().normalize() - pd.Timedelta(days=days)
    exercise_rows = df[(df['Exercise'] == exercise) & (df['Date'] >= date_cutoff)]

daily_best = exercise_rows.groupby('Date')['Weight'].max()

if exercise_rows.empty:
    st.info("No sets logged in this time range")
else:
    st.line_chart(daily_best)

