USE ECommerceDB;
GO

/*
Script: Data Normalization
Mục tiêu: Chuẩn hóa dữ liệu thô (Flat Table) thành các bảng quan hệ (Relational Tables) đạt chuẩn 3NF.
*/

-- 0. Xóa các bảng cũ nếu tồn tại trước khi tạo mới
-- Tuân thủ thứ tự xóa từ bảng Con (chứa Foreign Key) đến bảng Cha (chứa Primary Key).
IF OBJECT_ID('Orders', 'U') IS NOT NULL DROP TABLE Orders;
IF OBJECT_ID('Customers', 'U') IS NOT NULL DROP TABLE Customers;
IF OBJECT_ID('Products', 'U') IS NOT NULL DROP TABLE Products;
IF OBJECT_ID('Categories', 'U') IS NOT NULL DROP TABLE Categories;
GO

-- 1. Khởi tạo và nạp dữ liệu bảng Customers (Dimension Table)
-- Sử dụng GROUP BY và hàm tập hợp MAX() để xử lý các bản ghi dị thường (data anomalies)
CREATE TABLE Customers (
    Customer_Id INT PRIMARY KEY,
    Gender VARCHAR(50),
    Device_Type VARCHAR(50),
    Customer_Login_type VARCHAR(50)
);
GO

INSERT INTO Customers (Customer_Id, Gender, Device_Type, Customer_Login_type)
SELECT 
    CAST(Customer_Id AS INT), 
    MAX(Gender), 
    MAX(Device_Type), 
    MAX(Customer_Login_type)
FROM RawOrders
WHERE Customer_Id IS NOT NULL AND Customer_Id <> ''
GROUP BY CAST(Customer_Id AS INT);
GO

-- 2. Khởi tạo và nạp dữ liệu bảng Products (Dimension Table)
-- Lọc các sản phẩm duy nhất (DISTINCT) từ dữ liệu thô.
CREATE TABLE Products (
    Product_Id INT IDENTITY(1,1) PRIMARY KEY,
    Product_Name VARCHAR(255),
    Product_Category VARCHAR(100)
);
GO

INSERT INTO Products (Product_Name, Product_Category)
SELECT DISTINCT Product, Product_Category
FROM RawOrders
WHERE Product IS NOT NULL AND Product <> '';
GO

-- 3. Khởi tạo và nạp dữ liệu bảng Categories (Dimension Table)
-- Khởi tạo bảng danh mục có tính chất phân cấp (Hierarchical Data) thông qua Parent_Category_Id.
CREATE TABLE Categories (
    Category_Id INT PRIMARY KEY,
    Category_Name VARCHAR(100),
    Parent_Category_Id INT NULL
);
GO

BULK INSERT Categories
FROM 'C:\Users\ADMIN\Documents\CODE\sql\ECommerceAnalysis\data\cleaned\Categories.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO

-- 4. Khởi tạo và nạp dữ liệu bảng Orders (Fact Table)
-- Khai báo rõ ràng các Ràng buộc Khóa Ngoại (Foreign Key Constraints) tham chiếu đến Customers và Products.
CREATE TABLE Orders (
    Order_Id INT IDENTITY(1,1) PRIMARY KEY,
    Order_Date DATE,
    Order_Time TIME,
    Aging FLOAT,
    Customer_Id INT FOREIGN KEY REFERENCES Customers(Customer_Id),
    Product_Id INT FOREIGN KEY REFERENCES Products(Product_Id),
    Sales FLOAT,
    Quantity INT,
    Discount FLOAT,
    Profit FLOAT,
    Shipping_Cost FLOAT,
    Order_Priority VARCHAR(50),
    Payment_method VARCHAR(50)
);
GO

-- Nạp dữ liệu vào Fact Table, ép kiểu (CAST) từ VARCHAR sang định dạng chuẩn.
-- Thực hiện INNER JOIN với bảng Products để map Surrogate Key (Product_Id).
INSERT INTO Orders (
    Order_Date, Order_Time, Aging, Customer_Id, Product_Id, 
    Sales, Quantity, Discount, Profit, Shipping_Cost, 
    Order_Priority, Payment_method
)
SELECT 
    CAST(r.Order_Date AS DATE),
    CAST(r.Order_Time AS TIME),
    CASE WHEN r.Aging = '' THEN NULL ELSE CAST(r.Aging AS FLOAT) END,
    CAST(r.Customer_Id AS INT),
    p.Product_Id,
    CAST(r.Sales AS FLOAT),
    CAST(r.Quantity AS INT),
    CAST(r.Discount AS FLOAT),
    CAST(r.Profit AS FLOAT),
    CAST(r.Shipping_Cost AS FLOAT),
    r.Order_Priority,
    r.Payment_method
FROM RawOrders r
JOIN Products p ON r.Product = p.Product_Name AND r.Product_Category = p.Product_Category
WHERE r.Customer_Id IS NOT NULL AND r.Customer_Id <> '';
GO

-- 5. Tối ưu hóa Hiệu suất (Query Optimization / Indexing)
-- Tạo chỉ mục (Index) trên các cột thường xuyên được dùng để JOIN hoặc lọc (WHERE)
-- nhằm tăng tốc độ đọc dữ liệu (Data Retrieval) khi thực hiện các truy vấn phân tích.
CREATE NONCLUSTERED INDEX idx_orders_date ON Orders(Order_Date);
CREATE NONCLUSTERED INDEX idx_orders_customer_product ON Orders(Customer_Id, Product_Id);
GO

/*
Kiểm tra toàn vẹn dữ liệu
*/
SELECT 'Customers' AS TableName, COUNT(*) AS TotalRows FROM Customers
UNION ALL
SELECT 'Products' AS TableName, COUNT(*) AS TotalRows FROM Products
UNION ALL
SELECT 'Categories' AS TableName, COUNT(*) AS TotalRows FROM Categories
UNION ALL
SELECT 'Orders' AS TableName, COUNT(*) AS TotalRows FROM Orders;
GO
