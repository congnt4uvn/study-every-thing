# Bài 13 — Capstone: dịch vụ Java kiểu production

## Mục tiêu

Xây một service nhỏ end-to-end với thói quen kỹ thuật tốt: API sạch, test, persistence, config, và mức sẵn sàng vận hành cơ bản.

## Dự án: “Task Tracker API”

Xây REST API quản lý task.

### Yêu cầu (MVP)

- Tạo task
- Lấy task theo id
- List task (pagination đơn giản: `limit` + `offset`)
- Cập nhật trạng thái task
- Xoá task

Trường dữ liệu:

- `id` (string)
- `title` (không được rỗng)
- `status` (`OPEN`, `DONE`)
- `createdAt` (timestamp)

### Yêu cầu phi chức năng

- Validation lỗi trả 400.
- Không tìm thấy trả 404.
- Unit test cho core service logic.
- Integration test cho repository (tuỳ chọn nhưng khuyến nghị).

## Kiến trúc gợi ý

- Controller: chỉ map request/response
- Service: business rule + transaction
- Repository: truy cập DB
- DTO: shape public API
- Entity: shape DB

## Checklist theo bước

1) Tạo Spring Boot project (Web, Validation, Data JPA).

2) Thêm DB + migrations

- Dùng H2 trước nếu muốn nhanh.
- Chuyển sang PostgreSQL khi sẵn sàng.
- Thêm Flyway migration tạo bảng `tasks`.

3) Implement domain logic

- Định nghĩa rule chuyển trạng thái (nếu có).
- Validate title.

4) Implement endpoints

- `POST /api/tasks`
- `GET /api/tasks/{id}`
- `GET /api/tasks?limit=..&offset=..`
- `PATCH /api/tasks/{id}` (update status)
- `DELETE /api/tasks/{id}`

5) Thêm tests

- Unit test cho `TaskService`.
- Test validation và not-found (controller test hoặc integration).

6) Thêm “operational basics”

- Logging nhất quán (ít nhất message rõ ràng).
- Config bằng `application.yml` + biến môi trường.
- Thêm `/actuator/health` nếu dùng Spring Actuator.

## “Done” nghĩa là gì

- Chạy service local và gọi bằng curl/Postman.
- Test chạy kiểu CI bằng `mvn test` hoặc `gradle test`.
- Giải thích được vì sao business logic nên nằm ở service.

## Next (tuỳ chọn)

- Thêm authentication/authorization.
- Thêm cache (Redis) cho endpoint đọc nhiều.
- Docker hoá và thêm CI pipeline đơn giản.
