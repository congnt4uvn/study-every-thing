# Bài 06 — Build tốt hơn: cache, .dockerignore, multi-stage

## Mục tiêu
- Build nhanh hơn, image nhỏ hơn
- Hiểu cache invalidation (vì sao thay đổi nhỏ có thể làm rebuild nhiều)
- Dùng `.dockerignore` để tránh “rác” và bí mật lọt vào image
- Dùng multi-stage build cho image production

## Nền tảng caching
Docker cache các bước build (layer). Một bước có thể tái sử dụng khi:
- Nội dung instruction giống hệt, và
- Input của instruction không đổi (với `COPY`, nội dung file là yếu tố quyết định)

**Quy tắc:** đặt các bước hay thay đổi *về sau* trong Dockerfile.

### Ví dụ: Node app (thứ tự thân thiện với cache)
Không tốt (thay đổi source là rebuild dependency):
```dockerfile
COPY . .
RUN npm ci
```

Tốt hơn:
```dockerfile
COPY package*.json ./
RUN npm ci
COPY . .
```

## `.dockerignore`
Tạo `.dockerignore` để không đưa file không cần thiết vào build context.

Các mục thường dùng:
```gitignore
.git
node_modules
bin
obj
*.log
.env
.env.*
Dockerfile
compose*.yaml
```

Lợi ích:
- Tốc độ: context nhỏ hơn
- Bảo mật: tránh lộ secrets
- Đúng đắn: tránh artefact “máy tôi chạy được”

## Multi-stage build
Multi-stage giúp bạn:
- Build bằng tool nặng (SDK, compiler)
- Chỉ “ship” output runtime (image nhỏ)

Ví dụ (mang tính minh hoạ):
```dockerfile
# Build stage
FROM node:20 AS build
WORKDIR /src
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:1.27
COPY --from=build /src/dist /usr/share/nginx/html
```

## Build arguments và environment variables
- `ARG` chỉ tồn tại lúc build
- `ENV` tồn tại lúc runtime (bên trong container chạy)

Dùng phổ biến:
- `ARG` chọn chế độ build
- `ENV` cấu hình ứng dụng

## Lab thực hành
1. Tạo một folder có:
   - `Dockerfile`
   - `.dockerignore`
   - vài file dummy (`notes.txt`, `.env`, thư mục `node_modules/`)

2. Build 2 lần và so sánh tốc độ:
```powershell
docker build -t demo-cache:1.0 .
docker build -t demo-cache:1.0 .
```

3. Thay đổi file được copy *muộn* trong Dockerfile rồi build lại.
   - Quan sát: layer trước đó vẫn được cache.

4. Xác nhận `.dockerignore` hoạt động:
   - Thêm file lớn và ignore; build context không nên phình.

## Checklist
- Tôi giải thích được vì sao thứ tự Dockerfile ảnh hưởng tốc độ build
- Tôi hiểu `.dockerignore` và dùng như mặc định
- Tôi mô tả được multi-stage build và vì sao giúp image nhỏ

## Lỗi hay gặp
- **Copy cả repo quá sớm**: phá cache.
- **Quên `.dockerignore`**: dễ lộ secrets và build chậm.
- **Ship cả tool build**: image to + tăng bề mặt tấn công.
