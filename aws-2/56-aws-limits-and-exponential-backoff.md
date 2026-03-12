# Giới hạn AWS và Chiến lược Exponential Backoff

## Tổng quan

AWS có hai loại giới hạn (còn gọi là Quotas - Hạn ngạch) mà các nhà phát triển cần hiểu và quản lý khi làm việc với các dịch vụ AWS.

## Các loại Giới hạn AWS

### 1. Giới hạn Tốc độ API (API Rate Limits)

Giới hạn Tốc độ API xác định số lần bạn có thể gọi một AWS API trong một khoảng thời gian nhất định.

**Ví dụ:**
- **EC2 DescribeInstances API**: 100 lần gọi mỗi giây
- **S3 GetObject API**: 5,500 yêu cầu GET mỗi giây cho mỗi prefix

#### Điều gì xảy ra khi vượt quá Giới hạn Tốc độ?

Khi bạn vượt quá các giới hạn này, bạn sẽ gặp phải:
- **Lỗi Gián đoạn (Intermittent Errors)**: Các yêu cầu của bạn sẽ bị điều tiết (throttled)
- **ThrottlingException**: Mã lỗi cho biết đã vượt quá giới hạn tốc độ

#### Giải pháp cho các vấn đề về Giới hạn Tốc độ

**Đối với Lỗi Gián đoạn:**
- Triển khai **Chiến lược Exponential Backoff** (chi tiết bên dưới)

**Đối với Lỗi Liên tục:**
- Yêu cầu **tăng giới hạn điều tiết API** từ AWS
- Ví dụ: Nếu bạn liên tục cần hơn 100 lần gọi mỗi giây cho DescribeInstances, bạn có thể yêu cầu tăng (ví dụ: lên 300 lần gọi mỗi giây)

### 2. Hạn ngạch Dịch vụ (Service Quotas/Service Limits)

Hạn ngạch Dịch vụ xác định bạn có thể chạy bao nhiêu tài nguyên của một loại cụ thể.

**Ví dụ:**
- **On-Demand Standard Instances**: Tối đa 1,152 vCPU ảo mỗi tài khoản

#### Cách tăng Hạn ngạch Dịch vụ

1. **Phương pháp Thủ công**: Mở ticket hỗ trợ với AWS
2. **Phương pháp Lập trình**: Sử dụng Service Quotas API để yêu cầu tăng tự động

## Chiến lược Exponential Backoff

### Khi nào sử dụng Exponential Backoff

Triển khai Exponential Backoff khi bạn nhận được **ThrottlingException** do quá nhiều lần gọi API.

> **Mẹo Thi**: Các câu hỏi về ThrottlingException thường mong đợi Exponential Backoff là câu trả lời.

### Triển khai SDK

- **AWS SDK**: Cơ chế thử lại với Exponential Backoff **đã được bao gồm** theo mặc định
- **Gọi API Tùy chỉnh**: Nếu bạn tự triển khai các HTTP calls, bạn phải tự triển khai Exponential Backoff

### Nên thử lại Lỗi nào?

Khi triển khai logic thử lại tùy chỉnh:

✅ **NÊN Thử lại:**
- **Lỗi Server 5XX** (500, 503, v.v.)
- **Lỗi Throttling**

❌ **KHÔNG NÊN Thử lại:**
- **Lỗi Client 4XX** (400, 401, 403, v.v.)
- Những lỗi này cho thấy vấn đề với yêu cầu của bạn, và việc thử lại sẽ không thay đổi kết quả

### Cách hoạt động của Exponential Backoff

Chiến lược này bao gồm việc tăng gấp đôi thời gian chờ giữa mỗi lần thử lại:

```
Lần thử 1: Chờ 1 giây
Lần thử 2: Chờ 2 giây (gấp đôi)
Lần thử 3: Chờ 4 giây (gấp đôi)
Lần thử 4: Chờ 8 giây (gấp đôi)
Lần thử 5: Chờ 16 giây (gấp đôi)
```

### Lợi ích của Exponential Backoff

1. **Giảm Tải cho Server**: Càng thử lại nhiều, thời gian chờ càng dài
2. **Phân tán Tải**: Khi nhiều client triển khai chiến lược này đồng thời, tải tổng thể trên server giảm xuống
3. **Tăng Tỷ lệ Thành công**: Cho phép server phục hồi và phục vụ càng nhiều yêu cầu càng tốt

## Những điểm chính cần nhớ

- AWS có hai loại giới hạn: **Giới hạn Tốc độ API** và **Hạn ngạch Dịch vụ**
- Sử dụng **Exponential Backoff** cho lỗi ThrottlingException
- AWS SDK đã bao gồm Exponential Backoff theo mặc định
- Chỉ thử lại **lỗi 5XX**, không thử lại **lỗi 4XX**
- Yêu cầu tăng giới hạn khi bạn liên tục vượt quá hạn ngạch
- Exponential Backoff giúp phân phối tải theo thời gian, giảm áp lực lên server

## Tóm tắt

Hiểu rõ các giới hạn của AWS và triển khai các chiến lược thử lại phù hợp như Exponential Backoff là rất quan trọng để xây dựng các ứng dụng đáng tin cậy và có khả năng mở rộng trên AWS. Các cơ chế này giúp đảm bảo ứng dụng của bạn có thể xử lý throttling một cách ổn định trong khi vẫn duy trì hiệu suất tối ưu.