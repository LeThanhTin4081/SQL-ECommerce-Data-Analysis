USE ECommerceDB;
GO

/*
Script: Advanced Analytics
Mục tiêu: Khai thác cơ sở dữ liệu đã chuẩn hóa để giải quyết các bài toán kinh doanh 
sử dụng kỹ thuật SQL nâng cao (CTEs, Window Functions, Phân nhóm).
*/

-- 1. Tổng quan Doanh thu và Lợi nhuận
-- Insight: Đo lường sức khỏe tài chính tổng thể của doanh nghiệp.
SELECT 
    COUNT(Order_Id) AS Total_Orders,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM Orders;
GO

-- 2. Hiệu suất Bán hàng theo Tháng
-- Insight: Xác định các tháng cao điểm bán hàng để lên kế hoạch nhập hàng và tiếp thị.
SELECT 
    FORMAT(Order_Date, 'yyyy-MM') AS Month,
    SUM(Sales) AS Monthly_Sales,
    SUM(Profit) AS Monthly_Profit
FROM Orders
GROUP BY FORMAT(Order_Date, 'yyyy-MM')
ORDER BY Month;
GO

-- 3. Top 10 Sản phẩm Bán chạy nhất
-- Insight: Xác định các mặt hàng chủ lực mang lại doanh thu cao nhất.
SELECT TOP 10
    P.Product_Name,
    P.Product_Category,
    SUM(O.Sales) AS Total_Sales,
    SUM(O.Quantity) AS Total_Units_Sold
FROM Orders O
JOIN Products P ON O.Product_Id = P.Product_Id
GROUP BY P.Product_Name, P.Product_Category
ORDER BY Total_Sales DESC;
GO

-- 4. Hiệu suất Xử lý Đơn hàng
-- Insight: Theo dõi số ngày trung bình từ lúc đặt hàng đến lúc giao (Aging) để tối ưu vận hành.
SELECT 
    AVG(Aging) AS Avg_Processing_Time
FROM Orders;
GO

-- 5. Phân tích Chi phí Vận chuyển
-- Insight: So sánh chi phí vận chuyển giữa các mức độ ưu tiên của đơn hàng để tối ưu chi phí Logistics.
SELECT 
    Order_Priority,
    COUNT(Order_Id) AS Total_Orders,
    AVG(Shipping_Cost) AS Avg_Shipping_Cost
FROM Orders
GROUP BY Order_Priority
ORDER BY Avg_Shipping_Cost DESC;
GO

-- 6. Xu hướng Phương thức Thanh toán
-- Insight: Hiểu thói quen thanh toán của khách hàng để đưa ra chính sách ưu đãi phù hợp.
SELECT 
    Payment_method,
    COUNT(Order_Id) AS Total_Orders,
    SUM(Sales) AS Total_Revenue
FROM Orders
GROUP BY Payment_method
ORDER BY Total_Revenue DESC;
GO

/*
Sử dụng Window Functions
*/

-- 7. Xếp hạng Sản phẩm theo Doanh thu
-- Insight: Áp dụng hàm RANK() OVER() để xếp hạng sản phẩm linh hoạt mà không mất thông tin chi tiết.
SELECT 
    P.Product_Name,
    P.Product_Category,
    SUM(O.Sales) AS Total_Sales,
    RANK() OVER (ORDER BY SUM(O.Sales) DESC) AS Sales_Rank
FROM Orders O
JOIN Products P ON O.Product_Id = P.Product_Id
GROUP BY P.Product_Name, P.Product_Category
ORDER BY Total_Sales DESC;
GO

-- 8. Doanh thu Lũy kế theo Tháng (Running Total)
-- Insight: Theo dõi tốc độ tăng trưởng doanh thu cộng dồn qua từng tháng bằng ROWS BETWEEN UNBOUNDED PRECEDING.
WITH MonthlySales AS (
    SELECT 
        FORMAT(Order_Date, 'yyyy-MM') AS Order_Month,
        SUM(Sales) AS Monthly_Sales
    FROM Orders
    GROUP BY FORMAT(Order_Date, 'yyyy-MM')
)
SELECT
    Order_Month,
    Monthly_Sales,
    SUM(Monthly_Sales) OVER (ORDER BY Order_Month ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS Running_Total
FROM MonthlySales
ORDER BY Order_Month;
GO

/*
Sử dụng Common Table Expressions (CTEs)
*/

-- 9. Phân khúc Khách hàng Giá trị cao (High-Value Customers)
-- Insight: Sử dụng CTE để tính tổng tiền, sau đó JOIN để lấy thông tin chi tiết của Top 10 khách hàng VIP.
WITH CustomerSpending AS (
    SELECT 
        Customer_Id,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM Orders
    GROUP BY Customer_Id
)
SELECT TOP 10
    C.Customer_Id,
    C.Gender,
    CS.Total_Sales,
    CS.Total_Profit
FROM CustomerSpending CS
JOIN Customers C ON C.Customer_Id = CS.Customer_Id
ORDER BY CS.Total_Sales DESC;
GO

-- 10. Cây Phân cấp Danh mục (Recursive CTE)
-- Insight: Triển khai kỹ thuật đệ quy (Recursive) để móc nối danh mục Cha - Con (Parent-Child) theo cấp độ.
WITH CategoryHierarchy AS (
    -- Anchor member: Lấy các danh mục gốc (không có cha)
    SELECT 
        Category_Id,
        Parent_Category_Id,
        Category_Name,
        0 AS Level
    FROM Categories
    WHERE Parent_Category_Id IS NULL

    UNION ALL

    -- Recursive member: Gọi lại CTE để duyệt các danh mục con
    SELECT 
        c.Category_Id,
        c.Parent_Category_Id,
        c.Category_Name,
        ch.Level + 1
    FROM Categories c
    JOIN CategoryHierarchy ch ON c.Parent_Category_Id = ch.Category_Id
)
SELECT * 
FROM CategoryHierarchy
ORDER BY Level, Parent_Category_Id;
GO
