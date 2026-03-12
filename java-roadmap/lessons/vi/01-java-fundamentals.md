# Bài 01 — Nền tảng Java + cài đặt

## Mục tiêu

Cài JDK, chạy được chương trình Java, và nắm các phần cơ bản nhất: biến, kiểu dữ liệu, điều khiển luồng, và hàm (method).

## Khái niệm chính

- **JDK vs JRE**: JDK có compiler (`javac`) và tool; runtime chạy bytecode.
- File `.java` được compile thành `.class` chạy trên JVM.
- Java là ngôn ngữ **kiểu tĩnh**: type được kiểm tra khi compile.
- Điểm vào chương trình: `public static void main(String[] args)`.

## Cài đặt (chọn 1 cách)

### Cách A — IDE (khuyến nghị)

1. Cài JDK 21.
2. Cài IntelliJ IDEA Community.
3. Tạo project mới → Java.

### Cách B — Dùng terminal

1. Cài JDK 21.
2. Kiểm tra:

- `java -version`
- `javac -version`

## Thực hành

### 1) Hello World

Tạo `Hello.java`:

```java
public class Hello {
  public static void main(String[] args) {
    System.out.println("Hello, Java!");
  }
}
```

Compile và chạy:

```bash
javac Hello.java
java Hello
```

### 2) Kiểu dữ liệu và biến

```java
int age = 20;
double price = 19.99;
boolean active = true;
String name = "Ada";

System.out.println(name + " is " + age);
```

Lưu ý:

- `String` là class.
- `int`, `double`, `boolean` là primitive.

### 3) Control flow

```java
int n = 7;

if (n % 2 == 0) {
  System.out.println("even");
} else {
  System.out.println("odd");
}

for (int i = 0; i < 3; i++) {
  System.out.println(i);
}

int x = 0;
while (x < 3) {
  System.out.println("x=" + x);
  x++;
}
```

### 4) Method (hàm)

```java
static int add(int a, int b) {
  return a + b;
}
```

## Checklist

- Chạy được `java -version` và `javac -version`.
- Compile và chạy được file `.java`.
- Hiểu kiểu dữ liệu cơ bản và cách `if/for/while` hoạt động.
- Viết được method đơn giản.

## Lỗi thường gặp

- Nhầm `==` (so sánh) với `=` (gán).
- Quên Java cần class bao ngoài cho `main`.
- Dùng `var` quá sớm khi chưa hiểu type.

## Tiếp theo

Học OOP: class, object, và interface.
