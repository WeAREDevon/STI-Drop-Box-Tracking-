import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit Title
st.title("Google Form Responses Dashboard")

# Load Data from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/19ne8l1AVlXw712PbpWYY65wfwzRww-LoLfMihLDJZng/export?format=csv&gid=575000321"
data = pd.read_csv(sheet_url)

# Rename columns for easier handling
data.columns = [
    "Timestamp",
    "Location",
    "Notes",
    "Date of Sample Collection",
    "Patient Initials",
    "Test Result",
    "Treated",
    "EPT"
]

# Clean Data
data = data[~data["Timestamp"].str.contains("Timestamp", na=False)]
data["Test Result"] = data["Test Result"].fillna("Unknown")
data["Treated"] = data["Treated"].map({"True": "Treated", "False": "Not Treated"}).fillna("Unknown")
data["EPT"] = data["EPT"].map({"True": "EPT Provided", "False": "No EPT"}).fillna("Unknown")

# Metrics Summary
st.header("Metrics Summary")
st.metric("Total Records", len(data))
st.metric("Positive Results", (data["Test Result"] == "Positive").sum())
st.metric("Negative Results", (data["Test Result"] == "Negative").sum())

# Visualizations Section
st.header("Visualizations")

# Test Result Distribution - Pie Chart
st.subheader("Test Result Distribution")
test_result_fig = px.pie(
    data, 
    names="Test Result", 
    title="Test Result Distribution", 
    hole=0.3
)
st.plotly_chart(test_result_fig)

# Treatment Status - Bar Chart
st.subheader("Treatment Status Distribution")
treatment_fig = px.bar(
    data["Treated"].value_counts().reset_index(),
    x="index",
    y="Treated",
    labels={"index": "Treatment Status", "Treated": "Count"},
    title="Treatment Status Distribution",
    text_auto=True
)
st.plotly_chart(treatment_fig)

# Location-Based Trends - Bar Chart
st.subheader("Sample Collection by Location")
location_fig = px.bar(
    data["Location"].value_counts().reset_index(),
    x="index",
    y="Location",
    labels={"index": "Location", "Location": "Count"},
    title="Sample Collection by Location",
    text_auto=True
)
st.plotly_chart(location_fig)
