# Bài 12 — Bảo mật cơ bản: least privilege, secrets, scanning

## Mục tiêu
- Giảm bề mặt tấn công container bằng vài thói quen đơn giản
- Hiểu “đừng chạy root” và khi nào quan trọng
- Hiểu cách xử lý secrets và một số nền tảng supply-chain

## Nền tảng: Docker security là gì và không là gì
Docker giúp bạn:
- Cô lập tiến trình
- Hạn chế filesystem và network exposure
- Làm triển khai dễ tái lập

Docker không tự động:
- Sửa lỗ hổng trong dependency
- Ngăn rò rỉ credential
- Biến app không an toàn thành an toàn

## Thực hành bảo mật “đáng tiền”
### 1) Chọn base image hợp lý
- Ưu tiên image nhỏ và được bảo trì (vd `*-slim`, Alpine khi phù hợp)
- Ưu tiên version cụ thể thay vì `latest`
- Cập nhật base image định kỳ

### 2) Không chạy root (khi có thể)
Trong Dockerfile:
```dockerfile
# Ví dụ (mang tính minh hoạ)
RUN addgroup --system app && adduser --system --ingroup app app
USER app
```

Nếu app cần bind port thấp (<1024) hoặc ghi vào thư mục cụ thể, hãy cấu hình các path đó rõ ràng.

### 3) Không để secrets vào image
Tuyệt đối tránh:
- `COPY .env ...` vào image
- Hard-code API key trong Dockerfile

Nên làm:
- Cung cấp secrets lúc runtime (env vars, secret manager)
- Local dev: để secrets trong file bị ignore bởi git

### 4) Giảm quyền container ở runtime
Nâng cao nhưng rất hữu ích:
- Drop Linux capabilities
- Dùng read-only filesystem khi có thể
- Không mount Docker socket vào container app trừ khi bạn thật sự muốn “container điều khiển Docker”

Ví dụ flags (mang tính minh hoạ):
```bash
--read-only
--cap-drop=ALL
```

### 5) Scan image (khái niệm)
Scanning phát hiện CVE đã biết trong OS packages và đôi khi cả deps ngôn ngữ.

Tuỳ môi trường bạn có thể dùng:
- Docker Scout (Docker Desktop)
- Trivy (open-source phổ biến)
- Registry scanning (GHCR, ECR...)

## Nền tảng supply-chain
Rủi ro gồm:
- Base image bị compromise
- Typosquatting (pull `nignx` thay vì `nginx`)
- Dependency bị “tiêm” trong bước build

Giảm thiểu:
- Pin version
- Dùng registry đáng tin
- Review Dockerfile build steps
- Tính tới SBOM sau

## Lab thực hành (an toàn, cơ bản)
1. Inspect image chạy user nào:
```powershell
docker image inspect nginx:latest | Select-String -Pattern 'User'
```

2. Chạy container với read-only rootfs (có thể không chạy với mọi image):
```powershell
docker run --rm --read-only nginx:latest
```

Nếu fail, đó là bài học tốt: nhiều app cần thư mục tạm ghi được; bạn sẽ cấp phát path ghi được rõ ràng.

## Checklist
- Tôi tránh `latest` và chọn base được bảo trì
- Tôi hiểu vì sao secrets không được “nướng” vào image
- Tôi mô tả được vài lựa chọn hardening runtime
