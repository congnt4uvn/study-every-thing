# 02) OOP & Design (11–20)

## 11. What are the four OOP pillars?

**A:** Encapsulation, Abstraction, Inheritance, Polymorphism.

## 12. What is encapsulation in Java?

**A:** Hide internal state and expose behavior via methods (often getters/setters). Benefits: invariants, refactoring safety, reduced coupling.

## 13. What is polymorphism? Give an example.

**A:** The same interface can be implemented by different classes and invoked through the base type.

```java
List<String> a = new ArrayList<>();
List<String> b = new LinkedList<>();
```

Both are `List`, behavior differs internally.

## 14. Overloading vs overriding?

**A:**
- **Overloading**: same method name, different parameters (compile-time).
- **Overriding**: subclass replaces superclass method implementation (runtime dispatch).

## 15. What is composition, and why is it often preferred over inheritance?

**A:** Composition means “has-a” (delegation) instead of “is-a”. It reduces fragile base-class issues and makes behavior pluggable.

## 16. What is an immutable object? Why is it useful?

**A:** State cannot change after construction. Advantages: thread-safety, safe sharing, simpler reasoning, good cache keys.

## 17. What is the contract between `equals()` and `hashCode()`?

**A:** If `a.equals(b)` is true, `a.hashCode() == b.hashCode()` must be true. Also, `hashCode()` should be consistent while the object is unchanged.

## 18. What is the difference between `Comparable` and `Comparator`?

**A:**
- `Comparable<T>` defines natural ordering via `compareTo`.
- `Comparator<T>` defines external/custom ordering via `compare`.

Use `Comparator` for multiple sort strategies.

## 19. What is the difference between `throw` and `throws`?

**A:**
- `throw`: actually throws an exception instance.
- `throws`: declares that a method may throw exceptions.

## 20. What is a “checked” vs “unchecked” exception?

**A:**
- **Checked**: must be declared/handled (`IOException`).
- **Unchecked**: `RuntimeException` and subclasses (`NullPointerException`).

Checked exceptions model recoverable conditions; unchecked often model programming errors.
