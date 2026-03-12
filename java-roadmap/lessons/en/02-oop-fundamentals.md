# Lesson 02 — OOP fundamentals (classes, interfaces)

## Goal

Understand classes/objects, encapsulation, composition vs inheritance, and how interfaces enable clean design.

## Key concepts

- **Class** = blueprint; **object** = instance.
- Prefer **composition** (“has-a”) over inheritance (“is-a”) when possible.
- Encapsulation: keep fields private; expose behavior via methods.
- Interfaces define a contract; classes provide an implementation.

## Hands-on

### 1) Define a class with encapsulation

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

### 2) Interfaces + dependency injection (manual)

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

Notice:

- `Greeter` depends on the **interface**, not the implementation.
- This makes testing easy later.

### 3) Inheritance (use sparingly)

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

- You can create a class with private fields and public methods.
- You can explain composition vs inheritance.
- You can define and implement an interface.

## Common pitfalls

- Making fields public “for convenience”. (It becomes hard to enforce invariants.)
- Overusing inheritance to share code. (Prefer composition and small helpers.)
- Creating “God objects” that do everything.

## Next

Exceptions, packages, and generics — the tools you’ll use daily.
