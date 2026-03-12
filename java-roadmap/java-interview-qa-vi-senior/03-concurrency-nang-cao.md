# 03) Concurrency nâng cao (21–30)

## 21. “Happens-before” là gì, nói theo cách dễ hiểu?

**Đáp:** Nếu A happens-before B, thì mọi ghi của A **phải** được nhìn thấy bởi B theo đúng thứ tự. Java tạo happens-before qua: lock release/acquire, `volatile` write/read, start/join thread, và một số quy tắc cho `final`.

## 22. Safe publication là gì?

**Đáp:** Là đảm bảo object được “xuất bản” cho thread khác theo cách mà thread khác thấy state hợp lệ (không thấy field chưa khởi tạo). Cách phổ biến: publish qua `final` field, `volatile` reference, hoặc trong block `synchronized`.

## 23. `ThreadLocal` có rủi ro gì trong server?

**Đáp:** Dễ gây leak (giữ reference lâu trong thread pool), khó debug vì state “ẩn”, và sai khi chuyển execution giữa thread (async). Nếu dùng, phải `remove()` và cân nhắc context propagation.

## 24. `ReentrantLock` hơn `synchronized` ở điểm nào?

**Đáp:** Có tryLock, lock interruptible, fairness option, và condition variables linh hoạt. Nhưng dùng sai dễ quên unlock; `synchronized` đơn giản hơn và JVM tối ưu tốt.

## 25. Condition variable là gì (so với `wait/notify`)?

**Đáp:** `Condition` (từ `Lock`) cho phép nhiều “hàng đợi điều kiện” tách biệt, rõ ràng hơn `wait/notify` trên cùng một monitor. Giúp tránh đánh thức nhầm nhóm.

## 26. AQS (AbstractQueuedSynchronizer) là gì?

**Đáp:** Nền tảng để xây lock/synchronizer (vd `ReentrantLock`, `Semaphore`, `CountDownLatch`). Nó quản lý hàng đợi chờ (CLH-like), state và cơ chế park/unpark.

## 27. `Semaphore` dùng khi nào?

**Đáp:** Khi cần giới hạn số “permit” cho tài nguyên (vd tối đa N request đồng thời vào downstream), thay vì khóa độc quyền.

## 28. `CountDownLatch` vs `CyclicBarrier`?

**Đáp:**
- `CountDownLatch`: one-shot; chờ đến khi count về 0.
- `CyclicBarrier`: có thể tái sử dụng; nhiều thread chờ nhau tại barrier.

## 29. Vì sao `Collections.synchronizedList` không đủ trong mọi trường hợp?

**Đáp:** Nó synchronize từng method, nhưng iteration cần lock thủ công:

```java
synchronized (list) {
    for (var x : list) { /* ... */ }
}
```

Nếu không, có thể thấy race trong lúc iterate.

## 30. “Thundering herd” là gì trong concurrency?

**Đáp:** Khi nhiều thread bị đánh thức cùng lúc nhưng chỉ một số ít có thể tiến hành, gây context switch và giảm throughput. Hay gặp khi dùng `notifyAll()`/broadcast.
