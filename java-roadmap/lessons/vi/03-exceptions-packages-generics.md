# Bài 03 — Exception, package và generics

## Mục tiêu

Biết cách tổ chức code bằng package, hiểu cơ chế exception, và dùng generics để an toàn kiểu dữ liệu.

## Khái niệm chính

- Package ánh xạ theo thư mục; tránh trùng tên.
- Exception dành cho tình huống **bất thường** (không phải flow bình thường).
- Checked vs unchecked exception (thực tế: nhiều code ứng dụng hiện đại dùng unchecked, nhưng cần hiểu cả hai).
- Generics: `List<String>` nghĩa là list chỉ chứa string.

## Thực hành

### 1) Tạo package

Ví dụ đường dẫn:

- `src/main/java/com/example/app/Main.java`

```java
package com.example.app;

public class Main {
  public static void main(String[] args) {
    System.out.println("packaged!");
  }
}
```

### 2) Exception: throw, try/catch/finally

```java
static int parsePositiveInt(String s) {
  try {
    int n = Integer.parseInt(s);
    if (n <= 0) {
      throw new IllegalArgumentException("must be > 0");
    }
    return n;
  } catch (NumberFormatException e) {
    throw new IllegalArgumentException("not an integer: " + s, e);
  }
}
```

Nguyên tắc:

- Message phải có ngữ cảnh.
- Wrap exception khi cần giữ cause và thêm ý nghĩa.

### 3) Generics: wrapper có type

```java
public final class Box<T> {
  private final T value;

  public Box(T value) {
    this.value = value;
  }

  public T get() {
    return value;
  }
}

Box<String> b = new Box<>("hello");
String v = b.get();
```

### 4) Wildcards (đọc vs ghi)

```java
static int totalLength(java.util.List<? extends CharSequence> items) {
  int total = 0;
  for (CharSequence cs : items) {
    total += cs.length();
  }
  return total;
}
```

## Checklist

- Tổ chức code được bằng package.
- Throw và handle exception có chủ đích.
- Dùng generics (`List<T>`, `Map<K,V>`) tránh raw types.

## Lỗi thường gặp

- Catch `Exception` mọi nơi (quá rộng; che bug).
- Nuốt lỗi (catch rồi bỏ qua).
- Dùng raw type như `List` thay vì `List<String>`.

## Tiếp theo

Collections: các cấu trúc dữ liệu chuẩn trong Java.
