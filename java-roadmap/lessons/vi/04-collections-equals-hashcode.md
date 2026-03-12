# Bài 04 — Collections + equals/hashCode

## Mục tiêu

Học các collection cốt lõi (`List`, `Set`, `Map`) và quy tắc `equals()`/`hashCode()` để chúng hoạt động đúng.

## Khái niệm chính

- `List`: có thứ tự, cho phép trùng.
- `Set`: không cho phép trùng.
- `Map`: key → value.
- Trực giác Big-O quan trọng (ví dụ `HashMap` lookup trung bình $O(1)$).
- `equals()` và `hashCode()` phải nhất quán, nhất là khi dùng `HashSet` và key của `HashMap`.

## Thực hành

### 1) List và duyệt

```java
var names = new java.util.ArrayList<String>();
names.add("Ada");
names.add("Linus");

for (String name : names) {
  System.out.println(name);
}
```

### 2) Map

```java
var ages = new java.util.HashMap<String, Integer>();
ages.put("Ada", 20);

System.out.println(ages.get("Ada"));
System.out.println(ages.getOrDefault("Bob", -1));
```

### 3) equals/hashCode cho value object

```java
import java.util.Objects;

public final class UserId {
  private final String value;

  public UserId(String value) {
    if (value == null || value.isBlank()) {
      throw new IllegalArgumentException("value required");
    }
    this.value = value;
  }

  public String value() {
    return value;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof UserId other)) return false;
    return value.equals(other.value);
  }

  @Override
  public int hashCode() {
    return Objects.hash(value);
  }

  @Override
  public String toString() {
    return value;
  }
}
```

Thử:

```java
var set = new java.util.HashSet<UserId>();
set.add(new UserId("u1"));
System.out.println(set.contains(new UserId("u1"))); // phải là true
```

### 4) Khi nào dùng cái nào

- Cần thứ tự? `ArrayList`.
- Cần unique? `HashSet`.
- Cần lookup theo key? `HashMap`.
- Cần sort key? `TreeMap` / `TreeSet`.

## Checklist

- Chọn được `List` vs `Set` vs `Map` cho use case.
- Implement đúng `equals()`/`hashCode()` cho value object.
- Hiểu vì sao mutate key trong `HashMap` là nguy hiểm.

## Lỗi thường gặp

- Dùng object mutable làm key.
- Override `equals()` nhưng quên `hashCode()`.
- Tối ưu quá sớm bằng các collection “lạ”.

## Tiếp theo

Functional Java: lambda, streams, Optional.
