import streamlit as st
import pandas as pd
from io import BytesIO


# Configure the page layout and title
st.set_page_config(page_title="🔄 File Cleaner & Formatter", layout="wide")

# Custom CSS for styling
custom_css = """
<style>
/* Background color for the whole app */
.stApp {
    background-color: #f5f5f5;
}

/* Title styling */
h1 {
    color: #2E86C1;
    text-align: center;
    font-size: 36px;
    font-weight: bold;
}

/* Customizing buttons */
button {
    background-color: #28a745 !important;
    color: white !important;
    font-size: 18px !important;
    border-radius: 8px !important;
}

/* Styling for checkboxes */
div[role="checkbox"] {
    background-color: #ddd;
    padding: 10px;
    border-radius: 5px;
}

/* Dataframe styling */
[data-testid="stTable"] {
    border: 2px solid #3498db;
    border-radius: 8px;
    overflow: hidden;
}

/* File uploader styling */
div.stFileUploader {
    border: 2px dashed #2E86C1 !important;
    padding: 15px;
    border-radius: 10px;
    background-color: #eaf2f8;
}
</style>
"""

# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)
# Main title and introductory text
st.title("🔄 File Cleaner & Formatter")
st.write("🌟 Upload your Excel or CSV files to tidy up and reformat your data seamlessly 🌟")

# File uploader section
files = st.file_uploader("Drag and drop your files here (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if files:  # If files are uploaded
    for file in files:
        # Detect file type based on extension
        ext = file.name.split(".")[-1].lower()
        # Load data into a DataFrame
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        # Show a preview of the uploaded data
        st.subheader(f"📋 {file.name} - Quick Glimpse")
        st.dataframe(df.head())

        # Provide an option to handle missing data
        if st.checkbox(f"Handle Missing Data for {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("Missing data replaced successfully with column averages!")
            st.dataframe(df.head())

        # Let the user choose specific columns to keep
        selected_columns = st.multiselect(f"Pick Columns to Keep - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]  # Update DataFrame based on selected columns
        st.dataframe(df.head())  # Display updated data

        # Visualization option for numeric data
        if st.checkbox(f"📈 Generate Bar Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])  # Display bar chart for the first two numeric columns

        # Options for file format conversion
        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        # Button to initiate download
        if st.button(f"⬇️ Save {file.name} as {format_choice}"):
            output = BytesIO()  # Buffer for file output
            if format_choice == "CSV":
                df.to_csv(output, index=False)  # Save as CSV
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")  # Change file extension
            else:
                df.to_excel(output, index=False)  # Save as Excel
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")  # Change file extension
            output.seek(0)  # Reset buffer position
            st.download_button("⬇️ Download Processed File", file_name=new_name, data=output, mime=mime)  # Download button

        # Notify the user that the processing is done
        st.success("🎉 All operations completed successfully!")