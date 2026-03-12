# Elastic Beanstalk CLI và Quy Trình Triển Khai

## Tổng Quan

Elastic Beanstalk CLI (EB CLI) là một giao diện dòng lệnh bổ sung giúp làm việc với AWS Elastic Beanstalk dễ dàng và hiệu quả hơn nhiều. Mặc dù không bắt buộc phải biết cho kỳ thi AWS Developer, nhưng đây là một công cụ có giá trị để tự động hóa các pipeline phát triển.

## Các Lệnh EB CLI

EB CLI cung cấp một bộ lệnh toàn diện để quản lý các ứng dụng Elastic Beanstalk của bạn:

- `eb create` - Tạo môi trường mới
- `eb status` - Kiểm tra trạng thái môi trường
- `eb health` - Xem thông tin sức khỏe
- `eb events` - Hiển thị các sự kiện gần đây
- `eb logs` - Truy xuất logs
- `eb open` - Mở ứng dụng trong trình duyệt
- `eb deploy` - Triển khai ứng dụng
- `eb config` - Quản lý cấu hình
- `eb terminate` - Chấm dứt môi trường

Các lệnh này giúp bạn thực hiện những gì bạn có thể làm trong console Elastic Beanstalk, nhưng thông qua giao diện dòng lệnh.

## Khi Nào Nên Sử Dụng EB CLI

EB CLI đặc biệt hữu ích khi bạn muốn:

- Tự động hóa các pipeline phát triển
- Tăng tốc hiệu quả khi làm việc với Elastic Beanstalk
- Quản lý triển khai theo chương trình

**Lưu ý**: Kiến thức về EB CLI quan trọng hơn đối với kỳ thi AWS DevOps so với kỳ thi Developer.

## Triển Khai Ứng Dụng Beanstalk

### Điều Kiện Tiên Quyết

Bất kể bạn sử dụng console hay EB CLI, bạn cần mô tả các dependency của ứng dụng:

- **Python**: Tạo file `requirements.txt`
- **Node.js**: Tạo file `package.json`

### Quy Trình Triển Khai

1. **Đóng gói code**: Tạo file zip chứa tất cả code ứng dụng và file dependency
2. **Upload lên Beanstalk**: Upload file zip lên Elastic Beanstalk
3. **Tạo phiên bản ứng dụng**: Việc upload sẽ tạo ra một phiên bản ứng dụng mới
4. **Triển khai**: Deploy phiên bản ứng dụng bằng cách sử dụng:
   - Console Beanstalk, hoặc
   - EB CLI

### Quy Trình Bên Trong

Khi bạn upload file zip lên Beanstalk:

1. File zip được upload lên **Amazon S3**
2. Beanstalk tham chiếu đến zip bundle từ S3
3. Beanstalk triển khai zip đến từng EC2 instance trong môi trường của bạn
4. Các dependency được giải quyết từ `requirements.txt` (Python) hoặc `package.json` (Node.js)
5. Ứng dụng khởi động trên các instance

## Sử Dụng EB CLI Để Triển Khai

EB CLI đơn giản hóa quy trình triển khai bằng cách:

1. Tự động tạo file zip
2. Upload zip lên Beanstalk
3. Triển khai ứng dụng

Việc tự động hóa này giúp quy trình triển khai nhanh hơn và hiệu quả hơn.

## Tài Nguyên Bổ Sung

Để biết thêm thông tin chi tiết về cách cài đặt và sử dụng EB CLI, bạn có thể tham khảo trang web tài liệu chính thức của AWS.

**Lưu ý về Kỳ thi**: EB CLI nằm ngoài phạm vi của kỳ thi AWS Developer Associate và khóa học này. Thông tin được cung cấp ở đây chỉ để nhận thức về sự tồn tại của nó.

## Tóm Tắt

- EB CLI là công cụ bổ sung để quản lý các ứng dụng Elastic Beanstalk
- Nó cung cấp các lệnh để tự động hóa các thao tác Beanstalk thông dụng
- Các ứng dụng được đóng gói dưới dạng file zip với các mô tả dependency
- Các file zip được lưu trữ trong S3 và triển khai đến các EC2 instance
- EB CLI phù hợp hơn cho kỳ thi DevOps so với kỳ thi Developer