# 📂 Dữ liệu dự án (Data Directory)

Thư mục này lưu trữ toàn bộ dữ liệu phục vụ phân tích Thương mại điện tử (E-Commerce), được tổ chức theo hai giai đoạn xử lý: **raw** (dữ liệu thô) và **cleaned** (dữ liệu đã được chuẩn hóa).

---

## 1. Dữ liệu thô (raw data)

Dữ liệu nguyên bản được tải về từ Kaggle, chứa toàn bộ lịch sử giao dịch bán hàng chưa qua bất kỳ bước xử lý nào.

| Thông tin           | Chi tiết                                                                                    |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **File tổng hợp**   | `E-commerce Dataset.csv`                                                                    |
| **Nguồn gốc**       | [Kaggle E-Commerce Dataset](https://www.kaggle.com/datasets/mervemenekse/ecommerce-dataset) |
| **Giai đoạn**       | Toàn bộ năm 2018 (Tháng 1 - Tháng 12)                                                        |
| **Tổng số bản ghi** | 51,290 dòng                                                                                 |
| **Số cột**          | 16                                                                                          |

### Cấu trúc cột (Dữ liệu gốc)

| #   | Tên cột               | Mô tả                               |
| --- | --------------------- | ----------------------------------- |
| 1   | `Customer_Id`         | Mã định danh khách hàng             |
| 2   | `Order_Date`          | Ngày đặt hàng                       |
| 3   | `Time`                | Giờ đặt hàng                        |
| 4   | `Aging`               | Thời gian chờ xử lý đơn hàng (ngày) |
| 5   | `Gender`              | Giới tính khách hàng                |
| 6   | `Device_Type`         | Thiết bị sử dụng (Web/Mobile)       |
| 7   | `Customer_Login_type` | Loại tài khoản đăng nhập            |
| 8   | `Product_Category`    | Danh mục sản phẩm                   |
| 9   | `Product`             | Tên sản phẩm cụ thể                 |
| 10  | `Sales`               | Doanh thu                           |
| 11  | `Quantity`            | Số lượng sản phẩm bán ra            |
| 12  | `Discount`            | Mức giảm giá áp dụng                |
| 13  | `Profit`              | Lợi nhuận thu được                  |
| 14  | `Shipping_Cost`       | Chi phí vận chuyển                  |
| 15  | `Order_Priority`      | Mức độ ưu tiên của đơn hàng         |
| 16  | `Payment_method`      | Phương thức thanh toán              |

---

## 2. Dữ liệu đã xử lý (cleaned data)

Bộ dữ liệu đã qua tiền xử lý, bóc tách và chuẩn hóa (Normalization) thành các bảng quan hệ đạt chuẩn 3NF, sẵn sàng phục vụ phân tích bằng T-SQL và Data Visualization.

| Thông tin                 | Chi tiết                                    |
| ------------------------- | ------------------------------------------- |
| **Tổng số bảng (files)**  | 4 (Orders, Customers, Products, Categories) |
| **Phương thức chuẩn hóa** | SQL Server (ELT Pipeline)                   |

### Các file thành phần sau chuẩn hóa

Dữ liệu thô (Flat Table) được phân tách thành 1 bảng sự kiện (Fact) và 3 bảng thứ nguyên (Dimension):

| File             | Loại bảng | Tác dụng                                             |
| ---------------- | --------- | ---------------------------------------------------- |
| `Customers.csv`  | Dimension | Chứa thông tin nhân khẩu học (đã gộp trùng lặp).     |
| `Products.csv`   | Dimension | Danh sách các sản phẩm và khóa đại diện.             |
| `Categories.csv` | Dimension | Dữ liệu danh mục phục vụ phân tích đệ quy.           |
| `Orders.csv`     | Fact      | Bảng trung tâm chứa các chỉ số doanh thu, lợi nhuận. |

#### 2.1. Bảng Customers (Dimension)

Chứa thông tin nhân khẩu học của khách hàng duy nhất (đã xử lý trùng lặp bằng `MAX()`).

| Tên cột               | Kiểu dữ liệu | Mô tả                                |
| --------------------- | ------------ | ------------------------------------ |
| `Customer_Id`         | INT (PK)     | Mã định danh khách hàng (Khóa chính) |
| `Gender`              | VARCHAR      | Giới tính khách hàng                 |
| `Device_Type`         | VARCHAR      | Thiết bị sử dụng chính               |
| `Customer_Login_type` | VARCHAR      | Hình thức đăng nhập                  |

#### 2.2. Bảng Products (Dimension)

Danh sách các sản phẩm bán ra được lọc duy nhất (DISTINCT).

| Tên cột            | Kiểu dữ liệu | Mô tả                                        |
| ------------------ | ------------ | -------------------------------------------- |
| `Product_Id`       | INT (PK)     | Mã đại diện sản phẩm tự tăng (Surrogate Key) |
| `Product_Name`     | VARCHAR      | Tên sản phẩm cụ thể                          |
| `Product_Category` | VARCHAR      | Danh mục chứa sản phẩm đó                    |

#### 2.3. Bảng Categories (Dimension)

Dữ liệu danh mục phân cấp phục vụ phân tích đệ quy (Recursive CTE).

| Tên cột              | Kiểu dữ liệu | Mô tả                                  |
| -------------------- | ------------ | -------------------------------------- |
| `Category_Id`        | INT (PK)     | Mã danh mục                            |
| `Category_Name`      | VARCHAR      | Tên danh mục                           |
| `Parent_Category_Id` | INT (FK)     | Mã danh mục cha (dùng để nối dạng cây) |

#### 2.4. Bảng Orders (Fact)

Bảng trung tâm lưu trữ các chỉ số kinh doanh và các khóa ngoại liên kết.

| Tên cột          | Kiểu dữ liệu | Mô tả                                   |
| ---------------- | ------------ | --------------------------------------- |
| `Order_Id`       | INT (PK)     | Mã đơn hàng tự tăng                     |
| `Order_Date`     | DATE         | Ngày đặt hàng                           |
| `Order_Time`     | TIME         | Giờ đặt hàng                            |
| `Aging`          | FLOAT        | Thời gian chờ xử lý đơn hàng (ngày)     |
| `Customer_Id`    | INT (FK)     | Mã khách hàng (Liên kết bảng Customers) |
| `Product_Id`     | INT (FK)     | Mã sản phẩm (Liên kết bảng Products)    |
| `Sales`          | FLOAT        | Doanh thu                               |
| `Quantity`       | INT          | Số lượng bán ra                         |
| `Discount`       | FLOAT        | Mức giảm giá                            |
| `Profit`         | FLOAT        | Lợi nhuận                               |
| `Shipping_Cost`  | FLOAT        | Chi phí vận chuyển                      |
| `Order_Priority` | VARCHAR      | Mức độ ưu tiên                          |
| `Payment_method` | VARCHAR      | Phương thức thanh toán                  |
