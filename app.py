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

# Visualization: Test Results by Location
st.header("Test Results by Location")
test_results_chart = px.histogram(
    data, 
    x="Location", 
    color="Test_Result", 
    title="Distribution of Test Results by Location",
    barmode="group"
)
st.plotly_chart(test_results_chart)

# Visualization: Test Results Over Time
st.header("Test Results Over Time")
if not data["Date_of_Sample_Collection"].isnull().all():
    test_results_time_chart = px.line(
        data,
        x="Date_of_Sample_Collection",
        y=data.groupby("Date_of_Sample_Collection")["Test_Result"].transform("count"),
        title="Test Results Over Time",
        markers=True
    )
    st.plotly_chart(test_results_time_chart)
else:
    st.write("No valid dates available for visualization.")

# Visualization: Treated vs EPT
st.header("Treated vs EPT")
treated_ept_chart = px.sunburst(
    data,
    path=["Treated", "EPT"],
    title="Treated and EPT Status Distribution"
)
st.plotly_chart(treated_ept_chart)

# Ending Note
st.write("Thank you for using the dashboard!")
