# AWS Lambda Versions - Tài Liệu Học Tập

## Tổng Quan
AWS Lambda versions (phiên bản) cho phép bạn cố định một lượng code, tài nguyên và cài đặt cụ thể tại một thời điểm. Điều này giúp bạn tạo và quản lý các phiên bản khác nhau của Lambda function khi nó phát triển.

## Các Khái Niệm Chính

### Lambda Versions là gì?
- Versions là các bản snapshot (ảnh chụp) của code và cấu hình Lambda function
- Mỗi version là immutable (không thể thay đổi sau khi được publish)
- Cho phép function phát triển theo thời gian trong khi vẫn duy trì tham chiếu ổn định đến các phiên bản trước

### Xác Định Version
- **$LATEST**: Phiên bản chưa được publish, có thể chỉnh sửa
- **Numbered versions** (Phiên bản đánh số): Các phiên bản đã publish (1, 2, 3, v.v.)

## Hướng Dẫn Từng Bước: Tạo Lambda Versions

### Bước 1: Tạo Lambda Function
1. Tạo function mới với tên: `lambda-version-demo`
2. Runtime: Python 3.8
3. Tạo function

### Bước 2: Viết Code cho Version 1
```python
def lambda_handler(event, context):
    return "this is version one."
```

### Bước 3: Deploy và Test
1. Deploy các thay đổi của bạn
2. Tạo một sample test event
3. Test function
4. Xác nhận kết quả: "this is version one."

### Bước 4: Publish Version 1
1. Click **Action** → **Publish new version**
2. Thêm mô tả (tùy chọn)
3. Click **Publish**
4. Version 1 đã được tạo và không thể thay đổi

### Bước 5: Hiểu Hành Vi của Version
- Khi xem một published version (ví dụ: Version 1):
  - Designer/code editor ở chế độ chỉ đọc (read-only)
  - Bạn không thể sửa đổi code
  - Bạn vẫn có thể test function
  - Số version xuất hiện trong function overview

### Bước 6: Tiếp Tục Phát Triển
1. Quay lại main function ($LATEST)
2. Chỉnh sửa code cho version tiếp theo:
```python
def lambda_handler(event, context):
    return "this is version two."
```
3. Deploy và test các thay đổi
4. Function hiện giờ hiển thị: "this is version two."

## Lưu Ý Quan Trọng

- ✅ Published versions không thể thay đổi (immutable)
- ✅ Chỉ có $LATEST version mới có thể chỉnh sửa
- ✅ Mỗi published version duy trì snapshot code riêng của nó
- ✅ Bạn có thể test bất kỳ version nào bất cứ lúc nào
- ✅ Versions cho phép các chiến lược deployment và rollback an toàn

## Các Trường Hợp Sử Dụng

1. **Deployments An Toàn**: Test code mới mà không ảnh hưởng đến production
2. **Khả Năng Rollback**: Quay lại phiên bản ổn định trước đó một cách nhanh chóng
3. **A/B Testing**: Chạy nhiều versions khác nhau đồng thời
4. **Cập Nhật Dần Dần**: Sử dụng aliases để chuyển traffic giữa các versions

## Best Practices (Thực Hành Tốt Nhất)

- Luôn test kỹ lưỡng trước khi publish một version
- Thêm mô tả có ý nghĩa khi publish versions
- Sử dụng aliases để quản lý định tuyến version trong production
- Theo dõi các versions đang được sử dụng
- Dọn dẹp các old versions không sử dụng định kỳ

## Thuật Ngữ Quan Trọng

| Tiếng Anh | Tiếng Việt |
|-----------|------------|
| Version | Phiên bản |
| Immutable | Không thể thay đổi |
| Publish | Xuất bản/Phát hành |
| Deploy | Triển khai |
| Snapshot | Ảnh chụp/Bản sao lưu |
| Rollback | Quay lại/Hoàn tác |
| Alias | Bí danh |

---

**Bài Tập Thực Hành**: Tạo Lambda function của riêng bạn, publish nhiều versions, và test việc chuyển đổi giữa chúng để hiểu rõ workflow về tính immutability và versioning.
