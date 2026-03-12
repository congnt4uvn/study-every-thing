# AWS S3: Mã Hóa Mặc Định vs Chính Sách Bucket

## Tổng Quan

Tài liệu này giải thích mối quan hệ giữa mã hóa mặc định của S3 và chính sách bucket, cũng như cách chúng có thể được sử dụng để áp dụng các yêu cầu mã hóa cho các bucket S3 của bạn.

## Mã Hóa Mặc Định

### Hành Vi Mặc Định Hiện Tại

Theo mặc định, tất cả các bucket S3 hiện nay đều có **mã hóa mặc định được kích hoạt với SSE-S3** (Mã hóa phía máy chủ với khóa do Amazon S3 quản lý). Mã hóa này:
- Được áp dụng tự động cho các đối tượng mới
- Được bật mặc định cho tất cả các bucket mới

### Tùy Chỉnh Mã Hóa Mặc Định

Bạn có thể thay đổi cài đặt mã hóa mặc định để sử dụng các phương thức mã hóa khác nhau, chẳng hạn như:
- **SSE-KMS** (Mã hóa phía máy chủ với AWS Key Management Service)
- Các loại mã hóa được hỗ trợ khác

## Chính Sách Bucket Để Áp Dụng Mã Hóa

### Sử Dụng Chính Sách Bucket Để Bắt Buộc Mã Hóa

Chính sách bucket cung cấp một cách để **áp dụng mã hóa** bằng cách từ chối các lệnh gọi API không bao gồm các header mã hóa chính xác. Điều này cho phép bạn bắt buộc các phương thức mã hóa cụ thể cho các đối tượng được tải lên bucket của bạn.

### Ví Dụ Chính Sách Bucket

#### 1. Bắt Buộc Mã Hóa SSE-KMS

Chính sách này từ chối các yêu cầu PUT object không bao gồm header mã hóa AWS KMS:

```json
{
  "Effect": "Deny",
  "Action": "s3:PutObject",
  "Condition": {
    "StringNotEquals": {
      "s3:x-amz-server-side-encryption": "aws:kms"
    }
  }
}
```

#### 2. Bắt Buộc Mã Hóa SSE-C

Chính sách này từ chối các tải lên không bao gồm header thuật toán mã hóa phía khách hàng (SSE-C):

```json
{
  "Effect": "Deny",
  "Action": "s3:PutObject",
  "Condition": {
    "Null": {
      "s3:x-amz-server-side-encryption-customer-algorithm": "true"
    }
  }
}
```

## Thứ Tự Đánh Giá

**Quan trọng:** Chính sách bucket **luôn được đánh giá trước cài đặt mã hóa mặc định**. Điều này có nghĩa là:

1. Nếu chính sách bucket từ chối yêu cầu do thiếu header mã hóa, yêu cầu sẽ bị từ chối
2. Mã hóa mặc định chỉ được áp dụng nếu chính sách bucket cho phép yêu cầu tiếp tục
3. Chính sách bucket có quyền ưu tiên trong việc xác định các yêu cầu mã hóa

## Điểm Chính Cần Ghi Nhớ

- ✅ Mã hóa mặc định được bật theo mặc định với SSE-S3
- ✅ Bạn có thể tùy chỉnh cài đặt mã hóa mặc định (ví dụ: sang SSE-KMS)
- ✅ Chính sách bucket có thể được sử dụng để áp dụng các phương thức mã hóa cụ thể
- ✅ Chính sách bucket được đánh giá **trước** cài đặt mã hóa mặc định
- ✅ Sử dụng chính sách bucket để bắt buộc header mã hóa cho các đối tượng được tải lên

## Thực Hành Tốt Nhất

1. **Kích hoạt mã hóa mặc định** như một biện pháp bảo mật cơ bản
2. **Sử dụng chính sách bucket** khi bạn cần áp dụng các phương thức mã hóa cụ thể
3. **Ghi chép các yêu cầu mã hóa của bạn** cho nhóm và ứng dụng của bạn
4. **Kiểm tra chính sách bucket của bạn** để đảm bảo chúng hoạt động như mong đợi mà không chặn các tải lên hợp lệ