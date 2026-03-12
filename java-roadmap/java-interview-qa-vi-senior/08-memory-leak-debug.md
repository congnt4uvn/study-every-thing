# 08) Memory leak & Debug production (71–80)

## 71. “Memory leak” trong Java thường là gì (vì GC vẫn chạy)?

**Đáp:** Là tình huống object vẫn **reachable** do còn tham chiếu (cache không giới hạn, listener không remove, map giữ key, thread local…), nên GC không thể thu hồi.

## 72. Leak do cache hay gặp kiểu nào?

**Đáp:** Cache không có TTL/size limit, key cardinality tăng vô hạn (vd key theo userId/session), hoặc value giữ graph object lớn. Cần eviction rõ ràng và metrics.

## 73. Bạn dùng dominator tree để làm gì?

**Đáp:** Tìm object/nhóm object “thống trị” (giữ phần lớn memory). Nó trả lời: nếu cắt tham chiếu từ dominator, sẽ giải phóng bao nhiêu.

## 74. `WeakReference`/`SoftReference` dùng khi nào và rủi ro?

**Đáp:** Dùng để cache “không bắt buộc”, tránh giữ object quá lâu. Rủi ro: hành vi phụ thuộc GC, khó dự đoán; soft/weak cache không thay thế được eviction policy rõ.

## 75. Memory leak do classloader là gì?

**Đáp:** Classloader không được GC vì còn reference (thread, static, cache), kéo theo toàn bộ class/metadata. Hay gặp ở app server/hot-reload/plugin.

## 76. Làm sao phân biệt leak và spike tạm thời?

**Đáp:** Leak: after-GC heap “baseline” tăng dần theo thời gian. Spike: tăng rồi giảm về baseline sau GC/chu kỳ tải. Dùng GC log + heap after GC để xác nhận.

## 77. JFR (Java Flight Recorder) giúp gì?

**Đáp:** Thu thập sự kiện low-overhead: allocation, lock contention, I/O, thread scheduling, GC, safepoint… Rất hữu ích để chẩn đoán latency/throughput mà không cần profiler nặng.

## 78. `OutOfMemoryError: Direct buffer memory` nghĩa là gì?

**Đáp:** Thiếu native memory cho direct buffers (NIO). Có thể do leak buffer, hoặc giới hạn direct memory. Cần theo dõi allocation direct, đảm bảo release, và cấu hình phù hợp.

## 79. Vì sao “tăng Xmx” có thể chỉ trì hoãn vấn đề?

**Đáp:** Nếu leak/caches không giới hạn, tăng heap chỉ làm chết chậm hơn và có thể tăng pause. Cần tìm root cause và giới hạn/evict.

## 80. Quy trình xử lý incident hiệu năng bạn hay dùng?

**Đáp:** (1) Giảm impact (throttle/rollback), (2) thu thập evidence (metrics, trace, dump), (3) khoanh vùng bottleneck, (4) fix nhỏ có kiểm soát, (5) postmortem + guardrails (alerts, limits).
