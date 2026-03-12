# Bài 13 — Capstone: containerize app + publish image

## Mục tiêu
Chứng minh bạn có thể làm end-to-end:
- Tạo Dockerfile “hướng production”
- Chạy local bằng Compose (app + dependency)
- Tag và publish image (lên registry bạn quản lý)

## Gợi ý dự án capstone
Chọn một web app đơn giản bạn chạy được local (bất kỳ ngôn ngữ). Ví dụ:
- Python Flask/FastAPI
- Node Express
- .NET minimal API

Thêm 1 dependency service:
- Postgres hoặc Redis

## Deliverables (thứ bạn cần làm ra)
1) `.dockerignore`
2) `Dockerfile` (multi-stage nếu stack của bạn có bước build)
3) `compose.yaml` có ít nhất 2 service
4) README ngắn hướng dẫn chạy

## Template tham khảo (tuỳ biến theo stack)
### `.dockerignore` (khởi đầu)
```gitignore
.git
.env
.env.*
**/*.log
node_modules
bin
obj
__pycache__
.venv
```

### `compose.yaml` (ví dụ app + postgres)
```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: example
      POSTGRES_USER: app
      POSTGRES_DB: app
    volumes:
      - dbdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  app:
    build:
      context: .
    environment:
      DATABASE_URL: "postgres://app:example@db:5432/app"
    ports:
      - "8080:8080"
    depends_on:
      - db

volumes:
  dbdata:
```

### Mẫu Dockerfile
#### Mẫu A: runtime đơn giản (không có bước build)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["python", "app.py"]
```

#### Mẫu B: multi-stage build (khi bạn compile/build assets)
Multi-stage hữu ích nhất khi bạn có build output để copy sang runtime image nhỏ.

## Chạy và xác nhận
```powershell
# Build và start toàn bộ
docker compose up --build

# Terminal khác: xem trạng thái
docker compose ps

# Xem logs
docker compose logs -f
```

Checklist xác nhận:
- App chạy mà không cần bước thủ công ngoài Compose
- Restart container không làm mất dữ liệu DB (volume hoạt động)
- Không “nướng” secrets vào image
- Image build lặp lại được

## Publish image
1. Chọn scheme version (vd `1.0.0`, `1.0.1`)
2. Tag và push:
```powershell
# Ví dụ Docker Hub
docker tag <your-local-image>:latest <your-username>/<repo>:1.0.0
docker push <your-username>/<repo>:1.0.0
```

## Stretch goals (tuỳ chọn)
- Thêm healthcheck cho app
- Chạy app bằng non-root user
- Giảm size image bằng multi-stage và base nhỏ
- Thêm CI build + push theo tag

## Checklist
- Tôi build, chạy, debug, publish một Docker image thực tế
- Tôi giải thích được quyết định trong Dockerfile và Compose
- Tôi tái tạo môi trường trên máy khác được
