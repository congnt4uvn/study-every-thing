# Lesson 01 — Java fundamentals + setup

## Goal

Install a JDK, run Java programs, and learn the absolute basics of the language: variables, types, control flow, and functions.

## Key concepts

- **JDK vs JRE**: the JDK includes the compiler (`javac`) and tools; the runtime executes bytecode.
- Java source files (`.java`) compile to bytecode (`.class`) that runs on the JVM.
- Java is **statically typed**: types are checked at compile time.
- Program entry point: `public static void main(String[] args)`.

## Setup (pick one workflow)

### Option A — IDE (recommended)

1. Install JDK 21.
2. Install IntelliJ IDEA Community.
3. Create a new project → Java.

### Option B — Terminal only

1. Install JDK 21.
2. Verify:

- `java -version`
- `javac -version`

## Hands-on

### 1) Hello World

Create `Hello.java`:

```java
public class Hello {
  public static void main(String[] args) {
    System.out.println("Hello, Java!");
  }
}
```

Compile and run:

```bash
javac Hello.java
java Hello
```

### 2) Types and variables

```java
int age = 20;
double price = 19.99;
boolean active = true;
String name = "Ada";

System.out.println(name + " is " + age);
```

Things to notice:

- `String` is a class.
- `int`, `double`, `boolean` are primitives.

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

### 4) Methods (functions)

```java
static int add(int a, int b) {
  return a + b;
}
```

## Checklist

- You can run `java -version` and `javac -version`.
- You can compile and run a `.java` file.
- You understand basic types and how `if/for/while` works.
- You can write a simple method.

## Common pitfalls

- Confusing `==` (comparison) with `=` (assignment).
- Forgetting that Java needs a class wrapper for `main`.
- Using `var` everywhere without understanding types (save `var` for later).

## Next

Learn OOP fundamentals: classes, objects, and interfaces.
