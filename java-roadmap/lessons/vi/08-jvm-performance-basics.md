# Bài 08 — JVM cơ bản + hiệu năng

## Mục tiêu

Hiểu Java chạy trên JVM như thế nào, nắm bộ nhớ/GC cơ bản, và hình thành thói quen đo trước khi tối ưu.

## Khái niệm chính

- Java compile ra bytecode; JVM interpret và JIT-compile code “hot”.
- GC quản lý bộ nhớ; cấp phát object rẻ nhưng tốc độ cấp phát (allocation rate) mới là thứ cần chú ý.
- Tool hay gặp: `jcmd`, `jstack`, `jmap` (nâng cao), profiler (VisualVM, YourKit, async-profiler).
- Benchmark: microbenchmark rất dễ sai; khi cần số liệu chuẩn hãy dùng JMH.

## Thực hành

### 1) Xem cấu hình VM/memory

Chạy:

```bash
java -XshowSettings:vm -version
```

Tìm thông tin heap.

### 2) Đo thời gian đơn giản (chỉ để sanity check)

```java
long start = System.nanoTime();

long sum = 0;
for (int i = 0; i < 10_000_000; i++) {
  sum += i;
}

long elapsedMs = (System.nanoTime() - start) / 1_000_000;
System.out.println("sum=" + sum + " elapsedMs=" + elapsedMs);
```

### 3) Tư duy profiling

Trước khi tối ưu, hỏi:

- Chậm ở đâu? (đo)
- Tốn thời gian ở đâu? (profile)
- Thay đổi nào hiệu quả? (lặp lại)

## Checklist

- Giải thích được JVM ở mức cao (bytecode, JIT, GC).
- Biết vì sao benchmark kiểu `System.nanoTime()` có thể gây hiểu nhầm.
- Biết ít nhất 1 profiler để dùng.

## Lỗi thường gặp

- Tối ưu không đo.
- Tuning GC quá sớm.
- Nhầm throughput và latency.

## Tiếp theo

Testing và chất lượng: tự tin refactor mà không sợ vỡ.
