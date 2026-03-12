# 08) Stream & Lập trình hàm (71–80)

## 71. Stream trong Java là gì?

**Đáp:** Stream là pipeline xử lý dữ liệu theo kiểu khai báo; không phải data structure và chỉ tiêu thụ một lần.

## 72. Intermediate vs terminal operation?

**Đáp:**
- Intermediate: lazy (`map`, `filter`, `sorted`).
- Terminal: kích hoạt chạy (`collect`, `forEach`, `reduce`, `count`).

## 73. `map` vs `flatMap`?

**Đáp:**
- `map`: biến đổi 1-1.
- `flatMap`: 1-n rồi flatten.

```java
Stream<String> words = lines.flatMap(l -> Arrays.stream(l.split("\\s+")));
```

## 74. `Optional` dùng để làm gì và không nên dùng để làm gì?

**Đáp:** Dùng để mô tả giá trị có/không có khi trả về, giảm `null`. Không nên lạm dụng làm field; cũng không thay thế mọi null check.

## 75. `orElse` vs `orElseGet`?

**Đáp:** `orElse(x)` tính `x` ngay; `orElseGet(supplier)` lazy.

```java
value.orElseGet(this::expensiveDefault);
```

## 76. Method reference là gì?

**Đáp:** Cú pháp rút gọn của lambda.

```java
list.forEach(System.out::println);
```

## 77. `Collectors.toList()` vs `Stream.toList()`?

**Đáp:** `Stream.toList()` trả list không sửa được (unmodifiable, tùy implement). `Collectors.toList()` thường mutable nhưng không cam kết.

## 78. Khi nào parallel stream là ý tưởng tệ?

**Đáp:** Workload nhỏ, nhiều contention, có I/O blocking, cần order/side-effect. Luôn đo đạc, không đoán.

## 79. `reduce` là gì và lỗi hay gặp?

**Đáp:** Gộp phần tử thành một. Lỗi hay gặp: accumulator không associative hoặc có side-effect, khiến kết quả sai khi parallel.

## 80. Ví dụ group dữ liệu bằng stream.

**Đáp:**

```java
Map<String, Long> counts = words.stream()
    .collect(Collectors.groupingBy(w -> w, Collectors.counting()));
```
