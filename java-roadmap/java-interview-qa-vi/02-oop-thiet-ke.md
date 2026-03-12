# 02) OOP & Thiết kế (11–20)

## 11. 4 trụ cột OOP là gì?

**Đáp:** Đóng gói (Encapsulation), Trừu tượng (Abstraction), Kế thừa (Inheritance), Đa hình (Polymorphism).

## 12. Đóng gói (encapsulation) trong Java là gì?

**Đáp:** Ẩn state nội bộ, chỉ expose hành vi qua method. Lợi ích: giữ invariant, giảm coupling, dễ refactor.

## 13. Đa hình (polymorphism) là gì? Ví dụ.

**Đáp:** Gọi hành vi qua kiểu cha/interface, thực thi cụ thể phụ thuộc runtime.

```java
List<String> a = new ArrayList<>();
List<String> b = new LinkedList<>();
```

## 14. Overloading và overriding khác gì?

**Đáp:**
- **Overloading**: cùng tên, khác tham số (quyết định lúc compile).
- **Overriding**: subclass thay thế implement của superclass (dispatch lúc runtime).

## 15. Composition là gì, vì sao hay được ưu tiên hơn inheritance?

**Đáp:** Composition là “has-a” (ủy quyền/delegation). Nó giảm vấn đề “fragile base class”, giúp thay đổi hành vi linh hoạt hơn.

## 16. Object bất biến (immutable) là gì? Lợi ích?

**Đáp:** State không đổi sau khi tạo. Lợi ích: thread-safe, dễ reasoning, dùng làm key/cache ổn định.

## 17. Hợp đồng giữa `equals()` và `hashCode()`?

**Đáp:** Nếu `a.equals(b)` true thì `a.hashCode() == b.hashCode()` phải true. Hash phải ổn định khi object không thay đổi.

## 18. `Comparable` và `Comparator` khác nhau?

**Đáp:**
- `Comparable<T>`: thứ tự tự nhiên qua `compareTo`.
- `Comparator<T>`: thứ tự tùy chỉnh bên ngoài qua `compare`.

## 19. `throw` và `throws` khác gì?

**Đáp:**
- `throw`: ném một exception instance.
- `throws`: khai báo method có thể ném exception.

## 20. Exception checked và unchecked khác nhau?

**Đáp:**
- **Checked**: phải khai báo/handle (vd `IOException`).
- **Unchecked**: `RuntimeException` (vd `NullPointerException`).
