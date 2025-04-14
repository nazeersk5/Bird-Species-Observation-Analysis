import pandas as pd
import numpy as np

file_path = "Bird_Monitoring_Data_GRASSLAND.XLSX"  # Adjust path if needed
xls = pd.ExcelFile(file_path)
cleaned_sheets = {}

for sheet in xls.sheet_names:
    print(f"Processing sheet: {sheet}")
    data = pd.read_excel(xls, sheet)

    # ✅ 1. Drop empty rows and columns
    data.dropna(how="all", inplace=True)
    data.dropna(axis=1, how="all", inplace=True)

    # ✅ 2. Handle critical columns: 'Date' and 'Observer'
    required_columns = ["Date", "Observer"]
    data.dropna(subset=required_columns, inplace=True)

    # ✅ 3. Impute missing values based on data type
    if 'Temperature' in data.columns:
        data['Temperature'] = data['Temperature'].fillna(data['Temperature'].mean())
    if 'Humidity' in data.columns:
        data['Humidity'] = data['Humidity'].fillna(data['Humidity'].median())

    # Fill missing values in object (string) columns
    object_cols = data.select_dtypes(include=['object']).columns
    for col in object_cols:
        data[col] = data[col].fillna('unknown')

    # ✅ 4. Remove duplicate rows
    data.drop_duplicates(inplace=True)

    # ✅ 5. Convert data types
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    if 'Temperature' in data.columns:
        data['Temperature'] = pd.to_numeric(data['Temperature'], errors='coerce')
    if 'Humidity' in data.columns:
        data['Humidity'] = pd.to_numeric(data['Humidity'], errors='coerce')

    # ✅ 6. Outlier detection (IQR method)
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        outlier_mask = ~((data[col] < (Q1 - 1.5 * IQR)) | (data[col] > (Q3 + 1.5 * IQR)))
        data = data[outlier_mask]

    # ✅ 7. Standardize strings (lowercase and trim whitespace)
    for col in object_cols:
        data[col] = data[col].astype(str).str.lower().str.strip()

    # ✅ Save cleaned sheet
    cleaned_sheets[sheet] = data

# ✅ 8. Save all cleaned sheets to new Excel file
output_file = "Cleaned_Bird_Monitoring_Data_Grassland.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for sheet, cleaned_data in cleaned_sheets.items():
        cleaned_data.to_excel(writer, sheet_name=sheet, index=False)

print(f"✅ Data cleaning completed successfully! Saved to {output_file}")