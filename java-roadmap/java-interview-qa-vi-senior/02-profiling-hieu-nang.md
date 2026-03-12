# 02) Profiling & Hiệu năng (11–20)

## 11. Tối ưu hiệu năng: bạn bắt đầu từ đâu?

**Đáp:** Bắt đầu bằng **đo**: metrics (latency p50/p95/p99), CPU, GC, I/O, thread pool, và trace. Tối ưu khi đã có bottleneck rõ ràng, tránh tối ưu “cảm tính”.

## 12. Sampling profiler vs instrumentation profiler?

**Đáp:**
- Sampling: lấy mẫu stack định kỳ; overhead thấp; phù hợp production.
- Instrumentation: chèn hook vào method; chi tiết hơn nhưng overhead cao hơn.

## 13. Vì sao “microbenchmark” hay sai và cách làm đúng?

**Đáp:** Sai do warmup JIT, dead-code elimination, constant folding, GC noise. Làm đúng: dùng **JMH**, cấu hình warmup/measurement/fork, tránh đo I/O trong microbenchmark.

## 14. “False sharing” là gì?

**Đáp:** Nhiều thread ghi vào biến khác nhau nhưng nằm chung cache line → invalidate liên tục, performance tụt. Cách giảm: padding/đổi layout, dùng `LongAdder` thay vì 1 counter hot.

## 15. Vì sao logging có thể làm chậm hệ thống dù log level thấp?

**Đáp:** Do xây dựng message (string concat), serialization tham số, hoặc lock contention trong appender. Cách giảm: dùng parameterized logging và kiểm tra lazy (`logger.debug("x {}", v)`), giảm log chatty.

## 16. Bạn phân biệt CPU-bound và I/O-bound trong Java service thế nào?

**Đáp:** CPU-bound: CPU cao, run queue tăng, profile thấy hot methods. I/O-bound: nhiều thread WAITING/BLOCKED, latency phụ thuộc network/DB, CPU không cao nhưng throughput thấp.

## 17. “Backpressure” là gì và vì sao quan trọng?

**Đáp:** Là cơ chế giới hạn tốc độ producer khi consumer không kịp xử lý. Không có backpressure → queue phình, memory tăng, latency tăng và cuối cùng OOM.

## 18. Thread dump giúp gì trong incident?

**Đáp:** Cho biết thread state, deadlock, lock contention, thread pool bị kẹt, và nơi đang block (DB call, IO). Nên lấy nhiều dump cách nhau vài giây để thấy xu hướng.

## 19. Khi nào nên dùng caching, và rủi ro chính?

**Đáp:** Dùng khi read-heavy và dữ liệu thay đổi không quá nhanh. Rủi ro: stale data, invalidation khó, cache stampede, memory bloat. Cần TTL, size limit, và metrics hit-rate.

## 20. Vì sao “tối ưu GC” đôi khi không bằng “giảm allocation”?

**Đáp:** Allocation cao tạo áp lực GC; giảm allocation thường giảm pause lẫn CPU. Ví dụ: tránh tạo object tạm trong loop nóng, dùng primitive/struct-like (record/arrays) phù hợp, tái sử dụng buffer (cẩn thận leak).
