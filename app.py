import streamlit as st
import pandas as pd

FILE_PATH = "data/exercise_log.csv"

st.title("AI Gym Coach")
st.write("Choose exercise from the dropdown to view progress")

df = pd.read_csv(FILE_PATH)
df['Date'] = pd.to_datetime(df['Date'])

exercise_names = df['Exercise'].unique()

exercise = st.selectbox("Pick an exercise", exercise_names)

exercise_rows = df[(df['Exercise'] == exercise)]
daily_best = exercise_rows.groupby('Date')['Weight'].max()

st.line_chart(daily_best)

