# Hướng Dẫn Học Tập AWS Lambda

## Giới Thiệu về Lambda

AWS Lambda là dịch vụ điện toán serverless cho phép bạn chạy code mà không cần cung cấp hoặc quản lý máy chủ.

## Bắt Đầu với Lambda Console

Để truy cập giao diện thực hành Lambda:
1. Vào Lambda console
2. Điều hướng đến `/begin` trong URL
3. Giao diện này giúp bạn hiểu cách Lambda hoạt động

## Kiến Thức Cơ Bản về Lambda Function

### Các Ngôn Ngữ Lập Trình Được Hỗ Trợ

Lambda function có thể được viết bằng nhiều ngôn ngữ:
- .NET
- Java
- Node.js
- Python
- Ruby
- Custom runtime (cho các ngôn ngữ khác)

### Ví Dụ: Hello World

Khi bạn tạo một Lambda function Node.js cơ bản và nhấp **Run**, nó sẽ thực thi và trả về:
```
"Hello from Lambda."
```

## Kiến Trúc Hướng Sự Kiện (Event-Driven)

### Nguồn Sự Kiện Lambda

Lambda phản hồi với nhiều loại event trigger khác nhau:
- **Streaming analytics** - Xử lý các luồng dữ liệu thời gian thực
- **Ứng dụng di động** - Sự kiện từ điện thoại di động và IoT backend
- **S3 buckets** - Ảnh hoặc file được tải lên
- **Thiết bị IoT** - Dữ liệu từ camera và cảm biến

### Tự Động Mở Rộng (Auto Scaling)

Lambda tự động mở rộng dựa trên nhu cầu:
- Ban đầu chạy với tài nguyên tối thiểu (một cặp bánh răng)
- Khi có nhiều sự kiện hơn, Lambda tự động mở rộng
- Có thể mở rộng đến 8-9 instance hoặc nhiều hơn
- **Không cần quản lý máy chủ** - việc mở rộng diễn ra tự động

## Cân Nhắc về Chi Phí

### Mô Hình Giá

- **Free Tier**: Miễn phí hào phóng cho các lần gọi ban đầu
- **Trả theo mức sử dụng**: Chi phí tích lũy dựa trên:
  - Số lần invoke (gọi hàm)
  - Thời gian thực thi
  - Bộ nhớ được cấp phát

### Mẹo Tối Ưu Chi Phí

- Lambda có thể là **dịch vụ tiết kiệm chi phí**
- Quan trọng là phải ước tính khối lượng công việc của bạn
- Giám sát các mẫu invocation để dự đoán chi phí
- Xem xét giới hạn free tier thường xuyên

## Tạo Lambda Function Đầu Tiên

### Các Bước Để Tạo

1. Nhấp **Create a Function** trong Lambda console
2. Chọn sử dụng **blueprint**
3. Chọn blueprint **hello-world**
4. Cấu hình và triển khai

## Điểm Chính Cần Nhớ

✓ Lambda cung cấp điện toán serverless không cần quản lý hạ tầng

✓ Hỗ trợ nhiều ngôn ngữ lập trình

✓ Tự động mở rộng dựa trên nhu cầu

✓ Kiến trúc hướng sự kiện cho phép xử lý thời gian thực

✓ Tiết kiệm chi phí cho nhiều khối lượng công việc với kế hoạch phù hợp

---

**Bước Tiếp Theo**: Thực hành tạo Lambda function với các blueprint và event source khác nhau để hiểu đầy đủ khả năng của nó.
