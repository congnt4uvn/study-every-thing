# AWS S3 Versioning - Hướng dẫn Thực hành

## Giới thiệu

Trong hướng dẫn này, chúng ta sẽ khám phá tính năng versioning (quản lý phiên bản) của S3 và học cách quản lý các phiên bản khác nhau của objects trong S3 bucket.

## Kích hoạt S3 Versioning

Để bật versioning cho S3 bucket của bạn:

1. Truy cập tab **Properties** của bucket
2. Tìm mục cài đặt **Bucket Versioning**
3. Nhấp **Edit** và chọn **Enable**
4. Lưu các thay đổi

Sau khi được kích hoạt, bất kỳ file nào bạn ghi đè sẽ tạo một phiên bản mới thay vì thay thế hoàn toàn file hiện có.

## Upload và Cập nhật Files

Hãy minh họa versioning với một ví dụ thực tế:

### Upload Lần Đầu

1. Mở website tĩnh của bạn được host trên S3
2. Giả sử file `index.html` hiện tại hiển thị "I love coffee"

### Cập nhật Nội dung

1. Chỉnh sửa file `index.html` local của bạn thành "I really love coffee"
2. Lưu file
3. Upload file đã cập nhật lên S3 bucket
4. Việc upload sẽ tạo một phiên bản mới của file

Khi bạn refresh website, bạn sẽ thấy nội dung đã được cập nhật: "I REALLY love coffee."

## Hiểu về Version IDs

Để xem các version IDs:

1. Truy cập tab **Objects** của bucket
2. Bật toggle **Show versions**

Bạn sẽ nhận thấy:

- **Các file được upload trước khi versioning được bật** có version ID là `null` (ví dụ: `beach.jpg`, `coffee.jpg`)
- **Các file được upload sau khi bật versioning** có các version IDs duy nhất
- File `index.html` giờ hiển thị hai phiên bản:
  - Một với version ID `null` (upload trước khi có versioning)
  - Một với version ID duy nhất (lần upload gần đây)

## Rollback về Phiên bản Trước

Để quay lại phiên bản cũ hơn:

1. Đảm bảo **Show versions** được bật
2. Nhấp vào version ID mới hơn mà bạn muốn xóa
3. Chọn **Delete**
4. Thao tác này thực hiện **permanent delete** (xóa vĩnh viễn) phiên bản cụ thể đó
5. Gõ "permanently delete" để xác nhận
6. Nhấp **Delete objects**

Sau khi xóa phiên bản mới hơn, việc refresh website sẽ hiển thị nội dung trước đó: "I love coffee."

## Delete Markers (Dấu hiệu Xóa)

Khi bạn xóa một file mà không bật show versions:

1. Tắt **Show versions**
2. Chọn một file (ví dụ: `coffee.jpg`)
3. Nhấp **Delete**
4. Gõ "delete" để xác nhận

Điều này không xóa vĩnh viễn object. Thay vào đó, S3 tạo một **delete marker**.

### Hiểu về Delete Markers

- File xuất hiện như đã bị xóa trong chế độ xem thông thường
- Với **Show versions** được bật, bạn có thể thấy delete marker
- Các phiên bản file thực tế vẫn còn trong bucket
- Delete marker đóng vai trò là phiên bản hiện tại, che giấu các phiên bản trước đó

### Tác động của Delete Markers

Nếu bạn refresh webpage, các hình ảnh có delete markers sẽ hiển thị là không khả dụng (lỗi 404 Not Found).

## Khôi phục Objects Đã Xóa

Để khôi phục một file có delete marker:

1. Bật **Show versions**
2. Tìm delete marker trên file của bạn
3. Nhấp vào delete marker
4. Chọn **Delete** để xóa vĩnh viễn delete marker
5. Xác nhận việc xóa

Điều này khôi phục phiên bản trước đó của object. Refresh webpage sẽ hiển thị lại file.

## Best Practices (Phương pháp Tốt nhất)

- **Kiểm soát Phiên bản**: Sử dụng versioning để bảo vệ khỏi việc xóa và ghi đè ngoài ý muốn
- **Khôi phục**: Giữ các phiên bản cho các file quan trọng để dễ dàng rollback
- **Chi phí Lưu trữ**: Nhớ rằng mỗi phiên bản tiêu tốn dung lượng lưu trữ
- **Xóa Vĩnh viễn**: Thận trọng khi xóa vĩnh viễn các phiên bản cụ thể - hành động này không thể hoàn tác

## Kết luận

S3 versioning là một tính năng mạnh mẽ cung cấp:
- Bảo vệ khỏi việc xóa ngoài ý muốn
- Khả năng rollback các thay đổi
- Lịch sử phiên bản hoàn chỉnh của các objects

Hãy thoải mái thử nghiệm với versioning bằng cách upload nhiều phiên bản của các files và quan sát hành vi của delete markers và version rollbacks.