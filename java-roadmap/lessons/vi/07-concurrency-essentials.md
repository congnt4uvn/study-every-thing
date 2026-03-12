# Bài 07 — Concurrency thiết yếu

## Mục tiêu

Hiểu thread, executor, các primitive concurrency; học các pattern an toàn và tránh lỗi phổ biến.

## Khái niệm chính

- Race condition: kết quả phụ thuộc timing.
- Visibility: thread này có thể không thấy update của thread khác nếu không sync.
- Ưu tiên utility cấp cao: `ExecutorService`, `CompletableFuture`.
- Dùng `synchronized`/lock khi cần, và giữ vùng critical nhỏ.

## Thực hành

### 1) Vấn đề: shared mutable state

```java
public final class Counter {
  private int value = 0;
  public void inc() { value++; }
  public int get() { return value; }
}
```

Nếu nhiều thread gọi `inc()`, có thể bị mất lượt tăng.

### 2) Sửa bằng synchronized

```java
public final class SafeCounter {
  private int value = 0;
  public synchronized void inc() { value++; }
  public synchronized int get() { return value; }
}
```

### 3) Ưu tiên Atomic cho counter

```java
import java.util.concurrent.atomic.AtomicInteger;

public final class AtomicCounter {
  private final AtomicInteger value = new AtomicInteger(0);
  public void inc() { value.incrementAndGet(); }
  public int get() { return value.get(); }
}
```

### 4) ExecutorService để chạy task

```java
import java.util.concurrent.*;

ExecutorService pool = Executors.newFixedThreadPool(4);

Future<Integer> f = pool.submit(() -> 40 + 2);
System.out.println(f.get());

pool.shutdown();
```

### 5) CompletableFuture cho pipeline async

```java
import java.util.concurrent.CompletableFuture;

CompletableFuture<Integer> cf = CompletableFuture
  .supplyAsync(() -> 21)
  .thenApply(x -> x * 2);

System.out.println(cf.join());
```

## Checklist

- Giải thích được race condition và cách phòng tránh.
- Chạy được task trong thread pool.
- Chain async step bằng `CompletableFuture`.

## Lỗi thường gặp

- Tạo thread mới cho mỗi request/task.
- Quên shutdown executor.
- Giữ lock trong lúc làm I/O chậm.

## Tiếp theo

JVM và hiệu năng: code chạy như thế nào và đo lường ra sao.
