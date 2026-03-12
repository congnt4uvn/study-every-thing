# Bài 11 — Debug & troubleshooting

## Mục tiêu
- Debug container có hệ thống (không đoán mò)
- Dùng `logs`, `exec`, `inspect`, `stats`
- Nhận diện các lỗi Docker phổ biến

## Vòng lặp debug
Khi không chạy đúng, trả lời lần lượt:
1. Container có đang chạy không?
2. Nếu exit, *vì sao*?
3. Nếu đang chạy, app có listen đúng port/interface không?
4. Port có publish đúng chưa?
5. Networking giữa services đúng chưa?
6. Mount/permission đúng chưa?

## Các lệnh cốt lõi
### Có đang chạy không?
```powershell
docker ps
docker ps -a
```

### Log nói gì?
```powershell
docker logs <container>
docker logs -f <container>
```

### Cấu hình thực tế là gì?
```powershell
docker inspect <container>
```

Gợi ý xem:
- `Config.Env`
- `Config.Cmd`, `Config.Entrypoint`
- `NetworkSettings.Ports`
- `Mounts`

### Bên trong container đang thế nào?
```powershell
docker exec -it <container> sh
```

Trong container, kiểm tra:
- Process: `ps`
- Port đang listen: `ss -lntp` (có thể cần cài `iproute2`)
- DNS: `cat /etc/resolv.conf`, `nslookup <service>`

### Tài nguyên
```powershell
docker stats
```

Nếu memory “kịch trần”, kernel có thể kill process (OOM kill).

## Lỗi phổ biến và cách xử lý
### “Trong container chạy được, nhưng browser không vào được”
Nguyên nhân hay gặp:
- App chỉ listen `127.0.0.1` bên trong container
- Thiếu/sai port mapping

Cách sửa:
- Cho app listen `0.0.0.0` trong container
- Publish port bằng `-p host:container` hoặc Compose `ports:`

### “Connection refused” giữa services
Nguyên nhân hay gặp:
- Dùng `localhost` để gọi container khác
- Services không cùng network
- Sai port

Cách sửa:
- Dùng tên service (vd `http://db:5432`)

### Permission denied với mount
Nguyên nhân hay gặp:
- User trong container không có quyền ghi vào thư mục mount

Cách sửa:
- Dùng path ghi được
- Chỉnh ownership/permission
- Dùng volume cho service cần state

## Lab thực hành: debug container “hỏng” (cố ý)
1. Chạy nginx nhưng map sai port:
```powershell
docker run -d --name broken -p 8080:81 nginx:latest
```

2. Vào http://localhost:8080 (sẽ fail).

3. Chẩn đoán:
```powershell
docker ps
docker port broken
docker logs broken
docker inspect broken | Select-String -Pattern 'Ports'
```

4. Sửa bằng cách tạo lại với mapping đúng:
```powershell
docker rm -f broken
docker run -d --name fixed -p 8080:80 nginx:latest
```

Cleanup:
```powershell
docker rm -f fixed
```

## Checklist
- Tôi debug port mapping nhanh
- Tôi biết khi nào dùng `inspect` vs `exec`
- Tôi giải thích được vì sao `localhost` hay sai trong hệ nhiều container
