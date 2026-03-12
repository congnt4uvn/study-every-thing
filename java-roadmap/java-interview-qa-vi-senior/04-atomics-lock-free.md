# 04) Atomics & Lock-free (31–40)

## 31. CAS là gì?

**Đáp:** Compare-And-Set: cập nhật biến nếu giá trị hiện tại đúng như kỳ vọng. Đây là primitive cho nhiều thuật toán lock-free.

## 32. Vì sao CAS có thể “spin” và tốn CPU?

**Đáp:** Khi contention cao, nhiều thread CAS thất bại và retry liên tục. Khi đó lock-free không đồng nghĩa với “nhanh hơn”; cần đánh giá contention và backoff.

## 33. Vấn đề ABA trong CAS là gì?

**Đáp:** Giá trị đổi từ A → B → A; thread khác nhìn thấy vẫn là A và CAS thành công dù trạng thái đã thay đổi. Giải pháp: thêm version/stamp (vd `AtomicStampedReference`).

## 34. `AtomicLong` vs `LongAdder` khác nhau?

**Đáp:** `AtomicLong` dùng một biến, contention cao sẽ chậm. `LongAdder` phân tán cập nhật trên nhiều cell rồi cộng lại, thường nhanh hơn cho counter hot (đổi lại đọc `sum()` có chi phí và không “ngay lập tức” theo nghĩa tuyến tính chặt chẽ).

## 35. “Linearizability” là gì?

**Đáp:** Tính chất cho phép xem mỗi operation xảy ra tức thời tại một điểm giữa start/end, giúp reasoning đơn giản như chạy tuần tự. Không phải mọi cấu trúc concurrent đều linearizable.

## 36. `volatile` có làm tăng atomicity không?

**Đáp:** Không. `volatile` đảm bảo visibility và ordering nhất định. Atomicity chỉ áp dụng cho một số thao tác đơn giản (read/write của reference, int/long theo JMM hiện đại), không cho read-modify-write.

## 37. “Publication” với `final` field có gì đặc biệt?

**Đáp:** `final` có quy tắc đặc biệt trong JMM: nếu object được publish đúng cách sau constructor, thread khác sẽ thấy giá trị `final` đúng mà không cần lock thêm (dù vẫn cần publish an toàn).

## 38. Khi nào bạn chọn lock-free thay vì lock?

**Đáp:** Khi contention vừa phải và cần giảm latency do lock convoy; nhưng lock-free phức tạp, khó debug. Với contention cao, lock-free có thể tệ do spin.

## 39. “Lock convoy” là gì?

**Đáp:** Khi nhiều thread xếp hàng chờ một lock và bị context-switch dây chuyền, làm throughput giảm mạnh. Có thể xảy ra dưới tải cao hoặc khi lock giữ lâu.

## 40. Bạn kiểm chứng một bug concurrency như thế nào?

**Đáp:** Tái tạo bằng test stress (nhiều vòng, nhiều core), thêm timeouts, dùng thread sanitizer/analysis (nếu có), log sự kiện có thứ tự, và suy luận dựa trên happens-before. Không dựa vào “chạy thấy ok”.
