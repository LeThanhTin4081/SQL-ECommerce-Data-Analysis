"""
Charts module.
Reusable Plotly chart factory functions cho Dashboard.
Mỗi function trả về 1 Plotly Figure object, đã apply dark theme.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .styles import CHART_COLORS, PLOTLY_LAYOUT, COLORS


def _apply_layout(fig: go.Figure, title: str = "", height: int = 400) -> go.Figure:
    """Apply layout chuẩn (font, background, margin) cho mọi chart."""
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(
            text=title,
            font=dict(size=16, color=COLORS["text"], family="Inter, sans-serif"),
            x=0.02, y=0.97,
        ),
        height=height,
    )
    return fig


# Area / Line Charts

def monthly_trend_area(df: pd.DataFrame, height: int = 400) -> go.Figure:
    """Area chart hiển thị doanh thu và lợi nhuận theo 12 tháng."""
    monthly = (
        df.groupby("Year_Month")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
        .sort_values("Year_Month")
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly["Year_Month"],
        y=monthly["Sales"],
        name="Doanh thu",
        fill="tozeroy",
        fillcolor="rgba(102,126,234,0.15)",
        line=dict(color=COLORS["primary"], width=3),
        mode="lines+markers",
        marker=dict(size=7, color=COLORS["primary"]),
        hovertemplate="<b>%{x}</b><br>Doanh thu: $%{y:,.0f}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=monthly["Year_Month"],
        y=monthly["Profit"],
        name="Lợi nhuận",
        fill="tozeroy",
        fillcolor="rgba(0,227,150,0.1)",
        line=dict(color=COLORS["success"], width=3),
        mode="lines+markers",
        marker=dict(size=7, color=COLORS["success"]),
        hovertemplate="<b>%{x}</b><br>Lợi nhuận: $%{y:,.0f}<extra></extra>",
    ))

    _apply_layout(fig, "Doanh thu & Lợi nhuận theo Tháng", height)
    fig.update_xaxes(title="", tickangle=-45)
    fig.update_yaxes(title="USD ($)")

    return fig


def running_total_area(df: pd.DataFrame, height: int = 400) -> go.Figure:
    """Area chart hiển thị doanh thu lũy kế (Running Total) theo tháng."""
    monthly = (
        df.groupby("Year_Month")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Year_Month")
    )
    monthly["Running_Total"] = monthly["Sales"].cumsum()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly["Year_Month"],
        y=monthly["Running_Total"],
        fill="tozeroy",
        fillcolor="rgba(0,210,255,0.12)",
        line=dict(color=COLORS["accent"], width=3, shape="spline"),
        mode="lines+markers",
        marker=dict(size=8, color=COLORS["accent"]),
        hovertemplate="<b>%{x}</b><br>Lũy kế: $%{y:,.0f}<extra></extra>",
    ))

    # Đường ngang đánh dấu các mốc doanh thu quan trọng
    for milestone in [1_000_000, 3_000_000, 5_000_000]:
        if monthly["Running_Total"].max() > milestone:
            fig.add_hline(
                y=milestone,
                line_dash="dot",
                line_color="rgba(255,255,255,0.15)",
                annotation_text=f"${milestone / 1_000_000:.0f}M",
                annotation_font_color=COLORS["muted"],
                annotation_font_size=11,
            )

    _apply_layout(fig, "Doanh thu Lũy kế (Running Total)", height)
    fig.update_xaxes(title="")
    fig.update_yaxes(title="USD ($)")

    return fig


# Bar Charts

def top_products_bar(df: pd.DataFrame, top_n: int = 10, height: int = 400) -> go.Figure:
    """Horizontal bar chart hiển thị Top N sản phẩm theo doanh thu."""
    top = (
        df.groupby(["Product", "Product_Category"])["Sales"]
        .sum()
        .reset_index()
        .nlargest(top_n, "Sales")
        .sort_values("Sales", ascending=True)
    )

    fig = go.Figure(go.Bar(
        x=top["Sales"],
        y=top["Product"],
        orientation="h",
        marker=dict(
            color=top["Sales"],
            colorscale=[[0, COLORS["primary"]], [1, COLORS["accent"]]],
            line=dict(width=0),
            cornerradius=6,
        ),
        text=[f"${v:,.0f}" for v in top["Sales"]],
        textposition="outside",
        textfont=dict(color=COLORS["text"], size=11),
        hovertemplate="<b>%{y}</b><br>Doanh thu: $%{x:,.0f}<extra></extra>",
    ))

    _apply_layout(fig, f"Top {top_n} Sản phẩm Bán chạy", height)
    fig.update_xaxes(title="Doanh thu (USD)", showgrid=False)
    fig.update_yaxes(title="")
    fig.update_layout(margin=dict(l=140))

    return fig


def monthly_bar_line_combo(df: pd.DataFrame, height: int = 400) -> go.Figure:
    """Combo chart: Bar (doanh thu) kết hợp Line (lợi nhuận) theo tháng, dual Y-axis."""
    monthly = (
        df.groupby("Year_Month")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
        .sort_values("Year_Month")
    )

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=monthly["Year_Month"],
        y=monthly["Sales"],
        name="Doanh thu",
        marker=dict(
            color=monthly["Sales"],
            colorscale=[[0, "rgba(102,126,234,0.5)"], [1, COLORS["primary"]]],
            cornerradius=6,
        ),
        hovertemplate="<b>%{x}</b><br>Doanh thu: $%{y:,.0f}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=monthly["Year_Month"],
        y=monthly["Profit"],
        name="Lợi nhuận",
        mode="lines+markers",
        line=dict(color=COLORS["success"], width=3),
        marker=dict(size=8, color=COLORS["success"]),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Lợi nhuận: $%{y:,.0f}<extra></extra>",
    ))

    _apply_layout(fig, "Doanh thu (Bar) & Lợi nhuận (Line) theo Tháng", height)
    fig.update_layout(
        yaxis=dict(title="Doanh thu (USD)", gridcolor="rgba(255,255,255,0.05)"),
        yaxis2=dict(
            title="Lợi nhuận (USD)",
            overlaying="y",
            side="right",
            gridcolor="rgba(255,255,255,0.03)",
        ),
        barmode="group",
    )
    fig.update_xaxes(title="", tickangle=-45)

    return fig


def quarterly_comparison_bar(df: pd.DataFrame, height: int = 380) -> go.Figure:
    """Grouped bar chart so sánh doanh thu và lợi nhuận giữa Q1-Q4."""
    quarterly = (
        df.groupby("Quarter")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order_Id", "count"))
        .reset_index()
    )
    quarterly["Quarter_Label"] = quarterly["Quarter"].apply(lambda q: f"Q{q}")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=quarterly["Quarter_Label"], y=quarterly["Sales"],
        name="Doanh thu", marker_color=COLORS["primary"],
        text=[f"${v/1000:.0f}K" for v in quarterly["Sales"]],
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        x=quarterly["Quarter_Label"], y=quarterly["Profit"],
        name="Lợi nhuận", marker_color=COLORS["success"],
        text=[f"${v/1000:.0f}K" for v in quarterly["Profit"]],
        textposition="outside",
    ))

    _apply_layout(fig, "So sánh theo Quý", height)
    fig.update_layout(barmode="group")
    fig.update_xaxes(title="")
    fig.update_yaxes(title="USD ($)")

    return fig


def shipping_cost_bar(df: pd.DataFrame, height: int = 380) -> go.Figure:
    """Bar chart hiển thị chi phí vận chuyển trung bình theo mức ưu tiên đơn hàng."""
    priority = (
        df.groupby("Order_Priority")
        .agg(
            Avg_Cost=("Shipping_Cost", "mean"),
            Total_Orders=("Order_Id", "count"),
        )
        .reset_index()
        .sort_values("Avg_Cost", ascending=False)
    )

    colors_map = {
        "Critical": COLORS["danger"],
        "High": COLORS["warning"],
        "Medium": COLORS["primary"],
        "Low": COLORS["success"],
    }
    bar_colors = [colors_map.get(p, COLORS["primary"]) for p in priority["Order_Priority"]]

    fig = go.Figure(go.Bar(
        x=priority["Order_Priority"],
        y=priority["Avg_Cost"],
        marker=dict(color=bar_colors, cornerradius=8),
        text=[f"${v:.2f}" for v in priority["Avg_Cost"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Avg Cost: $%{y:.2f}<br>Orders: %{customdata:,}<extra></extra>",
        customdata=priority["Total_Orders"],
    ))

    _apply_layout(fig, "Chi phí Vận chuyển TB theo Mức Ưu tiên", height)
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Chi phí TB (USD)")

    return fig


def payment_bar(df: pd.DataFrame, height: int = 380) -> go.Figure:
    """Horizontal bar chart hiển thị doanh thu theo phương thức thanh toán."""
    payment = (
        df.groupby("Payment_Method")
        .agg(Revenue=("Sales", "sum"), Orders=("Order_Id", "count"))
        .reset_index()
        .sort_values("Revenue", ascending=True)
    )

    fig = go.Figure(go.Bar(
        x=payment["Revenue"],
        y=payment["Payment_Method"],
        orientation="h",
        marker=dict(
            color=[COLORS["primary"], COLORS["accent"], COLORS["warning"], COLORS["success"]],
            cornerradius=6,
        ),
        text=[f"${v:,.0f}" for v in payment["Revenue"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Doanh thu: $%{x:,.0f}<extra></extra>",
    ))

    _apply_layout(fig, "Doanh thu theo Phương thức Thanh toán", height)
    fig.update_xaxes(title="Doanh thu (USD)")
    fig.update_yaxes(title="")
    fig.update_layout(margin=dict(l=120))

    return fig


# Pie / Donut Charts

def category_donut(df: pd.DataFrame, height: int = 400) -> go.Figure:
    """Donut chart hiển thị phân bổ doanh thu theo danh mục sản phẩm."""
    cat = (
        df.groupby("Product_Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig = go.Figure(go.Pie(
        labels=cat["Product_Category"],
        values=cat["Sales"],
        hole=0.55,
        marker=dict(colors=CHART_COLORS[:len(cat)]),
        textinfo="label+percent",
        textfont=dict(size=11, color=COLORS["text"]),
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
    ))

    _apply_layout(fig, "Phân bổ Doanh thu theo Danh mục", height)
    fig.update_layout(
        annotations=[dict(
            text="<b>Revenue</b>",
            x=0.5, y=0.5,
            font=dict(size=14, color=COLORS["muted"]),
            showarrow=False,
        )]
    )

    return fig


def gender_donut(df: pd.DataFrame, height: int = 350) -> go.Figure:
    """Donut chart hiển thị phân bổ đơn hàng theo giới tính."""
    gender = df["Gender"].value_counts().reset_index()
    gender.columns = ["Gender", "Count"]

    fig = go.Figure(go.Pie(
        labels=gender["Gender"],
        values=gender["Count"],
        hole=0.55,
        marker=dict(colors=[COLORS["primary"], COLORS["danger"]]),
        textinfo="label+percent",
        textfont=dict(size=12, color=COLORS["text"]),
    ))

    _apply_layout(fig, "Phân bổ Giới tính", height)
    return fig


def device_donut(df: pd.DataFrame, height: int = 350) -> go.Figure:
    """Donut chart hiển thị phân bổ đơn hàng theo thiết bị (Web/Mobile)."""
    device = df["Device_Type"].value_counts().reset_index()
    device.columns = ["Device_Type", "Count"]

    fig = go.Figure(go.Pie(
        labels=device["Device_Type"],
        values=device["Count"],
        hole=0.55,
        marker=dict(colors=[COLORS["accent"], COLORS["warning"]]),
        textinfo="label+percent",
        textfont=dict(size=12, color=COLORS["text"]),
    ))

    _apply_layout(fig, "Phân bổ Thiết bị", height)
    return fig


def payment_donut(df: pd.DataFrame, height: int = 350) -> go.Figure:
    """Donut chart hiển thị phân bổ đơn hàng theo phương thức thanh toán."""
    pay = df["Payment_Method"].value_counts().reset_index()
    pay.columns = ["Method", "Count"]

    fig = go.Figure(go.Pie(
        labels=pay["Method"],
        values=pay["Count"],
        hole=0.55,
        marker=dict(colors=CHART_COLORS[:len(pay)]),
        textinfo="label+percent",
        textfont=dict(size=12, color=COLORS["text"]),
    ))

    _apply_layout(fig, "Phương thức Thanh toán", height)
    return fig


# Heatmap

def daily_sales_heatmap(df: pd.DataFrame, height: int = 350) -> go.Figure:
    """Heatmap hiển thị doanh thu theo ma trận Tháng x Ngày trong tuần."""
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_data = (
        df.groupby(["Month", "Day_of_Week"])["Sales"]
        .sum()
        .reset_index()
        .pivot(index="Day_of_Week", columns="Month", values="Sales")
        .reindex(day_order)
        .fillna(0)
    )

    fig = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=[f"T{m}" for m in heatmap_data.columns],
        y=heatmap_data.index,
        colorscale=[[0, "#0E1117"], [0.5, COLORS["primary"]], [1, COLORS["accent"]]],
        hovertemplate="<b>%{y}</b> - %{x}<br>Doanh thu: $%{z:,.0f}<extra></extra>",
        colorbar=dict(
            title=dict(text="USD", font=dict(color=COLORS["muted"])),
            tickfont=dict(color=COLORS["muted"]),
        ),
    ))

    _apply_layout(fig, "Heatmap Doanh thu (Tháng x Thứ)", height)

    return fig


# Treemap

def category_treemap(df: pd.DataFrame, height: int = 450) -> go.Figure:
    """Treemap hiển thị doanh thu phân cấp theo Category rồi đến Product."""
    tree_data = (
        df.groupby(["Product_Category", "Product"])["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.treemap(
        tree_data,
        path=["Product_Category", "Product"],
        values="Sales",
        color="Sales",
        color_continuous_scale=[[0, COLORS["card"]], [0.5, COLORS["primary"]], [1, COLORS["accent"]]],
    )

    _apply_layout(fig, "Treemap Doanh thu (Category > Product)", height)
    fig.update_traces(
        textfont=dict(size=12, color="white"),
        hovertemplate="<b>%{label}</b><br>Doanh thu: $%{value:,.0f}<extra></extra>",
    )

    return fig


# Histogram

def aging_histogram(df: pd.DataFrame, height: int = 380) -> go.Figure:
    """Histogram hiển thị phân bổ thời gian xử lý đơn hàng (Aging) kèm đường trung bình."""
    fig = go.Figure(go.Histogram(
        x=df["Aging"].dropna(),
        nbinsx=20,
        marker=dict(
            color=COLORS["warning"],
            line=dict(width=1, color="rgba(255,255,255,0.1)"),
        ),
        hovertemplate="Aging: %{x} ngày<br>Số đơn: %{y:,}<extra></extra>",
    ))

    avg_aging = df["Aging"].mean()
    fig.add_vline(
        x=avg_aging,
        line_dash="dash",
        line_color=COLORS["danger"],
        annotation_text=f"TB: {avg_aging:.1f} ngày",
        annotation_font_color=COLORS["danger"],
        annotation_font_size=12,
    )

    _apply_layout(fig, "Phân bổ Thời gian Xử lý Đơn hàng (Aging)", height)
    fig.update_xaxes(title="Số ngày")
    fig.update_yaxes(title="Số đơn hàng")

    return fig


# Radar / Polar (cho trang ML Segmentation)

def rfm_radar(cluster_data: dict, height: int = 450) -> go.Figure:
    """Radar chart so sánh 5 chỉ số RFM giữa 3 clusters.

    Args:
        cluster_data: Dict với key là cluster_id (0, 1, 2), value là dict chứa:
            - name: tên cluster (vd: "Premium")
            - color: mã màu hex
            - values: list 5 giá trị [Recency, Frequency, Monetary, Avg_Discount, Avg_Profit]
        height: chiều cao chart (px)

    Returns:
        Plotly Figure object đã apply theme.
    """
    categories = ["Recency", "Frequency", "Monetary", "Avg Discount", "Avg Profit"]

    fig = go.Figure()

    for cluster_id, data in cluster_data.items():
        values = data["values"] + [data["values"][0]]
        cats = categories + [categories[0]]

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=cats,
            fill="toself",
            fillcolor=f"rgba({_hex_to_rgb(data['color'])},0.15)",
            line=dict(color=data["color"], width=2),
            name=data["name"],
            marker=dict(size=6, color=data["color"]),
        ))

    _apply_layout(fig, "So sánh RFM giữa 3 Phân khúc", height)
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                gridcolor="rgba(255,255,255,0.08)",
                tickfont=dict(size=10, color=COLORS["muted"]),
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.08)",
                tickfont=dict(size=11, color=COLORS["text"]),
            ),
        ),
    )

    return fig


def _hex_to_rgb(hex_color: str) -> str:
    """Chuyển mã màu hex sang chuỗi RGB dạng 'r,g,b' để dùng trong rgba()."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{r},{g},{b}"
