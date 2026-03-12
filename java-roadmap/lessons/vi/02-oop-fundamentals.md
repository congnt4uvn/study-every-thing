# Bài 02 — OOP cơ bản (class, interface)

## Mục tiêu

Hiểu class/object, encapsulation, composition vs inheritance, và cách interface giúp thiết kế sạch.

## Khái niệm chính

- **Class** = bản thiết kế; **object** = instance.
- Ưu tiên **composition** (“có”) hơn inheritance (“là”) khi có thể.
- Encapsulation: để field private; expose hành vi bằng method.
- Interface định nghĩa contract; class triển khai implementation.

## Thực hành

### 1) Class có encapsulation

```java
public final class BankAccount {
  private final String id;
  private long balanceCents;

  public BankAccount(String id, long initialBalanceCents) {
    if (id == null || id.isBlank()) {
      throw new IllegalArgumentException("id required");
    }
    if (initialBalanceCents < 0) {
      throw new IllegalArgumentException("balance cannot be negative");
    }
    this.id = id;
    this.balanceCents = initialBalanceCents;
  }

  public String getId() {
    return id;
  }

  public long getBalanceCents() {
    return balanceCents;
  }

  public void deposit(long amountCents) {
    if (amountCents <= 0) {
      throw new IllegalArgumentException("deposit must be positive");
    }
    balanceCents += amountCents;
  }

  public void withdraw(long amountCents) {
    if (amountCents <= 0) {
      throw new IllegalArgumentException("withdraw must be positive");
    }
    if (amountCents > balanceCents) {
      throw new IllegalStateException("insufficient funds");
    }
    balanceCents -= amountCents;
  }
}
```

### 2) Interface + dependency injection (tự làm)

```java
public interface Clock {
  long nowEpochMillis();
}

public final class SystemClock implements Clock {
  @Override
  public long nowEpochMillis() {
    return System.currentTimeMillis();
  }
}

public final class Greeter {
  private final Clock clock;

  public Greeter(Clock clock) {
    this.clock = clock;
  }

  public String greet(String name) {
    if (name == null || name.isBlank()) {
      return "Hello";
    }
    return "Hello, " + name + " (t=" + clock.nowEpochMillis() + ")";
  }
}
```

Điểm quan trọng:

- `Greeter` phụ thuộc **interface** thay vì implementation.
- Cách này giúp test dễ hơn.

### 3) Inheritance (dùng vừa đủ)

```java
public class Animal {
  public void speak() {
    System.out.println("...");
  }
}

public class Dog extends Animal {
  @Override
  public void speak() {
    System.out.println("woof");
  }
}
```

## Checklist

- Tạo được class với private fields và public methods.
- Giải thích được composition vs inheritance.
- Tạo và implement được interface.

## Lỗi thường gặp

- Để field public “cho tiện”. (Về sau rất khó giữ invariant.)
- Lạm dụng inheritance để reuse code. (Ưu tiên composition + helper nhỏ.)
- Tạo “God object” làm mọi thứ.

## Tiếp theo

Exception, package, generics — các công cụ dùng hằng ngày.
