# 04) Collections & Generics (31–40)

## 31. `List` vs `Set` vs `Map` khác nhau?

**Đáp:**
- `List`: có thứ tự, cho phép trùng.
- `Set`: không trùng (theo `equals/hashCode`).
- `Map`: cặp key → value; key duy nhất.

## 32. `ArrayList` vs `LinkedList` — trade-off?

**Đáp:**
- `ArrayList`: truy cập theo index nhanh; append tốt; insert giữa tốn shift.
- `LinkedList`: insert/remove đầu-cuối tốt (khi có iterator), nhưng random access kém và cache locality xấu.

## 33. `HashMap` vs `TreeMap`?

**Đáp:**
- `HashMap`: trung bình O(1), không sắp xếp.
- `TreeMap`: O(log n), key được sort.

## 34. `HashSet` vs `TreeSet`?

**Đáp:** Tương tự map: `HashSet` hash-based; `TreeSet` sorted và log-time.

## 35. `ConcurrentHashMap` là gì, vì sao không chỉ `synchronized` `HashMap`?

**Đáp:** `ConcurrentHashMap` được thiết kế cho concurrency tốt hơn (giảm lock contention, hoạt động mở rộng tốt). Đồng bộ toàn bộ `HashMap` thường thành “nút cổ chai”.

## 36. Generics là gì và giải quyết vấn đề gì?

**Đáp:** Tăng type-safety lúc compile, giảm ép kiểu (cast).

```java
List<String> names = new ArrayList<>();
```

## 37. Type erasure là gì?

**Đáp:** Thông tin type parameter bị xóa phần lớn ở runtime. `List<String>` và `List<Integer>` đều là `List` lúc runtime, ảnh hưởng reflection/overload.

## 38. Wildcard `? extends T` và `? super T`?

**Đáp:**
- `? extends T`: đọc như T (producer), thường không add được.
- `? super T`: ghi được T (consumer), đọc ra `Object`.

Nhớ mẹo **PECS**.

## 39. Vì sao `List<Object>` không nhận `List<String>`?

**Đáp:** Generics **invariant**. Dùng `List<? extends Object>` (hoặc `List<?>`) nếu chỉ cần đọc.

## 40. Fail-fast và fail-safe iterator?

**Đáp:**
- Fail-fast (vd `ArrayList`): sửa cấu trúc khi iterate → `ConcurrentModificationException`.
- Fail-safe/weakly consistent (một số concurrent collections): iterator vẫn chạy trên snapshot/quan sát yếu.
