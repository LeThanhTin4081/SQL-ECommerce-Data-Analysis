"""
Data Loader module.
Load & cache CSV files cho Dashboard.
Sử dụng @st.cache_data để chỉ load 1 lần, tái sử dụng across pages.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Đường dẫn tới thư mục data cleaned
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "cleaned"


@st.cache_data(show_spinner="🔄 Đang tải dữ liệu...")
def load_orders() -> pd.DataFrame:
    """Load bảng Orders (Fact table), khoảng 51,290 rows."""
    df = pd.read_csv(DATA_DIR / "Orders.csv")

    # Ép kiểu chuẩn cho các cột số và ngày
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Discount"] = pd.to_numeric(df["Discount"], errors="coerce")
    df["Shipping_Cost"] = pd.to_numeric(df["Shipping_Cost"], errors="coerce")
    df["Aging"] = pd.to_numeric(df["Aging"], errors="coerce")

    # Tạo các cột phụ trợ phục vụ filter và group by
    df["Month"] = df["Order_Date"].dt.month
    df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
    df["Year_Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Quarter"] = df["Order_Date"].dt.quarter
    df["Day_of_Week"] = df["Order_Date"].dt.day_name()

    return df


@st.cache_data(show_spinner="🔄 Đang tải dữ liệu khách hàng...")
def load_customers() -> pd.DataFrame:
    """Load bảng Customers (Dimension), khoảng 39K rows."""
    return pd.read_csv(DATA_DIR / "Customers.csv")


@st.cache_data(show_spinner="🔄 Đang tải dữ liệu sản phẩm...")
def load_products() -> pd.DataFrame:
    """Load bảng Products (Dimension), khoảng 30 rows."""
    return pd.read_csv(DATA_DIR / "Products.csv")


@st.cache_data(show_spinner="🔄 Đang tải danh mục...")
def load_categories() -> pd.DataFrame:
    """Load bảng Categories (Dimension), 5 rows."""
    return pd.read_csv(DATA_DIR / "Categories.csv")


def load_all_data():
    """Load toàn bộ 4 bảng, trả về tuple (orders, customers, products, categories)."""
    return load_orders(), load_customers(), load_products(), load_categories()
