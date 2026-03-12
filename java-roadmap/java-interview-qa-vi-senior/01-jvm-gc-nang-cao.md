# 01) JVM & GC nâng cao (1–10)

## 1. Các vùng bộ nhớ chính của JVM là gì (từ góc nhìn thực tế)?

**Đáp:** Thường nói theo: heap (young/old), metaspace (metadata class), stack (mỗi thread), code cache (JIT), và native/off-heap. Sự cố production hay gặp: OOM heap, OOM metaspace, native OOM (direct buffer), và pause GC.

## 2. G1 GC hoạt động theo “region” nghĩa là gì, và lợi ích?

**Đáp:** G1 chia heap thành nhiều **region** nhỏ và thu gom theo region để đạt mục tiêu pause-time. Nó ưu tiên thu gom region “nhiều rác” trước (garbage-first) và cố gắng giữ pause dưới target.

## 3. Khi nào bạn cân nhắc ZGC / Shenandoah?

**Đáp:** Khi cần độ trễ rất thấp (pause cực ngắn) với heap lớn. Trade-off: yêu cầu JDK/OS phù hợp, có thể khác về throughput, và cần hiểu rõ đặc tính workload.

## 4. “Allocation rate” và “promotion rate” là gì? Vì sao quan trọng?

**Đáp:**
- Allocation rate: tốc độ tạo object.
- Promotion rate: tốc độ object được đẩy từ young → old.

Chúng quyết định tần suất GC và nguy cơ full/old GC. Allocation cao + promotion cao thường gây áp lực GC và latency.

## 5. GC log dùng để trả lời câu hỏi nào?

**Đáp:** Ít nhất 4 câu: (1) pause bao lâu và khi nào, (2) GC nguyên nhân gì, (3) heap thay đổi thế nào trước/sau, (4) xu hướng (leak/promotion) có tăng dần không.

## 6. Thế nào là “GC thrashing”?

**Đáp:** Hệ thống spend phần lớn thời gian làm GC nhưng vẫn thiếu bộ nhớ, throughput giảm mạnh. Dấu hiệu: GC rất thường xuyên, CPU cao, request latency tăng, heap dao động nhanh.

## 7. Metaspace là gì và OOM metaspace thường do đâu?

**Đáp:** Metaspace chứa metadata của class. OOM metaspace hay do nạp quá nhiều class (dynamic class generation, classloader leak trong plugin/app server), hoặc cấu hình giới hạn metaspace quá thấp.

## 8. “Safepoint” là gì và liên quan gì đến pause?

**Đáp:** Safepoint là điểm JVM có thể dừng threads an toàn để thực hiện VM operation (GC, deopt, bias revocation…). Pause không chỉ do GC; safepoint “đợi” thread đến điểm an toàn cũng có thể tăng latency.

## 9. Bạn dùng heap dump để làm gì, và cần cẩn thận điều gì?

**Đáp:** Heap dump giúp tìm “ai giữ tham chiếu” đến object (dominator tree), xác định leak/caches. Cẩn thận: dump lớn tốn I/O và có thể ảnh hưởng production; cần quy trình (lúc thấp tải, đủ disk, bảo mật dữ liệu).

## 10. Các flag JVM bạn hay xem khi xử lý OOM/GC?

**Đáp:** Tùy JDK, nhưng hay xem nhóm: `-Xms/-Xmx`, cấu hình GC, log GC, `-XX:MaxMetaspaceSize`, `-XX:+HeapDumpOnOutOfMemoryError`, đường dẫn heap dump, và bật JFR khi cần.
