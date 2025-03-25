import pandas as pd
import streamlit as st
from service.ingestion import process_pdf
from service.visualization import plot_donut_chart, plot_bar_chart, plot_category_bar_chart, plot_sales_over_time, plot_crafter_bubble_chart


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

                # Bar Chart: Total cost & item count per item number
                item_sales = processed_df.groupby("Item Number").agg(
                    {"Total Cost": "sum", "Item Name": "count"}).reset_index()
                item_sales.rename(columns={"Item Name": "Count"}, inplace=True)

                # New Chart: Category-level (Item Name) analysis
                category_sales = processed_df.groupby("Item Name").agg(
                    {"Total Cost": "sum", "Item Number": "count"}).reset_index()
                category_sales.rename(columns={"Item Number": "Count"}, inplace=True)

                processed_df["Date Sold"] = pd.to_datetime(processed_df["Date Sold"])
                sales_over_time = processed_df.groupby(processed_df["Date Sold"].dt.to_period("M"))["Price"].sum()
                sales_over_time.index = sales_over_time.index.to_timestamp()

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

                col1, col2 = st.columns(2)

                with col1:
                    st.write("### Sales by Item Category")
                    if not category_sales.empty:
                        plot_category_bar_chart(category_sales)
                    else:
                        st.warning("Not enough data for category-level chart.")

                with col2:
                    st.write("### Sales Over Time")
                    if not sales_over_time.empty:
                        plot_sales_over_time(sales_over_time)
                    else:
                        st.warning("Not enough data for time-series chart.")

                st.write("### Crafter Performance (Bubble Chart)")
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
