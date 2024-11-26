import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

# Set up the app title and layout
st.set_page_config(page_title="Order Management App", page_icon="📦", layout="wide")

# Simulate a database (in-memory for now)
if "orders" not in st.session_state:
    st.session_state["orders"] = pd.DataFrame(columns=["Order ID", "Customer Name", "Product", "Quantity", "Price", "Status", "Date"])

# Utility functions
def add_order(order_id, customer_name, product, quantity, price):
    new_order = {
        "Order ID": order_id,
        "Customer Name": customer_name,
        "Product": product,
        "Quantity": quantity,
        "Price": price,
        "Status": "Pending",
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state["orders"] = pd.concat([st.session_state["orders"], pd.DataFrame([new_order])], ignore_index=True)

def update_status(order_id, new_status):
    orders = st.session_state["orders"]
    orders.loc[orders["Order ID"] == order_id, "Status"] = new_status
    st.session_state["orders"] = orders

# Sidebar menu
st.sidebar.title("📋 Order Management")
menu = st.sidebar.radio("Menu", ["Dashboard", "Create Order", "Manage Orders", "Analytics"])

# Dashboard View
if menu == "Dashboard":
    st.title("📊 Order Management Dashboard")
    st.write("Welcome to the Order Management App! Use the sidebar to navigate.")
    
    total_orders = len(st.session_state["orders"])
    pending_orders = len(st.session_state["orders"][st.session_state["orders"]["Status"] == "Pending"])
    completed_orders = len(st.session_state["orders"][st.session_state["orders"]["Status"] == "Completed"])

    # Display summary cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", total_orders)
    col2.metric("Pending Orders", pending_orders)
    col3.metric("Completed Orders", completed_orders)

# Create Order View
elif menu == "Create Order":
    st.title("📝 Create a New Order")
    with st.form("Create Order Form"):
        order_id = st.text_input("Order ID", help="Unique identifier for the order")
        customer_name = st.text_input("Customer Name", help="Enter the name of the customer")
        product = st.text_input("Product", help="Product being ordered")
        quantity = st.number_input("Quantity", min_value=1, help="Number of units")
        price = st.number_input("Price", min_value=0.0, format="%.2f", help="Price per unit")
        submitted = st.form_submit_button("Add Order")
        
        if submitted:
            if not order_id or not customer_name or not product:
                st.error("Please fill out all required fields!")
            else:
                add_order(order_id, customer_name, product, quantity, price)
                st.success(f"Order {order_id} added successfully!")

# Manage Orders View
elif menu == "Manage Orders":
    st.title("🛠️ Manage Orders")
    orders = st.session_state["orders"]

    if not orders.empty:
        st.dataframe(orders)

        with st.expander("Update Order Status"):
            order_id = st.selectbox("Select Order ID", options=orders["Order ID"].unique())
            new_status = st.selectbox("New Status", ["Pending", "Completed", "Canceled"])
            if st.button("Update Status"):
                update_status(order_id, new_status)
                st.success(f"Order {order_id} status updated to {new_status}!")
    else:
        st.info("No orders available to manage.")

# Analytics View
elif menu == "Analytics":
    st.title("📈 Order Analytics")
    orders = st.session_state["orders"]

    if not orders.empty:
        # Summary statistics
        total_revenue = orders["Price"].sum()
        avg_order_value = orders["Price"].mean()
        completed_orders = len(orders[orders["Status"] == "Completed"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${total_revenue:,.2f}")
        col2.metric("Avg Order Value", f"${avg_order_value:,.2f}")
        col3.metric("Completed Orders", completed_orders)

        # Orders by Status Chart
        status_counts = orders["Status"].value_counts()
        st.bar_chart(status_counts)
    else:
        st.info("No orders to analyze.")
