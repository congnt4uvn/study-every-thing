# AWS API Gateway - Ghi Log và Giám Sát

## Tổng Quan
Tài liệu này trình bày về ghi log, tracing, các chỉ số giám sát và cơ chế throttling của API Gateway.

---

## 1. Tích Hợp CloudWatch Logs

### Tính Năng
- **Mục đích**: Ghi lại thông tin request và response body đi qua API Gateway
- **Cấp độ cấu hình**: Được bật ở Stage Level
- **Các mức Log**: 
  - ERROR (thông tin tối thiểu)
  - INFO (thông tin vừa phải)
  - DEBUG (thông tin chi tiết nhất)
- **Tính linh hoạt**: Có thể ghi đè cài đặt cho từng API riêng biệt

### Luồng Request
```
User → API Gateway → CloudWatch Logs
              ↓
          Backend
              ↓
     API Gateway → CloudWatch Logs
              ↓
           User
```

### ⚠️ Cảnh Báo Bảo Mật
Việc bật CloudWatch Logs có thể ghi lại thông tin nhạy cảm. Cần thận trọng khi sử dụng trong môi trường production.

---

## 2. X-Ray Tracing

### Mục Đích
- Cung cấp thông tin tracing phân tán cho các request qua API Gateway
- **Best Practice**: Bật X-Ray cho cả API Gateway và Lambda để có cái nhìn toàn diện

### Lợi Ích
- Khả năng hiển thị end-to-end
- Xác định điểm nghẽn hiệu suất
- Phân tích luồng request

---

## 3. CloudWatch Metrics

### Cấu Hình
- Được giám sát theo từng stage
- Có thể bật detailed metrics

### Các Chỉ Số Quan Trọng

#### Chỉ Số Cache
- **CacheHitCount**: Số lần truy xuất cache thành công
  - Số liệu cao = Cache hiệu quả
- **CacheMissCount**: Số lần cache không có dữ liệu
  - Số liệu cao = Cache không hiệu quả

#### Chỉ Số Request
- **Count**: Tổng số API request trong một khoảng thời gian

#### Chỉ Số Hiệu Suất
- **IntegrationLatency**: Thời gian API Gateway:
  - Chuyển tiếp request đến backend
  - Nhận response từ backend
  - Cho biết thời gian xử lý của backend

- **Latency**: Tổng thời gian từ khi API Gateway:
  - Nhận request từ client
  - Trả về response cho client
  - Bao gồm: IntegrationLatency + thời gian xử lý của API Gateway
  
**Các Thành Phần Latency**:
- Kiểm tra authorization và authentication
- Tra cứu cache
- Mapping templates
- Các hoạt động khác của API Gateway

**Quan trọng**: Latency ≥ IntegrationLatency

#### ⏱️ Giới Hạn Timeout
**Thời gian request tối đa: 29 giây**
- Nếu Latency hoặc IntegrationLatency vượt quá 29 giây → Xảy ra Timeout

#### Chỉ Số Lỗi
- **4XXError**: Lỗi phía client (request không hợp lệ từ client)
- **5XXError**: Lỗi phía server (lỗi backend)

---

## 4. API Gateway Throttling

### Giới Hạn Tài Khoản
- **Tốc độ Throttle Mặc định**: 10,000 request/giây (trên tất cả các API)
- **Loại Giới Hạn**: Soft limit (có thể tăng khi yêu cầu AWS)

### ⚠️ Tác Động Chéo Giữa Các API
Nếu một API gặp lưu lượng truy cập lớn, các API khác trong cùng tài khoản cũng có thể bị throttle.

### Phản Hồi Lỗi Throttling
- **Mã Lỗi**: `429 Too Many Requests`
- **Loại Lỗi**: Lỗi phía client
- **Chiến Lược Retry**: Sử dụng exponential backoff

### Chiến Lược Tối Ưu Throttling

#### 1. Stage Limits
Đặt giới hạn throttle ở cấp stage để ngăn một stage tiêu thụ hết quota.

#### 2. Method Limits
Cấu hình giới hạn cho từng API method để bảo vệ khỏi các cuộc tấn công có mục tiêu.

#### 3. Usage Plans
Định nghĩa các plan để throttle theo từng customer, đảm bảo phân phối tài nguyên công bằng.

### So Sánh Với Lambda
Tương tự như giới hạn Lambda Concurrency:
- API quá tải không có giới hạn có thể làm throttle các API khác
- Giới hạn hợp lý ngăn ngừa lỗi chuỗi (cascading failures)

---

## Tóm Tắt Best Practices

1. ✅ Bật CloudWatch Logs để debug (cẩn thận với dữ liệu nhạy cảm)
2. ✅ Sử dụng X-Ray cho distributed tracing giữa các service
3. ✅ Giám sát Latency vs IntegrationLatency để xác định nút thắt
4. ✅ Đặt stage và method limits phù hợp
5. ✅ Triển khai usage plans cho throttling theo customer
6. ✅ Sử dụng exponential backoff cho lỗi 429
7. ✅ Giữ request dưới 29 giây để tránh timeout

---

## Điểm Chính Cho Kỳ Thi

- **CloudWatch Logs**: Cấp stage, với các mức ERROR/INFO/DEBUG
- **X-Ray**: Tracing đầy đủ khi tích hợp với Lambda
- **Latency** > **IntegrationLatency** (luôn luôn)
- Giới hạn **timeout 29 giây**
- Throttle mặc định **10,000 req/s** (soft limit)
- **Lỗi 429** = Too Many Requests (có thể retry với exponential backoff)
- **4XX** = Lỗi client, **5XX** = Lỗi server
- **CacheHitCount** vs **CacheMissCount** cho biết hiệu quả cache
