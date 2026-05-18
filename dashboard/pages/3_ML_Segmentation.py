"""
ML Segmentation page.
Hiển thị kết quả K-Means Clustering (RFM) từ notebook customer_segmentation.
Dữ liệu tĩnh (hardcoded) từ kết quả huấn luyện mô hình.
"""

import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.styles import inject_css, section_header, COLORS, CLUSTER_COLORS, CHART_COLORS
from utils.charts import rfm_radar


st.set_page_config(
    page_title="ML Segmentation | E-Commerce 2018",
    page_icon="🧠",
    layout="wide",
)

inject_css()


with st.sidebar:
    st.markdown(f"""
    <div class="custom-sidebar-header">
        <div style="font-size:1.4rem;margin-bottom:4px;">🧠</div>
        <div style="
            font-size:1.1rem;font-weight:700;
            background:linear-gradient(135deg, {COLORS['primary']}, {COLORS['accent']});
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            background-clip:text;
        ">ML Segmentation</div>
        <div style="font-size:0.75rem;color:{COLORS['muted']};margin-top:2px;">Customer Clustering</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(102,126,234,0.15), rgba(118,75,162,0.15));
        border: 1px solid rgba(102,126,234,0.2);
        border-radius: 12px;
        padding: 16px;
        margin-top: 12px;
    ">
        <div style="font-size:0.8rem;color:{COLORS['muted']};margin-bottom:8px;">💡 Lưu ý</div>
        <div style="font-size:0.85rem;color:{COLORS['text']};line-height:1.5;">
            Trang này hiển thị kết quả phân cụm Machine Learning (K-Means) đã được huấn luyện trên <b>toàn bộ tập dữ liệu</b>.
        </div>
        <div style="font-size:0.85rem;color:{COLORS['text']};line-height:1.5;margin-top:8px;">
            Bộ lọc thời gian <b>không</b> áp dụng tại đây để đảm bảo tính toàn vẹn của Model.
        </div>
    </div>
    """, unsafe_allow_html=True)


# Dữ liệu kết quả K-Means đã huấn luyện từ notebook
CLUSTER_INFO = {
    0: {
        "name": "Premium One-Time",
        "icon": "💎",
        "count": 12864,
        "pct": 33,
        "color": CLUSTER_COLORS[0],
        "monetary": 220,
        "frequency": 1.13,
        "recency": 158,
        "avg_discount": 0.29,
        "avg_profit": 120,
        "description": "Mua 1 lần, lợi nhuận cao ($120/đơn), sẵn sàng chi trả giá cao.",
        "strategy": "Gửi email/SMS nhắc nhở mua lại, cross-sell sản phẩm liên quan. "
                     "Biên lợi nhuận cao nhất, cần chiến lược chuyển đổi thành khách trung thành.",
    },
    1: {
        "name": "Low-Value",
        "icon": "📉",
        "count": 17135,
        "pct": 44,
        "color": CLUSTER_COLORS[1],
        "monetary": 102,
        "frequency": 1.08,
        "recency": 159,
        "avg_discount": 0.29,
        "avg_profit": 29,
        "description": "Nhóm đông nhất, chi tiêu thấp ($102), lợi nhuận thấp, nguy cơ rời bỏ cao.",
        "strategy": "Chiến dịch retargeting với voucher giảm giá để kích hoạt lại. "
                     "Cần đánh giá chi phí Marketing vs. giá trị mang lại (ROI).",
    },
    2: {
        "name": "VIP Loyal",
        "icon": "👑",
        "count": 8996,
        "pct": 23,
        "color": CLUSTER_COLORS[2],
        "monetary": 357,
        "frequency": 2.24,
        "recency": 92,
        "avg_discount": 0.32,
        "avg_profit": 84,
        "description": "Mua gần đây nhất (92 ngày), tần suất cao nhất (2.24 lần), "
                       "chi tiêu lớn nhất ($357), 79% là Nam giới.",
        "strategy": "Triển khai chương trình loyalty, ưu đãi độc quyền, early access sản phẩm mới. "
                     "Chủ yếu là Nam giới (79%), cần thiết kế chiến dịch phù hợp đối tượng.",
    },
}

TOTAL_CUSTOMERS = 38995
SILHOUETTE_SCORE = 0.315
K_VALUE = 3


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
    ">🧠 Customer Segmentation — K-Means Clustering</h2>
    <p style="color:{COLORS['muted']};font-size:0.9rem;margin:0;">
        Phân nhóm {TOTAL_CUSTOMERS:,} khách hàng bằng mô hình RFM + K-Means (K={K_VALUE})
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("")


# Thông tin mô hình: Methodology + Metrics
col_method, col_score, col_total = st.columns(3)

with col_method:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(26,31,46,0.95), rgba(14,17,23,0.85));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 20px; text-align: center;
        border-top: 3px solid {COLORS['primary']};
    ">
        <div style="font-size:1.4rem;margin-bottom:6px;">🔬</div>
        <div style="font-size:1.2rem;font-weight:700;color:{COLORS['text']};">RFM + K-Means</div>
        <div style="font-size:0.75rem;color:{COLORS['muted']};margin-top:4px;">
            StandardScaler + Elbow Method
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_score:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(26,31,46,0.95), rgba(14,17,23,0.85));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 20px; text-align: center;
        border-top: 3px solid {COLORS['accent']};
    ">
        <div style="font-size:1.4rem;margin-bottom:6px;">📐</div>
        <div style="font-size:1.2rem;font-weight:700;color:{COLORS['accent']};">{SILHOUETTE_SCORE}</div>
        <div style="font-size:0.75rem;color:{COLORS['muted']};margin-top:4px;">
            Silhouette Score
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_total:
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(26,31,46,0.95), rgba(14,17,23,0.85));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 20px; text-align: center;
        border-top: 3px solid {COLORS['success']};
    ">
        <div style="font-size:1.4rem;margin-bottom:6px;">👥</div>
        <div style="font-size:1.2rem;font-weight:700;color:{COLORS['success']};">{TOTAL_CUSTOMERS:,}</div>
        <div style="font-size:0.75rem;color:{COLORS['muted']};margin-top:4px;">
            Tổng khách hàng phân nhóm
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")


# 3 Cluster summary cards
st.markdown(section_header("kết quả phân nhóm (3 clusters)"), unsafe_allow_html=True)

cluster_cols = st.columns(3)

for i, (cluster_id, info) in enumerate(CLUSTER_INFO.items()):
    with cluster_cols[i]:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(26,31,46,0.95), rgba(14,17,23,0.85));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 24px;
            border-left: 4px solid {info['color']};
            border-left: 4px solid {info['color']};
            height: 340px;
            display: flex;
            flex-direction: column;
        ">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                <span style="font-size:1.6rem;">{info['icon']}</span>
                <span style="font-size:1.1rem;font-weight:700;color:{info['color']};">{info['name']}</span>
            </div>
            <div style="
                font-size:2rem;font-weight:800;color:{COLORS['text']};margin-bottom:4px;
            ">{info['pct']}%</div>
            <div style="font-size:0.8rem;color:{COLORS['muted']};margin-bottom:16px;">
                {info['count']:,} khách hàng
            </div>
            <div style="font-size:0.82rem;color:{COLORS['muted']};line-height:1.6;margin-bottom:12px;flex-grow:1;">
                {info['description']}
            </div>
            <div style="
                display:grid; grid-template-columns:1fr 1fr; gap:8px;
                font-size:0.78rem; color:{COLORS['text']};
            ">
                <div>💰 <span style="color:{COLORS['muted']}">Monetary:</span> ${info['monetary']}</div>
                <div>🔄 <span style="color:{COLORS['muted']}">Frequency:</span> {info['frequency']}</div>
                <div>📅 <span style="color:{COLORS['muted']}">Recency:</span> {info['recency']}d</div>
                <div>📊 <span style="color:{COLORS['muted']}">Profit:</span> ${info['avg_profit']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("")


# Donut phân bổ cluster và Bar chart so sánh Monetary
st.markdown(section_header("phân bổ khách hàng & so sánh monetary, profit"), unsafe_allow_html=True)

col_donut, col_bar = st.columns([2, 3])

with col_donut:
    # Donut chart phân bổ số lượng khách hàng theo cluster
    fig_cluster_donut = go.Figure(go.Pie(
        labels=[info["name"] for info in CLUSTER_INFO.values()],
        values=[info["count"] for info in CLUSTER_INFO.values()],
        hole=0.55,
        marker=dict(colors=[info["color"] for info in CLUSTER_INFO.values()]),
        textinfo="percent",
        textfont=dict(size=12, color=COLORS["text"]),
        hovertemplate="<b>%{label}</b><br>%{value:,} khách<br>%{percent}<extra></extra>",
    ))

    fig_cluster_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=COLORS["text"], size=13),
        title=dict(text="Phân bổ Khách hàng", font=dict(size=16, color=COLORS["text"]), x=0.02, y=0.97),
        height=380,
        margin=dict(l=20, r=20, t=40, b=20),
        annotations=[dict(
            text=f"<b>{TOTAL_CUSTOMERS:,}</b>",
            x=0.5, y=0.5,
            font=dict(size=14, color=COLORS["muted"]),
            showarrow=False,
        )],
    )

    st.plotly_chart(fig_cluster_donut, width="stretch")

with col_bar:
    fig_compare = go.Figure()
    metrics = ["Monetary", "Avg Profit"]
    metric_values = {
        "Monetary": [220, 102, 357],
        "Avg Profit": [120, 29, 84],
    }
    cluster_names = ["Premium One-Time", "Low-Value", "VIP Loyal"]
    bar_colors = [CLUSTER_COLORS[0], CLUSTER_COLORS[1], CLUSTER_COLORS[2]]

    for i, name in enumerate(cluster_names):
        fig_compare.add_trace(go.Bar(
            x=metrics,
            y=[metric_values[m][i] for m in metrics],
            name=name,
            marker_color=bar_colors[i],
            text=[f"${metric_values[m][i]}" for m in metrics],
            textposition="outside",
        ))

    fig_compare.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=COLORS["text"], size=13),
        title=dict(text="So sánh Monetary & Profit", font=dict(size=16, color=COLORS["text"]), x=0.02, y=0.97),
        height=380,
        margin=dict(l=20, r=20, t=60, b=20),
        barmode="group",
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="USD ($)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", yanchor="top", y=1.15, xanchor="right", x=1),
    )

    st.plotly_chart(fig_compare, width="stretch")


# Đề xuất chiến lược Marketing cho từng cluster
st.markdown(section_header("đề xuất chiến lược marketing"), unsafe_allow_html=True)

strategy_cols = st.columns(3)

for i, (cluster_id, info) in enumerate(CLUSTER_INFO.items()):
    with strategy_cols[i]:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(26,31,46,0.9), rgba(14,17,23,0.8));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 20px;
            border-top: 3px solid {info['color']};
            height: 190px;
        ">
            <div style="font-size:0.95rem;font-weight:700;color:{info['color']};margin-bottom:10px;">
                {info['icon']} {info['name']}
            </div>
            <div style="font-size:0.82rem;color:{COLORS['muted']};line-height:1.7;">
                {info['strategy']}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
