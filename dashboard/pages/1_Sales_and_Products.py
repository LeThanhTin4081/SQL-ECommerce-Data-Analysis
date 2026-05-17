"""
Sales and Products page.
Phân tích xu hướng doanh thu, xếp hạng sản phẩm, so sánh quý và heatmap.
Tương ứng SQL Query #2, #3, #7, #8, #10.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_orders
from utils.styles import inject_css, kpi_card, section_header, COLORS, CHART_COLORS
from utils.charts import (
    monthly_bar_line_combo,
    running_total_area,
    daily_sales_heatmap,
    top_products_bar,
    quarterly_comparison_bar,
)


st.set_page_config(
    page_title="Sales & Products | E-Commerce 2018",
    page_icon="📊",
    layout="wide",
)

inject_css()

df = load_orders()


# Sidebar: bộ lọc dữ liệu
with st.sidebar:
    st.markdown(f"""
    <div class="custom-sidebar-header">
        <div style="font-size:1.4rem;margin-bottom:4px;">📊</div>
        <div style="
            font-size:1.1rem;font-weight:700;
            background:linear-gradient(135deg, {COLORS['primary']}, {COLORS['accent']});
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            background-clip:text;
        ">Sales & Products</div>
        <div style="font-size:0.75rem;color:{COLORS['muted']};margin-top:2px;">Phân tích doanh thu & sản phẩm</div>
    </div>
    """, unsafe_allow_html=True)

    month_range = st.slider(
        "Khoảng tháng",
        min_value=1, max_value=12,
        value=(1, 12),
        format="Tháng %d",
        key="sales_month",
    )

    categories = ["Tất cả"] + sorted(df["Product_Category"].unique().tolist())
    selected_cat = st.selectbox("Danh mục sản phẩm", categories, key="sales_cat")

    top_n = st.slider("Số sản phẩm Top N", min_value=5, max_value=30, value=10, key="sales_topn")

# Áp dụng filter
df_filtered = df[(df["Month"] >= month_range[0]) & (df["Month"] <= month_range[1])]
if selected_cat != "Tất cả":
    df_filtered = df_filtered[df_filtered["Product_Category"] == selected_cat]


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
    ">📊 Sales & Products Analysis</h2>
    <p style="color:{COLORS['muted']};font-size:0.9rem;margin:0;">Phân tích {len(df_filtered):,} đơn hàng (Tháng {month_range[0]} – {month_range[1]}, 2018) {f'| Danh mục: {selected_cat}' if selected_cat != 'Tất cả' else ''}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("")


# KPI cards cho trang Sales
total_sales = df_filtered["Sales"].sum()
total_profit = df_filtered["Profit"].sum()
total_quantity = df_filtered["Quantity"].sum()
avg_discount = df_filtered["Discount"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(kpi_card(
        "Doanh thu", f"${total_sales:,.0f}",
        "💰", COLORS["primary"],
    ), unsafe_allow_html=True)

with col2:
    st.markdown(kpi_card(
        "Lợi nhuận", f"${total_profit:,.0f}",
        "📈", COLORS["success"],
    ), unsafe_allow_html=True)

with col3:
    st.markdown(kpi_card(
        "SL bán ra", f"{total_quantity:,}",
        "📦", COLORS["accent"],
    ), unsafe_allow_html=True)

with col4:
    st.markdown(kpi_card(
        "Giảm giá TB", f"{avg_discount:.1%}",
        "🏷", COLORS["warning"],
    ), unsafe_allow_html=True)

st.markdown("")


# Biểu đồ combo: Bar doanh thu + Line lợi nhuận theo tháng (Query #2)
st.markdown(section_header("xu hướng doanh thu & lợi nhuận theo tháng"), unsafe_allow_html=True)
st.plotly_chart(monthly_bar_line_combo(df_filtered, height=420), width="stretch")


# Doanh thu lũy kế và Heatmap doanh thu
st.markdown(section_header("doanh thu lũy kế & phân bố theo ngày"), unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1])

with col_left:
    st.plotly_chart(running_total_area(df_filtered, height=380), width="stretch")

with col_right:
    st.plotly_chart(daily_sales_heatmap(df_filtered, height=380), width="stretch")


# Bảng xếp hạng sản phẩm (Query #3, #7)
st.markdown(section_header("xếp hạng sản phẩm"), unsafe_allow_html=True)
st.plotly_chart(top_products_bar(df_filtered, top_n=top_n, height=480), width="stretch")


# Bảng dữ liệu chi tiết Top N sản phẩm kèm Rank
st.markdown(section_header("bảng chi tiết xếp hạng sản phẩm"), unsafe_allow_html=True)

product_ranking = (
    df_filtered.groupby(["Product", "Product_Category"])
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Units=("Quantity", "sum"),
        Avg_Discount=("Discount", "mean"),
    )
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
    .head(top_n)
    .reset_index(drop=True)
)
product_ranking.index += 1
product_ranking.index.name = "Rank"

# Format hiển thị
display_df = product_ranking.copy()
display_df["Total_Sales"] = display_df["Total_Sales"].apply(lambda x: f"${x:,.0f}")
display_df["Total_Profit"] = display_df["Total_Profit"].apply(lambda x: f"${x:,.0f}")
display_df["Total_Units"] = display_df["Total_Units"].apply(lambda x: f"{x:,}")
display_df["Avg_Discount"] = display_df["Avg_Discount"].apply(lambda x: f"{x:.1%}")
display_df.columns = ["Sản phẩm", "Danh mục", "Doanh thu", "Lợi nhuận", "SL bán", "Giảm giá TB"]

st.dataframe(display_df, width="stretch", height=400)


# So sánh doanh thu và lợi nhuận theo quý
st.markdown(section_header("so sánh theo quý"), unsafe_allow_html=True)
st.plotly_chart(quarterly_comparison_bar(df_filtered, height=380), width="stretch")

st.markdown("<br>", unsafe_allow_html=True)
