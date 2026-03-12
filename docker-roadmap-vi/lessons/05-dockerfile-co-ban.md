# Bài 05 — Nền tảng Dockerfile

## Mục tiêu
- Viết Dockerfile để build image chạy được
- Hiểu các instruction chính: `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`, `ENTRYPOINT`, `EXPOSE`
- Hiểu build context và vì sao `.dockerignore` quan trọng

## Build context
Khi bạn chạy `docker build .`, dấu `.` là **build context**.
- Docker sẽ gửi context cho builder
- Context lớn làm build chậm
- File nhạy cảm trong context có thể bị copy vào image ngoài ý muốn

## Ví dụ Dockerfile tối giản
Ví dụ này build image chạy một lệnh đơn giản.

```dockerfile
FROM alpine:3.19
CMD ["echo", "hello from a container"]
```

Build và run:
```powershell
docker build -t hello-alpine:1.0 .
docker run --rm hello-alpine:1.0
```

## Các instruction quan trọng (ý nghĩa thực tế)
- `FROM` — base image
- `WORKDIR` — đặt thư mục làm việc (tạo nếu chưa có)
- `COPY` — copy file vào image (từ build context)
- `RUN` — chạy lệnh lúc build (tạo layer mới)
- `ENV` — biến môi trường
- `EXPOSE` — “tài liệu” về port dự kiến (không tự publish port)
- `CMD` — tham số mặc định (có thể override khi `docker run`)
- `ENTRYPOINT` — chương trình chính (thường dùng cho “luôn chạy cái này”)

### `CMD` vs `ENTRYPOINT`
- `CMD` là “tham số mặc định”.
- `ENTRYPOINT` là “chương trình”.

Mẫu phổ biến:
```dockerfile
ENTRYPOINT ["myapp"]
CMD ["--help"]
```

## Lab thực hành: container hoá HTTP server nhỏ (không cần code)
Dùng Python built-in web server.

Tạo folder có file `index.html`, rồi dùng Dockerfile:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY index.html /app/index.html
EXPOSE 8000
CMD ["python", "-m", "http.server", "8000"]
```

Build + run:
```powershell
docker build -t tiny-web:1.0 .
docker run --rm -p 8000:8000 tiny-web:1.0
```

Vào http://localhost:8000

## Checklist
- Tôi giải thích được build context
- Tôi build image từ Dockerfile và chạy được
- Tôi hiểu `CMD` vs `ENTRYPOINT` ở mức cơ bản

## Lỗi hay gặp
- **Quên build context**: `COPY` chỉ copy từ build context (không copy từ path bất kỳ trên máy).
- **Copy quá nhiều**: bài sau bạn sẽ xử lý bằng `.dockerignore`.
- **Dùng `latest` khắp nơi**: nên chọn version cụ thể cho base.
