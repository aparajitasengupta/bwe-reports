from io import BytesIO

import fitz
import pandas as pd
import re

def process_pdf(uploaded_file):
    """
    Extract text from a PDF file object, clean up duplicate headers, and process data.
    """
    try:
        # Open the PDF directly from bytes instead of a file path
        pdf_bytes = BytesIO(uploaded_file.read())  # Convert uploaded file to byte stream
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")  # Open from byte stream

        all_lines = [line for page in doc for line in page.get_text().split("\n")]
        df = pd.DataFrame(all_lines, columns=["Content"])

        df_cleaned = remove_duplicate_headers(df)
        processed_df = process_data(df_cleaned)

        return processed_df
    except Exception as e:
        raise RuntimeError(f"Error processing PDF: {e}")

    # **Step 1: Remove repeated headers across pages**
    df_cleaned = remove_duplicate_headers(df)

    # **Step 2: Process cleaned data**
    processed_df = process_data(df_cleaned)

    return processed_df

def remove_duplicate_headers(df):
    """
    Identifies and removes duplicate column headers that appear across pages.
    """
    headers = ["Customer Name", "Account Number", "Item Name", "Item Number", "Price", "Date Sold"]

    cleaned_lines = []
    seen_headers = False  # Flag to track if we’ve seen the headers before

    for line in df["Content"]:
        if all(header in line for header in headers):  # If line contains all column headers
            if seen_headers:  # Skip duplicate headers after the first occurrence
                continue
            seen_headers = True  # Mark headers as seen
        cleaned_lines.append(line)  # Add the valid line

    # Convert cleaned data back into a DataFrame
    return pd.DataFrame(cleaned_lines, columns=["Content"])

def process_data(df):
    """
    Process extracted and cleaned PDF data ensuring items are assigned to correct customers.
    """
    rows = []
    product_data = []  # Store items until assigned
    current_customer = None
    current_account = None

    for idx, row in df.iterrows():
        content = row["Content"].strip()

        # **Step 1: Detect customers BEFORE processing items**
        if re.match(r"^[A-Za-z\s,.\(\)&'-]+$", content) and idx + 1 < len(df):
            potential_account = df.iloc[idx + 1]["Content"].strip()
            if re.match(r"^\d{3,5}$", potential_account):  # Ensure account number format
                # Assign items to the previous customer before changing
                if current_customer and current_account and product_data:
                    for item in product_data:
                        rows.append([current_customer, current_account] + item)
                    product_data = []  # Reset items for the new customer

                # Update new customer info
                current_customer = content
                current_account = potential_account
                print(f"Detected Customer: {current_customer}, Account: {current_account}")
                continue  # Move to next line

        # **Step 2: Detect item numbers and store them**
        elif re.match(r"^\d{1,5}-[\d]+$", content.replace(",", "")):  # Allow up to 5 digits before "-"
            item_number = content.replace(",", "")  # Remove commas from item numbers

            try:
                item_name = df.iloc[idx - 1]["Content"].strip()  # Item Name appears before Item Number
                price_line = df.iloc[idx + 1]["Content"].strip()  # Price is after Item Number
                price = float(price_line.replace("$", "").replace(",", "")) if "$" in price_line else None
                date_sold = df.iloc[idx + 2]["Content"].strip()  # Date Sold appears after Price

                # Store item but do not assign yet
                product_data.append([item_name, item_number, price, date_sold])
                print(f"Processing Item - Name: {item_name}, Number: {item_number}, Price: {price}, Date: {date_sold}")

            except Exception as e:
                print(f"Error processing item data: {e}")

            continue

    # **Store the last batch of customer data**
    if current_customer and current_account and product_data:
        for item in product_data:
            rows.append([current_customer, current_account] + item)

    # Convert to DataFrame
    columns = ["Crafter Name", "Account Number", "Item Name", "Item Number", "Price", "Date Sold"]
    result_df = pd.DataFrame(rows, columns=columns)

    print("\nFinal Processed DataFrame:")
    print(result_df.head(50))

    return result_df
