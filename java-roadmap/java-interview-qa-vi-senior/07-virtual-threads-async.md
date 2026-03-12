# 07) Virtual threads & Async (61–70)

## 61. Virtual thread khác platform thread ở điểm nào?

**Đáp:** Platform thread ánh xạ 1-1 với OS thread. Virtual thread là lightweight, JVM schedule lên một pool platform threads; mục tiêu là xử lý lượng lớn tác vụ đồng thời với code blocking-friendly.

## 62. Vì sao virtual thread phù hợp với I/O blocking?

**Đáp:** Khi virtual thread block (vd chờ socket), JVM có thể “unmount” và dùng platform thread cho task khác, giảm số OS thread cần thiết.

## 63. Khi nào virtual thread không giúp nhiều?

**Đáp:** CPU-bound (vẫn bị giới hạn bởi core), hoặc khi code dùng synchronized/lock giữ lâu gây pinning/contended (tùy trường hợp). Cần benchmark và hiểu library mình dùng.

## 64. “Pinning” (khái niệm) trong virtual threads là gì?

**Đáp:** Một số thao tác có thể khiến virtual thread bị gắn chặt vào platform thread trong lúc block, làm giảm lợi ích. Thiết kế đồng bộ/lock cần cân nhắc.

## 65. `CompletableFuture` pitfalls phổ biến?

**Đáp:** Quên xử lý exception, chain chạy trên common pool gây tranh CPU, mixing blocking trong async pipeline, và khó trace context. Cần executor rõ ràng và chiến lược error handling.

## 66. Bạn chọn async callback hay “blocking style + virtual threads” theo tiêu chí gì?

**Đáp:** Nếu hệ thống chủ yếu I/O-bound và muốn đơn giản hoá code, blocking style với virtual threads có thể rất hấp dẫn. Nếu đã có reactive end-to-end và cần backpressure chặt, reactive vẫn phù hợp. Quyết định dựa trên kiến trúc + thư viện.

## 67. Structured concurrency (khái niệm) giải quyết gì?

**Đáp:** Nhóm các task con vào một scope: dễ cancel, propagate lỗi, và đảm bảo “không rò rỉ” task chạy nền. Nó làm concurrency dễ quản lý hơn (đặc biệt khi kết hợp virtual threads).

## 68. Vì sao “bounded executor” quan trọng?

**Đáp:** Không giới hạn task/thread → memory bloat và latency. Bounded executor/queue giúp backpressure và ổn định hệ thống.

## 69. Khi nào dùng `ForkJoinPool`?

**Đáp:** Cho bài toán chia nhỏ (divide-and-conquer) CPU-bound. Không nên dùng cho I/O blocking (trừ khi có thiết kế phù hợp) vì có thể làm starvation.

## 70. Bạn xử lý cancellation trong async như thế nào?

**Đáp:** Propagate signal cancel (interrupt/cancel token), đảm bảo I/O có timeout, và cleanup resource. Cancellation “best-effort” cần thiết kế từ đầu.
