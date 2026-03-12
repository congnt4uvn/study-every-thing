# Bài 09 — Docker Compose căn bản

## Mục tiêu
- Hiểu Compose là gì (và không phải gì)
- Chạy app nhiều container bằng `compose.yaml`
- Dùng `up`, `down`, `logs`, `exec` hiệu quả

## Compose làm gì
Docker Compose cho phép bạn khai báo tập service (container), network, volume trong YAML và chạy chúng cùng nhau.

Rất hợp cho:
- Stack dev local (app + database + cache)
- Môi trường demo
- Triển khai nhỏ trên một host

Không phải là:
- Orchestrator đa node (Kubernetes/Swarm/Nomad...)

## Ví dụ tối giản: nginx
Tạo `compose.yaml`:

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
```

Chạy:
```powershell
docker compose up -d

docker compose ps
docker compose logs
```

Dừng:
```powershell
docker compose down
```

## Các lệnh Compose hữu ích
- `docker compose up` — tạo/chạy services
- `docker compose down` — dừng/xoá services (thêm `-v` để xoá volume)
- `docker compose logs -f` — theo dõi logs
- `docker compose exec <service> <cmd>` — chạy lệnh trong service đang chạy
- `docker compose config` — xem cấu hình hợp nhất/đã validate

## Lab thực hành: app + redis (không cần code)
Tạo `compose.yaml`:

```yaml
services:
  redis:
    image: redis:7
    ports:
      - "6379:6379"

  client:
    image: alpine:3.19
    depends_on:
      - redis
    command: ["sh", "-c", "apk add --no-cache redis; redis-cli -h redis ping"]
```

Chạy:
```powershell
docker compose up --build
```

Kết quả mong đợi có `PONG`.

Cleanup:
```powershell
docker compose down
```

## Checklist
- Tôi giải thích Compose ở mức tổng quan
- Tôi chạy stack nhiều service được
- Tôi xem logs và exec vào service được

## Lỗi hay gặp
- **Thụt lề YAML**: sai 1 dấu cách là hỏng.
- **`depends_on` không đảm bảo “ready”**: chỉ đảm bảo thứ tự start, không đảm bảo service đã sẵn sàng. (Bạn sẽ xử lý “ready” bằng healthcheck ở bài sau.)
