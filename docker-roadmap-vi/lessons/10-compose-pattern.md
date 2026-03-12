# Bài 10 — Mẫu Compose: dev/prod, env, healthcheck

## Mục tiêu
- Dùng environment variables an toàn và dễ đoán
- Dùng healthcheck để phát hiện “sẵn sàng”
- Tổ chức Compose cho dev vs prod mà không rối

## Environment variables trong Compose
Có 3 kiểu phổ biến:

1) Khai báo inline:
```yaml
services:
  app:
    image: myapp:1.0
    environment:
      LOG_LEVEL: "debug"
      PORT: "8080"
```

2) Dùng `.env` (Compose tự đọc `.env` cùng thư mục):
```env
APP_PORT=8080
LOG_LEVEL=debug
```

```yaml
services:
  app:
    image: myapp:1.0
    ports:
      - "${APP_PORT}:8080"
    environment:
      LOG_LEVEL: "${LOG_LEVEL}"
```

3) `env_file:` dùng file riêng:
```yaml
services:
  app:
    env_file:
      - ./app.env
```

### Gợi ý
- Không “nướng” secrets vào image.
- `.env` phù hợp cho config local không nhạy cảm.
- Với production, dùng secret manager của nền tảng; với local dev, đừng commit secrets.

## Healthchecks
Healthcheck là lệnh Docker chạy để quyết định container có “healthy” không.

Ví dụ:
```yaml
services:
  web:
    image: nginx:latest
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/"]
      interval: 10s
      timeout: 3s
      retries: 5
```

Vì sao quan trọng:
- Nhìn ra vấn đề readiness nhanh
- Giúp đội debug “nó lên nhưng không dùng được”

> Lưu ý: Dù có healthcheck, ứng dụng vẫn nên tự retry/backoff khi gọi dependency.

## Dev vs prod (đơn giản mà hiệu quả)
Giữ tối giản:
- Một `compose.yaml` định nghĩa services
- Tuỳ chọn `compose.override.yaml` cho tweak riêng của developer

Ví dụ tweak dev-only:
- Bind mounts
- Live reload
- Expose thêm port

Ví dụ override:
```yaml
services:
  app:
    volumes:
      - ./:/app
    environment:
      LOG_LEVEL: "debug"
```

## Compose profiles (tuỳ chọn)
Profile giúp bật dịch vụ “phụ” khi cần.

```yaml
services:
  jaeger:
    image: jaegertracing/all-in-one
    profiles: ["observability"]
```

Chạy với:
```powershell
docker compose --profile observability up -d
```

## Lab thực hành: thêm healthcheck + tư duy readiness
1. Dùng service có thể trả HTTP (nginx là đủ).
2. Thêm healthcheck.
3. Start stack và xem trạng thái:
```powershell
docker compose up -d

docker compose ps
```

Tìm trạng thái `healthy`.

## Checklist
- Tôi dùng `.env` và variable substitution an toàn
- Tôi thêm healthcheck và đọc được trạng thái health
- Tôi có chiến lược tách dev/prod cho Compose

## Lỗi hay gặp
- **Nghĩ `depends_on` nghĩa là “ready”**: chủ yếu chỉ đảm bảo thứ tự start.
- **Commit secrets**: `.env` hay bị commit nhầm; nhớ thêm vào `.gitignore`.
