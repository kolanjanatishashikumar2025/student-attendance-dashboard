import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your data
class_df = pd.read_csv("classwisetotalstudents.csv",engine='python', on_bad_lines='skip')
absence_df = pd.read_csv("studentterm1data.csv",engine='python', on_bad_lines='skip')

# Preprocess
absence_df['Date'] = pd.to_datetime(absence_df['Date'], dayfirst=True, errors='coerce')
absence_df['ReasonAbr'] = absence_df['ReasonAbr'].fillna('Unknown')

# Sidebar filters
selected_class = st.sidebar.selectbox("Filter by Class", options=["All"] + class_df["Class"].tolist())
filtered_df = absence_df if selected_class == "All" else absence_df[absence_df["Class"] == selected_class]

#1. Date Range Filter
#Add a slider or date picker to filter by week/month/term:

min_date = absence_df['Date'].min()
max_date = absence_df['Date'].max()
selected_range = st.sidebar.date_input("Date range", [min_date, max_date])

filtered_df = filtered_df[
    (filtered_df['Date'] >= pd.to_datetime(selected_range[0])) &
    (filtered_df['Date'] <= pd.to_datetime(selected_range[1]))
]


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
