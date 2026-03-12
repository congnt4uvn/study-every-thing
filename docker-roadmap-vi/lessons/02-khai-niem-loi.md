# Bài 02 — Khái niệm lõi: image, container, layer, registry

## Mục tiêu
- Hiểu image/layer và vì sao build có thể cache
- Hiểu filesystem của container (read-only layers + writable layer)
- Hiểu registry, repository, tag, digest

## Khái niệm
### Image và layer
Docker image thường được build từ **Dockerfile**. Mỗi instruction (như `RUN`, `COPY`) tạo một **layer** mới.

Vì sao layer quan trọng:
- Layer được định danh theo nội dung (content-addressed) và có thể tái sử dụng
- Tái sử dụng layer giúp build/pull nhanh hơn
- Một thay đổi nhỏ có thể làm “invalid” layer và các layer phía sau

### Filesystem của container
Khi chạy image, Docker thêm một lớp writable mỏng ở trên:
- Image layers (chỉ đọc)
- Container layer (ghi/đọc)

Xoá container => lớp writable đó cũng mất.

### Registry, repo, tag, digest
- **Registry**: server lưu image (Docker Hub, GHCR, ECR...)
- **Repository**: “không gian tên” cho các image liên quan (vd `library/nginx`)
- **Tag**: nhãn có thể thay đổi (vd `nginx:1.27`, `nginx:latest`)
- **Digest**: hash nội dung *bất biến* (vd `nginx@sha256:...`)

Gợi ý:
- Dùng **tag** cho con người
- Dùng **digest** cho triển khai cần tái lập (reproducible)

## Khám phá image trên máy
```powershell
# Liệt kê image
docker images

# Xem metadata (env, entrypoint, ports...)
docker image inspect nginx:latest

# Xem lịch sử layer
docker history nginx:latest
```

## Lab thực hành
1. Pull 2 tag và so sánh:
```powershell
docker pull alpine:3.19
docker pull alpine:latest
docker images alpine
```

2. Xem tag trỏ tới nội dung khác nhau:
```powershell
docker image inspect alpine:3.19 | Select-String -Pattern 'Id|RepoTags|RepoDigests'
```

3. Chạy container và ghi file:
```powershell
docker run --name tmp -it alpine:3.19 sh
# trong container:
echo "hello" > /hello.txt
cat /hello.txt
exit
```

Start lại và kiểm tra file còn (cùng container):
```powershell
docker start -ai tmp
cat /hello.txt
exit
```

Xoá container và xác nhận dữ liệu biến mất:
```powershell
docker rm -f tmp
```

## Checklist
- Tôi giải thích được layer và caching
- Tôi biết tag có thể thay đổi, digest là bất biến
- Tôi hiểu vì sao dữ liệu ghi trong container mất khi xoá container

## Đáp án mini-quiz Bài 01
1. Cần có image (hoặc được pull) trước khi tạo container.
2. Map host port 8080 → container port 80.
3. `docker ps` mặc định chỉ hiện container đang chạy; dùng `docker ps -a` để xem tất cả.
