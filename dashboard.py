import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your data
class_df = pd.read_csv("classwisetotalstudents.csv")
absence_df = pd.read_csv("studentterm1data.csv")

# Preprocess
absence_df['Date'] = pd.to_datetime(absence_df['Date'], dayfirst=True, errors='coerce')
absence_df['ReasonAbr'] = absence_df['ReasonAbr'].fillna('Unknown')

# Sidebar filters
selected_class = st.sidebar.selectbox("Filter by Class", options=["All"] + class_df["Class"].tolist())
filtered_df = absence_df if selected_class == "All" else absence_df[absence_df["Class"] == selected_class]

# Prepare pie chart data
reason_counts = filtered_df['ReasonAbr'].value_counts().to_dict()
non_late = filtered_df[filtered_df['ReasonAbr'] != 'Latecoming']['NRIC/FIN/UIN'].nunique()
total_students = class_df['HeadKount'].sum()
present = total_students - non_late
reason_counts["Present"] = present

# Plot pie chart
fig, ax = plt.subplots()
ax.pie(reason_counts.values(), labels=reason_counts.keys(), autopct='%1.1f%%', startangle=140)
ax.axis('equal')
st.title("Attendance Breakdown")
st.pyplot(fig)
