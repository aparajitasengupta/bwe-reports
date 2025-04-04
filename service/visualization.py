import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.dates as mdates
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.io as pio
import io


def categorize_account(account_number):
    try:
        num = int(account_number)
    except:
        return "Unknown"

    if num >= 1000:
        return "Wholesale"
    elif 100 <= num < 200:
        return "Food"
    elif 200 <= num < 300:
        return "Stationery/Jewelry/Accessories"
    elif 300 <= num < 400:
        return "Home/Linens"
    elif 400 <= num < 500:
        return "Toys"
    elif 500 <= num < 600:
        return "Clothing/Children’s"
    elif 600 <= num < 700:
        return "Sweaters/Knits"
    elif 700 <= num < 800:
        return "Holiday"
    elif 800 <= num < 900:
        return "Wood Items/Toys"
    elif 900 <= num < 1000:
        return "Former Consignor Items"
    else:
        return "Unknown"


def plot_donut_chart(account_total_cost):
    df = account_total_cost.reset_index()
    df.columns = ["Account", "Total_Cost"]
    df["Category"] = df["Account"].apply(categorize_account)

    category_summary = df.groupby("Category")["Total_Cost"].sum().reset_index()

    fig = px.pie(
        category_summary,
        values="Total_Cost",
        names="Category",
        hole=0.5,
        title="Total Cost by Category"
    )

    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="Category: %{label}<br>Total Cost: $%{value:.2f}<extra></extra>"
    )

    fig.update_layout(width=600, height=500)
    st.plotly_chart(fig, use_container_width=True)

    # PNG Download
    buf = io.BytesIO()
    pio.write_image(fig, buf, format='png')
    st.download_button(
        label="Download Chart as PNG",
        data=buf.getvalue(),
        file_name="donut_chart.png",
        mime="image/png"
    )


def plot_bar_chart(item_sales):
    # Sort by total cost for height, but color by quantity sold
    item_sales = item_sales.sort_values(by="Total_Cost", ascending=False)

    fig = px.bar(
        item_sales,
        x="Item_Name",
        y="Total_Cost",
        color="Count",
        color_continuous_scale="turbo",
        hover_data={
            "Item_Name": True,
            "Total_Cost": ":$.2f",
            "Count": True
        },
        labels={
            "Item_Name": "Item",
            "Total_Cost": "Total Item Cost ($)",
            "Count": "Quantity Sold"
        },
        title="Total Item Cost per Item (Colored by Quantity Sold)"
    )

    fig.update_layout(
        xaxis_tickangle=45,
        xaxis_tickfont_size=8,
        height=500,
        margin=dict(t=50, b=150),
    )

    st.plotly_chart(fig, use_container_width=True)

    # PNG download
    buf = io.BytesIO()
    pio.write_image(fig, buf, format="png")
    st.download_button(
        label="Download Chart as PNG",
        data=buf.getvalue(),
        file_name="item_sales_chart.png",
        mime="image/png"
    )



def plot_sales_over_time(sales_over_time):
    fig = px.line(
        sales_over_time.reset_index(),
        x="Date Sold",
        y="Price",
        markers=True,
        title="Total Sales Over Time",
        labels={
            "Date Sold": "Date",
            "Price": "Total Sales ($)"
        },
        template="plotly_white"
    )

    fig.update_traces(
        hovertemplate="<b>Date:</b> %{x|%b %d, %Y}<br><b>Total Sales:</b> $%{y:.2f}",
        line=dict(color="steelblue", width=2),
        marker=dict(size=7)
    )

    fig.update_layout(
        height=500,
        xaxis=dict(tickformat="%b %d", tickangle=45),
        yaxis=dict(title="Total Sales ($)"),
        margin=dict(t=50, b=80),
    )

    st.plotly_chart(fig, use_container_width=True)

    # PNG Download
    buf = io.BytesIO()
    pio.write_image(fig, buf, format="png")
    st.download_button(
        label="Download Chart as PNG",
        data=buf.getvalue(),
        file_name="sales_over_time_chart.png",
        mime="image/png"
    )


def plot_crafter_bubble_chart(processed_df, top_n=20):
    crafter_stats = (
        processed_df.groupby("Crafter Name")
        .agg(
            Total_Sales=("Price", "sum"),
            Quantity_Sold=("Item Name", "count"),
            Avg_Price=("Price", "mean")
        )
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
        .head(top_n)
    )

    fig = px.scatter(
        crafter_stats,
        x="Quantity_Sold",
        y="Total_Sales",
        size="Avg_Price",
        text="Crafter Name",
        color="Avg_Price",
        color_continuous_scale=px.colors.sequential.Viridis,
        hover_data={
            "Crafter Name": True,
            "Total_Sales": ":$.2f",
            "Quantity_Sold": True,
            "Avg_Price": ":$.2f"
        },
        title="Crafter Performance",
        labels={
            "Quantity_Sold": "Quantity Sold",
            "Total_Sales": "Total Sales ($)",
            "Avg_Price": "Avg Price ($)"
        }
    )

    fig.update_traces(textposition="top center")
    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    buf = io.BytesIO()
    pio.write_image(fig, buf, format="png")

    st.download_button(
        label="Download Chart as PNG",
        data=buf.getvalue(),
        file_name="crafter_bubble_chart.png",
        mime="image/png"
    )
