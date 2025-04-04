import pandas as pd
import streamlit as st
from service.ingestion import process_pdf
from service.visualization import plot_donut_chart, plot_bar_chart, plot_sales_over_time, plot_crafter_bubble_chart


def main():
    # Streamlit app configuration
    st.set_page_config(
        page_title="Brooklyn Women's Exchange",
        page_icon="images/icon.png",
        layout="wide",
    )

    set_background_color()

    # Header Image
    st.image("images/new-ban.png", use_container_width=True)

    st.title("PDF Uploader and Analysis Tool")
    st.write("Upload a PDF file to extract, process, and visualize the data.")

    uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Processing PDF..."):
            processed_df = process_pdf(uploaded_file)

        if not isinstance(processed_df, pd.DataFrame):
            st.error("Unexpected return type from `process_pdf`")
        else:
            st.success("PDF processed successfully!")
            st.write("### Processed Data:")
            st.dataframe(processed_df, use_container_width=True)

            # **Step 1: Aggregate Data for Visualization**
            try:
                processed_df["Total Cost"] = processed_df["Price"]  # Rename for consistency

                # Donut Chart: Total cost per account
                account_total_cost = processed_df.groupby("Account Number")["Total Cost"].sum()

                item_sales = processed_df.groupby("Item Number").agg(
                    Total_Cost=("Total Cost", "sum"),
                    Count=("Item Name", "count"),
                    Item_Name=("Item Name", "first")
                ).reset_index()

                # Filter to only include items sold at least 3 times
                item_sales = item_sales[item_sales["Count"] >= 3]

                processed_df["Date Sold"] = pd.to_datetime(processed_df["Date Sold"], errors="coerce")
                sales_over_time = processed_df.groupby("Date Sold")["Price"].sum().reset_index()
                sales_over_time.columns = ["Date Sold", "Price"]
                sales_over_time["Date Sold"] = pd.to_datetime(sales_over_time["Date Sold"])

                # **Step 2: Render Charts**
                st.write("## Visualizations")

                col1, col2 = st.columns(2)

                with col1:
                    if not account_total_cost.empty:
                        st.write("### Total Cost per Account")
                        plot_donut_chart(account_total_cost)
                    else:
                        st.warning("Not enough data for donut chart.")

                with col2:
                    if not item_sales.empty:
                        st.write("### Sales per Item")
                        plot_bar_chart(item_sales)
                    else:
                        st.warning("Not enough data for bar chart.")



                st.write("### Sales Over Time")
                if not sales_over_time.empty:
                        plot_sales_over_time(sales_over_time)
                else:
                        st.warning("Not enough data for time-series chart.")

                st.write("### Crafter Performance")
                plot_crafter_bubble_chart(processed_df)


            except KeyError as e:
                st.error(f"Missing expected column: {e}")

    else:
        st.warning("Please upload a PDF file to proceed.")

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 6, 1])

    with col2:
        st.markdown(
            """
            <div style='text-align: center; padding: 20px 0; font-size: 14px; color: #555;'>
                Having issues or need help? <br>
                <a href="mailto:appy.sengupta@gmail.com" style="color: #D9534F; font-weight: bold; text-decoration: none;">
                    📧 Contact Support
                </a>
                <br><br>
                <span style="font-size: 12px; color: #999;">
                    © 2025 Brooklyn Women's Exchange · All rights reserved
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )


def set_background_color():
    """
    Adds a custom background color to the Streamlit app.
    """
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #EFECEC; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
