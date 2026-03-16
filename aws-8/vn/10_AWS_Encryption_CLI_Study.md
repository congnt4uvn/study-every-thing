# AWS Encryption CLI - Hướng Dẫn Học Tập

## Tổng Quan
Hướng dẫn này bao gồm cài đặt và sử dụng AWS Encryption CLI để mã hóa và giải mã dữ liệu bằng AWS Key Management Service (KMS).

## Cài Đặt

### Điều Kiện Tiên Quyết
- Python được cài đặt trên hệ thống của bạn
- Quyền truy cập vào các dịch vụ AWS

### Các Bước Cài Đặt

1. **Kiểm Tra Phiên Bản Python**
   - Xác minh cài đặt Python của bạn
   - Hướng dẫn cho Windows cũng có sẵn

2. **Cài Đặt AWS Encryption CLI**
   ```bash
   pip install aws-encryption-cli
   ```

3. **Xác Minh Cài Đặt**
   ```bash
   aws-encryption-cli --version
   ```
   - Ví dụ kết quả: Encryption CLI phiên bản 1.3.7

## Các Khái Niệm Chính

### Mã Hóa Data Key
- Phần này bao gồm cách mã hóa hoạt động trong thực tế
- **Lưu Ý**: Kiến thức về thực thi không bắt buộc cho kỳ thi, nhưng hữu ích cho ứng dụng thực tế

### Thiết Lập Master Key
- Xuất CMK (Customer Master Key) ARN
- Không thể chỉ sử dụng bí danh khóa
- Phải sử dụng ARN đầy đủ của khóa

## Quá Trình Mã Hóa

### Bước 1: Chuẩn Bị Tệp
Tạo một tệp văn bản để mã hóa:
```bash
vi hello.txt
```
- Ví dụ: Tạo một tệp với dữ liệu nhạy cảm
- Kích thước tệp có thể thay đổi (1MB+)

### Bước 2: Thiết Lập Khóa
```bash
key=<your-cmk-arn>
```

### Bước 3: Mã Hóa Tệp
```bash
aws-encryption-cli encrypt \
  --plaintext-input hello.txt \
  --master-key factory=aws-kms key=$key \
  --metadata-output metadata \
  --output output/
```

**Tương đương PowerShell cũng có sẵn nếu cần**

#### Các Xem Xét Quan Trọng:
- **Metadata Output**: Không thể nằm trong thư mục đầu ra
- Tạo một thư mục đầu ra riêng biệt nếu cần
- Encryption context là tùy chọn (có thể bỏ qua để đơn giản)

### Tệp Đầu Ra
Sau khi mã hóa, bạn sẽ có:
1. **metadata** - Tài liệu JSON chứa:
   - Thuật toán được sử dụng
   - Thông tin Data Key
   - Chi tiết nhà cung cấp khóa
   - Encryption context
   - Các thông số mã hóa khác

2. **output/hello.txt.encrypted** - Tệp được mã hóa
   - Hiển thị như gibberish khi xem
   - Chứa tham chiếu KMS khóa và data key được tạo
   - Cần thiết để giải mã trong tương lai

## Quá Trình Giải Mã

### Bước 1: Chạy Lệnh Giải Mã
```bash
aws-encryption-cli decrypt \
  --ciphertext-input output/hello.txt.encrypted \
  --metadata-output metadata \
  --output decrypted/
```

### Bước 2: Tạo Thư Mục Đầu Ra
```bash
mkdir decrypted
```

### Kết Quả
- Dữ liệu được mã hóa được giải mã
- Nội dung tệp gốc được khôi phục
- Siêu dữ liệu về quá trình giải mã được lưu

## Những Điểm Chính Cần Nhớ

1. **Mã Hóa Tệp**: Đảm bảo dữ liệu nhạy cảm được bảo vệ bằng AWS KMS
2. **Metadata**: Cung cấp thông tin về quá trình mã hóa
3. **Giải Mã**: Yêu cầu cùng quyền AWS IAM như mã hóa
4. **Master Keys**: Phải sử dụng ARN đầy đủ, không chỉ bí danh
5. **Quản Lý Đầu Ra**: Lên kế hoạch cấu trúc thư mục một cách cẩn thận

## Mẹo Thực Tế

- Luôn đảm bảo bạn có quyền AWS IAM thích hợp
- Theo dõi ARN CMK của bạn để tham khảo
- Sử dụng tệp metadata cho kiểm toán và tài liệu
- Encryption SDK tự động xử lý quản lý khóa
- Kiểm tra các quy trình mã hóa/giải mã trước khi sử dụng trên máy chủ

## Ghi Chú Chuẩn Bị Kỳ Thi

- Tập trung vào việc hiểu các khái niệm, không phải ghi nhớ các lệnh chính xác
- Biết khi nào sử dụng AWS Encryption CLI
- Hiểu các nguyên tắc quản lý khóa KMS
- Quen thuộc với các khái niệm về encryption context và metadata
