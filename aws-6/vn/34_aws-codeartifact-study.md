# Tài Liệu Học Tập AWS CodeArtifact

## Tổng Quan
AWS CodeArtifact là dịch vụ kho lưu trữ artifact được quản lý hoàn toàn, giúp các tổ chức dễ dàng lưu trữ, phát hành và chia sẻ các gói phần mềm được sử dụng trong quy trình phát triển phần mềm một cách bảo mật.

## Các Khái Niệm Chính

### 1. Repository (Kho lưu trữ)
- Repository chứa các gói (packages) và có thể kết nối với các repository bên ngoài
- Ví dụ: Demo Repository được kết nối với PyPI store

### 2. Upstream Repository (Kho nguồn trên)
- Các repository có thể có upstream repositories để kéo packages từ đó
- Cho phép lấy packages từ các nguồn bên ngoài như public PyPI
- Có thể cấu hình nhiều upstream repositories nếu cần

### 3. Domain (Miền)
- Đại diện cho ranh giới tổ chức để lưu trữ dữ liệu artifact
- Tất cả repositories và packages được lưu trữ trong một domain
- Quy ước đặt tên: thường là tên công ty (ví dụ: `my-company`)
- **Bảo mật**: Yêu cầu khóa KMS để mã hóa
  - Có thể sử dụng khóa do AWS quản lý
  - Hoặc khóa KMS tùy chỉnh để kiểm soát nâng cao

### 4. External Connection (Kết nối bên ngoài)
- Cho phép upstream repositories kết nối với các kho packages công khai
- Ví dụ: PyPI store với kết nối bên ngoài đến public python.org PyPI

## Hướng Dẫn Thực Hành Chi Tiết

### Bước 1: Tạo Repository
1. Truy cập AWS CodeArtifact console
2. Click "Create repository"
3. Đặt tên: `Demo Repository`
4. Tùy chọn chọn upstream (ví dụ: Python store)

### Bước 2: Định Nghĩa Domain
1. Chọn AWS account của bạn
2. Tạo domain mới nếu chưa có
3. Đặt tên domain (ví dụ: `my-company`)
4. Chọn khóa KMS để mã hóa (AWS managed hoặc custom)

### Bước 3: Xem Lại Cấu Hình
- Repository chính: `demo-repository`
- Upstream repository: `pypi-store`
- External connection: Public PyPI store

## Kết Nối pip với CodeArtifact

### Phương Pháp 1: Thiết Lập CLI Tự Động (Có thể gặp vấn đề)
```bash
# Có thể không hoạt động trong CloudShell do vấn đề tương thích pip vs pip3
aws codeartifact login --tool pip --domain my-company --repository demo-repository
```

### Phương Pháp 2: Thiết Lập Thủ Công (Khuyến nghị)

#### Bước 1: Lấy Authorization Token
```bash
export CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token \
    --domain my-company \
    --domain-owner <account-id> \
    --region <region> \
    --query authorizationToken \
    --output text)
```

**Lưu Ý Quan Trọng:**
- Token có hiệu lực trong **12 giờ**
- Sau khi hết hạn, bạn phải tạo lại token
- Xác minh token: `echo $CODEARTIFACT_AUTH_TOKEN`

#### Bước 2: Cấu Hình pip
```bash
pip3 config set global.index-url https://aws:$CODEARTIFACT_AUTH_TOKEN@<domain>-<account-id>.d.codeartifact.<region>.amazonaws.com/pypi/<repository>/simple/
```

**Lưu ý:** Sử dụng `pip3` thay vì `pip` nếu gặp lỗi "pip not found" trong CloudShell.

#### Bước 3: Cài Đặt Packages
```bash
pip3 install response
```

Lệnh này sẽ:
- Kết nối với CodeArtifact repository
- Kéo package được chỉ định (`response`)
- Tự động tải xuống tất cả dependencies
- Lưu cache các packages trong CodeArtifact để sử dụng sau

## Các Vấn Đề Thường Gặp & Giải Pháp

### Vấn đề: "pip: command not found" trong CloudShell
**Giải pháp:** Sử dụng `pip3` thay vì `pip`
- CloudShell có `pip3` được cài đặt mặc định
- CodeArtifact CLI có thể không phát hiện điều này một cách chính xác

### Vấn đề: Token hết hạn
**Triệu chứng:** Không thể kết nối hoặc cài đặt packages
**Giải pháp:** Tạo lại authorization token (hiệu lực 12 giờ)

## Lợi Ích của AWS CodeArtifact

1. **Quản Lý Package Tập Trung**: Nguồn duy nhất cho tất cả dependencies
2. **Bảo Mật**: Lưu trữ được mã hóa với KMS, kiểm soát truy cập dựa trên IAM
3. **Caching**: Giảm các lần gọi mạng bên ngoài, cải thiện tốc độ build
4. **Kiểm Soát Phiên Bản**: Theo dõi và quản lý các phiên bản package
5. **Tích Hợp**: Hoạt động với npm, pip, Maven, NuGet và nhiều hơn nữa

## Thực Hành Tốt Nhất

- Thường xuyên xoay vòng (rotate) authorization tokens
- Sử dụng khóa KMS tùy chỉnh cho các môi trường nhạy cảm
- Cấu hình upstream repositories để cache các packages thường dùng
- Triển khai IAM policies để kiểm soát truy cập chi tiết
- Giám sát việc sử dụng repository thông qua CloudWatch

## Mẹo Thi

- Ghi nhớ hiệu lực token: **12 giờ**
- Domain là bắt buộc để tạo repository
- Mã hóa KMS là bắt buộc cho domains
- CodeArtifact hỗ trợ nhiều định dạng package (PyPI, npm, Maven, NuGet)
- Upstream repositories cho phép cache packages từ nguồn bên ngoài
