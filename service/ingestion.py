import fitz  # PyMuPDF for PDF processing
import pandas as pd
import re

def process_pdf(pdf_path):
    """
    Extract text from the PDF, process it, and return processed DataFrame,
    account totals for the donut chart, and item sales for the bar chart.
    """
    # Extract text from the PDF
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        text += doc[page_num].get_text()

    # Convert text to DataFrame
    lines = text.split("\n")
    df = pd.DataFrame(lines, columns=["Content"])

    # Print the extracted DataFrame for debugging
    print("Initial DataFrame (Extracted from PDF):")
    print(df.head(20))  # Print the first 20 rows for inspection

    # Process the data
    processed_df = process_data(df)

    # Group by Account Number for donut chart
    account_total_cost = processed_df.groupby('Account Number')['Total Cost'].sum()

    # Group by Item Number for bar chart
    item_sales = processed_df.groupby('Item Number').agg({'Total Cost': 'sum', 'Count': 'sum'}).reset_index()

    return processed_df, account_total_cost, item_sales

def process_data(df):
    """
    Process the extracted PDF data and return a structured DataFrame.
    """
    rows = []
    current_account_number = None
    current_customer_name = None
    item_data = []

    for idx, row in df.iterrows():
        content = row['Content']
        content = content.strip()

        # Step 1: Detect customer name
        if re.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+)*$", content) and "TOTAL" not in content:
            if current_account_number is not None and item_data:
                for item in item_data:
                    rows.append(item + [current_customer_name, current_account_number])
            current_customer_name = content
            item_data = []
            continue

        # Step 2: Detect account number (3 or 4 digits)
        elif re.match(r"^\d{3,4}$", content):
            if current_account_number is not None and item_data:
                for item in item_data:
                    rows.append(item + [current_customer_name, current_account_number])
            current_account_number = content
            continue

        # Step 3: Detect item number and its corresponding data
        elif re.match(r"^\d{3}-\d{2,4}$", content):
            item_number = content
            try:
                # Item name is above the item number
                item_name = df.iloc[idx - 1]['Content'].strip()
                # Price is below the item number
                price = df.iloc[idx + 1]['Content'].strip()
                price = float(price.replace('$', '').replace(',', ''))  # Clean and convert price
                item_data.append([item_name, item_number, price])
            except Exception as e:
                print(f"Error processing item data: {e}")
            continue

    # Append any remaining items for the last account
    if current_account_number is not None and item_data:
        for item in item_data:
            rows.append(item + [current_customer_name, current_account_number])

    # Create a DataFrame from the processed data
    columns = ['Item Name', 'Item Number', 'Price', 'Customer Name', 'Account Number']
    result_df = pd.DataFrame(rows, columns=columns)

    # Group by 'Account Number' and 'Item Number' to calculate totals and counts
    result_df = result_df.groupby(
        ['Item Name', 'Item Number', 'Customer Name', 'Account Number'], as_index=False
    ).agg({
        'Price': ['sum', 'count']  # Calculate total cost and count
    })

    # Flatten the multi-index columns
    result_df.columns = ['Item Name', 'Item Number', 'Customer Name', 'Account Number', 'Total Cost', 'Count']

    # Print the final processed DataFrame for debugging
    print("\nFinal Processed DataFrame:")
    print(result_df.head(20))  # Print the first 20 rows for inspection

    return result_df
