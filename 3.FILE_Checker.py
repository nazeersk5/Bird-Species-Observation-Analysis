import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Validation Tool", layout="centered")
st.title("📊 Dataset Validator for Bird Monitoring Data")

uploaded_file = st.file_uploader("Upload your Excel (.xlsx) file", type=["xlsx"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    df_dict = pd.read_excel(uploaded_file, sheet_name=None)  # Read all sheets

    overall_clean = True  # Flag to check if all sheets are clean

    for sheet_name, df in df_dict.items():
        st.subheader(f"📄 Sheet: {sheet_name}")

        # Basic checks for each sheet
        missing_report = df.isnull().sum()
        empty_rows = df[df.isnull().all(axis=1)]
        empty_cols = df.columns[df.isnull().all()]

        # Check conditions
        if missing_report.sum() == 0 and empty_rows.empty and len(empty_cols) == 0:
            st.success("✅ This sheet is clean!")
        else:
            overall_clean = False
            st.warning("⚠️ Issues Found:")
            if missing_report.sum() > 0:
                st.write("🔸 Columns with missing values:")
                st.write(missing_report[missing_report > 0])
            if not empty_rows.empty:
                st.write(f"🔸 Found {len(empty_rows)} fully empty rows.")
            if len(empty_cols) > 0:
                st.write(f"🔸 Found {len(empty_cols)} fully empty columns: {list(empty_cols)}")

    if overall_clean:
        st.success("🎉 The uploaded dataset is fully clean across all sheets!")
    else:
        st.error("❌ The dataset has cleaning issues! Please fix before processing.")

else:
    st.info("👈 Please upload a dataset to validate.")

