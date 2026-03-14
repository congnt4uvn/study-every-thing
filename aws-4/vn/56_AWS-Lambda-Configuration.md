# Hướng Dẫn Cấu Hình AWS Lambda

## Tổng Quan
Tài liệu này bao gồm các tùy chọn cấu hình quan trọng cho AWS Lambda functions, tập trung vào cài đặt bộ nhớ, CPU và timeout.

## Cấu Hình Bộ Nhớ (Memory)

### Phạm Vi Bộ Nhớ
- **Tối thiểu**: 128 MB
- **Tối đa**: 10,240 MB (10 GB)
- Bộ nhớ có thể được cấu hình trong phạm vi này

### Điểm Quan Trọng
- Nhiều bộ nhớ hơn = Nhiều sức mạnh CPU hơn (tỷ lệ thuận)
- Bộ nhớ cao hơn = Chi phí cao hơn
- **Quan trọng**: Giám sát việc sử dụng bộ nhớ của Lambda function để tối ưu chi phí
- Đặt bộ nhớ theo nhu cầu thực tế - không quá ít (vấn đề hiệu suất), không quá nhiều (lãng phí tiền)

## Cấu Hình CPU

### Chủ Đề Thi Quan Trọng ⚠️
**KHÔNG có cách nào để thay đổi CPU độc lập với bộ nhớ trong AWS Lambda**

- CPU được phân bổ tự động tỷ lệ thuận với bộ nhớ
- Để có CPU nhanh hơn hoặc nhiều lõi CPU hơn: **Tăng phân bổ bộ nhớ**
- Đây là câu hỏi thi rất phổ biến

## Cấu Hình Timeout (Hết Thời Gian Chờ)

### Timeout Là Gì?
- Xác định thời gian Lambda function có thể chạy trước khi Lambda đưa ra lỗi
- Mặc định: Có thể đặt bất kỳ giá trị nào lên đến timeout tối đa (15 phút)

### Ví Dụ Tình Huống
- Nếu timeout được đặt thành **3 giây**:
  - Lambda function với thời gian hoạt động 2 giây: ✅ Thành công
  - Lambda function với thời gian hoạt động 5 giây: ❌ Thất bại (lỗi timeout)

### Thực Hành Tốt Nhất
- Đặt timeout dựa trên thời gian thực thi dự kiến của function
- Để dự phòng cho sự biến động trong thời gian thực thi
- Giám sát thời lượng thực thi thực tế để tối ưu cài đặt timeout

## Ví Dụ Thực Hành

```python
import time

def lambda_handler(event, context):
    time.sleep(2)  # Mô phỏng 2 giây làm việc
    return "prod"
```

**Kết quả**: Function hoàn thành thành công (~2000 milliseconds thời lượng)

```python
import time

def lambda_handler(event, context):
    time.sleep(5)  # Mô phỏng 5 giây làm việc
    return "prod"
```

**Kết quả**: Function thất bại nếu timeout được đặt thành 3 giây

## Tóm Tắt
1. **Memory (Bộ nhớ)** kiểm soát cả phân bổ bộ nhớ và sức mạnh CPU
2. **CPU** không thể cấu hình độc lập - điều chỉnh bộ nhớ thay vì
3. **Timeout** ngăn các function chạy vô thời hạn
4. Luôn tối ưu cài đặt dựa trên mức sử dụng thực tế để kiểm soát chi phí
