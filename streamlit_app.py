import streamlit as st
from service.ingestion import process_pdf
from service.visualization import plot_donut_chart, plot_bar_chart


def main():
    # Set up the Streamlit app configuration
    st.set_page_config(
        page_title="Brooklyn Women's Exchange",
        page_icon="images/icon.png",
        layout="wide",
    )

    # Add a custom background color using CSS
    set_background_color()

    # Display the header image
    st.image("images/new-ban.png", use_container_width=True)

    # App title and description
    st.title("PDF Uploader and Analysis Tool")
    st.write("Upload a PDF file to extract, process, and visualize the data.")

    # File uploader
    uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded file locally for processing
        with open("uploaded_file.pdf", "wb") as f:
            f.write(uploaded_file.read())

        try:
            # Process the PDF file using the ingestion module
            processed_df, account_total_cost, item_sales = process_pdf("uploaded_file.pdf")

            # Display success message
            st.success("PDF processed successfully!")

            # Display the processed DataFrame
            st.write("### Processed Data:")
            st.dataframe(processed_df)

            # Display the donut chart
            st.write("### Total Cost per Account Number")
            plot_donut_chart(account_total_cost)

            # Display the bar chart
            st.write("### Total Sales and Quantity Sold per Item Number")
            plot_bar_chart(item_sales)

        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")
    else:
        st.warning("Please upload a PDF file to proceed.")


def set_background_color():
    # Use Streamlit's ability to inject custom HTML/CSS
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #EFECEC; 
            background-color: #EFECEC; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
