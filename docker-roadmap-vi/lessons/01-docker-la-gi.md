# Bài 01 — Docker là gì + cài đặt + container đầu tiên

## Mục tiêu
Sau bài này bạn có thể:
- Giải thích (dễ hiểu) Docker *làm gì* và *không làm gì*
- Cài Docker và kiểm tra chạy được
- Chạy container đầu tiên và hiểu những gì đang xảy ra

## Mô hình tư duy (mental model)
Docker là một bộ công cụ giúp bạn **đóng gói** phần mềm (kèm runtime/dependencies) thành một **image**, rồi **chạy** image đó thành **container** có mức độ cô lập.

- **Image**: “mẫu” *chỉ-đọc* (giống snapshot) chứa filesystem + metadata
- **Container**: một *phiên chạy* của image (có thêm một lớp ghi/đọc nhỏ)

Docker không phải là:
- Máy ảo (VM) (VM chạy cả hệ điều hành guest)
- Thứ thay thế quản lý dependency đúng cách
- “Tấm khiên” bảo mật tuyệt đối (container giảm rủi ro, nhưng không biến app kém an toàn thành an toàn)

## Cài đặt (Windows)
Trên Windows, cấu hình phổ biến nhất là **Docker Desktop** dùng backend **WSL 2**.

1. Cài Docker Desktop
   - Bật WSL 2 (Docker Desktop thường hướng dẫn)
   - Khởi động lại nếu được yêu cầu
2. Mở PowerShell mới và kiểm tra:

```powershell
docker version
docker info
```

Nếu `docker info` hiển thị thông tin server, Docker engine đang chạy.

### Lỗi cài đặt hay gặp
- **“WSL kernel not installed”**: cài/cập nhật kernel WSL 2
- **Virtualization bị tắt**: bật virtualization trong BIOS/UEFI
- **Docker Desktop không lên**: thử chuyển sang WSL 2 backend trong settings

## Container đầu tiên
### 1) Hello World
```powershell
docker run hello-world
```

Điều xảy ra:
- Docker kiểm tra máy bạn có image `hello-world` chưa
- Nếu chưa có, nó sẽ pull từ registry (Docker Hub)
- Nó tạo container, chạy, in output, rồi thoát

### 2) Chạy web server (nginx)
```powershell
# Chạy nginx nền (detached)
docker run -d --name web -p 8080:80 nginx:latest

# Xem container đang chạy
docker ps
```

Mở http://localhost:8080 trên trình duyệt.

### 3) Dừng và xoá
```powershell
# Dừng container
docker stop web

# Xoá container
docker rm web
```

## Lệnh quan trọng (tóm tắt)
- `docker version` — phiên bản client/server
- `docker info` — thông tin engine (storage driver, backend)
- `docker run` — tạo + chạy container
- `docker ps` — liệt kê container đang chạy (`-a` gồm cả container đã dừng)
- `docker stop` / `docker rm` — dừng/xoá container

## Lab thực hành
1. Chạy `hello-world` 2 lần.
   - Quan sát: lần đầu tải image; lần sau dùng cache.
2. Chạy `nginx` và đổi host port:
   - Thử `-p 9090:80` và vào http://localhost:9090
3. Luyện cleanup:
   - Dừng, xoá, kiểm tra `docker ps -a` trống

## Checklist
- Tôi phân biệt được image vs container
- Tôi chạy được container phục vụ HTTP và truy cập qua port mapping
- Tôi biết dừng và xoá container

## Mini-quiz (đáp án ở bài sau)
1. Khi chạy `docker run nginx`, thứ nào cần có trước: image hay container?
2. `-p 8080:80` nghĩa là gì?
3. Vì sao `docker ps` không hiện container đã exit?
