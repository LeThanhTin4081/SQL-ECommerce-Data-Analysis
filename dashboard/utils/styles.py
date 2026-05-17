"""
Styles module.
CSS Theme, Design Constants và reusable HTML components cho Dashboard.
Dark-mode premium với glassmorphism, gradient animations.
"""


# Color palette cho toàn bộ Dashboard
COLORS = {
    "bg": "#0E1117",
    "card": "#1A1F2E",
    "card_hover": "#242B3D",
    "primary": "#667EEA",
    "secondary": "#764BA2",
    "accent": "#00D2FF",
    "success": "#00E396",
    "warning": "#F6AD55",
    "danger": "#FC5C7D",
    "text": "#FAFAFA",
    "muted": "#8892B0",
    "border": "rgba(255,255,255,0.08)",
}

# Dãy màu tuần tự cho Plotly charts
CHART_COLORS = [
    "#667EEA", "#00D2FF", "#FC5C7D", "#F6AD55",
    "#00E396", "#764BA2", "#FF6B6B", "#4ECDC4",
    "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD",
]

# Màu riêng cho từng cluster K-Means
CLUSTER_COLORS = {
    0: "#00D2FF",   # Premium One-Time
    1: "#F6AD55",   # Low-Value
    2: "#764BA2",   # VIP Loyal
}


# Layout mặc định cho mọi Plotly chart (transparent background, font Inter)
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=COLORS["text"], size=13),
    margin=dict(l=20, r=20, t=40, b=20),
    hoverlabel=dict(
        bgcolor=COLORS["card"],
        font_size=13,
        font_family="Inter, sans-serif",
        bordercolor=COLORS["border"],
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        zerolinecolor="rgba(255,255,255,0.05)",
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        zerolinecolor="rgba(255,255,255,0.05)",
    ),
)


# CSS tùy chỉnh: Google Font, sidebar, tabs, metric cards, dataframe, section headers
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    html { scroll-behavior: smooth; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0E1117 0%, #1A1F2E 100%);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #667EEA;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(26,31,46,0.6);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.06);
        padding: 10px 20px;
        color: #8892B0;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667EEA, #764BA2) !important;
        color: #FAFAFA !important;
        border: none !important;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(26,31,46,0.9), rgba(14,17,23,0.8));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 20px 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(102,126,234,0.15);
    }
    [data-testid="stMetricLabel"] {
        color: #8892B0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667EEA, #00D2FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.06);
    }

    hr {
        border-color: rgba(255,255,255,0.06) !important;
    }

    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #8892B0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(102,126,234,0.3);
    }
</style>
"""


def kpi_card(title: str, value: str, icon: str, color: str = "#667EEA", subtitle: str = "") -> str:
    """Tạo HTML cho 1 KPI card glassmorphism với gradient border-top."""
    subtitle_html = f'<div style="font-size:0.75rem;color:#8892B0;margin-top:4px;">{subtitle}</div>' if subtitle else ""
    return f"""
    <div style="
        background: linear-gradient(135deg, rgba(26,31,46,0.95), rgba(14,17,23,0.85));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: default;
        border-top: 3px solid {color};
    ">
        <div style="font-size:1.8rem;margin-bottom:8px;">{icon}</div>
        <div style="
            font-size: 1.9rem;
            font-weight: 800;
            background: linear-gradient(135deg, {color}, #00D2FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 4px;
        ">{value}</div>
        <div style="
            font-size: 0.8rem;
            color: #8892B0;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        ">{title}</div>
        {subtitle_html}
    </div>
    """


def section_header(text: str) -> str:
    """Tạo HTML cho section header với style uppercase và border-bottom."""
    return f'<div class="section-header">{text}</div>'


def inject_css():
    """Inject toàn bộ custom CSS vào trang Streamlit hiện tại."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
