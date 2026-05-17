# 📊 Dashboard Tương tác — Báo cáo Tổng hợp E-Commerce 2018

Trực quan hóa toàn bộ kết quả phân tích SQL và ML Segmentation cho dữ liệu E-Commerce 2018 thành **Dashboard tương tác 4 trang**, phục vụ ra quyết định kinh doanh nhanh chóng và chính xác.

**Nguồn dữ liệu:** Đọc trực tiếp từ `../data/cleaned/` (4 file CSV đã chuẩn hóa 3NF) — không cần SQL Server chạy.

---

## 🚀 Cài đặt & Khởi chạy

```bash
cd dashboard
pip install -r requirements.txt
python -m streamlit run Overview.py
```

Truy cập tại: `http://localhost:8501`

---

## 📑 Cấu trúc 4 Trang Dashboard

| # | Trang | File | Nội dung chính | SQL Query tương ứng |
|---|-------|------|----------------|---------------------|
| 1 | **Executive Overview** | `Overview.py` | 5 KPI cards (Doanh thu, Lợi nhuận, Biên LN, Đơn hàng, Aging), Monthly trend area chart, Category donut, Top 5 sản phẩm, Quick highlights | Tổng hợp |
| 2 | **Sales & Products** | `pages/1_Sales_and_Products.py` | Combo chart (Bar+Line), Running total area, Heatmap (Month × Weekday), Product ranking table, Category treemap, Quarterly comparison | #2, #3, #7, #8, #10 |
| 3 | **Customers & Ops** | `pages/2_Customers_and_Ops.py` | Demographics (Gender, Device, Login donuts), Top 10 VIP table + Insight, Aging histogram, Shipping cost by priority, Payment analysis | #4, #5, #6, #9 |
| 4 | **ML Segmentation** | `pages/3_ML_Segmentation.py` | 3 Cluster cards (K-Means RFM), RFM Radar chart, Cluster donut, RFM comparison bar, Marketing strategy recommendations | ML notebook |

---

## 🛠 Kiến trúc Module

| Module | Vai trò | Chi tiết |
|--------|--------|----------|
| `utils/data_loader.py` | Data Layer | Load & cache 4 CSV files với `@st.cache_data`, ép kiểu dữ liệu, tạo features thời gian (Month, Quarter, Year_Month) |
| `utils/charts.py` | Chart Factory | 15+ hàm tạo biểu đồ Plotly (Area, Bar, Donut, Heatmap, Treemap, Radar, Histogram, Combo), đồng bộ theme Dark mode |
| `utils/styles.py` | Design System | Color palette (9 màu), Plotly layout template, CSS injection (Glassmorphism, Inter font, gradient animations), KPI card component |
| `.streamlit/config.toml` | App Config | Dark theme configuration, headless server |

---

## 🎨 Thiết kế UI

- **Dark Mode Premium** với glassmorphism cards và gradient border-top
- **Font Inter** (Google Fonts) cho typography chuyên nghiệp
- **Plotly charts** với hover tooltips, smooth transitions, custom color palette
- **Sidebar filters** tương tác: slider tháng, dropdown danh mục, radio giới tính/thiết bị
- **Responsive layout** tự điều chỉnh theo kích thước màn hình

### Color Palette

| Vai trò | Hex | Dùng cho |
|---------|-----|----------|
| Primary | `#667EEA` | Gradient chính, buttons |
| Accent | `#00D2FF` | Highlights, trend lines |
| Success | `#00E396` | Lợi nhuận, tăng trưởng |
| Warning | `#F6AD55` | Cảnh báo, aging cao |
| Danger | `#FC5C7D` | Metrics giảm, chi phí |

---

## 📦 Tech Stack

| Thành phần | Công nghệ | Vai trò |
|-----------|----------|---------|
| Framework | **Streamlit** 1.57+ | Multi-page app, Dark mode, Caching |
| Charts | **Plotly** (Graph Objects) | 15+ loại biểu đồ tương tác |
| Data | **Pandas** | Aggregation, Feature engineering |
| Styling | Custom CSS injection | Glassmorphism, animations |
| Font | Inter (Google Fonts) | Typography chuyên nghiệp |

---
