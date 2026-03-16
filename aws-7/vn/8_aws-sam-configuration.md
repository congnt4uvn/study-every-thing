# AWS SAM - Quản Lý Nhiều Môi Trường với samconfig.toml

## Tổng Quan
AWS SAM (Serverless Application Model) cung cấp cách thức hiệu quả để quản lý nhiều môi trường triển khai (dev, prod, staging, v.v.) trong stack phát triển của bạn bằng cách sử dụng file cấu hình.

## File SAMconfig.toml

### Mục Đích
File `samconfig.toml` cho phép bạn định nghĩa các tham số đặc thù cho từng môi trường trong việc triển khai SAM, giúp loại bỏ nhu cầu phải chỉ định tham số thủ công mỗi lần triển khai.

### Định Dạng File
File cấu hình sử dụng định dạng TOML (Tom's Obvious, Minimal Language) và tổ chức các tham số theo môi trường và loại lệnh.

## Cấu Trúc Cấu Hình

### Ví Dụ Môi Trường Development (Phát Triển)
```toml
[dev.deploy.parameters]
stack_name = "my-app-dev"
s3_bucket = "my-deployment-bucket-dev"
s3_prefix = "dev"
region = "us-east-1"
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Environment=development"

[dev.sync.parameters]
# Các tham số sync cho môi trường dev
```

### Ví Dụ Môi Trường Production (Sản Xuất)
```toml
[prod.deploy.parameters]
stack_name = "my-app-prod"
s3_bucket = "my-deployment-bucket-prod"
s3_prefix = "prod"
region = "us-east-1"
capabilities = "CAPABILITY_IAM"
parameter_overrides = "Environment=production"

[prod.sync.parameters]
# Các tham số sync cho môi trường prod
```

## Lệnh Triển Khai

### Triển Khai lên Môi Trường Development
```bash
sam deploy --config-env dev
```

### Triển Khai lên Môi Trường Production
```bash
sam deploy --config-env prod
```

## Cách Hoạt Động

1. **Thiết Lập Ban Đầu**: Tạo file `samconfig.toml` trong thư mục gốc của dự án SAM
2. **Định Nghĩa Môi Trường**: Cấu hình tham số cho từng môi trường (dev, prod, staging, v.v.)
3. **Tự Động Chọn Tham Số**: SAM CLI đọc file TOML và áp dụng đúng tham số dựa trên cờ `--config-env`
4. **Đơn Giản Hóa Triển Khai**: Triển khai lên bất kỳ môi trường nào chỉ với một lệnh duy nhất

## Các Tham Số Quan Trọng

- **stack_name**: Tên CloudFormation stack cho môi trường
- **s3_bucket**: S3 bucket để lưu trữ các artifact triển khai
- **s3_prefix**: Tiền tố để tổ chức file trong S3
- **region**: AWS region để triển khai
- **capabilities**: Khả năng IAM yêu cầu (ví dụ: CAPABILITY_IAM)
- **parameter_overrides**: Các tham số tùy chỉnh truyền vào SAM template

## Lợi Ích

✅ **Cô Lập Môi Trường**: Cấu hình riêng biệt cho các môi trường khác nhau  
✅ **Giảm Lỗi**: Không cần nhập tham số thủ công giúp giảm sai sót khi triển khai  
✅ **Kiểm Soát Phiên Bản**: Cấu hình dưới dạng code - theo dõi thay đổi trong Git  
✅ **Khả Năng Mở Rộng**: Thêm không giới hạn môi trường khi cần  
✅ **Hợp Tác Nhóm**: Quy trình triển khai chuẩn hóa giữa các thành viên trong nhóm

## Mẹo Thi Chứng Chỉ

⚠️ **Quan Trọng cho Kỳ Thi Chứng Chỉ AWS**:
- Hiểu cách cấu hình nhiều môi trường sử dụng `samconfig.toml`
- Biết cấu trúc lệnh: `sam deploy --config-env <environment>`
- Nhận biết định dạng và cấu trúc file TOML
- Hiểu về parameter overrides và các thiết lập đặc thù cho môi trường

## Thực Hành Tốt Nhất

1. Lưu trữ `samconfig.toml` trong hệ thống quản lý phiên bản (version control)
2. Sử dụng tên môi trường có ý nghĩa (dev, staging, prod)
3. Không lưu dữ liệu nhạy cảm trong file cấu hình (sử dụng parameter overrides hoặc secrets manager)
4. Ghi chép các tham số bắt buộc cho các thành viên trong nhóm
5. Test thay đổi cấu hình trong môi trường dev trước khi áp dụng lên prod

## Thuật Ngữ Quan Trọng

- **SAM**: Serverless Application Model - Mô hình Ứng dụng Serverless
- **TOML**: Tom's Obvious, Minimal Language - Ngôn ngữ cấu hình tối giản
- **Deploy**: Triển khai
- **Stack**: Ngăn xếp tài nguyên CloudFormation
- **Environment**: Môi trường (dev, prod, staging)
- **Parameter Overrides**: Ghi đè tham số

---

**Các Dịch Vụ AWS Liên Quan**: CloudFormation, Lambda, API Gateway, S3  
**Liên Quan Chứng Chỉ**: AWS Certified Developer Associate, AWS Certified Solutions Architect
