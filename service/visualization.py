import matplotlib.pyplot as plt
import matplotlib.cm as cm
import streamlit as st

def plot_donut_chart(account_total_cost):
    """
    Plot and display a donut chart for account totals.
    """
    cmap = cm.get_cmap('terrain', len(account_total_cost))
    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        account_total_cost,
        autopct=lambda pct: f"${pct / 100. * sum(account_total_cost):.2f}",
        startangle=90,
        wedgeprops=dict(width=0.3),
        colors=cmap(range(len(account_total_cost))),
    )
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)
    ax.legend(account_total_cost.index, title="Account Numbers", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.title("Total Cost per Account Number")
    st.pyplot(fig)

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
