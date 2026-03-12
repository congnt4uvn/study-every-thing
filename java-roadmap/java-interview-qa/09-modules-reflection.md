# 09) Modules, Reflection & Modern Java (81–90)

## 81. What is the Java module system (JPMS)?

**A:** Introduced in Java 9, JPMS organizes code into modules with explicit dependencies and strong encapsulation via `module-info.java`.

## 82. What does `requires` and `exports` mean in `module-info.java`?

**A:**
- `requires`: this module depends on another.
- `exports`: exposes a package for other modules to use.

## 83. Why can reflection fail on newer Java versions?

**A:** Strong encapsulation can block illegal reflective access. Libraries may need proper module declarations or JVM flags (as a last resort).

## 84. What is reflection, and when is it appropriate?

**A:** Reflection inspects/invokes classes/methods at runtime. It’s useful for frameworks (DI, serialization) but has downsides: performance overhead, reduced safety, harder refactoring.

## 85. What is an annotation, and how is it used?

**A:** Metadata attached to code elements. With retention `RUNTIME`, frameworks can read it via reflection.

## 86. What is the difference between `@Retention(SOURCE|CLASS|RUNTIME)`?

**A:**
- `SOURCE`: discarded by compiler.
- `CLASS`: in bytecode, not necessarily available at runtime.
- `RUNTIME`: available via reflection at runtime.

## 87. What are sealed classes?

**A:** A class/interface can restrict which types may extend/implement it.

```java
public sealed interface Shape permits Circle, Rectangle {}
```

Useful for closed hierarchies and exhaustive `switch`.

## 88. Pattern matching for `instanceof` — what problem does it solve?

**A:** It reduces boilerplate casting.

```java
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

## 89. What are text blocks (`"""`)?

**A:** Multi-line string literals that preserve formatting and reduce escaping, useful for JSON/SQL snippets.

## 90. What is a virtual thread (Project Loom), conceptually?

**A:** A lightweight thread managed by the JVM, enabling high concurrency with a thread-per-task style while reducing OS thread overhead.
