# **🛍️ Dự Án Phân Tích E-Commerce Toàn Diện (End-to-End E-Commerce Analytics)**

![Banner](assets/avt.png)

## **🔎 1. Tổng quan dự án**

Dự án này là một **giải pháp phân tích dữ liệu toàn diện (Full-Stack Data Solution)** cho doanh nghiệp thương mại điện tử dựa trên tập dữ liệu lịch sử năm 2018 (51,290 đơn hàng). Quy trình triển khai chuyên nghiệp và khép kín qua 4 trụ cột cốt lõi:

| Trụ cột     | 1. Xây dựng ELT Pipeline       | 2. T-SQL Advanced Analytics     | 3. ML Customer Segmentation   | 4. Streamlit Interactive Dashboard |
| :---------- | :----------------------------- | :------------------------------ | :---------------------------- | :--------------------------------- |
| **Công cụ** | SQL Server, `BULK INSERT`, 3NF | Window Functions, Recursive CTE | Python, Scikit-Learn, K-Means | Streamlit, Plotly, Custom CSS      |

> 💡 **Lưu ý dành cho Nhà tuyển dụng / Technical Reviewer:**
> File `README.md` này đóng vai trò là **Báo cáo tổng quan**. Bạn có thể truy cập chi tiết mã nguồn và báo cáo từng phần thông qua bảng liên kết nhanh dưới đây:

| Phân khu                  | Mô tả chi tiết                                                        | Liên kết nhanh                           |
| :------------------------ | :-------------------------------------------------------------------- | :--------------------------------------- |
| **1. Dữ liệu (Data)**     | Cấu trúc dữ liệu raw/cleaned, Data Dictionary chi tiết                | [data/](./data/)                         |
| **2. Kiến trúc Pipeline** | Luồng xử lý ELT, sơ đồ Database Schema chuẩn 3NF                      | [DATA_PIPELINE.md](./DATA_PIPELINE.md)   |
| **3. Báo cáo Analytics**  | 10 truy vấn T-SQL phức tạp kèm hình ảnh kết quả và Key Insights       | [sql/](./sql/)                           |
| **4. ML Segmentation**    | Pipeline học máy, K-Means Clustering và hồ sơ các cụm khách hàng      | [machine_learning/](./machine_learning/) |
| **5. Dashboard**          | Streamlit Multi-page App, Custom CSS theme và Plotly charts tương tác | [dashboard/](./dashboard/)               |

---

## **🎯 2. Mục tiêu dự án (Objectives)**

- **Chuẩn hóa Cơ sở Dữ liệu:** Chuyển đổi dữ liệu phẳng thô (Kaggle) thành mô hình cơ sở dữ liệu quan hệ đạt chuẩn 3NF (gồm Fact và Dimension) để lưu trữ khoa học.
- **Phân tích & Khai thác Insight:** Viết các truy vấn SQL để đo lường các chỉ số tài chính (doanh thu, lợi nhuận), xu hướng mùa vụ và hiệu suất logistics (thời gian xử lý đơn hàng).
- **Phân cụm Khách hàng:** Ứng dụng mô hình Machine Learning K-Means phân loại khách hàng thành 3 cụm hành vi mua sắm RFM rõ rệt để định hướng chiến lược tiếp thị.
- **Trực quan hóa Dữ liệu:** Thiết kế và xây dựng Streamlit Dashboard tương tác đa trang giúp người dùng dễ dàng theo dõi và lọc số liệu động theo thời gian thực.

---

## **🔆 3. Kỹ năng dữ liệu được thể hiện**

| Vai trò                          | Công cụ & Kỹ thuật áp dụng                                                                                                              |
| :------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Nạp & Chuẩn hóa Dữ liệu**   | Nhập dữ liệu từ file CSV thô vào SQL Server bằng lệnh `BULK INSERT`, tổ chức lại cấu trúc bảng Fact & Dimension cơ bản                  |
| **2. Truy vấn Dữ liệu (SQL)**    | Viết truy vấn lấy số liệu, kết nối bảng (Joins), gom nhóm dữ liệu (Aggregation) và ứng dụng một số Window Functions (`RANK()`, `SUM()`) |
| **3. Phân tích Khách hàng (ML)** | Sử dụng Python (Pandas, Scikit-Learn) để xử lý dữ liệu RFM và phân cụm khách hàng bằng thuật toán K-Means cơ bản                        |
| **4. Trực quan hóa (Dashboard)** | Thiết kế giao diện báo cáo tương tác đa trang và vẽ các biểu đồ Plotly trực quan bằng Streamlit                                         |

---

## **📌 4. Quy trình thực hiện**

### **4.1. Extract & Load (Khai thác và Nạp Dữ liệu)**

Xây dựng kịch bản tự động khởi tạo cơ sở dữ liệu `ECommerceDB` và nạp siêu tốc 51,290 bản ghi từ file `.csv` thô vào bảng Staging (`RawOrders`) bằng `BULK INSERT`, áp dụng ép kiểu an toàn `VARCHAR(MAX)` để ngăn chặn lỗi dữ liệu khi nhập thô.

> 📁 **Mã nguồn:** [`sql/01_setup_and_import.sql`](./sql/01_setup_and_import.sql)

### **4.2. Data Normalization (Chuẩn hóa cấu trúc 3NF)**

Bóc tách bảng phẳng Staging thành mô hình quan hệ 3NF gồm 3 bảng Dimension (`Customers`, `Products`, `Categories`) và 1 bảng Fact (`Orders`). Việc này giúp loại bỏ trùng lặp dữ liệu, đảm bảo tính toàn vẹn (Referential Integrity) và tăng tốc hiệu năng truy xuất.

> 📁 **Xem sơ đồ Database Schema và kỹ thuật xử lý:** [`DATA_PIPELINE.md`](./DATA_PIPELINE.md)

### **4.3. Advanced SQL Analytics (Phân tích Kinh doanh)**

Thực thi 10 bài toán phân tích kinh doanh đa chiều từ Tài chính, Logistics đến Vận hành thông qua các kỹ thuật SQL nâng cao:

- **Window Functions:** Dùng `RANK() OVER` xếp hạng doanh thu và `SUM() OVER(ORDER BY)` để tính dòng tiền tích lũy (Running Total).
- **Recursive CTE:** Duyệt cây đệ quy đa cấp để vẽ cây danh mục cha - con (`Parent_Category_Id` -> `Category_Id`).
  > 📁 **Xem toàn bộ 10 Báo cáo Insights kèm hình ảnh kết quả:** [`sql/`](./sql/)

### **4.4. Machine Learning Customer Segmentation (Phân khúc Khách hàng bằng Học máy)**

Xây dựng pipeline phân cụm khách hàng nâng cao trên Python (Jupyter Notebook):

- Trích xuất đặc trưng **RFM** (Recency, Frequency, Monetary) kết hợp `Avg_Discount` và `Avg_Profit` từ Database.
- Chuẩn hóa bằng `StandardScaler`, xác định số lượng cụm tối ưu $K=3$ qua phương pháp Elbow và Silhouette Score.
- Phân nhóm 38,995 khách hàng thành 3 cụm hành vi rõ rệt: _VIP Loyal_, _Premium One-Time_, và _Low-Value_.
  > 📁 **Chi tiết notebook và báo cáo:** [`machine_learning/`](./machine_learning/)

### **4.5. Streamlit Interactive Dashboard (Thiết kế Dashboard Tương tác)**

Chuyển hóa toàn bộ SQL Analytics và kết quả Machine Learning thành Dashboard trực quan:

- Sử dụng Streamlit làm framework, tích hợp hơn 15 biểu đồ Plotly tương tác.
- Áp dụng ngôn ngữ thiết kế Premium Dark Theme, hiệu ứng hover, thẻ KPI Glassmorphism và khả năng lọc dữ liệu theo thời gian thực (Sidebar Filters).
  > 📁 **Chi tiết giao diện:** [`dashboard/`](./dashboard/)

---

## **📊 5. Thông tin chi tiết & Phát hiện Kinh doanh (Business Insights & Findings)**

### 📌 Phân tích Doanh số & Tài chính (Financial Performance)

- Doanh nghiệp đạt doanh thu xuất sắc **$7.81M** với biên lợi nhuận ròng rất ấn tượng **46.22%** (Lợi nhuận ròng đạt **$3.61M**), chứng minh cấu trúc định giá sản phẩm và tối ưu chi phí vận hành cực kỳ tốt.
- Doanh thu bộc lộ rõ tính mùa vụ: Tháng 2 chạm đáy, nhưng bùng nổ mạnh mẽ vào cuối năm. Trong đó, Tháng 5 đạt **$824.5k** và Tháng 11 (Black Friday) đạt đỉnh cao nhất năm với **$877.9k**, tạo ra cơ hội lớn để tối ưu chuỗi cung ứng trước mùa cao điểm.

### 📌 Các sản phẩm bán chạy nhất (Top-Selling Products)

- Ngành hàng **Thời trang (Fashion)** đóng vai trò là động cơ tăng trưởng chính khi chiếm trọn 7/10 vị trí sản phẩm bán chạy nhất doanh nghiệp.
- **Áo thun (T-Shirts - $578.3k)** và **Đồng hồ Titak (Titak watch - $531.5k)** là hai sản phẩm thống trị doanh số. Chiến lược bán kèm (Bundling) các mặt hàng bán chậm với hai sản phẩm chủ lực này có thể kích thích tiêu dùng chéo hiệu quả.

### 📌 Chân dung & Phân khúc Khách hàng (Customer Profiling & AI Segmentation)

- **Top 10 khách hàng VIP** (chi tiêu nhiều nhất) có mức tích lũy từ **$800 đến $925** mỗi người (trung bình **$860**), trong đó đa số là Nam giới.
- **Mô hình K-Means** phân nhóm thành công 3 cụm khách hàng rõ rệt:
  - **VIP Loyal (23% khách hàng):** Nhóm mua hàng gần đây nhất (trung bình 92 ngày), mua nhiều nhất (2.24 lần) và chi tiêu trung bình cao nhất ($357/đơn). Nhóm này chủ yếu là **Nam giới (79%)**.
  - **Premium One-Time (33% khách hàng):** Nhóm mua 1 lần nhưng biên lợi nhuận/đơn cực lớn ($120/đơn). Cần chiến dịch Cross-sell để chuyển đổi họ thành VIP.
  - **Low-Value (44% khách hàng):** Nhóm đông nhất nhưng chi tiêu rất thấp ($102/đơn), có nguy cơ rời bỏ cao.

### 📌 Tối ưu hóa Xử lý đơn hàng & Vận chuyển (Order Fulfillment & Logistics)

- **Điểm nghẽn vận hành:** Thời gian xử lý đơn hàng trung bình (Aging) ở mức **5.26 ngày**. Đây là cảnh báo đỏ cho thấy quy trình kho bãi (Warehouse Operations) đang bị quá tải.
- **Chi phí Logistics:** Cấu trúc chi phí vận chuyển được đàm phán rất tốt ở mức giá sàn cố định (Flat-rate) dao động hẹp từ $6.94 đến $7.22. Tuy nhiên, các đơn hàng ưu tiên khẩn cấp vẫn làm tăng chi phí phụ phí đáng kể, đòi hỏi quy trình phân bổ kho tối ưu hơn để giảm đơn khẩn cấp.

### 📌 Kênh thanh toán & Thói quen mua sắm (Payment Methods)

- **Thẻ tín dụng (Credit Card)** thống trị tuyệt đối với **74.48% tổng doanh thu** ($5.82M), cho thấy khách hàng ưa chuộng thanh toán không tiền mặt.
- Theo sau là Lệnh chuyển tiền (**18.70%**) và Ví điện tử (E-wallet) mới chỉ chiếm **5.41%**, mở ra cơ hội liên kết ví điện tử để tăng khuyến mãi hoàn tiền (cashback) nhằm kích thích chuyển đổi giỏ hàng.

---

## **📊 6. Dashboard Tương tác (Interactive Dashboard)**

Toàn bộ kết quả phân tích SQL và ML được trực quan hóa thành **Streamlit Dashboard** gồm 4 trang:

| Trang                | Nội dung                                                                   |
| -------------------- | -------------------------------------------------------------------------- |
| **Overview**         | 5 KPI cards, xu hướng doanh thu 12 tháng, phân bổ danh mục, Top 5 sản phẩm |
| **Sales & Products** | Combo chart, Running total, Heatmap, Ranking table, Treemap, So sánh quý   |
| **Customers & Ops**  | Demographics, VIP table, Aging histogram, Shipping cost, Payment analysis  |
| **ML Segmentation**  | 3 Cluster cards, RFM Radar, Donut phân bổ, Đề xuất Marketing               |

👉 **Xem chi tiết hình ảnh giao diện và báo cáo tại:** [dashboard/](./dashboard/)

---

## **💡 7. Đề xuất Kinh doanh (Business Recommendations)**

📌 **Tối ưu hóa Hiệu suất Xử lý Đơn hàng**

- Triển khai **tự động hóa trong kho hàng** để giảm thời gian xử lý trung bình (hiện tại là 5.26 ngày).
- Giới thiệu **tính năng theo dõi đơn hàng theo thời gian thực (real-time order tracking)** để nâng cao tính minh bạch và lòng tin của khách hàng.

📌 **Tăng Doanh thu với Các chương trình Khuyến mãi có mục tiêu**

- Tận dụng **xu hướng bán hàng theo mùa** bằng cách tung ra các đợt giảm giá độc quyền vào các tháng cao điểm.
- Quảng cáo các **sản phẩm có thứ hạng cao (Áo phông, Đồng hồ, và Giày)**.

📌 **Chiến lược Tiếp thị theo Phân khúc Khách hàng AI (ML-Driven Segment Strategy)**
Dựa trên kết quả phân cụm bằng thuật toán K-Means, áp dụng 3 chiến lược tiếp thị cá nhân hóa chuyên biệt để tối ưu hóa tỷ lệ chuyển đổi và tăng trưởng vòng đời khách hàng (LTV):

- **Cụm VIP Loyal (23% khách hàng - Động cơ doanh thu):** Nhóm trung thành, chi tiêu lớn, chủ yếu là Nam giới (79%).
  - _Chiến lược:_ Xây dựng chương trình **đặc quyền VIP (Loyalty Club)**, gửi thông tin ưu đãi sớm (early access) cho các bộ sưu tập thời trang nam và sản phẩm đồng hồ cao cấp. Thiết kế các đặc quyền phi tài chính như chăm sóc khách hàng VIP riêng biệt.
- **Cụm Premium One-Time (33% khách hàng - Tiềm năng bứt phá):** Nhóm mua 1 lần nhưng sẵn sàng chi tiêu cao, mang lại biên lợi nhuận lớn nhất ($120/đơn) nhưng đã lâu chưa mua lại (trung bình 158 ngày).
  - _Chiến lược:_ Kích hoạt chiến dịch **Win-back / Re-engagement** tự động thông qua email/SMS cá nhân hoá. Gợi ý các sản phẩm bán chéo (Cross-sell) hoặc nâng cấp (Up-sell) liên quan trực tiếp đến mặt hàng họ đã từng mua kèm mã giảm giá giới hạn thời gian (tạo cảm giác khan hiếm).
- **Cụm Low-Value (44% khách hàng - Tối ưu hóa chi phí):** Nhóm đông nhất nhưng chi tiêu rất thấp ($102/đơn), tần suất mua thấp và nguy cơ rời bỏ (churn) cực cao.
  - _Chiến lược:_ Tự động hóa tiếp thị với các voucher giảm giá sâu để xả hàng tồn kho nhóm dưới, nhưng cần **kiểm soát chặt chẽ ngân sách tiếp thị (ROI-focused)** để không bào mòn biên lợi nhuận vốn đã rất mỏng của nhóm này.

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

## **🔗 8. Cấu trúc thư mục (Repository Structure)**

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
