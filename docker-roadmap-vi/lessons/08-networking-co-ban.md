# Bài 08 — Networking: ports, DNS, bridge network

## Mục tiêu
- Hiểu publish port và networking giữa các container
- Tạo user-defined bridge network
- Dùng Docker DNS để service discovery

## Publish port
Container có network namespace riêng. Publish port giúp “mở” port của container ra host.

```powershell
# host:8080 -> container:80
docker run -d --name web -p 8080:80 nginx:latest
```

Ghi chú:
- `-p 8080:80` là chỉ định rõ
- `-p 80` (không ghi host port) sẽ publish ra một host port ngẫu nhiên

## Networking giữa container
Docker có network `bridge` mặc định. Các container trên cùng user-defined network có thể resolve nhau theo tên.

### Tạo network
```powershell
docker network create appnet
docker network ls
```

### Chạy 2 container trên network đó
```powershell
docker run -d --name api --network appnet nginx:latest

docker run --rm -it --name client --network appnet alpine:3.19 sh
# trong client:
# (cài curl)
apk add --no-cache curl
curl -I http://api
exit
```

Nếu `curl http://api` chạy, Docker DNS đã resolve `api` sang IP container.

### Inspect network
```powershell
docker network inspect appnet
```

## Vì sao user-defined network tốt hơn default bridge
- DNS tự động theo tên container
- Cô lập tốt hơn
- Dễ dự đoán cho ứng dụng nhiều service

## Lab thực hành
1. Publish port và xem mapping:
```powershell
docker run -d --name web2 -p 8081:80 nginx:latest
docker port web2
```

2. Service discovery theo tên (dùng lab `appnet` ở trên).

3. Cleanup:
```powershell
docker rm -f web web2 api
docker network rm appnet
```

## Checklist
- Tôi hiểu host port vs container port
- Tôi tạo network và kết nối container vào đó được
- Tôi hiểu service discovery theo tên trong Docker network

## Lỗi hay gặp
- **Dùng `localhost` giữa các container**: trong container, `localhost` là chính nó. Hãy dùng tên container/service.
- **Xung đột port**: chỉ một tiến trình có thể bind một host port.
