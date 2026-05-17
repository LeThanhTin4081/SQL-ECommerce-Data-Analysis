"""
Customers and Operations page.
Phân tích nhân khẩu học khách hàng, VIP, vận hành và thanh toán.
Tương ứng SQL Query #4, #5, #6, #9.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_orders, load_customers
from utils.styles import inject_css, kpi_card, section_header, COLORS, CHART_COLORS
from utils.charts import (
    gender_donut,
    device_donut,
    login_donut,
    payment_donut,
    payment_bar,
    shipping_cost_bar,
    aging_histogram,
)


st.set_page_config(
    page_title="Customers & Ops | E-Commerce 2018",
    page_icon="👤",
    layout="wide",
)

inject_css()

df = load_orders()
df_customers = load_customers()


# Sidebar: bộ lọc dữ liệu
with st.sidebar:
    st.markdown(f"""
    <div class="custom-sidebar-header">
        <div style="font-size:1.4rem;margin-bottom:4px;">👤</div>
        <div style="
            font-size:1.1rem;font-weight:700;
            background:linear-gradient(135deg, {COLORS['primary']}, {COLORS['accent']});
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            background-clip:text;
        ">Customers & Ops</div>
        <div style="font-size:0.75rem;color:{COLORS['muted']};margin-top:2px;">Nhân khẩu học & vận hành</div>
    </div>
    """, unsafe_allow_html=True)

    gender_filter = st.radio(
        "Giới tính",
        ["Tất cả", "Male", "Female"],
        key="cust_gender",
    )

    device_filter = st.radio(
        "Thiết bị",
        ["Tất cả", "Web", "Mobile"],
        key="cust_device",
    )

    priority_options = ["Tất cả"] + sorted(df["Order_Priority"].dropna().unique().tolist())
    priority_filter = st.selectbox("Mức ưu tiên đơn hàng", priority_options, key="cust_priority")

# Áp dụng filter
df_filtered = df.copy()
if gender_filter != "Tất cả":
    df_filtered = df_filtered[df_filtered["Gender"] == gender_filter]
if device_filter != "Tất cả":
    df_filtered = df_filtered[df_filtered["Device_Type"] == device_filter]
if priority_filter != "Tất cả":
    df_filtered = df_filtered[df_filtered["Order_Priority"] == priority_filter]


# Header trang
st.markdown(f"""
<div style="padding: 10px 0 5px 0;">
    <h2 style="
        font-weight: 700;
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['accent']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2px;
    ">👤 Customers & Operations</h2>
    <p style="color:{COLORS['muted']};font-size:0.9rem;margin:0;">
        Phân tích {len(df_filtered):,} đơn hàng | {df_filtered['Customer_Id'].nunique():,} khách hàng
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("")


# KPI cards
unique_customers = df_filtered["Customer_Id"].nunique()
male_pct = (df_filtered[df_filtered["Gender"] == "Male"].shape[0] / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
top_payment_method = df_filtered["Payment_Method"].mode().iloc[0] if len(df_filtered) > 0 else "N/A"
avg_aging = df_filtered["Aging"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(kpi_card(
        "Khách hàng", f"{unique_customers:,}",
        "👥", COLORS["primary"],
    ), unsafe_allow_html=True)

with col2:
    st.markdown(kpi_card(
        "Tỷ lệ Nam", f"{male_pct:.0f}%",
        "👨", COLORS["accent"],
    ), unsafe_allow_html=True)

with col3:
    st.markdown(kpi_card(
        "PT thanh toán #1", top_payment_method,
        "💳", COLORS["success"],
    ), unsafe_allow_html=True)

with col4:
    aging_color = COLORS["danger"] if avg_aging > 5 else COLORS["success"]
    st.markdown(kpi_card(
        "Aging TB", f"{avg_aging:.1f} ngày",
        "⏱", aging_color,
    ), unsafe_allow_html=True)

st.markdown("")


# Phân tích nhân khẩu học khách hàng
st.markdown(section_header("nhân khẩu học khách hàng"), unsafe_allow_html=True)

col_gender, col_device, col_login = st.columns(3)

with col_gender:
    st.plotly_chart(gender_donut(df_filtered, height=350), width="stretch")

with col_device:
    st.plotly_chart(device_donut(df_filtered, height=350), width="stretch")

with col_login:
    st.plotly_chart(login_donut(df_filtered, height=350), width="stretch")


# Bảng Top 10 khách hàng VIP (Query #9)
st.markdown(section_header("top 10 khách hàng vip (chi tiêu cao nhất)"), unsafe_allow_html=True)

vip_customers = (
    df_filtered.groupby(["Customer_Id", "Gender"])
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order_Id", "count"),
        Avg_Aging=("Aging", "mean"),
    )
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
    .head(10)
    .reset_index(drop=True)
)
vip_customers.index += 1
vip_customers.index.name = "Rank"

# Hiển thị bảng VIP và insight
col_table, col_insight = st.columns([3, 2])

with col_table:
    display_vip = vip_customers.copy()
    display_vip["Total_Sales"] = display_vip["Total_Sales"].apply(lambda x: f"${x:,.0f}")
    display_vip["Total_Profit"] = display_vip["Total_Profit"].apply(lambda x: f"${x:,.0f}")
    display_vip["Avg_Aging"] = display_vip["Avg_Aging"].apply(lambda x: f"{x:.1f}")
    display_vip.columns = ["Customer ID", "Giới tính", "Tổng DT", "Tổng LN", "Số đơn", "Aging TB"]

    st.dataframe(display_vip, width="stretch", height=400)

with col_insight:
    # Tính tỉ lệ giới tính trong top VIP
    vip_male_count = vip_customers[vip_customers["Gender"] == "Male"].shape[0]
    vip_female_count = 10 - vip_male_count
    vip_avg_sales = vip_customers["Total_Sales"].mean()

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(118,75,162,0.15), rgba(102,126,234,0.1));
        border: 1px solid rgba(118,75,162,0.2);
        border-radius: 16px;
        padding: 24px;
        margin-top: 8px;
    ">
        <h4 style="color:{COLORS['text']};margin-top:0;">🔍 Key Insight</h4>
        <p style="color:{COLORS['muted']};font-size:0.9rem;line-height:1.7;">
            Top 10 khách hàng VIP có chi tiêu trung bình
            <span style="color:{COLORS['accent']};font-weight:700;">${vip_avg_sales:,.0f}</span>.
        </p>
        <p style="color:{COLORS['muted']};font-size:0.9rem;line-height:1.7;">
            Phân bố giới tính:
            <span style="color:{COLORS['primary']};font-weight:700;">{vip_male_count} Nam</span> /
            <span style="color:{COLORS['danger']};font-weight:700;">{vip_female_count} Nữ</span>
        </p>
        <p style="color:{COLORS['muted']};font-size:0.85rem;line-height:1.7;margin-bottom:0;">
            💡 Đây là cơ sở để triển khai chương trình khách hàng thân thiết VIP
            và các chiến dịch marketing nhắm mục tiêu theo giới tính.
        </p>
    </div>
    """, unsafe_allow_html=True)


# Phân tích vận hành và logistics
st.markdown(section_header("vận hành & logistics"), unsafe_allow_html=True)

col_aging, col_shipping = st.columns([1, 1])

with col_aging:
    st.plotly_chart(aging_histogram(df_filtered, height=400), width="stretch")

with col_shipping:
    st.plotly_chart(shipping_cost_bar(df_filtered, height=400), width="stretch")


# Phân tích phương thức thanh toán (Query #6)
st.markdown(section_header("phân tích phương thức thanh toán"), unsafe_allow_html=True)

col_pay_donut, col_pay_bar = st.columns([1, 1])

with col_pay_donut:
    st.plotly_chart(payment_donut(df_filtered, height=400), width="stretch")

with col_pay_bar:
    st.plotly_chart(payment_bar(df_filtered, height=400), width="stretch")

st.markdown("<br>", unsafe_allow_html=True)
