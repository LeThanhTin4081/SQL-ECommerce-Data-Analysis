# 🛒 Phân tích Quy trình Xử lý Đơn hàng E-Commerce (Order Fulfillment Analysis)

## 🔎 1. Tổng quan dự án

Dự án thực hiện quy trình kỹ thuật dữ liệu và phân tích kinh doanh toàn diện (End-to-End) cho một doanh nghiệp thương mại điện tử, dựa trên tập dữ liệu lịch sử giao dịch năm 2018. Quy trình được triển khai qua các giai đoạn chính:

- **Khai thác & Nạp dữ liệu (Extract & Load):** Nhập 51,290 bản ghi giao dịch thô vào SQL Server thông qua kỹ thuật `BULK INSERT` với bảng Staging (`RawOrders`).
- **Chuẩn hóa dữ liệu (Data Normalization):** Chuyển đổi dữ liệu phẳng (Flat Data) thành mô hình quan hệ đạt chuẩn 3NF gồm 1 Fact Table (`Orders`) và 3 Dimension Tables (`Customers`, `Products`, `Categories`).
- **Phân tích nâng cao (Advanced Analytics):** Sử dụng các kỹ thuật T-SQL chuyên sâu (Window Functions, Recursive CTEs, Ranking Functions) để khai thác insights về tài chính, hành vi khách hàng và hiệu suất vận hành.

| Giai đoạn   | 1. Nạp dữ liệu (E-L)      | 2. Chuẩn hóa 3NF (T) | 3. Phân tích nâng cao  |
| ----------- | ------------------------- | -------------------- | ---------------------- |
| **Công cụ** | SQL Server, `BULK INSERT` | T-SQL, Data Modeling | CTEs, Window Functions |

Bộ dữ liệu gốc gồm **51,290 đơn hàng** giao dịch trong toàn bộ năm 2018 (Tháng 1 – Tháng 12), tạo ra tổng doanh thu **7.8 triệu USD** với biên lợi nhuận **46.2%**.

> 💡 **Lưu ý dành cho Nhà tuyển dụng / Technical Reviewer:**
> File `README.md` này chỉ đóng vai trò là **Báo cáo Tổng quan (Executive Summary)** trình bày các phát hiện chính và luồng dự án.
> Chi tiết về Data Dictionary, Kiến trúc Pipeline và 10 kết quả truy vấn phân tích chuyên sâu đã được ghi chú rõ ràng trong từng thư mục như bảng sau:

| Phân khu               | Mô tả                                                           | Liên kết                                 |
| ---------------------- | --------------------------------------------------------------- | ---------------------------------------- |
| **Dữ liệu (Data)**     | Cấu trúc dữ liệu raw/cleaned, Data Dictionary chi tiết          | [`data/`](./data/)                       |
| **Kiến trúc Pipeline** | Luồng xử lý ELT, mô hình cơ sở dữ liệu 3NF                      | [`DATA_PIPELINE.md`](./DATA_PIPELINE.md) |
| **Báo cáo Analytics**  | 10 truy vấn T-SQL phức tạp kèm hình ảnh kết quả và Key Insights | [`sql/`](./sql/)                         |
| **ML Segmentation**    | K-Means Clustering (RFM) phân nhóm 38,995 khách hàng            | [`machine_learning/`](./machine_learning/) |
| **Dashboard**          | Streamlit Dashboard tương tác: 4 trang báo cáo trực quan        | [`dashboard/`](./dashboard/)             |

---

## 🔆 2. Kỹ năng dữ liệu được thể hiện

| Kỹ năng                   | Công cụ / Kỹ thuật                                                              |
| ------------------------- | ------------------------------------------------------------------------------- |
| **Data Engineering**      | SQL Server, ELT Pipeline, `BULK INSERT`, Staging Tables                         |
| **Data Modeling**         | Database Normalization (3NF), Fact & Dimension Tables, Primary/Foreign Keys     |
| **Advanced SQL (T-SQL)**  | Window Functions (`RANK`, `SUM OVER`), Recursive CTEs, Common Table Expressions |
| **Business Intelligence** | Phân tích tỷ suất lợi nhuận, nhận diện nút thắt vận hành, Customer Profiling    |

---

## 🎯 3. Mục tiêu dự án (Objectives)

- ✔ **Tối ưu hóa hiệu suất xử lý đơn hàng** – Theo dõi sự chậm trễ và cải thiện thời gian hoàn thành đơn hàng.
- ✔ **Xác định các sản phẩm bán chạy nhất** – Hiểu rõ những sản phẩm nào tạo ra doanh thu cao nhất.
- ✔ **Phân khúc khách hàng giá trị cao** – Phân tích hành vi chi tiêu và mức độ tương tác của khách hàng.
- ✔ **Giảm chi phí vận chuyển** – Đánh giá sự biến động chi phí dựa trên mức độ ưu tiên của đơn hàng (order priority).
- ✔ **Xác định phương thức thanh toán ưa thích** – Xác định sở thích thanh toán của khách hàng để có chiến lược tài chính tốt hơn.

---

## 📌 4. Quy trình thực hiện

### 4.1. Extract & Load (Khai thác và Nạp Dữ liệu)

Xây dựng kịch bản tự động khởi tạo cơ sở dữ liệu và nạp toàn bộ 51,290 bản ghi từ file `.csv` thô vào bảng tạm `RawOrders` (Staging Table) bằng lệnh `BULK INSERT`, áp dụng ép kiểu an toàn `VARCHAR(MAX)` để tránh mất mát dữ liệu.

> 📁 **Chi tiết mã nguồn:** [`sql/01_setup_and_import.sql`](./sql/01_setup_and_import.sql)

### 4.2. Data Normalization (Chuẩn hóa cấu trúc 3NF)

Từ bảng Staging phẳng, dữ liệu được bóc tách và định tuyến vào mô hình quan hệ:

- 3 bảng **Dimension**: `Customers`, `Products`, `Categories` (thiết lập cấu trúc đệ quy cha-con).
- 1 bảng **Fact**: `Orders` (lưu trữ các metrics kinh doanh: Doanh thu, Lợi nhuận, Chi phí vận chuyển).
  > 📁 **Xem sơ đồ Database Schema và chi tiết kỹ thuật tại:** [`DATA_PIPELINE.md`](./DATA_PIPELINE.md)

### 4.3. Advanced Analytics (Phân tích Kinh doanh)

Thực thi 10 kịch bản truy vấn phân tích đa chiều (Sales, Operations, Customer, Logistics) sử dụng các kỹ thuật T-SQL nâng cao:

- **Window Functions:** Xếp hạng sản phẩm (`RANK() OVER`) và tính doanh thu lũy kế (`SUM() OVER`).
- **Common Table Expressions (CTEs):** Tổ chức logic phân tích phức tạp thành các khối mã dễ đọc, dễ tái sử dụng.
- **Recursive CTEs:** Truy xuất và vẽ cây phân cấp danh mục hàng hóa (Parent-Child).
  > 📁 **Xem toàn bộ 10 Báo cáo Insights kèm hình ảnh kết quả tại:** [`sql/`](./sql/)

---

## 📊 5. Thông tin chi tiết & Phát hiện Kinh doanh (Business Insights & Findings)

### 📌 Phân tích Doanh số & Doanh thu (Sales & Revenue Analysis)

- Doanh nghiệp đã tạo ra **7,8 triệu USD tổng doanh số**, với **biên lợi nhuận 3,6 triệu USD (46.2%)**.
- **Doanh số đạt đỉnh vào tháng 5 và tháng 11**, cho thấy những **xu hướng nhu cầu theo mùa vụ** rõ rệt.

### 📌 Các sản phẩm bán chạy nhất (Top-Selling Products)

- Các danh mục bán chạy nhất là **Thời trang (Fashion) và Giày dép (Footwear)**, với **Áo phông (T-Shirts), Đồng hồ (Watches), và Giày chạy bộ (Running Shoes)** dẫn đầu doanh số.
- **Bán kèm (Bundling) các mặt hàng bán chậm với các sản phẩm có hiệu suất cao** có thể giúp tăng doanh số tổng thể.

### 📌 Phân khúc & Giữ chân Khách hàng (Customer Segmentation & Retention)

- **Những khách hàng chi tiêu nhiều nhất chủ yếu là nam giới**, làm nổi bật cơ hội cho các **chương trình khuyến mãi có mục tiêu (targeted promotions)**.
- Một **chương trình khách hàng thân thiết VIP** có thể nâng cao tỷ lệ giữ chân khách hàng và **tăng số lần mua lại (repeat purchases)**.

### 📌 Tối ưu hóa Xử lý đơn hàng & Chi phí Vận chuyển (Order Fulfillment & Shipping Cost Optimization)

- **Các đơn hàng có mức ưu tiên cao (High-priority orders) có chi phí vận chuyển cao hơn đáng kể**.
- Khuyến khích **đặt hàng số lượng lớn (bulk orders) và các tùy chọn giao hàng tiêu chuẩn (standard delivery)** có thể giúp giảm chi phí logistics.

### 📌 Sở thích về Phương thức Thanh toán (Payment Method Preferences)

- **Thẻ tín dụng (Credit cards) chiếm ưu thế trong các giao dịch (74% tổng doanh thu)**, trong khi tỷ lệ áp dụng **ví điện tử (e-wallet) vẫn ở mức thấp**.
- **Đẩy mạnh các ưu đãi thanh toán kỹ thuật số** có thể làm tăng tỷ lệ chuyển đổi khi thanh toán (checkout conversion rates).

---

## 📊 6. Dashboard Tương tác (Interactive Dashboard)

Toàn bộ kết quả phân tích SQL và ML được trực quan hóa thành **Streamlit Dashboard** gồm 4 trang:

| Trang | Nội dung | Highlights |
|-------|---------|-----------|
| **Overview** | 5 KPI cards, xu hướng doanh thu 12 tháng, phân bổ danh mục, Top 5 sản phẩm | Glassmorphism cards, Area chart |
| **Sales & Products** | Combo chart, Running total, Heatmap, Ranking table, Treemap, So sánh quý | Filters: tháng, danh mục, Top N |
| **Customers & Ops** | Demographics, VIP table, Aging histogram, Shipping cost, Payment analysis | Filters: giới tính, thiết bị, ưu tiên |
| **ML Segmentation** | 3 Cluster cards, RFM Radar, Donut phân bổ, Đề xuất Marketing | K-Means (K=3) hardcoded results |

**Chạy Dashboard:**

```bash
cd dashboard
pip install -r requirements.txt
python -m streamlit run Overview.py
```

---

## 💡 7. Đề xuất Kinh doanh (Business Recommendations)

📌 **Tối ưu hóa Hiệu suất Xử lý Đơn hàng**

- Triển khai **tự động hóa trong kho hàng** để giảm thời gian xử lý trung bình (hiện tại là 5,25 ngày).
- Giới thiệu **tính năng theo dõi đơn hàng theo thời gian thực (real-time order tracking)** để nâng cao tính minh bạch và lòng tin của khách hàng.

📌 **Tăng Doanh thu với Các chương trình Khuyến mãi có mục tiêu**

- Tận dụng **xu hướng bán hàng theo mùa** bằng cách tung ra các đợt giảm giá độc quyền vào các tháng cao điểm.
- Quảng cáo các **sản phẩm có thứ hạng cao (Áo phông, Đồng hồ, và Giày)**.

📌 **Cải thiện Chiến lược Giữ chân Khách hàng**

- Tạo ra các **ưu đãi được cá nhân hóa cho khách hàng mua lại** dựa trên lịch sử mua sắm.
- Triển khai **chương trình khách hàng thân thiết (loyalty program)** để khuyến khích chi tiêu lặp lại.

📌 **Giảm Chi phí Vận chuyển mà không ảnh hưởng đến Thời gian Giao hàng**

- Cung cấp **giao hàng tiêu chuẩn miễn phí (free standard shipping) cho các đơn hàng lớn** để giảm chi phí logistics trên mỗi mặt hàng.
- Tối ưu hóa **quan hệ đối tác với các hãng vận chuyển** để có mức giá vận chuyển ưu tiên được chiết khấu.

📌 **Nâng cao Tính linh hoạt khi Thanh toán & Trải nghiệm Thanh toán**

- Khuyến khích **giao dịch bằng ví điện tử và thẻ ghi nợ** bằng cách đưa ra các ưu đãi hoàn tiền (cashback).
- Giới thiệu các tùy chọn **Mua trước, Trả sau (Buy Now, Pay Later - BNPL)** để giảm tỷ lệ bỏ rơi giỏ hàng (cart abandonment).

---

## 🔧 8. Công nghệ sử dụng (Technologies Used)

- **Database**: SQL Server
- **Query Language**: Advanced SQL (T-SQL)
- **Data Processing**: SQL Server / VS Code
- **Dashboard**: Streamlit, Plotly, Pandas
- **Machine Learning**: scikit-learn (K-Means Clustering, RFM)

---

## 🔗 9. Cấu trúc thư mục (Repository Structure)

```text
ECommerceAnalysis/
├── assets/                         # Hình ảnh Database Schema, Kết quả truy vấn
├── data/                           # Dữ liệu raw/cleaned và Data Dictionary
│   ├── raw/
│   ├── cleaned/
│   └── README.md
├── sql/                            # Các scripts T-SQL và Báo cáo Analytics
│   ├── 01_setup_and_import.sql
│   ├── 02_data_normalization.sql
│   ├── 03_advanced_analytics.sql
│   └── README.md
├── machine_learning/               # K-Means Clustering (RFM)
│   ├── customer_segmentation.ipynb
│   └── README.md
├── dashboard/                      # Streamlit Dashboard (Interactive)
│   ├── Overview.py                 # Trang chính: KPI + Xu hướng
│   ├── pages/
│   │   ├── 1_Sales_and_Products.py # Phân tích doanh thu & sản phẩm
│   │   ├── 2_Customers_and_Ops.py  # Khách hàng & Vận hành
│   │   └── 3_ML_Segmentation.py    # Kết quả K-Means Clustering
│   ├── utils/                      # Data loader, Charts, CSS theme
│   └── requirements.txt
├── DATA_PIPELINE.md                # Kiến trúc ELT Pipeline
└── README.md                       # Báo cáo tổng quan dự án (File hiện tại)
```
