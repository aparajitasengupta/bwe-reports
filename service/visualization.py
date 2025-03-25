import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.dates as mdates
import streamlit as st
import plotly.express as px
import plotly.io as pio
import io



def plot_donut_chart(account_total_cost):
    fig = px.pie(
        values=account_total_cost.values,
        names=account_total_cost.index.astype(str),
        hole=0.5,
        title="Total Cost per Account Number"
    )

    fig.update_traces(
        textinfo="none",
        hovertemplate="Account Number: %{label}<br>Total Cost: $%{value:.2f}<extra></extra>"
    )

    fig.update_layout(width=600, height=475)
    st.plotly_chart(fig, use_container_width=True)
    buf = io.BytesIO()
    pio.write_image(fig, buf, format='png')
    st.download_button(
        label="Download Chart as PNG",
        data=buf.getvalue(),
        file_name="donut_chart.png",
        mime="image/png"
    )



def plot_bar_chart(item_sales):
    """
    Plot and display a bar chart for item sales.
    """
    cmap = cm.summer
    fig, ax = plt.subplots(figsize=(10, 6))
    norm = plt.Normalize(item_sales['Total Cost'].min(), item_sales['Total Cost'].max())
    bars = ax.bar(item_sales['Item Number'], item_sales['Total Cost'], color=cmap(norm(item_sales['Total Cost'])))
    for bar, count in zip(bars, item_sales['Count']):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, str(count), ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.set_title('Total Sales and Quantity Sold per Item Number', fontsize=14)
    ax.set_xlabel('Item Number', fontsize=12)
    ax.set_ylabel('Total Sales ($)', fontsize=12)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button(
        label="Download Chart as PNG",
        data=buf.getvalue(),
        file_name="item_sales_chart.png",
        mime="image/png"
    )


def plot_category_bar_chart(category_sales):
    fig, ax1 = plt.subplots(figsize=(10, 12))
    ax2 = ax1.twiny()
    y = range(len(category_sales))
    bar_height = 0.4

    # 🎨 Colors
    cost_color = "#FF6B6B"
    count_color = "lightgreen"

    ax1.barh([i - bar_height / 2 for i in y], category_sales["Total Cost"], height=bar_height,
             label="Total Cost ($)", color=cost_color)
    ax2.barh([i + bar_height / 2 for i in y], category_sales["Count"], height=bar_height,
             label="Count", color=count_color)

    ax1.set_ylabel("Item Name")
    ax1.set_xlabel("Total Sales ($)", color=cost_color)
    ax2.set_xlabel("Quantity Sold", color=count_color)

    ax1.set_yticks(y)
    ax1.set_yticklabels(category_sales["Item Name"])

    fig.legend(loc="upper right")
    plt.title("Sales and Count by Item Category")
    st.pyplot(fig, use_container_width=True)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button(
        label="Download Chart as PNG",
        data=buf.getvalue(),
        file_name="category_sales_chart.png",
        mime="image/png"
    )


def plot_sales_over_time(sales_over_time):
    fig, ax = plt.subplots(figsize=(10, 10.5))
    ax.plot(sales_over_time.values, sales_over_time.index, marker="o")

    ax.set_title("Total Sales Over Time", fontsize=14)
    ax.set_xlabel("Total Sales ($)")
    ax.set_ylabel("Date")
    ax.grid(True)

    # Determine granularity of data (monthly vs daily)
    date_range = sales_over_time.index.max() - sales_over_time.index.min()
    if date_range.days > 60:
        ax.yaxis.set_major_locator(mdates.MonthLocator(interval=1))
        ax.yaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    else:
        ax.yaxis.set_major_locator(mdates.DayLocator(interval=7))  # every 7 days
        ax.yaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    fig.autofmt_xdate()  # Rotate if needed
    st.pyplot(fig, use_container_width=True)

    # Download button
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    st.download_button(
        label="Download Chart as PNG",
        data=buf.getvalue(),
        file_name="sales_over_time_chart.png",
        mime="image/png"
    )

def plot_crafter_bubble_chart(processed_df, top_n=20):
    # Aggregate stats
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
        color_continuous_scale=px.colors.sequential.Reds,
        hover_data={
            "Crafter Name": True,
            "Total_Sales": ":$.2f",
            "Quantity_Sold": True,
            "Avg_Price": ":$.2f"
        },
        title="Crafter Performance Bubble Chart",
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
