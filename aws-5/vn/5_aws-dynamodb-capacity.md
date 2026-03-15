# AWS DynamoDB - Chế Độ Dung Lượng

## Tổng Quan
Tài liệu này bao gồm các chế độ dung lượng DynamoDB, RCU (Read Capacity Units - Đơn vị dung lượng đọc), và cấu hình WCU (Write Capacity Units - Đơn vị dung lượng ghi).

## Cấu Hình Chế Độ Dung Lượng

### Truy Cập Cài Đặt Dung Lượng
1. Chọn bảng DynamoDB của bạn (ví dụ: bảng User)
2. Điều hướng đến phía bên phải
3. Nhấp vào **Additional settings** (Cài đặt bổ sung)
4. Truy cập **Read/Write capacity** (Dung lượng đọc/ghi)
5. Nhấp **Edit** (Chỉnh sửa)

### Các Tính Năng Chính
- Cài đặt được xác định khi tạo bảng có thể được thay đổi
- Bạn có thể **chuyển đổi giữa các chế độ dung lượng** bất cứ lúc nào
- Dung lượng có thể được điều chỉnh theo thời gian dựa trên nhu cầu của bạn

## Các Chế Độ Dung Lượng

### 1. Chế Độ On-Demand (Theo Yêu Cầu)

**Đặc Điểm:**
- Thanh toán đơn giản - chỉ trả tiền cho số lần đọc và ghi thực tế
- **Chi phí:** Đắt hơn từ 2-3 lần so với chế độ provisioned
- Không cần lập kế hoạch dung lượng

**Trường Hợp Sử Dụng Tốt Nhất:**
- Khối lượng công việc không thể dự đoán
- Môi trường phát triển
- Sử dụng không thường xuyên (ví dụ: không sử dụng trong 24 giờ, sau đó sử dụng nhiều trong 1 giờ)
- Ứng dụng có lưu lượng truy cập biến đổi mạnh

**Ưu Điểm:** Tính phí dựa trên mức sử dụng thực tế - xuất sắc cho khối lượng công việc không liên tục

### 2. Chế Độ Provisioned Capacity (Dung Lượng Được Cấp Phát)

**Đặc Điểm:**
- Yêu cầu lập kế hoạch và tính toán RCU và WCU
- Tiết kiệm chi phí hơn on-demand
- Giá cả có thể dự đoán được

**Các Tham Số Cấu Hình:**

#### Sử Dụng Capacity Calculator (Máy Tính Dung Lượng):
1. **Kích thước item trung bình:** ví dụ: 6 kilobytes
2. **Số lần đọc mỗi giây:** ví dụ: 3 lần đọc/giây
3. **Số lần ghi mỗi giây:** ví dụ: 2 lần ghi/giây
4. **Loại tính nhất quán khi đọc:**
   - Eventually consistent (Nhất quán cuối cùng)
   - Strongly consistent (Nhất quán mạnh)
   - Transactional (Giao dịch - chủ đề nâng cao)
5. **Loại tính nhất quán khi ghi:**
   - Standard (Tiêu chuẩn)
   - Transactional (Giao dịch - chủ đề nâng cao)

**Kết Quả Từ Calculator:**
- RCU cần thiết (Read Capacity Units)
- WCU cần thiết (Write Capacity Units)
- Chi phí ước tính hàng tháng

## Các Khái Niệm Chính

### RCU (Read Capacity Units - Đơn Vị Dung Lượng Đọc)
Đơn vị đại diện cho khả năng thông lượng đọc cho bảng của bạn.

### WCU (Write Capacity Units - Đơn Vị Dung Lượng Ghi)
Đơn vị đại diện cho khả năng thông lượng ghi cho bảng của bạn.

### Các Loại Tính Nhất Quán Khi Đọc:
- **Eventually Consistent:** Tùy chọn mặc định, tiêu thụ RCU thấp hơn
- **Strongly Consistent:** Đảm bảo dữ liệu mới nhất, tiêu thụ RCU cao hơn
- **Transactional:** Cho các giao dịch ACID (sẽ đề cập trong các chủ đề nâng cao)

### Các Loại Tính Nhất Quán Khi Ghi:
- **Standard:** Chế độ ghi mặc định
- **Transactional:** Cho các giao dịch ACID (sẽ đề cập trong các chủ đề nâng cao)

## Thực Hành Tốt Nhất

1. **Sử dụng Capacity Calculator** để ước tính nhu cầu của bạn
2. **Thực hành với các tình huống khác nhau** để hiểu về lập kế hoạch dung lượng
3. **Bắt đầu với on-demand** cho phát triển/kiểm thử
4. **Chuyển sang provisioned** cho môi trường production với khối lượng công việc có thể dự đoán
5. **Giám sát mức sử dụng** và điều chỉnh dung lượng khi cần thiết

## Tối Ưu Hóa Chi Phí

- **On-demand:** Tốt nhất cho khối lượng công việc không thể dự đoán hoặc không thường xuyên
- **Provisioned:** Tốt nhất cho các mẫu lưu lượng ổn định, có thể dự đoán
- Cân nhắc sử dụng chế độ provisioned với auto-scaling cho khối lượng công việc có thể dự đoán nhưng biến đổi

---

*Lưu ý: Đây là hướng dẫn cơ bản. Các chủ đề nâng cao như các hoạt động transactional sẽ được đề cập riêng.*
