# Bài 03 — Vòng đời container + CLI thiết yếu

## Mục tiêu
- Thành thạo các lệnh dùng hằng ngày
- Hiểu trạng thái container (created, running, exited)
- Biết khi nào dùng `run` vs `start` vs `exec`

## Vòng đời và “lệnh nào làm gì”
### `docker run`
Tạo *và* chạy container mới.

```powershell
# Mỗi lần chạy sẽ tạo container mới
docker run --rm alpine:3.19 echo "hi"
```

- `--rm` sẽ xoá container sau khi exit (rất tiện cho tác vụ one-off).

### `docker start`
Chạy lại một container *đã tồn tại* (đang stop).

```powershell
docker create --name myalpine alpine:3.19
docker start myalpine
```

### `docker exec`
Chạy lệnh bên trong một container *đang chạy*.

```powershell
docker run -d --name web -p 8080:80 nginx:latest
docker exec -it web sh
```

## Các lệnh thiết yếu
### Liệt kê
```powershell
docker ps           # đang chạy
docker ps -a        # tất cả
```

### Logs
```powershell
docker logs web
docker logs -f web  # theo dõi liên tục
```

### Inspect
```powershell
docker inspect web
```

### Tài nguyên
```powershell
docker stats
```

### Cleanup
```powershell
# Dừng/xoá container cụ thể
docker stop web
docker rm web

# Xem dung lượng Docker đang chiếm
docker system df
```

> Tip: Tránh dùng `docker system prune -a` cho tới khi bạn hiểu rõ nó xoá gì.

## Lab thực hành: “phá nỗi sợ”
1. Chạy container sống lâu:
```powershell
docker run -d --name sleeper alpine:3.19 sh -c "while true; do date; sleep 2; done"
```

2. Xem logs:
```powershell
docker logs -f sleeper
```

3. Exec vào container (ở terminal khác):
```powershell
docker exec -it sleeper sh
ps
exit
```

4. Inspect:
```powershell
docker inspect sleeper | Select-String -Pattern '"IPAddress"|"Image"|"Mounts"'
```

5. Cleanup:
```powershell
docker rm -f sleeper
```

## Checklist
- Tôi xem logs và exec vào container đang chạy được
- Tôi biết dùng `inspect` để hiểu container cấu hình thế nào
- Tôi cleanup container an toàn

## Lỗi hay gặp
- **Dùng `exec` với container đã dừng**: phải start trước.
- **Nhầm `run` và `start`**: `run` sẽ tạo container mới mỗi lần (trừ khi bạn quản lý tên và vòng đời).
- **Quên publish port**: `EXPOSE` chỉ là “tài liệu”; không tự mở port host.
