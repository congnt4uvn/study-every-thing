# 07) Đa luồng (61–70)

## 61. Process và thread khác nhau thế nào?

**Đáp:** Process có không gian địa chỉ riêng; thread chia sẻ bộ nhớ trong cùng process nhưng có stack riêng và được scheduler quản lý.

## 62. `synchronized` làm gì?

**Đáp:** Cung cấp mutual exclusion và thiết lập happens-before: vào monitor = acquire lock; ra monitor = release lock, đảm bảo visibility.

## 63. `volatile` dùng để làm gì?

**Đáp:** Đảm bảo **nhìn thấy** cập nhật giữa các thread và hạn chế reordering; không đảm bảo atomic cho thao tác tổng hợp.

```java
private volatile boolean running = true;
```

## 64. Vì sao `i++` không thread-safe?

**Đáp:** Là chuỗi read-modify-write; có thể lost update. Dùng `AtomicInteger.incrementAndGet()` hoặc lock.

## 65. Deadlock là gì? Nguyên nhân hay gặp?

**Đáp:** Nhiều thread giữ lock và chờ lock của nhau theo vòng. Hay do lock theo thứ tự không nhất quán.

## 66. `wait()` vs `sleep()`?

**Đáp:**
- `wait()`: nhả monitor và chờ `notify`; phải gọi khi đang giữ monitor.
- `sleep()`: ngủ nhưng **không** nhả lock.

## 67. `notify()` vs `notifyAll()`?

**Đáp:** `notify()` đánh thức 1 thread; `notifyAll()` đánh thức tất cả. `notifyAll()` thường an toàn hơn nhưng có thể gây thundering herd.

## 68. `ExecutorService` là gì, vì sao dùng?

**Đáp:** Quản lý thread pool và chạy task theo policy; tách “submit” khỏi “execute”.

```java
ExecutorService pool = Executors.newFixedThreadPool(8);
Future<Integer> f = pool.submit(() -> 42);
```

## 69. `Runnable` vs `Callable`?

**Đáp:** `Runnable` không trả kết quả và không ném checked exception; `Callable<V>` trả kết quả và có thể ném checked exception.

## 70. `CompletableFuture` là gì, dùng khi nào?

**Đáp:** API bất đồng bộ để compose pipeline, combine, xử lý lỗi.

```java
CompletableFuture.supplyAsync(this::load)
    .thenApply(this::transform)
    .exceptionally(ex -> fallback());
```
