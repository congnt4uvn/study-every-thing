# Những điểm mới trong Java 17 (LTS) (Bài học)

Java 17 (2021) là bản Long-Term Support. Trong thực tế, nâng cấp lên Java 17 thường đồng nghĩa với việc “nhận” một loạt cải tiến ngôn ngữ và nền tảng đã chín muồi xuyên suốt Java 9–17.

Bài này tập trung vào các tính năng bạn hay gặp nhất khi chuyển từ Java 8 lên Java 17.

## 1) Hệ thống Module (JPMS) (Java 9)

**Mục tiêu:** Đóng gói tốt hơn và cấu hình phụ thuộc rõ ràng.

- *Module* là tập package có tên, khai báo phụ thuộc tường minh.
- Khai báo module trong `module-info.java`.

Ví dụ tối giản:

```java
module com.example.app {
  requires java.sql;
  exports com.example.app.api;
}
```

Gợi ý thực tế:
- Nhiều ứng dụng chạy Java 17 vẫn không cần module hoá code nội bộ.
- Dù vậy, bạn hưởng lợi từ việc JDK “đóng” các internal API (ít hack reflection hơn).

## 2) `var` cho biến local (Java 10)

**Mục tiêu:** Giảm boilerplate nhưng vẫn giữ static typing.

```java
import java.util.ArrayList;

public class VarDemo {
  public static void main(String[] args) {
    var list = new ArrayList<String>();
    list.add("hello");
    System.out.println(list.get(0));
  }
}
```

Quy tắc:
- `var` chỉ dùng cho **biến local**.
- Kiểu được suy luận tại compile-time và “cố định”.

## 3) HTTP Client chuẩn (Java 11)

`java.net.http.HttpClient` thay thế `HttpURLConnection`.

```java
import java.net.URI;
import java.net.http.*;

public class HttpClientDemo {
  public static void main(String[] args) throws Exception {
    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder(URI.create("https://example.com"))
        .GET()
        .build();

    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    System.out.println(response.statusCode());
  }
}
```

## 4) Text Blocks (Java 15)

**Mục tiêu:** String nhiều dòng rõ ràng, ít escape.

```java
public class TextBlocks {
  public static void main(String[] args) {
    String json = """
      {
        "name": "Alice",
        "active": true
      }
      """;

    System.out.println(json);
  }
}
```

## 5) Switch Expressions (Java 14)

Switch có thể là expression trả về giá trị.

```java
public class SwitchExpr {
  static int score(String grade) {
    return switch (grade) {
      case "A" -> 100;
      case "B" -> 80;
      case "C" -> 60;
      default -> 0;
    };
  }
}
```

## 6) Records (Java 16)

**Mục tiêu:** Data class bất biến (immutable) gọn nhẹ.

```java
public class Records {
  public record Point(int x, int y) {}

  public static void main(String[] args) {
    Point p = new Point(1, 2);
    System.out.println(p.x() + "," + p.y());
  }
}
```

## 7) Pattern Matching cho `instanceof` (Java 16)

```java
public class InstanceofPattern {
  static int lengthIfString(Object o) {
    if (o instanceof String s) {
      return s.length();
    }
    return -1;
  }
}
```

## 8) Sealed Classes (chính thức ở Java 17)

**Mục tiêu:** Giới hạn những class nào được phép kế thừa/implement.

```java
public class Sealed {
  public sealed interface Shape permits Circle, Rectangle {}

  public static final class Circle implements Shape {
    public final double r;
    public Circle(double r) { this.r = r; }
  }

  public static final class Rectangle implements Shape {
    public final double w, h;
    public Rectangle(double w, double h) { this.w = w; this.h = h; }
  }
}
```

## 9) NullPointerException “thông minh hơn” (Java 14)

Thông báo lỗi NPE thường chỉ ra chính xác đoạn null dereference trong chuỗi gọi (ví dụ `a.b().c()`).

## 10) GC & hiệu năng (9–17)

- G1 GC là mặc định (Java 9+)
- Nhiều cải tiến JIT/runtime
- Nhận diện tốt hơn môi trường container (giới hạn RAM/CPU)

## Checklist nâng cấp (Java 8 → 17)

- Cập nhật Maven/Gradle plugins, CI images, IDE.
- Kiểm tra lại reflection vào JDK internal (có thể cần `--add-opens`).
- Re-test TLS/crypto (server cũ có thể lỗi).

## Bài tập

1. Chuyển DTO class sang `record`.
2. Dùng text block để embed JSON/SQL.
3. Model một hierarchy đóng (vd `PaymentMethod`) bằng sealed types.
