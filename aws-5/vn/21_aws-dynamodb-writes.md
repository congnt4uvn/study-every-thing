# AWS DynamoDB: Các Thao Tác Ghi Dữ Liệu

## Tổng Quan
Hiểu rõ các loại thao tác ghi khác nhau trong DynamoDB là rất quan trọng để xây dựng các ứng dụng đáng tin cậy và hiệu quả. Tài liệu này bao gồm ba loại ghi chính: ghi đồng thời, ghi có điều kiện và ghi nguyên tử.

---

## 1. Ghi Đồng Thời (Concurrent Writes)

### Ghi Đồng Thời Là Gì?
Ghi đồng thời xảy ra khi nhiều người dùng hoặc tiến trình cố gắng cập nhật cùng một mục đồng thời mà không có bất kỳ sự phối hợp nào.

### Ví Dụ Kịch Bản
- **Người dùng 1**: Cập nhật mục với `value = 1`
- **Người dùng 2**: Cập nhật mục với `value = 2`

### Điều Gì Xảy Ra?
- Cả hai thao tác ghi đều thành công
- Lần ghi thứ hai có thể ghi đè lên lần ghi đầu tiên (nếu nó xảy ra sau)
- Cuối cùng, chỉ một giá trị sẽ được giữ lại (có thể là `value = 2`)

### Vấn Đề
- Cả hai người dùng đều nhận được phản hồi thành công
- Tuy nhiên, chỉ có một bản cập nhật thực sự được lưu giữ
- Điều này tạo ra hành vi không thể dự đoán và có thể gây mất tính nhất quán của dữ liệu

---

## 2. Ghi Có Điều Kiện (Conditional Writes) - Khóa Lạc Quan

### Giải Pháp Cho Vấn Đề Ghi Đồng Thời
Ghi có điều kiện cho phép bạn chỉ định các điều kiện phải được đáp ứng trước khi thao tác ghi được thực thi.

### Cách Hoạt Động
Thao tác ghi chỉ thành công nếu một điều kiện được chỉ định là đúng tại thời điểm thực thi.

### Ví Dụ Kịch Bản
- **Người dùng 1**: "Cập nhật giá trị thành 1, nhưng CHỈ nếu giá trị hiện tại = 0"
- **Người dùng 2**: "Cập nhật giá trị thành 2, nhưng CHỈ nếu giá trị hiện tại = 0"

### Điều Gì Xảy Ra?
1. **Lần ghi đầu tiên (Người dùng 1)**: 
   - Kiểm tra điều kiện: value = 0 ✓
   - Ghi thành công → giá trị trở thành 1
   
2. **Lần ghi thứ hai (Người dùng 2)**:
   - Kiểm tra điều kiện: value = 0 ✗ (giá trị hiện tại là 1)
   - Ghi thất bại

### Lợi Ích
- Ngăn chặn ghi đè không mong muốn
- Đảm bảo tính nhất quán của dữ liệu
- Cách tiếp cận này được gọi là **Khóa Lạc Quan (Optimistic Locking)**

---

## 3. Ghi Nguyên Tử (Atomic Writes)

### Ghi Nguyên Tử Là Gì?
Ghi nguyên tử cho phép bạn thực hiện các thao tác tăng/giảm mà không cần đọc giá trị hiện tại trước.

### Ví Dụ Kịch Bản
- **Người dùng 1**: "Tăng giá trị thêm 1"
- **Người dùng 2**: "Tăng giá trị thêm 2"

### Điều Gì Xảy Ra?
- Cả hai thao tác đều thành công
- Giá trị cuối cùng được tăng theo tổng: 1 + 2 = 3
- Không có mất mát dữ liệu

### Lợi Ích
- Cả hai thao tác đều được áp dụng chính xác
- Không có điều kiện tranh chấp (race conditions)
- Hoàn hảo cho các bộ đếm và thao tác tích lũy

---

## Những Điểm Chính Cần Nhớ

| Loại Ghi | Tỷ Lệ Thành Công | Tính Nhất Quán Dữ Liệu | Trường Hợp Sử Dụng |
|----------|------------------|------------------------|-------------------|
| Ghi Đồng Thời | Cả hai thành công | ❌ Thấp (ghi cuối thắng) | Không khuyến nghị |
| Ghi Có Điều Kiện | Một thành công | ✅ Cao (với điều kiện) | Cập nhật cần xác thực |
| Ghi Nguyên Tử | Cả hai thành công | ✅ Cao (cộng dồn) | Bộ đếm, số liệu |

---

## Các Phương Pháp Hay Nhất

1. **Tránh ghi đồng thời** trừ khi mất dữ liệu là có thể chấp nhận được
2. **Sử dụng ghi có điều kiện** khi bạn cần đảm bảo tính toàn vẹn của dữ liệu
3. **Sử dụng ghi nguyên tử** cho các thao tác tăng/giảm
4. Luôn xử lý các lỗi ghi có điều kiện trong logic ứng dụng của bạn

---

## Các Dịch Vụ AWS Liên Quan
- Amazon DynamoDB
- DynamoDB Streams
- DynamoDB Transactions

---

*Tài Liệu Học Tập | Các Thao Tác Ghi DynamoDB trên AWS*
