"""
Executive Overview page.
Trang chính Dashboard, hiển thị báo cáo tổng hợp E-Commerce năm 2018.
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.data_loader import load_orders
from utils.styles import inject_css, kpi_card, section_header, COLORS
from utils.charts import monthly_trend_area, category_donut, top_products_bar


# Cấu hình trang
st.set_page_config(
    page_title="E-Commerce Dashboard 2018",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()


# Load dữ liệu
df = load_orders()


with st.sidebar:
    st.markdown(f"""
    <div class="custom-sidebar-header">
        <div style="font-size:1.4rem;margin-bottom:4px;">🛒</div>
        <div style="
            font-size:1.1rem;font-weight:700;
            background:linear-gradient(135deg, {COLORS['primary']}, {COLORS['accent']});
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            background-clip:text;
        ">E-Commerce Dashboard</div>
        <div style="font-size:0.75rem;color:{COLORS['muted']};margin-top:2px;">Annual Report 2018</div>
    </div>
    """, unsafe_allow_html=True)

    month_range = st.slider(
        "📅 Chọn khoảng tháng",
        min_value=1, max_value=12,
        value=(1, 12),
        format="Tháng %d",
    )

# Lọc dữ liệu theo khoảng tháng được chọn
df_filtered = df[(df["Month"] >= month_range[0]) & (df["Month"] <= month_range[1])]
filtered_count = len(df_filtered)

# Hiển thị thông tin giai đoạn dữ liệu (cập nhật theo filter)
with st.sidebar:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15));
        border: 1px solid rgba(102,126,234,0.2);
        border-radius: 12px;
        padding: 16px;
        margin-top: 12px;
    ">
        <div style="font-size:0.8rem;color:{COLORS['muted']};margin-bottom:8px;">📅 Giai đoạn dữ liệu</div>
        <div style="font-size:1rem;color:{COLORS['text']};font-weight:600;">Tháng {month_range[0]} – Tháng {month_range[1]}, 2018</div>
        <div style="font-size:0.75rem;color:{COLORS['muted']};margin-top:4px;">{filtered_count:,} đơn hàng</div>
    </div>
    """, unsafe_allow_html=True)


# Header trang
st.markdown(f"""
<div style="text-align: center; padding: 20px 0 10px 0;">
    <h1 style="
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['accent']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 4px;
    ">🛒 E-Commerce Annual Report 2018</h1>
    <p style="color:{COLORS['muted']};font-size:1rem;margin:0;">
        Báo cáo Tổng hợp Kinh doanh — Phân tích {filtered_count:,} đơn hàng
        (Tháng {month_range[0]} – Tháng {month_range[1]}, 2018)
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("")


# Tính toán các chỉ số KPI chính
total_revenue = df_filtered["Sales"].sum()
total_profit = df_filtered["Profit"].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_orders = len(df_filtered)
avg_aging = df_filtered["Aging"].mean()

# Hiển thị 5 KPI cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(kpi_card(
        "Tổng Doanh thu", f"${total_revenue/1_000_000:.2f}M",
        "💰", COLORS["primary"],
    ), unsafe_allow_html=True)

with col2:
    st.markdown(kpi_card(
        "Tổng Lợi nhuận", f"${total_profit/1_000_000:.2f}M",
        "📈", COLORS["success"],
    ), unsafe_allow_html=True)

with col3:
    st.markdown(kpi_card(
        "Biên Lợi nhuận", f"{profit_margin:.1f}%",
        "📊", COLORS["accent"],
    ), unsafe_allow_html=True)

with col4:
    st.markdown(kpi_card(
        "Tổng Đơn hàng", f"{total_orders:,}",
        "📦", COLORS["warning"],
    ), unsafe_allow_html=True)

with col5:
    aging_color = COLORS["danger"] if avg_aging > 5 else COLORS["success"]
    st.markdown(kpi_card(
        "TB Xử lý Đơn", f"{avg_aging:.1f} ngày",
        "⏱", aging_color,
    ), unsafe_allow_html=True)

st.markdown("")


# Biểu đồ xu hướng doanh thu và lợi nhuận theo tháng
st.markdown(section_header("📈 xu hướng doanh thu & lợi nhuận theo tháng"), unsafe_allow_html=True)
st.plotly_chart(monthly_trend_area(df_filtered, height=420), width="stretch")


# Phân bổ danh mục và Top 5 sản phẩm
st.markdown(section_header("🏆 phân bổ doanh thu & sản phẩm nổi bật"), unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1])

with col_left:
    st.plotly_chart(category_donut(df_filtered, height=420), width="stretch")

with col_right:
    st.plotly_chart(top_products_bar(df_filtered, top_n=5, height=420), width="stretch")


# Tính toán các điểm nổi bật chính
st.markdown(section_header("⚡ điểm nổi bật chính"), unsafe_allow_html=True)

monthly_sales = df_filtered.groupby("Month")["Sales"].sum()
peak_month_num = monthly_sales.idxmax()
month_names_vn = {1:"Tháng 1",2:"Tháng 2",3:"Tháng 3",4:"Tháng 4",5:"Tháng 5",6:"Tháng 6",
                  7:"Tháng 7",8:"Tháng 8",9:"Tháng 9",10:"Tháng 10",11:"Tháng 11",12:"Tháng 12"}
peak_month = month_names_vn.get(peak_month_num, f"T{peak_month_num}")
peak_revenue = monthly_sales.max()

top_product = df_filtered.groupby("Product")["Sales"].sum().idxmax()
top_payment = df_filtered.groupby("Payment_Method")["Sales"].sum().idxmax()
top_payment_pct = (
    df_filtered.groupby("Payment_Method")["Sales"].sum().max()
    / total_revenue * 100
) if total_revenue > 0 else 0

# Hiển thị 4 highlight cards
h1, h2, h3, h4 = st.columns(4)

with h1:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(102,126,234,0.12), rgba(0,210,255,0.08));
        border: 1px solid rgba(102,126,234,0.15);
        border-radius: 14px; padding: 18px; text-align: center;
    ">
        <div style="font-size:1.4rem;">📅</div>
        <div style="font-size:0.9rem;font-weight:700;color:{COLORS['text']};margin:6px 0 2px 0;">{peak_month}</div>
        <div style="font-size:0.7rem;color:{COLORS['muted']};">Tháng đạt đỉnh (${peak_revenue:,.0f})</div>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(0,227,150,0.12), rgba(0,210,255,0.08));
        border: 1px solid rgba(0,227,150,0.15);
        border-radius: 14px; padding: 18px; text-align: center;
    ">
        <div style="font-size:1.4rem;">🏆</div>
        <div style="font-size:0.9rem;font-weight:700;color:{COLORS['text']};margin:6px 0 2px 0;">{top_product}</div>
        <div style="font-size:0.7rem;color:{COLORS['muted']};">Sản phẩm #1 doanh thu</div>
    </div>
    """, unsafe_allow_html=True)

with h3:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(252,92,125,0.12), rgba(246,173,85,0.08));
        border: 1px solid rgba(252,92,125,0.15);
        border-radius: 14px; padding: 18px; text-align: center;
    ">
        <div style="font-size:1.4rem;">💳</div>
        <div style="font-size:0.9rem;font-weight:700;color:{COLORS['text']};margin:6px 0 2px 0;">{top_payment}</div>
        <div style="font-size:0.7rem;color:{COLORS['muted']};">PT thanh toán #1 ({top_payment_pct:.0f}% DT)</div>
    </div>
    """, unsafe_allow_html=True)

with h4:
    unique_customers = df_filtered["Customer_Id"].nunique()
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(118,75,162,0.12), rgba(102,126,234,0.08));
        border: 1px solid rgba(118,75,162,0.15);
        border-radius: 14px; padding: 18px; text-align: center;
    ">
        <div style="font-size:1.4rem;">👥</div>
        <div style="font-size:0.9rem;font-weight:700;color:{COLORS['text']};margin:6px 0 2px 0;">{unique_customers:,}</div>
        <div style="font-size:0.7rem;color:{COLORS['muted']};">Khách hàng duy nhất</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
