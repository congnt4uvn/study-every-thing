# 05) I/O & Networking (41–50)

## 41. Blocking I/O vs non-blocking I/O khác nhau?

**Đáp:** Blocking: thread chờ I/O hoàn tất. Non-blocking: call trả về ngay, dùng selector/callback để biết khi nào sẵn sàng. Non-blocking giúp scale tốt hơn khi có nhiều kết nối, nhưng code phức tạp hơn.

## 42. NIO Selector là gì?

**Đáp:** Cơ chế multiplexing: một thread có thể theo dõi nhiều channel và xử lý khi channel sẵn sàng đọc/ghi, thay vì 1 thread/connection.

## 43. `ByteBuffer` direct vs heap khác nhau?

**Đáp:** Direct buffer nằm ngoài heap (native), thường giảm copy khi I/O, nhưng cấp phát/giải phóng đắt hơn và có thể gây native OOM nếu leak. Heap buffer rẻ hơn nhưng có thể tốn copy.

## 44. “Head-of-line blocking” trong HTTP/1.1 là gì?

**Đáp:** Khi nhiều request dùng chung một kết nối tuần tự, request sau bị chặn bởi request trước. HTTP/2 multiplexing giảm vấn đề này (dù vẫn có HOL ở tầng TCP trong một số trường hợp).

## 45. Làm sao tránh “connection leak” khi gọi HTTP/DB?

**Đáp:** Luôn đóng response/body đúng cách, dùng pool quản lý, set timeouts (connect/read), và monitor pool metrics. Với JDBC, dùng try-with-resources cho `ResultSet/Statement/Connection`.

## 46. Timeouts nào là “bắt buộc” trong service-to-service?

**Đáp:** Ít nhất: connect timeout, read timeout (hoặc response timeout), và tổng thời gian cho request. Không timeout → thread pool bị kẹt, lan truyền sự cố.

## 47. Circuit breaker là gì (khái niệm)?

**Đáp:** Khi downstream lỗi/timeout liên tục, circuit breaker “mở” để fail-fast, giảm tải và cho downstream hồi phục. Thường kết hợp retry có giới hạn và backoff.

## 48. Retry có thể gây hại thế nào?

**Đáp:** Nếu retry không kiểm soát, nó khuếch đại tải (retry storm), làm downstream chết nhanh hơn. Nên có backoff + jitter, giới hạn retry, và chỉ retry lỗi có thể hồi phục.

## 49. Vì sao “async” không tự động nhanh hơn?

**Đáp:** Async giảm số thread block, nhưng vẫn bị giới hạn bởi downstream và CPU. Async cũng tăng độ phức tạp (context propagation, debug, ordering).

## 50. Bạn debug latency network trong Java service thế nào?

**Đáp:** Kết hợp: tracing (span breakdown), metrics timeouts/retries, log thời gian từng bước, thread dump (blocked), và packet/OS metrics khi cần. Luôn xác định “đang chờ ở đâu”.
