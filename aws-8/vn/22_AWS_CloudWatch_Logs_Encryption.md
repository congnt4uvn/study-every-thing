# Mã Hóa AWS CloudWatch Logs bằng KMS

## Tổng Quan
Mã hóa CloudWatch Logs cho phép bạn mã hóa các nhật ký của mình bằng các khóa AWS Key Management Service (KMS) để tăng cường bảo mật và tuân thủ.

## Các Khái Niệm Chính

### Mức Độ Mã Hóa
- **Phạm Vi Mã Hóa**: Mã hóa xảy ra ở **mức log group**, không phải ở mức log stream
- **Liên Kết Khóa KMS**: Bạn có thể liên kết một khóa chính (CMK) với một log group để mã hóa tất cả các nhật ký trong nhóm đó

### Các Phương Pháp Liên Kết Khóa KMS

#### 1. Liên Kết Khóa KMS với Log Group Hiện Tại
Sử dụng lệnh `associate-kms-key` để liên kết khóa KMS với log group hiện tại.

**Hạn Chế**: Bạn không thể thực hiện thao tác này thông qua bảng điều khiển CloudWatch. Bạn phải sử dụng:
- CloudWatch Logs API
- AWS CLI
- AWS SDK

#### 2. Tạo Log Group Mới với Khóa KMS
Sử dụng lệnh `create-log-group` để tạo log group mới chưa tồn tại và trực tiếp liên kết nó với khóa KMS tại thời điểm tạo.

## Các Lệnh CLI

### Liên Kết Khóa KMS với Log Group Hiện Tại
```bash
aws logs associate-kms-key \
  --log-group-name <tên-log-group> \
  --kms-key-id <id-khóa-kms> \
  --region <vùng>
```

### Tạo Log Group với Khóa KMS
```bash
aws logs create-log-group \
  --log-group-name <tên-log-group> \
  --kms-key-id <id-khóa-kms> \
  --region <vùng>
```

## Ví Dụ Thực Tế

### Khắc Phục Sự Cố: Ngoại Lệ Access Denied

Khi cố gắng liên kết khóa KMS với log group, bạn có thể gặp phải:
```
AccessDeniedException: Associate KMS key operation failed
```

**Các Nguyên Nhân Có Thể**:
1. Khóa KMS không tồn tại
2. Khóa KMS không được phép sử dụng với log group
3. Quyền IAM không đủ

**Giải Pháp**:
- Xác minh khóa KMS tồn tại trong tài khoản AWS của bạn
- Đảm bảo chính sách khóa cho phép dịch vụ CloudWatch Logs sử dụng khóa
- Kiểm tra quyền IAM cho người dùng/vai trò của bạn

## Các Ghi Chú Quan Trọng

1. **Hạn Chế Bảng Điều Khiển**: Giao diện bảng điều khiển AWS Management không cung cấp tùy chọn để liên kết khóa KMS với log group sau khi tạo
2. **Mức Log Group**: Tất cả các log stream trong một log group chia sẻ cùng một khóa mã hóa
3. **Kiểm Soát Truy Cập**: Cần có chính sách khóa KMS thích hợp và quyền IAM để thiết lập mã hóa thành công

## Các Thực Hành Tốt Nhất

- Sử dụng mã hóa KMS cho các log groups chứa thông tin nhạy cảm
- Đảm bảo chính sách khóa KMS được cấu hình đúng để cho phép dịch vụ CloudWatch Logs truy cập
- Kiểm tra liên kết khóa trong môi trường không phải sản xuất trước
- Theo dõi việc sử dụng khóa KMS cho mục đích tuân thủ và kiểm toán
