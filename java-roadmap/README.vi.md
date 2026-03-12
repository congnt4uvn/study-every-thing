# Lộ trình học Java (Từ số 0 → Thành thạo)

Đây là lộ trình **thực hành** để học **Java** từ nền tảng đến mức có thể xây dựng và vận hành một dịch vụ backend nhỏ theo phong cách production.

## Cách dùng lộ trình

- Học theo thứ tự.
- Mỗi bài: đọc khái niệm, chạy code, rồi hoàn thành checklist.
- Ghi chú lại: bạn đã thử gì, lỗi gì xảy ra, và bạn đã sửa thế nào.

## Điều kiện đầu vào

- Không cần biết lập trình trước (nhưng nếu biết sẽ học nhanh hơn).
- Máy tính có thể cài JDK và chạy terminal.

## Chuẩn bị môi trường (khuyến nghị)

- JDK 21 (hoặc 17 nếu bạn cần LTS phổ biến)
- IDE: IntelliJ IDEA Community hoặc VS Code
- Git

Tuỳ chọn (hữu ích về sau):

- Docker Desktop
- PostgreSQL (local) hoặc DB managed

## Danh sách bài học

1. [Bài 01 — Nền tảng Java + cài đặt](lessons/vi/01-java-fundamentals.md)
2. [Bài 02 — OOP cơ bản (class, interface)](lessons/vi/02-oop-fundamentals.md)
3. [Bài 03 — Exception, package và generics](lessons/vi/03-exceptions-packages-generics.md)
4. [Bài 04 — Collections + equals/hashCode](lessons/vi/04-collections-equals-hashcode.md)
5. [Bài 05 — Lambda, Streams, Optional](lessons/vi/05-functional-streams-optional.md)
6. [Bài 06 — I/O, JSON và HTTP client](lessons/vi/06-io-json-http.md)
7. [Bài 07 — Concurrency thiết yếu](lessons/vi/07-concurrency-essentials.md)
8. [Bài 08 — JVM cơ bản + hiệu năng](lessons/vi/08-jvm-performance-basics.md)
9. [Bài 09 — Testing + bộ công cụ chất lượng](lessons/vi/09-testing-quality.md)
10. [Bài 10 — Build tools: Maven / Gradle](lessons/vi/10-build-tools-maven-gradle.md)
11. [Bài 11 — Spring Boot + REST API](lessons/vi/11-spring-boot-rest.md)
12. [Bài 12 — SQL + JPA + transaction](lessons/vi/12-sql-jpa-transactions.md)
13. [Bài 13 — Capstone: dịch vụ Java kiểu production](lessons/vi/13-capstone-service.md)

## Gợi ý lịch học theo tuần

- Tuần 1: Bài 01–03
- Tuần 2: Bài 04–06
- Tuần 3: Bài 07–10
- Tuần 4: Bài 11–13 (capstone)

## Tiêu chí “thành thạo”

- Viết được Java “đúng chất” (class, generics, collections, streams).
- Xây được REST API có validation, test, và lưu dữ liệu DB.
- Hiểu JVM ở mức thực dụng (bộ nhớ, GC cơ bản, cách profile).
- Ship được service nhỏ với default tốt: logging, config, error handling, build lặp lại được.
