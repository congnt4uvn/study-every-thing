# 04) Collections & Generics (31–40)

## 31. List vs Set vs Map — what’s the difference?

**A:**
- `List`: ordered, allows duplicates.
- `Set`: no duplicates (by `equals/hashCode`).
- `Map`: key → value pairs; keys are unique.

## 32. `ArrayList` vs `LinkedList` — tradeoffs?

**A:**
- `ArrayList`: fast random access, amortized append; inserts in middle cost due to shifting.
- `LinkedList`: fast inserts/removes at ends (with iterator), but poor cache locality and slow random access.

In practice, `ArrayList` is most common.

## 33. `HashMap` vs `TreeMap`?

**A:**
- `HashMap`: O(1) average operations; no ordering.
- `TreeMap`: O(log n); sorted by key (natural or comparator).

## 34. `HashSet` vs `TreeSet`?

**A:** Similar to map counterparts: `HashSet` is hash-based, `TreeSet` is sorted and log-time.

## 35. What is a `ConcurrentHashMap`, and why not just synchronize a `HashMap`?

**A:** `ConcurrentHashMap` provides concurrent access with internal coordination designed for scalability. Synchronizing the whole map typically becomes a single lock bottleneck.

## 36. What are generics, and what problem do they solve?

**A:** Generics add **compile-time type safety** and remove many casts.

```java
List<String> names = new ArrayList<>();
```

## 37. What is type erasure?

**A:** Generic type parameters are erased at runtime (mostly). `List<String>` and `List<Integer>` are both `List` at runtime, affecting reflection and overloads.

## 38. Explain wildcards: `? extends T` vs `? super T`.

**A:**
- `? extends T`: producer (read T), you generally can’t add (except `null`).
- `? super T`: consumer (write T), reading yields `Object`.

Rule of thumb: **PECS** — Producer Extends, Consumer Super.

## 39. Why does `List<Object>` not accept `List<String>`?

**A:** Generics are **invariant**: `String` is a subtype of `Object`, but `List<String>` is not a subtype of `List<Object>`. Use `List<? extends Object>` if you need covariance.

## 40. Fail-fast vs fail-safe iterators?

**A:**
- Fail-fast (e.g., `ArrayList`): iterator throws `ConcurrentModificationException` if modified structurally during iteration.
- Fail-safe (e.g., some concurrent collections): iterator works on a snapshot/weakly consistent view.
