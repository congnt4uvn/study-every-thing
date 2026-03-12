# Bài 10 — Build tools: Maven / Gradle

## Mục tiêu

Hiểu cấu trúc project chuẩn và cách Maven/Gradle quản lý dependency, compile và test.

## Khái niệm chính

- Build tool giúp project tái lập được.
- Dependency có version; cần nâng cấp có chủ đích.
- Layout chuẩn (Maven/Gradle):
  - `src/main/java` (code chạy thật)
  - `src/test/java` (test)

## Thực hành (đi theo Maven)

### 1) Tạo Maven project

Nếu đã có Maven:

```bash
mvn -v
```

Generate project (ví dụ):

```bash
mvn archetype:generate -DgroupId=com.example -DartifactId=demo -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

### 2) Thêm dependency

Dependency hay gặp:

- JUnit 5 cho test
- Jackson cho JSON

Bạn sẽ sửa `pom.xml` để thêm.

### 3) Build và test

```bash
mvn test
mvn package
```

## Thực hành (đi theo Gradle)

Nếu dùng Gradle, hãy nắm tương đương:

- `build.gradle` / `build.gradle.kts`
- `gradle test`
- khối khai báo dependency

## Checklist

- Giải thích được vì sao build tool quan trọng.
- Thêm được dependency và dùng trong code.
- Chạy được test qua build tool.

## Lỗi thường gặp

- Copy/paste version ngẫu nhiên.
- Không pin phiên bản tool trong team.
- Trộn khái niệm Gradle/Maven.

## Tiếp theo

Spring Boot: cách phổ biến để build HTTP API trong Java.
