# 06) JVM, Memory & GC (51–60)

## 51. What is JIT compilation?

**A:** The JVM compiles frequently executed bytecode (“hot” code) into optimized native code at runtime to improve performance.

## 52. What is the difference between stack and heap?

**A:**
- **Stack**: per-thread frames (locals, call info). Fast allocation; freed on return.
- **Heap**: shared objects/arrays; managed by GC.

## 53. What causes `OutOfMemoryError`?

**A:** Common causes: memory leak (unbounded collections/caches), too small heap, too many classes/metaspace usage, huge allocations, off-heap native memory pressure.

## 54. `OutOfMemoryError` vs `StackOverflowError`?

**A:**
- `OutOfMemoryError`: cannot allocate memory (heap/metaspace/native).
- `StackOverflowError`: too deep recursion or huge stack frames.

## 55. What is GC, and what is it trying to optimize?

**A:** Garbage collection reclaims unreachable objects. Most collectors optimize for throughput, latency, or a balance, based on the observation that most objects die young.

## 56. What is a stop-the-world pause?

**A:** A period where application threads are paused so the JVM can perform a GC phase or other VM operations. Modern collectors reduce pause time but don’t eliminate it entirely.

## 57. What is “escape analysis”?

**A:** JIT analysis to determine if an object can be allocated on the stack or optimized away (scalar replacement) when it doesn’t escape a method/thread.

## 58. What are classloaders, and why do they matter?

**A:** Classloaders load classes and define namespaces. They matter for isolation (app servers), plugin systems, and memory leaks (classloader retention prevents unloading).

## 59. What is the Java Memory Model (JMM) in one sentence?

**A:** The JMM defines rules for visibility and ordering of reads/writes across threads, enabling correct concurrent programming via constructs like `volatile`, locks, and `final`.

## 60. Name a few JDK tools useful for JVM troubleshooting.

**A:** `jcmd`, `jstack`, `jmap`, `jstat`, `jconsole`, `jvisualvm` (external distribution), Flight Recorder (JFR) / Mission Control.
