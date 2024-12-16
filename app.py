import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit Title
st.title("Google Form Responses Dashboard")

# Load the Data from Google Sheets
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

# Clean the dataset
data = data[~data["Timestamp"].str.contains("Timestamp", na=False)]  # Remove header rows if repeated
data["Test Result"] = data["Test Result"].fillna("Unknown")
data["Treated"] = data["Treated"].map({"True": "Treated", "False": "Not Treated"}).fillna("Unknown")
data["EPT"] = data["EPT"].map({"True": "EPT Provided", "False": "No EPT"}).fillna("Unknown")

# Sidebar for filtering
st.sidebar.header("Filter Options")
location_filter = st.sidebar.multiselect("Select Locations", data["Location"].unique(), default=data["Location"].unique())

# Apply filters
filtered_data = data[data["Location"].isin(location_filter)]

# Metrics
st.header("Metrics Summary")
st.metric("Total Records", len(filtered_data))
st.metric("Positive Results", (filtered_data["Test Result"] == "Positive").sum())
st.metric("Negative Results", (filtered_data["Test Result"] == "Negative").sum())

# Visualizations
st.header("Visualizations")

# Test Result Distribution
st.subheader("Test Result Distribution")
test_result_fig = px.bar(
    filtered_data["Test Result"].value_counts().reset_index(),
    x="index",
    y="Test Result",
    labels={"index": "Test Result", "Test Result": "Count"},
    title="Test Result Distribution"
)
st.plotly_chart(test_result_fig)

# Treatment Status Distribution
st.subheader("Treatment Status Distribution")
treatment_fig = px.bar(
    filtered_data["Treated"].value_counts().reset_index(),
    x="index",
    y="Treated",
    labels={"index": "Treatment Status", "Treated": "Count"},
    title="Treatment Status Distribution"
)
st.plotly_chart(treatment_fig)

# Location-based Trends
st.subheader("Sample Collection by Location")
location_fig = px.bar(
    filtered_data["Location"].value_counts().reset_index(),
    x="index",
    y="Location",
    labels={"index": "Location", "Location": "Count"},
    title="Sample Collection by Location"
)
st.plotly_chart(location_fig)
