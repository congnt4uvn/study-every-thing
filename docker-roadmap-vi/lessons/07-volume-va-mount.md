# Bài 07 — Dữ liệu: volume, bind mount, quyền truy cập

## Mục tiêu
- Hiểu dữ liệu container nằm ở đâu
- Chọn đúng giữa bind mount và volume
- Tránh các “bẫy” đường dẫn trên Windows/WSL

## Vì sao quản lý dữ liệu quan trọng
Container nên “dễ bỏ”. Nếu app lưu dữ liệu quan trọng *bên trong* filesystem của container và bạn xoá container, dữ liệu mất.

Thường bạn sẽ dùng một trong hai:
- **Bind mount**: map path trên host vào container (rất hợp cho dev)
- **Volume**: storage do Docker quản lý (hợp cho database và state bền)

## Bind mounts
Bind mount map thư mục/file trên host vào container.

Ví dụ:
```powershell
# Mount thư mục hiện tại vào /app
docker run --rm -it -v ${PWD}:/app alpine:3.19 sh
```

Use cases:
- Sửa code trong IDE và container chạy code đó
- Chia sẻ file config với container

## Volumes
Volume do Docker quản lý và nằm trong vùng storage của Docker.

Tạo và inspect:
```powershell
docker volume create mydata
docker volume ls
docker volume inspect mydata
```

Dùng trong container:
```powershell
docker run -d --name voltest -v mydata:/data alpine:3.19 sh -c "echo hi > /data/hello.txt; sleep 3600"
```

## Named volume vs anonymous volume
- Named volume: `mydata:/data` (dễ tái sử dụng)
- Anonymous volume: `-v /data` (khó theo dõi hơn; đôi lúc vẫn OK)

## Quyền truy cập (điểm hay đau đầu)
Container thường chạy user Linux (kể cả trên Windows thông qua WSL2).

Triệu chứng:
- “Permission denied” khi ghi vào thư mục mount

Hướng xử lý:
- Ưu tiên image chạy non-root *nhưng* hỗ trợ path có thể ghi
- Với dev bind mount, căn chỉnh UID/GID hoặc cấu hình app dùng thư mục ghi được
- Với production, tránh bind mount; dùng volume + ownership rõ ràng

## Ghi chú Windows + WSL2
Trên Windows, Docker Desktop + WSL2 nghĩa là:
- Linux container chạy trong môi trường Linux (WSL/VM)
- Hiệu năng file khác nhau tuỳ path bạn mount từ:
  - Path trong filesystem WSL (thường nhanh hơn), vs
  - Path trong filesystem Windows (có thể chậm hơn)

Nếu bạn dùng WSL2 nhiều, cân nhắc đặt project dev bên trong filesystem WSL.

## Lab thực hành
1. Kiểm tra bind mount:
```powershell
mkdir mount-demo
Set-Content -Path .\mount-demo\hello.txt -Value "hello"
docker run --rm -it -v ${PWD}\mount-demo:/data alpine:3.19 sh -c "ls -la /data; cat /data/hello.txt"
```

2. Kiểm tra volume có bền không:
```powershell
docker volume create persistdemo
docker run --rm -v persistdemo:/data alpine:3.19 sh -c "date > /data/created.txt"
docker run --rm -v persistdemo:/data alpine:3.19 sh -c "cat /data/created.txt"
```

3. Cleanup:
```powershell
docker volume rm persistdemo
```

## Checklist
- Tôi phân biệt được bind mount và volume
- Tôi tạo/inspect/xoá volume được
- Tôi biết cách tiếp cận lỗi permission thay vì đoán mò
