# 01) Language Basics (1–10)

## 1. What is Java, and why is it “platform independent”?

**A:** Java source compiles to **bytecode** (`.class`). The bytecode runs on a **JVM** for the target OS/CPU. “Write once, run anywhere” is achieved by shipping bytecode + JVM implementation.

## 2. JDK vs JRE vs JVM — what’s the difference?

**A:**
- **JVM**: runs bytecode (execution engine + GC + JIT).
- **JRE**: JVM + standard libraries to run apps.
- **JDK**: JRE + tools to build/debug (e.g., `javac`, `jar`, `javadoc`, `jcmd`).

## 3. What are primitives in Java? List them.

**A:** 8 primitives: `byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean`. They are value types (not objects) and have fixed sizes (except `boolean` is JVM-dependent in memory representation).

## 4. What is autoboxing/unboxing?

**A:** Automatic conversion between primitives and wrapper types.

```java
Integer x = 10;   // autoboxing (int -> Integer)
int y = x;        // unboxing (Integer -> int)
```

Watch for `NullPointerException` when unboxing `null`.

## 5. Explain `==` vs `.equals()`.

**A:**
- `==` compares **primitive values** or **object references** (same object?).
- `.equals()` compares **logical equality** (by convention) and can be overridden.

`String` overrides `.equals()` to compare characters.

## 6. What are `static` members used for?

**A:** `static` belongs to the **class**, not an instance.
- `static` fields: shared state (use carefully; concurrency + testability).
- `static` methods: utility behavior not tied to instance state.
- `static` blocks: one-time class initialization.

## 7. What is the difference between `final`, `finally`, and `finalize()`?

**A:**
- `final`: cannot be reassigned (variable), overridden (method), or extended (class).
- `finally`: block that runs after `try` (even if exceptions occur).
- `finalize()`: legacy GC hook; deprecated and should be avoided.

## 8. What is pass-by-value in Java?

**A:** Java is **always pass-by-value**.
- For primitives: the value is copied.
- For objects: the **reference value** is copied (both point to same object).

## 9. What are access modifiers and their scopes?

**A:**
- `private`: only inside the class.
- (package-private): no modifier; only within package.
- `protected`: package + subclasses (even in other packages, with rules).
- `public`: everywhere.

## 10. What is the difference between an interface and an abstract class?

**A:**
- **Interface**: describes a contract; can have `default`/`static` methods; multiple inheritance of type.
- **Abstract class**: partial implementation + shared state; single inheritance.
