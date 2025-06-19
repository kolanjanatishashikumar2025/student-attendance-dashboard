import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your data
class_df = pd.read_csv("classwisetotalstudents.csv",engine='python', on_bad_lines='skip')
absence_df = pd.read_csv("studentterm1data.csv",engine='python', on_bad_lines='skip')

# Preprocess
absence_df['Date'] = pd.to_datetime(absence_df['Date'], dayfirst=True, errors='coerce')
absence_df['ReasonAbr'] = absence_df['ReasonAbr'].fillna('Unknown')


# Sidebar Filters
st.sidebar.header("Filter Options")

# Class filter
class_options = ["All"] + sorted(absence_df["Class"].dropna().unique())
selected_class = st.sidebar.selectbox("Select Class", class_options)

# Date Range filter
absence_df['Date'] = pd.to_datetime(absence_df['Date'], dayfirst=True, errors='coerce')
min_date = absence_df['Date'].min()
max_date = absence_df['Date'].max()
selected_range = st.sidebar.date_input("Date Range", [min_date, max_date])

# Apply filters
filtered_df = absence_df.copy()
if selected_class != "All":
    filtered_df = filtered_df[filtered_df["Class"] == selected_class]
filtered_df = filtered_df[
    (filtered_df['Date'] >= pd.to_datetime(selected_range[0])) &
    (filtered_df['Date'] <= pd.to_datetime(selected_range[1]))
]

# Sidebar buttons
st.sidebar.header("Select Visualization")
show_pie = st.sidebar.button("🎯 Pie Chart")
show_bar = st.sidebar.button("📊 Bar Chart")
show_table = st.sidebar.button("📋 Top Offenders Table")

# Main Area - Show visual based on button
if show_pie:
    st.title("Attendance Breakdown")
    reason_counts = filtered_df['ReasonAbr'].value_counts().to_dict()
    
    # Calculate Present
    non_late = filtered_df[filtered_df['ReasonAbr'] != 'Latecoming']['NRIC/FIN/UIN'].nunique()
    total_students = class_df['HeadKount'].sum()
    reason_counts["Present"] = total_students - non_late

    # Plot Pie
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.pie(reason_counts.values(), labels=reason_counts.keys(), autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

elif show_bar:
    st.title("Absence Reasons Count")
    reason_counts = filtered_df['ReasonAbr'].value_counts()
    st.bar_chart(reason_counts)

elif show_table:
    st.title("Top Repeat Offenders")
    top_students = (
        filtered_df.groupby(['NRIC/FIN/UIN', 'Name'])
        .size()
        .reset_index(name='Events')
        .sort_values(by='Events', ascending=False)
        .head(10)
    )
    st.dataframe(top_students)

else:
    st.info("Select a visualization from the left panel to display results.")
