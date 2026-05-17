# Streamlit Dashboard — E-Commerce 2018 Annual Report

Dashboard tương tác trực quan hóa toàn bộ kết quả phân tích SQL và ML Segmentation
cho dữ liệu E-Commerce 2018 (51,290 đơn hàng, 38,995 khách hàng).

## Cài đặt & Chạy

```bash
pip install -r requirements.txt
python -m streamlit run Overview.py
```

## Cấu trúc 4 trang

| Trang | File | Mô tả |
|-------|------|-------|
| **Executive Overview** | `Overview.py` | 5 KPI cards, Monthly trend (Area), Category donut, Top 5 products, Quick highlights |
| **Sales & Products** | `pages/1_Sales_and_Products.py` | Combo chart (Bar+Line), Running total, Heatmap (Month x Weekday), Product ranking table, Treemap, Quarterly comparison |
| **Customers & Ops** | `pages/2_Customers_and_Ops.py` | Demographics (Gender, Device, Login donuts), VIP table, Aging histogram, Shipping cost by priority, Payment analysis |
| **ML Segmentation** | `pages/3_ML_Segmentation.py` | 3 Cluster cards (K-Means RFM), Radar chart, Cluster donut, RFM comparison, Marketing strategy |

## Tech Stack

- **Streamlit** 1.57+ (Dark mode, multi-page)
- **Plotly** (15+ reusable chart functions)
- **Pandas** (Data loading, aggregation)
- **Custom CSS** (Glassmorphism, Inter font, gradient animations)

## Modules

| Module | Vai trò |
|--------|--------|
| `utils/data_loader.py` | Load & cache 4 CSV files với `@st.cache_data` |
| `utils/charts.py` | Factory functions cho Area, Bar, Donut, Heatmap, Treemap, Radar, Histogram |
| `utils/styles.py` | Color palette, Plotly layout, CSS injection, KPI card component |
| `.streamlit/config.toml` | Dark theme configuration |

## Dữ liệu

Dashboard đọc trực tiếp từ `../data/cleaned/` (4 CSV files đã chuẩn hóa 3NF).
Không cần SQL Server chạy.
