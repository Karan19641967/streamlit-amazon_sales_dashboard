import streamlit as st
import pandas as pd
import plotly.express as px

# --- Streamlit Config ---
st.set_page_config(page_title="Amazon Sales Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Amazon Sale Report Data cleaned.csv", parse_dates=["Date"])
    df["Month"] = df["Date"].dt.to_period("M")
    return df

st.title("📦 Amazon Sales Performance Dashboard")
df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filter Data")
states = st.sidebar.multiselect("Select State(s):", options=df["State"].unique(), default=df["State"].unique())
categories = st.sidebar.multiselect("Select Category(ies):", options=df["Category"].unique(), default=df["Category"].unique())

df_filtered = df[(df["State"].isin(states)) & (df["Category"].isin(categories))]

# --- KPIs ---
total_sales = df_filtered["Sale Amount"].sum()
total_orders = len(df_filtered)
top_category = df_filtered["Category"].mode()[0] if not df_filtered.empty else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("🧾 Total Orders", total_orders)
col3.metric("🏆 Top Category", top_category)

st.markdown("---")

# --- Charts ---
col4, col5 = st.columns(2)

# Bar Chart: Sales by Category
category_sales = df_filtered.groupby("Category")["Sale Amount"].sum().sort_values().reset_index()
fig_bar = px.bar(category_sales, x="Sale Amount", y="Category", orientation="h", title="Sales by Category")
col4.plotly_chart(fig_bar, use_container_width=True)

# Line Chart: Monthly Sales
monthly_sales = df_filtered.groupby("Month")["Sale Amount"].sum().reset_index()
fig_line = px.line(monthly_sales, x="Month", y="Sale Amount", markers=True, title="Monthly Sales Trend")
col5.plotly_chart(fig_line, use_container_width=True)

# --- Download ---
st.download_button("📥 Download Filtered Data", data=df_filtered.to_csv(index=False), file_name="filtered_sales.csv")

st.markdown("###### Made by Karan with ❤️", unsafe_allow_html=True)
