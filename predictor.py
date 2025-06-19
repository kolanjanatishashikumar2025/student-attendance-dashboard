# predictor.py

import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

st.title("🎯 Student Absence Risk Predictor")

# === 1. Load Data ===
df = pd.read_csv("studentterm1data.csv", engine='python', on_bad_lines='skip')

# === 2. Preprocess ===
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
df = df.dropna(subset=['Date'])

df['Week'] = df['Date'].dt.isocalendar().week
df['Year'] = df['Date'].dt.isocalendar().year
df['Weekday'] = df['Date'].dt.day_name()
df['AbsentFlag'] = df['ReasonAbr'].apply(lambda x: 0 if str(x).lower().strip() == 'latecoming' else 1)

# === 3. Group Weekly ===
weekly = df.groupby(['NRIC/FIN/UIN', 'Name', 'Week']).agg(
    AbsenceCount=('AbsentFlag', 'sum'),
    LateCount=('ReasonAbr', lambda x: (x == 'Latecoming').sum()),
    DaysAbsent=('Weekday', 'nunique')
).reset_index()

weekly['AbsentThisWeek'] = weekly['AbsenceCount'].apply(lambda x: 1 if x > 0 else 0)

# === Sidebar ===
if st.sidebar.button("🧠 Predict Absentee Risk"):

    # === 4. Features & Model Training ===
    X = weekly[['AbsenceCount', 'LateCount', 'DaysAbsent']]
    y = weekly['AbsentThisWeek']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # === 5. Predict Full Dataset ===
    weekly['PredictedRisk'] = model.predict(X)

    st.success("Prediction completed! Displaying results...")

    # === 6. Visual: Risk by Week ===
    st.subheader("📊 Predicted Absence Risk by Week")
    chart_data = weekly[weekly['PredictedRisk'] == 1].groupby('Week').size()
    st.bar_chart(chart_data)

    # === 7. Table: Top At-Risk Students ===
    st.subheader("📋 Top Predicted At-Risk Students")
    high_risk = weekly[weekly['PredictedRisk'] == 1].sort_values(by='AbsenceCount', ascending=False)
    st.dataframe(high_risk[['NRIC/FIN/UIN', 'Name', 'Week', 'AbsenceCount', 'LateCount', 'DaysAbsent']].head(10))

else:
    st.info("Click the button in the sidebar to run the prediction model.")
