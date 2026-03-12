# Bài 04 — Thực hành image: pull, tag, inspect, push

## Mục tiêu
- Pull image, hiểu naming, chọn đúng tag
- Tag image cho repo của bạn
- Push lên registry (khái niệm + thao tác cơ bản)

## Cú pháp tên image
Một tham chiếu image thường có dạng:

- `nginx:1.27` (mặc định Docker Hub)
- `docker.io/library/nginx:1.27` (ghi rõ)
- `ghcr.io/myorg/myapp:1.0.0` (GitHub Container Registry)

Thành phần:
- **Registry host** (tuỳ chọn)
- **Namespace/repo**
- **Tag** (tuỳ chọn, mặc định `latest`)

## Pull và inspect
```powershell
docker pull nginx:1.27
docker image inspect nginx:1.27
```

## Tagging
Tag chỉ là “con trỏ” tới một image ID.

```powershell
# Ví dụ: gán thêm tag mới cho cùng image
docker tag nginx:1.27 my-nginx:1.27

docker images my-nginx
```

## Pushing (tổng quan)
Để push, bạn cần:
- Tài khoản registry
- Repo bạn có quyền ghi
- `docker login` để xác thực

Luồng ví dụ:
```powershell
# Đăng nhập (sẽ hỏi credentials)
docker login

# Tag image theo registry/repo bạn sở hữu (ví dụ Docker Hub)
docker tag my-nginx:1.27 <your-dockerhub-username>/my-nginx:1.27

# Push
docker push <your-dockerhub-username>/my-nginx:1.27
```

## Digest để tái lập
Nếu deploy `myapp:latest`, nó có thể thay đổi âm thầm. Hãy ưu tiên tag có version.

Để tái lập tối đa:
- Pin base image bằng digest trong Dockerfile (làm ở bài sau)
- Pin image triển khai bằng digest trong môi trường runtime

## Lab thực hành
1. Pull và so sánh size:
```powershell
docker pull alpine:3.19
docker pull ubuntu:24.04
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

2. Inspect entrypoint/cmd:
```powershell
docker image inspect ubuntu:24.04 | Select-String -Pattern 'Entrypoint|Cmd'
```

3. Cleanup tag không dùng (giữ lại ít nhất 1 tag):
```powershell
docker rmi my-nginx:1.27
```

## Checklist
- Tôi hiểu tag là gì và vì sao `latest` rủi ro
- Tôi tag image để push lên registry được
- Tôi biết quy trình push cơ bản
