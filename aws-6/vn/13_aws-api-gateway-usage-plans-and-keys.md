# AWS API Gateway - Usage Plans và API Keys

## Tổng Quan

Usage Plans và API Keys trong AWS API Gateway cho phép bạn kiếm tiền và kiểm soát quyền truy cập vào các API của mình. Những tính năng này giúp bạn quản lý ai có thể truy cập API, họ có thể sử dụng bao nhiêu và tốc độ gọi API của họ.

## Khái Niệm Chính

### Usage Plans (Gói Sử Dụng)

Một usage plan định nghĩa:
- **Ai** có thể truy cập một hoặc nhiều API stages và methods
- **Bao nhiêu** họ có thể truy cập API (quotas - hạn ngạch)
- **Nhanh như thế nào** họ có thể truy cập API (throttling - giới hạn tốc độ)
- **API keys nào** được liên kết để xác định và đo lường quyền truy cập của khách hàng

### Throttling Limits (Giới Hạn Tốc Độ)

- Kiểm soát tốc độ người dùng có thể gọi API
- Áp dụng ở cấp độ API key
- Giúp ngăn chặn lạm dụng API và quản lý tải

### Quota Limits (Hạn Ngạch)

- Tổng số request được phép trong một khoảng thời gian
- Ví dụ: Giới hạn 10,000 requests mỗi tháng
- Có thể sử dụng để triển khai các mô hình định giá theo tầng

### API Keys (Khóa API)

- Các chuỗi ký tự phân phối cho khách hàng
- Cho phép khách hàng xác thực request một cách an toàn
- Sử dụng kết hợp với usage plans để kiểm soát quyền truy cập
- Phải được cung cấp trong header `x-api-key` khi gọi API

## Các Bước Triển Khai

Thực hiện theo thứ tự các bước sau để cấu hình usage plans và API keys:

1. **Tạo APIs**
   - Tạo một hoặc nhiều APIs trong API Gateway

2. **Cấu Hình Methods**
   - Cấu hình các methods yêu cầu API key
   - Đánh dấu các endpoint cụ thể cần xác thực

3. **Deploy APIs**
   - Deploy các APIs đến các stages của bạn (dev, staging, production, v.v.)

4. **Tạo/Import API Keys**
   - Tạo hoặc import API keys để phân phối cho các developers/khách hàng

5. **Tạo Usage Plan**
   - Đặt giới hạn throttle mong muốn
   - Đặt giới hạn quota
   - Định nghĩa các chính sách truy cập

6. **Liên Kết Resources** ⚠️ **Bước Quan Trọng**
   - Liên kết API stages với usage plan
   - Liên kết API keys với usage plan
   - **Nếu quên bước này, mọi thứ sẽ không hoạt động!**

## Yêu Cầu Khi Gọi API

Người gọi phải cung cấp API key trong request:
```
x-api-key: <giá-trị-api-key-của-bạn>
```

## Lợi Ích

- **Kiếm Tiền**: Thu phí khách hàng cho việc sử dụng API
- **Kiểm Soát Truy Cập**: Quản lý ai có thể sử dụng API
- **Giới Hạn Tốc Độ**: Ngăn chặn lạm dụng và quản lý tải server
- **Giám Sát Sử Dụng**: Theo dõi mức tiêu thụ API của khách hàng
- **Định Giá Linh Hoạt**: Triển khai các mô hình định giá theo tầng

## Lưu Ý Quan Trọng

- Giới hạn throttling được áp dụng ở cấp độ API key
- Giới hạn quota đại diện cho tổng số requests
- Bước liên kết (bước 6) rất quan trọng - quên bước này sẽ khiến hệ thống không hoạt động
- API keys phải được phân phối an toàn cho khách hàng
