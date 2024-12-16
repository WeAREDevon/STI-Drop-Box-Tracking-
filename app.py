import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit Title
st.title("Google Form Responses Dashboard")

# Load the Data from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/19ne8l1AVlXw712PbpWYY65wfwzRww-LoLfMihLDJZng/export?format=csv&gid=575000321"
data = pd.read_csv(sheet_url)

# Rename Columns for Usability (Adjust if needed based on your sheet's structure)
data.columns = [
    "Timestamp", 
    "Location", 
    "Notes_Comments", 
    "Date_of_Sample_Collection", 
    "Patient_Initials", 
    "Test_Result", 
    "Treated", 
    "EPT"
]

# Preprocessing
data["Date_of_Sample_Collection"] = pd.to_datetime(data["Date_of_Sample_Collection"], errors="coerce")
data["Treated"] = data["Treated"].astype(str)

# Visualization: Test Results Distribution
st.header("Test Results Distribution")
test_results_chart = px.histogram(
    data, 
    x="Test_Result", 
    title="Distribution of Test Results",
    text_auto=True
)
st.plotly_chart(test_results_chart)

# Visualization: Test Results Over Time
st.header("Test Results Over Time")
if not data["Date_of_Sample_Collection"].isnull().all():
    test_results_time_chart = px.line(
        data.groupby("Date_of_Sample_Collection").size().reset_index(name="Count"),
        x="Date_of_Sample_Collection",
        y="Count",
        title="Test Results Over Time",
        markers=True
    )
    st.plotly_chart(test_results_time_chart)
else:
    st.write("No valid dates available for visualization.")

# Ending Note
st.write("Thank you for using the dashboard!")
