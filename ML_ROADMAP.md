# 🤖 Lộ trình Tích hợp Machine Learning (Phase 2 Roadmap)

Dự án này không chỉ dừng lại ở mức xử lý dữ liệu và phân tích bằng SQL. Nền tảng **Data Warehouse** và **Data Model** (chuẩn 3NF) vững chắc mà chúng ta đã xây dựng chính là bệ phóng hoàn hảo để triển khai các mô hình **Machine Learning (Học máy)**.

Dưới đây là kế hoạch nâng cấp dự án bằng cách kết hợp sức mạnh của SQL (Xử lý Data) và Machine Learning (Dự đoán) để tạo ra một "combo hủy diệt" giải quyết các bài toán Kinh doanh thực tế:

---

## 💡 Ý tưởng 1: Phân nhóm Khách hàng Thông minh (Customer Segmentation)
Đây là bài toán **Học không giám sát (Unsupervised Learning)** kinh điển nhất trong ngành Bán lẻ & E-commerce nhằm tối ưu hóa chi phí Marketing.

*   **Vấn đề:** Thay vì chia khách hàng một cách thủ công, cảm tính bằng lệnh SQL `GROUP BY` đơn giản, chúng ta cần một hệ thống AI tự động phát hiện các cụm khách hàng có hành vi mua sắm tương đồng.
*   **Phương pháp triển khai:** 
    *   Trích xuất các đặc trưng (Features) từ SQL bằng mô hình **RFM** (Recency - Thời gian mua gần nhất, Frequency - Tần suất mua, Monetary - Tổng tiền chi tiêu) và độ nhạy cảm với Giảm giá (Discount Sensitivity).
    *   Sử dụng thuật toán **K-Means Clustering** để gom cụm.
*   **Kết quả kỳ vọng:** Thuật toán sẽ tự động chia tập khách hàng thành các cụm (Clusters) chiến lược:
    *   🌟 **Cụm 1: Khách "Sộp" (VIP)** - Ít quan tâm đến Discount, thường xuyên mua đồ đắt tiền (Sales cao, Profit dày).
    *   🔥 **Cụm 2: Khách "Săn sale" (Bargain Hunters)** - Chỉ mua khi có Discount cao, biên lợi nhuận (Profit margin) mỏng.
    *   🌊 **Cụm 3: Khách lướt sóng (Occasional Shoppers)** - Mua 1 lần rồi thôi, cần các chiến dịch Retargeting để kéo họ quay lại.
*   **Điểm nhấn (Wow Factor):** Trực quan hóa các cụm khách hàng này bằng biểu đồ phân tán **3D Scatter Plot** để cung cấp góc nhìn sâu sắc cho đội ngũ Marketing. Đảm bảo nhà tuyển dụng nhìn vào sẽ cực kỳ ấn tượng!

---

## 💡 Ý tưởng 2: Dự đoán Lợi nhuận / Doanh thu (Profit/Sales Prediction)
Đây là bài toán **Học có giám sát (Supervised Learning - Regression)** nhằm hỗ trợ bộ phận Tài chính và Kinh doanh ra quyết định.

*   **Vấn đề:** Công ty chuẩn bị ra mắt một chương trình khuyến mãi và cần dự báo: *"Nếu bán một sản phẩm thuộc ngành hàng A, qua App di động, giảm giá 15%, áp dụng freeship... thì đơn hàng này liệu có sinh lời hay bị lỗ?"*
*   **Phương pháp triển khai:** 
    *   Xây dựng mô hình dự đoán (Predictive Model) sử dụng các thuật toán mạnh mẽ như **XGBoost Regressor** hoặc **Random Forest**.
    *   Dạy cho máy học dựa trên các cột đặc trưng: `Discount`, `Shipping_Cost`, `Device_Type`, `Product_Category`, `Order_Priority`...
*   **Kết quả kỳ vọng:** Mô hình sẽ tự động dự đoán ra con số chính xác ở cột `Profit` (Lợi nhuận) hoặc `Sales` (Doanh thu) cho một đơn hàng bất kỳ trong tương lai.
*   **Điểm nhấn (Wow Factor):** Ứng dụng AI vào việc tối ưu hóa **Chiến lược Giá (Pricing Strategy)**. Chứng minh cho nhà tuyển dụng thấy khả năng liên kết giữa kỹ thuật Machine Learning và hiệu quả tài chính của doanh nghiệp.

---

## 🛠 Hướng dẫn Triển khai (Next Steps)
Để tiến hành Giai đoạn 2 này, kiến trúc dự án sẽ được mở rộng theo các bước sau:
1.  Tạo một thư mục mới tên là `machine_learning/` ngay trong Repository này.
2.  Khởi tạo một file **Jupyter Notebook (`.ipynb`)**.
3.  Sử dụng thư viện `pyodbc` hoặc `sqlalchemy` trong Python để kết nối trực tiếp vào Database `ECommerceDB` trên hệ thống SQL Server.
4.  Viết truy vấn SQL ngay trong Python để kéo dữ liệu sạch về DataFrame của thư viện `Pandas`.
5.  Huấn luyện mô hình Machine Learning bằng `scikit-learn` và `xgboost`.
