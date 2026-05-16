/*
Script: Database Setup & Data Ingestion
Mục tiêu: Khởi tạo Cơ sở dữ liệu và nạp dữ liệu thô (Raw Data) từ tệp CSV vào Staging Area.
*/

-- 1. Khởi tạo Cơ sở dữ liệu
-- Lưu ý: Nếu database đã tồn tại, hãy cẩn trọng khi chạy lại lệnh này.
CREATE DATABASE ECommerceDB;
GO

USE ECommerceDB;
GO

-- 2. KHỞI TẠO STAGING TABLE (BẢNG TRUNG GIAN)
-- Bảng RawOrders đóng vai trò là Landing Zone cho dữ liệu thô.
-- Cấu trúc tất cả các cột bằng kiểu dữ liệu VARCHAR nhằm ngăn chặn 
-- lỗi Data Truncation hoặc Type Mismatch trong quá trình Ingestion (Nạp dữ liệu).
CREATE TABLE RawOrders (
    Order_Date VARCHAR(50),
    Order_Time VARCHAR(50),
    Aging VARCHAR(50),
    Customer_Id VARCHAR(50),
    Gender VARCHAR(50),
    Device_Type VARCHAR(50),
    Customer_Login_type VARCHAR(50),
    Product_Category VARCHAR(100),
    Product VARCHAR(255),
    Sales VARCHAR(50),
    Quantity VARCHAR(50),
    Discount VARCHAR(50),
    Profit VARCHAR(50),
    Shipping_Cost VARCHAR(50),
    Order_Priority VARCHAR(50),
    Payment_method VARCHAR(50)
);
GO

-- 3. THỰC THI QUÁ TRÌNH NẠP DỮ LIỆU (BULK INSERT INGESTION)
-- Tối ưu hóa hiệu suất load (Batch Processing) đối với dữ liệu khối lượng lớn.
BULK INSERT RawOrders
FROM 'C:\Users\ADMIN\Documents\CODE\sql\ECommerceAnalysis\data\raw\E-commerce Dataset.csv'
WITH (
    FIRSTROW = 2,           -- Bỏ qua dòng tiêu đề (Header row)
    FIELDTERMINATOR = ',',  -- Định dạng dấu phân cách cột (Comma separated)
    ROWTERMINATOR = '\n',   -- Định dạng dấu phân cách dòng (Newline delimiter)
    TABLOCK                 -- Áp dụng khóa cấp độ bảng (Table-level lock) để tăng tốc độ I/O
);
GO

-- 4. KIỂM TRA SƠ BỘ (DATA VALIDATION)
-- Lấy mẫu 10 bản ghi đầu tiên để xác thực tính toàn vẹn của dữ liệu sau khi Import.
SELECT TOP 10 * FROM RawOrders;
GO
