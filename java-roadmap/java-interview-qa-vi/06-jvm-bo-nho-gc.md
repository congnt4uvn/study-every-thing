# 06) JVM, Bộ nhớ & GC (51–60)

## 51. JIT compilation là gì?

**Đáp:** JVM biên dịch bytecode “hot” sang native code đã tối ưu trong lúc chạy để tăng hiệu năng.

## 52. Stack và heap khác nhau?

**Đáp:**
- **Stack**: theo thread, chứa frame (local vars, call info); giải phóng khi return.
- **Heap**: chứa object/array dùng chung; GC quản lý.

## 53. Nguyên nhân thường gặp của `OutOfMemoryError`?

**Đáp:** Leak (cache/collection tăng mãi), heap quá nhỏ, metaspace tăng do classloading, cấp phát khối lớn, áp lực native/off-heap.

## 54. `OutOfMemoryError` vs `StackOverflowError`?

**Đáp:**
- OOM: không cấp phát được bộ nhớ.
- SOE: đệ quy quá sâu hoặc frame quá lớn.

## 55. GC là gì và tối ưu điều gì?

**Đáp:** GC thu hồi object không còn reachable. Collector tối ưu theo throughput, latency hoặc cân bằng (dựa trên giả định “đa số object sống ngắn”).

## 56. Stop-the-world pause là gì?

**Đáp:** Thời điểm JVM tạm dừng thread ứng dụng để làm một số pha GC/VM operation. Collector hiện đại giảm pause nhưng không loại bỏ hoàn toàn.

## 57. Escape analysis là gì?

**Đáp:** JIT phân tích xem object có “thoát” khỏi scope không để tối ưu (stack allocation/scalar replacement) khi phù hợp.

## 58. Classloader là gì, vì sao quan trọng?

**Đáp:** Classloader nạp class và tạo namespace. Quan trọng trong app server/plugin và các memory leak do giữ tham chiếu classloader khiến không unload được.

## 59. Java Memory Model (JMM) là gì (1 câu)?

**Đáp:** JMM định nghĩa quy tắc về visibility và ordering giữa các thread, và cách `volatile`, lock, `final` tạo happens-before.

## 60. Kể vài tool của JDK để debug JVM.

**Đáp:** `jcmd`, `jstack`, `jmap`, `jstat`, `jconsole`, JFR (Flight Recorder) / Mission Control.
