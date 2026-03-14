# Cấu Hình và Hiệu Suất AWS Lambda Function

## Cấu Hình RAM cho Lambda

### Phân Bổ Bộ Nhớ
- **Mặc định**: 128 megabyte RAM
- **Tối đa**: 10 gigabyte RAM
- **Bước tăng**: Mỗi lần tăng 1 megabyte

### Mối Quan Hệ giữa vCPU Credits và RAM
- RAM càng nhiều = vCPU credits càng nhiều
- **Quan trọng**: Bạn không thể thiết lập vCPU trực tiếp
- Bạn phải tăng RAM để gián tiếp nhận thêm vCPU

### Ngưỡng vCPU
- **Tại 1,792 MB RAM**: Function nhận được tương đương **một vCPU đầy đủ**
- **Trên 1,792 MB**: Bạn nhận được nhiều hơn một vCPU
- **Cần multi-threading** để tận dụng các vCPU bổ sung

### Ứng Dụng CPU-Bound
- Nếu ứng dụng của bạn **phụ thuộc vào CPU** (tính toán nặng):
  - Tăng RAM để cải thiện hiệu suất
  - Điều này giảm thời gian thực thi
  - **Câu hỏi thi thường gặp** ⚠️

## Cấu Hình Timeout cho Lambda

### Cài Đặt Mặc Định
- **Timeout mặc định**: 3 giây
- Nếu function chạy > 3 giây → Lỗi timeout

### Timeout Tối Đa
- **Tối đa**: 900 giây (15 phút)
- Phạm vi thực thi hợp lệ: 0 giây đến 15 phút

### Hướng Dẫn Trường Hợp Sử Dụng
- **0-15 phút**: Phù hợp với Lambda ✅
- **Trên 15 phút**: Xem xét các giải pháp thay thế ❌
  - AWS Fargate
  - Amazon ECS
  - Amazon EC2
- **Chủ đề thi** ⚠️

## Hiệu Suất Lambda và Execution Context

### Execution Context là gì?
Execution context là một **môi trường runtime tạm thời** có chức năng:
- Khởi tạo các dependencies bên ngoài của Lambda code
- Thiết lập kết nối database
- Tạo HTTP clients và SDK clients

### Tính Bền Vững của Context
- Execution context được **duy trì trong một khoảng thời gian**
- Dự đoán một lời gọi Lambda function khác
- Cải thiện hiệu suất cho các lần gọi tiếp theo

### Best Practices (Thực Hành Tốt Nhất)
- Khởi tạo connections và clients bên ngoài handler function
- Tái sử dụng execution context khi có thể
- Giảm chi phí cold start

## Điểm Quan Trọng Cho Kỳ Thi 📝

1. **Quan hệ RAM → vCPU**: Tăng RAM để nhận thêm vCPU
2. **Ngưỡng 1,792 MB**: Một vCPU đầy đủ tại mức bộ nhớ này
3. **Ứng dụng CPU-bound**: Tăng RAM để cải thiện hiệu suất
4. **Giới hạn 15 phút**: Thời gian thực thi Lambda tối đa
5. **Tác vụ chạy lâu**: Sử dụng Fargate/ECS/EC2 thay vì Lambda
6. **Execution context**: Được tái sử dụng qua các lần gọi để tăng hiệu suất
