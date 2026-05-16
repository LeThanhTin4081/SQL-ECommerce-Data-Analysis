# E-Commerce Data Pipeline Architecture (ELT)

Để đảm bảo hiệu suất, khả năng mở rộng và dễ dàng bảo trì, dự án này áp dụng mô hình **ELT (Extract - Load - Transform)**. Toàn bộ quy trình xử lý dữ liệu được module hóa thành 3 kịch bản (scripts) riêng biệt, tuân thủ các best practices của Data Engineering.

---

## 📦 Bước 1: Extract & Load (Khai thác và Nạp Dữ liệu)
**📍 File thực thi:** `sql/01_setup_and_import.sql`

*   **Mục tiêu:** Di chuyển dữ liệu gốc từ định dạng CSV bên ngoài vào môi trường Cơ sở dữ liệu một cách an toàn và toàn vẹn.
*   **Chi tiết triển khai:**
    *   Khởi tạo cơ sở dữ liệu `ECommerceDB`.
    *   Thiết kế bảng `RawOrders` đóng vai trò là **Staging Table**. Tất cả các cột được định nghĩa là `VARCHAR(MAX)` hoặc `VARCHAR(255)` để tránh lỗi Data Truncation và Format Mismatch trong quá trình Import.
    *   Sử dụng lệnh `BULK INSERT` để tối ưu hóa thời gian load đối với tập dữ liệu có khối lượng lớn (51.290 bản ghi).

---

## 🛠️ Bước 2: Data Normalization (Chuẩn hóa Dữ liệu)
**📍 File thực thi:** `sql/02_data_normalization.sql`

*   **Mục tiêu:** Áp dụng các quy tắc chuẩn hóa (Database Normalization) để chuyển đổi Staging Table (Flat Data) thành cấu trúc Relational Data Model đạt chuẩn 3NF.
*   **Chi tiết triển khai:**
    1.  **Customers (Dimension Table):** Trích xuất thông tin khách hàng duy nhất. Xử lý các data anomalies (khách hàng có nhiều phương thức đăng nhập) bằng cách áp dụng hàm Aggregation (`MAX()`) kết hợp `GROUP BY`.
    2.  **Products (Dimension Table):** Trích xuất danh mục sản phẩm duy nhất. Sử dụng thuộc tính `IDENTITY` để tự động khởi tạo Surrogate Key (`Product_Id`).
    3.  **Categories (Dimension Table):** Import dữ liệu phân cấp danh mục (Hierarchical Data) chứa thuộc tính `Parent_Category_Id` để phục vụ các bài toán phân tích đệ quy.
    4.  **Orders (Fact Table):** Xây dựng bảng trung tâm lưu trữ thông tin giao dịch. Thực hiện Data Type Casting (ép kiểu dữ liệu) sang dạng chuẩn (`INT`, `FLOAT`, `DATE`). Đồng thời, thiết lập các ràng buộc toàn vẹn (Foreign Key Constraints) liên kết với các bảng Dimension.

---

## 📊 Bước 3: Advanced Analytics (Phân tích Kinh doanh Nâng cao)
**📍 File thực thi:** `sql/03_advanced_analytics.sql`

*   **Mục tiêu:** Khai thác cơ sở dữ liệu đã chuẩn hóa để rút ra các thông tin chi tiết (insights) phục vụ ra quyết định kinh doanh.
*   **Kỹ thuật SQL áp dụng:**
    *   **Common Table Expressions (CTEs):** Cấu trúc hóa các luồng logic phân tích phức tạp thành các khối mã dễ đọc, dễ tái sử dụng.
    *   **Recursive CTEs:** Xử lý và truy xuất dữ liệu phân cấp (cây danh mục hàng hóa) từ bảng `Categories`.
    *   **Window Functions (`RANK`, `DENSE_RANK`, `SUM() OVER`, `LAG`, `LEAD`):** Triển khai các bài toán tính toán nâng cao như: xếp hạng mặt hàng bán chạy, theo dõi doanh thu lũy kế (Running Total), và tính toán tăng trưởng qua từng khoảng thời gian (MoM/YoY Growth).
