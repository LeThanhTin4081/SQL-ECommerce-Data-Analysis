# 🧠 Phân nhóm Khách hàng Thông minh (Customer Segmentation)

Sử dụng thuật toán **K-Means Clustering** trên mô hình **RFM** để tự động phân nhóm 38,995 khách hàng thành các phân khúc chiến lược, phục vụ tối ưu hóa chi phí Marketing.

**Nguồn dữ liệu:** Kết nối trực tiếp vào Database `ECommerceDB` trên SQL Server (đã xây dựng ở Phase 1 — SQL Analytics).

---

## 💡 Bài toán Kinh doanh

**Vấn đề:** Thay vì chia khách hàng một cách thủ công, cảm tính bằng lệnh SQL `GROUP BY` đơn giản, chúng ta cần một hệ thống AI tự động phát hiện các cụm khách hàng có hành vi mua sắm tương đồng.

**Phương pháp:**

- Trích xuất đặc trưng (Features) từ SQL bằng mô hình **RFM** (Recency, Frequency, Monetary) kết hợp Avg_Discount và Avg_Profit.
- Chuẩn hóa dữ liệu bằng **StandardScaler** (bắt buộc vì K-Means nhạy cảm với thang đo).
- Xác định số cụm tối ưu bằng **Elbow Method** + **Silhouette Score**.
- Huấn luyện mô hình **K-Means** với K=3.

---

## 🛠 Quy trình Triển khai (Implementation Pipeline)

| Bước                       | Nội dung                                                               | Công cụ / Kỹ thuật           |
| -------------------------- | ---------------------------------------------------------------------- | ---------------------------- |
| **1. Kết nối**             | Kết nối Python trực tiếp vào Database `ECommerceDB` trên SQL Server    | `pyodbc`                     |
| **2. Feature Engineering** | Viết truy vấn SQL (CTE + Aggregation) để tính RFM cho từng Customer_Id | `pandas`, SQL Query          |
| **3. Preprocessing**       | Xử lý missing values, chuẩn hóa dữ liệu bằng StandardScaler            | `scikit-learn`               |
| **4. Training**            | Xác định K tối ưu (Elbow + Silhouette → K=3), huấn luyện K-Means       | `KMeans`, `silhouette_score` |
| **5. Profiling**           | Phân tích đặc điểm từng Cluster bằng biểu đồ và bảng thống kê          | `pandas`, `matplotlib`       |
| **6. Visualization**       | Trực quan hóa 3D Scatter Plot phân bố 3 cụm khách hàng                 | `matplotlib` (3D)            |

---

## 📊 Kết quả Phân nhóm

Mô hình K-Means (K=3, Silhouette Score ≈ 0.315) đã phân nhóm thành công **38,995 khách hàng** thành 3 phân khúc:

| Cụm | Tên gọi              | Số lượng | Tỉ lệ | Đặc điểm chính                                                                                      |
| --- | -------------------- | -------- | ----- | --------------------------------------------------------------------------------------------------- |
| 0   | **Premium One-Time** | 12,864   | 33%   | Mua 1 lần, lợi nhuận cao (120 USD/đơn), sẵn sàng chi trả giá cao                                    |
| 1   | **Low-Value**        | 17,135   | 44%   | Nhóm đông nhất, chi tiêu thấp (102 USD), lợi nhuận thấp, nguy cơ rời bỏ cao                         |
| 2   | **VIP Loyal**        | 8,996    | 23%   | Mua gần đây nhất (92 ngày), tần suất cao nhất (2.24 lần), chi tiêu lớn nhất (357 USD), 79% Nam giới |

### Chỉ số RFM trung bình theo từng cụm

| Chỉ số           | Ý nghĩa                        | Cụm 0 | Cụm 1 | Cụm 2 |
| ---------------- | ------------------------------ | ----- | ----- | ----- |
| **Recency**      | Số ngày kể từ lần mua cuối     | 158   | 159   | 92    |
| **Frequency**    | Tần suất mua hàng (lần)        | 1.13  | 1.08  | 2.24  |
| **Monetary**     | Tổng chi tiêu (USD)            | 220   | 102   | 357   |
| **Avg_Discount** | Mức giảm giá trung bình        | 0.29  | 0.29  | 0.32  |
| **Avg_Profit**   | Lợi nhuận trung bình/đơn (USD) | 120   | 29    | 84    |

---

## 🎯 Đề xuất Chiến lược Marketing

Dựa trên kết quả phân nhóm, đề xuất 3 chiến lược Marketing tương ứng:

1. **VIP Loyal (Cụm 2):** Triển khai chương trình loyalty, ưu đãi độc quyền, early access sản phẩm mới để giữ chân. Nhóm này chủ yếu là Nam giới (79%), cần thiết kế chiến dịch phù hợp đối tượng.
2. **Premium One-Time (Cụm 0):** Gửi email/SMS nhắc nhở mua lại, cross-sell sản phẩm liên quan. Đây là nhóm có biên lợi nhuận cao nhất, cần chiến lược chuyển đổi thành khách trung thành.
3. **Low-Value (Cụm 1):** Chiến dịch retargeting với voucher giảm giá để kích hoạt lại. Nhóm đông nhất nhưng chi tiêu thấp, cần đánh giá chi phí Marketing vs. giá trị mang lại.

---
