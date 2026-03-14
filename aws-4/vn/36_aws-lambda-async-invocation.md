# AWS Lambda - Gọi Hàm Bất Đồng Bộ (Asynchronous Invocation)

## Tổng Quan
Gọi hàm bất đồng bộ là phương thức thực thi AWS Lambda function mà người gọi không cần đợi hàm hoàn thành. Phương thức này hữu ích cho kiến trúc hướng sự kiện và các tác vụ xử lý nền.

## Các Khái Niệm Chính

### Bất Đồng Bộ vs Đồng Bộ
- **Bất đồng bộ (Asynchronous)**: Người gọi nhận được xác nhận ngay lập tức (HTTP 202) nhưng không nhận được giá trị trả về của hàm
- **Đồng bộ (Synchronous)**: Người gọi đợi hàm hoàn thành và nhận kết quả

### Mã Trạng Thái
- **202 Accepted**: Cho biết Lambda function đã được gọi bất đồng bộ thành công
- Mã trạng thái được trả về bất kể hàm thành công hay thất bại

## Cách Gọi Lambda Bất Đồng Bộ

### Sử Dụng AWS CLI
Bạn không thể gọi Lambda bất đồng bộ từ AWS Console. Bạn phải sử dụng AWS CLI:

```bash
aws lambda invoke \
  --function-name demo-lambda \
  --invocation-type Event \
  --payload '{"key1": "value1"}' \
  response.json
```

### Sử Dụng AWS CloudShell
CloudShell cung cấp một shell trên trình duyệt với AWS CLI đã được cài đặt sẵn, rất tiện lợi cho việc kiểm tra các lần gọi Lambda.

## Giám Sát Các Lần Gọi Bất Đồng Bộ

### CloudWatch Logs
Vì các lần gọi bất đồng bộ không trả về kết quả trực tiếp, bạn cần kiểm tra CloudWatch Logs để xem:
- Chi tiết thực thi hàm
- Giá trị trả về
- Lỗi và ngoại lệ

**Các bước kiểm tra logs:**
1. Vào Lambda Console → Function của bạn
2. Click vào tab "Monitor"
3. Xem "CloudWatch logs"
4. Chọn log stream gần đây
5. Xem xét chi tiết thực thi

## Xử Lý Lỗi

### Hành Vi Quan Trọng
- Ngay cả khi Lambda function thất bại trong quá trình gọi bất đồng bộ, AWS CLI vẫn trả về HTTP 202
- Bạn phải kiểm tra CloudWatch Logs để xác định hàm thành công hay thất bại
- Lỗi được ghi vào CloudWatch nhưng không được trả về cho người gọi

### Ví Dụ Tình Huống Lỗi
```python
# Hàm này sẽ thất bại nhưng vẫn trả về 202
def lambda_handler(event, context):
    raise Exception("Đã xảy ra lỗi!")
```

## Các Thực Hành Tốt Nhất

1. **Luôn giám sát CloudWatch Logs** cho các lần gọi bất đồng bộ
2. **Thiết lập CloudWatch Alarms** để phát hiện lỗi
3. **Sử dụng Dead Letter Queues (DLQ)** để lưu các lần gọi thất bại
4. **Xem xét chính sách retry** cho các lỗi tạm thời
5. **Kiểm tra cả tình huống thành công và thất bại** để hiểu rõ hành vi

## Các Trường Hợp Sử Dụng Gọi Bất Đồng Bộ

- Xử lý hình ảnh hoặc video
- Gửi thông báo
- Pipeline chuyển đổi dữ liệu
- Các tác vụ nền không cần phản hồi ngay lập tức
- Quy trình làm việc hướng sự kiện

## Tóm Tắt

Gọi Lambda bất đồng bộ là lý tưởng khi bạn không cần kết quả ngay lập tức. Điểm chính cần nhớ là mã trạng thái 202 chỉ xác nhận lần gọi đã được chấp nhận, không phải là nó đã thành công. Luôn sử dụng CloudWatch Logs để giám sát kết quả thực thi thực sự.
