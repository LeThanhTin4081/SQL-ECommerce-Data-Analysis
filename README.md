# **Phân tích Quy trình Xử lý Đơn hàng E-Commerce (E-Commerce Order Fulfillment Analysis)**  

## 📖 **Tổng quan Dự án (Project Overview)**  
Dự án này phân tích **quy trình xử lý đơn hàng (order fulfillment process)** của một doanh nghiệp thương mại điện tử (e-commerce), bao gồm **xu hướng bán hàng (sales trends), hiệu suất sản phẩm (product performance), phân khúc khách hàng (customer segmentation), tối ưu hóa chi phí vận chuyển (shipping cost optimization), và phân tích phương thức thanh toán (payment method analysis)**.  

Sử dụng **Các kỹ thuật SQL nâng cao (Advanced SQL Techniques)** kết hợp tư duy thiết kế **Data Pipeline (ELT)**, dự án trích xuất những thông tin chuyên sâu để giúp doanh nghiệp **cải thiện logistics, tăng doanh số, và nâng cao mức độ hài lòng của khách hàng**.  

---

## 🎯 **Mục tiêu (Objectives)**  
✔ **Tối ưu hóa hiệu suất xử lý đơn hàng** – Theo dõi sự chậm trễ và cải thiện thời gian hoàn thành đơn hàng.  
✔ **Xác định các sản phẩm bán chạy nhất** – Hiểu rõ những sản phẩm nào tạo ra doanh thu cao nhất.  
✔ **Phân khúc khách hàng giá trị cao** – Phân tích hành vi chi tiêu và mức độ tương tác của khách hàng.  
✔ **Giảm chi phí vận chuyển** – Đánh giá sự biến động chi phí dựa trên mức độ ưu tiên của đơn hàng (order priority).  
✔ **Xác định phương thức thanh toán ưa thích** – Xác định sở thích thanh toán của khách hàng để có chiến lược tài chính tốt hơn.  

---

## 📂 **Tổng quan Dữ liệu (Dataset Overview)**  
- **Nguồn dữ liệu (Source)**: Hồ sơ giao dịch E-Commerce với **51.290 dòng** và **16 cột**. ([E-commerce Dataset trên Kaggle](https://www.kaggle.com/datasets/mervemenekse/ecommerce-dataset))  
- **Tiền xử lý dữ liệu (Data Transformation)**: Dữ liệu thô đã được **chuẩn hóa (normalized) thành 4 bảng** để truy vấn hiệu quả hơn:
  - `Orders` – Chi tiết đơn hàng, bao gồm doanh số (sales), lợi nhuận (profit), và chi phí vận chuyển (shipping costs).  
  - `Customers` – Thông tin nhân khẩu học của khách hàng như giới tính (gender), loại đăng nhập (login type), và thiết bị (device).  
  - `Products` – Danh sách tất cả các sản phẩm và danh mục của chúng.  
  - `Categories` – Phân loại rộng hơn của các loại sản phẩm.  

---

## 🚀 **Các kỹ thuật SQL Nâng cao được sử dụng (Advanced SQL Techniques Used)**  
Dự án này kết hợp **Các kỹ thuật SQL Nâng cao** để cải thiện hiệu suất truy vấn (query performance), đơn giản hóa quá trình phân tích và tạo ra những thông tin sâu sắc:  

### **1️⃣ Window Functions**  
   - Được sử dụng để **xếp hạng các sản phẩm bán chạy (rank top-selling products)** và **tính toán doanh số lũy kế theo thời gian (cumulative sales)**.  
   - Giúp **hiểu rõ xu hướng nhu cầu sản phẩm một cách linh hoạt**.  

### **2️⃣ Common Table Expressions (CTEs)**  
   - Đơn giản hóa **phân tích phân khúc khách hàng** bằng cách tổ chức các câu truy vấn phức tạp (complex queries).  
   - Tăng tính dễ đọc và duy trì **việc thực thi truy vấn theo mô-đun (modular query execution)**.  

### **3️⃣ Ranking Functions (RANK() OVER)**  
   - Gán thứ hạng cho các sản phẩm dựa trên tổng doanh số.  
   - Hữu ích cho việc **xác định các mặt hàng có hiệu suất tốt nhất một cách hiệu quả**.  

### **4️⃣ Partitioning & Indexing (Phân vùng & Đánh chỉ mục để Tối ưu hiệu suất)**  
   - Được sử dụng để **tối ưu hóa truy vấn (query optimization)**, đặc biệt là với các tập dữ liệu lớn.  
   - Đảm bảo **trích xuất thông tin nhanh hơn** từ dữ liệu đơn hàng và khách hàng.  

---

## 📊 **Thông tin chi tiết & Phát hiện Kinh doanh (Business Insights & Findings)**  

### **📌 Phân tích Doanh số & Doanh thu (Sales & Revenue Analysis)**  
- Doanh nghiệp đã tạo ra **7,8 triệu USD tổng doanh số**, với **biên lợi nhuận 3,6 triệu USD**.  
- **Doanh số đạt đỉnh vào tháng 5 và tháng 11**, cho thấy những **xu hướng nhu cầu theo mùa vụ** rõ rệt.  

### **📌 Các sản phẩm bán chạy nhất (Top-Selling Products)**  
- Các danh mục bán chạy nhất là **Thời trang (Fashion) và Giày dép (Footwear)**, với **Áo phông (T-Shirts), Đồng hồ (Watches), và Giày chạy bộ (Running Shoes)** dẫn đầu doanh số.  
- **Bán kèm (Bundling) các mặt hàng bán chậm với các sản phẩm có hiệu suất cao** có thể giúp tăng doanh số tổng thể.  

### **📌 Phân khúc & Giữ chân Khách hàng (Customer Segmentation & Retention)**  
- **Những khách hàng chi tiêu nhiều nhất chủ yếu là nam giới**, làm nổi bật cơ hội cho các **chương trình khuyến mãi có mục tiêu (targeted promotions)**.  
- Một **chương trình khách hàng thân thiết VIP** có thể nâng cao tỷ lệ giữ chân khách hàng và **tăng số lần mua lại (repeat purchases)**.  

### **📌 Tối ưu hóa Xử lý đơn hàng & Chi phí Vận chuyển (Order Fulfillment & Shipping Cost Optimization)**  
- **Các đơn hàng có mức ưu tiên cao (High-priority orders) có chi phí vận chuyển cao hơn đáng kể**.  
- Khuyến khích **đặt hàng số lượng lớn (bulk orders) và các tùy chọn giao hàng tiêu chuẩn (standard delivery)** có thể giúp giảm chi phí logistics.  

### **📌 Sở thích về Phương thức Thanh toán (Payment Method Preferences)**  
- **Thẻ tín dụng (Credit cards) chiếm ưu thế trong các giao dịch (74% tổng doanh thu)**, trong khi tỷ lệ áp dụng **ví điện tử (e-wallet) vẫn ở mức thấp**.  
- **Đẩy mạnh các ưu đãi thanh toán kỹ thuật số** có thể làm tăng tỷ lệ chuyển đổi khi thanh toán (checkout conversion rates).  

---

## 💡 **Đề xuất Kinh doanh (Business Recommendations)**  
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

## 🔧 **Công nghệ sử dụng (Technologies Used)**  
- **Database**: SQL Server  
- **Query Language**: Advanced SQL (T-SQL)  
- **Data Processing**: SQL Server / VS Code  

---

## 📂 **Cấu trúc Thư mục (Repository Structure)**  
```text
📁 data                 
 ┣ 📁 raw               <-- File dataset thô ban đầu (E-commerce Dataset.csv)
 ┗ 📁 cleaned           <-- Các file dữ liệu đã được làm sạch và chuẩn hóa (nếu có)
📁 sql                  
 ┣ 📜 01_setup_and_import.sql   <-- Script nạp dữ liệu thô (ETL)
 ┣ 📜 02_data_normalization.sql <-- Script chuẩn hóa cấu trúc 3NF
 ┗ 📜 03_advanced_analytics.sql <-- Script phân tích Insight kinh doanh
📜 DATA_PIPELINE.md     <-- Tài liệu giải thích kiến trúc Data Pipeline
📜 README.md            <-- Tài liệu tổng quan dự án
```

---

## 🔮 **Giai đoạn 2: Định hướng Tích hợp Machine Learning (Upcoming Phase)**  
Sau khi hoàn thiện nền tảng Data Warehouse và Data Model bằng SQL Server, dự án sẽ được mở rộng sang Phân tích Dự đoán (Predictive Analytics) bằng Machine Learning:

📌 **Customer Segmentation (Phân cụm Khách hàng):** 
Áp dụng thuật toán **K-Means Clustering** trên dữ liệu RFM (Recency, Frequency, Monetary) được trích xuất từ SQL để tự động phân nhóm khách hàng (VIP, Bargain Hunters, Churn-risk).

📌 **Profit/Sales Prediction (Dự đoán Lợi nhuận/Doanh thu):** 
Sử dụng các mô hình học có giám sát như **XGBoost Regressor** hoặc **Random Forest** để dự báo biên lợi nhuận (Profit Margin) của các chiến dịch giảm giá và chính sách vận chuyển mới.

📌 **End-to-end Data Dashboard:** 
Kết nối trực tiếp Database SQL Server với **Power BI** để xây dựng báo cáo động (Interactive Dashboard), kết hợp cả dữ liệu lịch sử và kết quả dự báo từ AI.
