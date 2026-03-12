# 09) Thiết kế API & Khả dụng (81–90)

## 81. Idempotency là gì và vì sao cần?

**Đáp:** Gọi cùng một request nhiều lần cho cùng key vẫn ra kết quả như một lần. Cần vì retry/timeouts có thể khiến client gửi lại. Thiết kế idempotency key cho POST quan trọng.

## 82. Thế nào là “timeout budget” trong một request?

**Đáp:** Tổng thời gian cho request phải được chia cho các call downstream. Nếu downstream timeout không hợp lý, request vượt budget → cascade failure.

## 83. Bulkhead pattern là gì?

**Đáp:** Cách ly tài nguyên (thread pool/connection pool) theo loại workload để một phần hỏng không kéo sập toàn hệ thống.

## 84. Load shedding là gì?

**Đáp:** Chủ động từ chối/giảm tải khi quá tải để giữ hệ thống sống (trả lỗi nhanh, degrade). Tốt hơn là treo toàn bộ.

## 85. Khi nào bạn dùng queue, khi nào không?

**Đáp:** Queue tốt để buffer và tách tốc độ producer/consumer, nhưng nếu không có backpressure/limit, queue thành “hố rác” gây OOM và tăng latency. Luôn có size limit và chiến lược drop.

## 86. Thiết kế pagination: offset vs cursor?

**Đáp:** Offset đơn giản nhưng chậm với dữ liệu lớn và dễ sai khi dữ liệu thay đổi. Cursor/seek pagination ổn định hơn và hiệu năng tốt hơn, nhưng phức tạp hơn.

## 87. API versioning: làm sao tránh phá vỡ client?

**Đáp:** Ưu tiên backward-compatible changes (thêm field mới, giữ behavior cũ), dùng version trong URL/header khi cần breaking, và có deprecation policy rõ.

## 88. Bạn thiết kế error model như thế nào?

**Đáp:** Có error code ổn định, message cho người đọc, và metadata (traceId, retryable, field errors). Tránh trả stacktrace thô ra client.

## 89. Observability tối thiểu cho Java service gồm gì?

**Đáp:** Metrics (RED/USE), structured logs có traceId, distributed tracing, và dashboards/alerts cho saturation (CPU, GC, thread pool, connection pool).

## 90. Bạn tránh “cascading failure” bằng cách nào?

**Đáp:** Timeouts bắt buộc, giới hạn concurrency (bulkhead/semaphore), circuit breaker, retry có kiểm soát, và degrade gracefully. Kết hợp rate limiting ở biên.
