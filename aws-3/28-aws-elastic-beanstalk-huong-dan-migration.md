# Hướng Dẫn Migration AWS Elastic Beanstalk

## Tổng Quan

Hướng dẫn này bao gồm các chiến lược migration quan trọng cho AWS Elastic Beanstalk, thường xuất hiện trong các kỳ thi chứng chỉ AWS. Chúng ta sẽ khám phá hai tình huống migration chính:

1. Migration Load Balancer
2. Tách RDS Database

---

## Migration Load Balancer

### Hạn Chế Quan Trọng

Sau khi tạo môi trường Elastic Beanstalk, **bạn không thể thay đổi loại Elastic Load Balancer** - chỉ có thể thay đổi cấu hình của nó.

### Hiểu Về Giới Hạn

- Nếu bạn tạo **Classic Load Balancer**, bạn chỉ có thể chỉnh sửa các cài đặt của Classic Load Balancer
- Bạn **không thể nâng cấp** trực tiếp từ Classic Load Balancer lên Application Load Balancer
- Bạn **không thể thay đổi** trực tiếp từ Application Load Balancer sang Network Load Balancer

### Các Bước Migration

Để migration giữa các loại Load Balancer khác nhau, thực hiện theo các bước sau:

#### Bước 1: Tạo Môi Trường Mới
Tạo một môi trường Elastic Beanstalk mới với cùng cấu hình **ngoại trừ** loại Load Balancer.

**Lưu Ý Quan Trọng:** Bạn không thể sử dụng tính năng clone vì nó sẽ sao chép chính xác cùng loại và cấu hình Load Balancer. Bạn phải tạo lại cấu hình theo cách thủ công.

#### Bước 2: Triển Khai Ứng Dụng
Triển khai ứng dụng của bạn lên môi trường mới với loại Load Balancer mong muốn (ví dụ: Application Load Balancer).

#### Bước 3: Chuyển Hướng Traffic
Chuyển traffic từ môi trường cũ sang môi trường mới bằng một trong các phương pháp sau:
- **CNAME swap** (triển khai Blue/Green)
- **Cập nhật DNS qua Route 53**

Cả hai phương pháp đều hoạt động hiệu quả cho việc migration traffic.

---

## Migration RDS Database

### Phương Pháp Development vs Production

#### Môi Trường Development/Test
RDS có thể được cung cấp trực tiếp trong môi trường Elastic Beanstalk, thuận tiện cho:
- Môi trường phát triển
- Mục đích testing

#### Vấn Đề Với Môi Trường Production
Trong production, việc cung cấp RDS trong Beanstalk **không được khuyến nghị** vì:
- Vòng đời của database bị gắn liền với vòng đời của môi trường Beanstalk
- Việc xóa môi trường Beanstalk có thể ảnh hưởng đến database của bạn

### Best Practice Cho Production

Tách RDS Database ra khỏi môi trường Elastic Beanstalk và tham chiếu nó thông qua:
- Connection strings
- Biến môi trường (environment variables)

---

## Tách RDS Khỏi Elastic Beanstalk

Nếu RDS của bạn đã được tích hợp với Beanstalk stack, hãy làm theo các bước sau để tách nó ra:

### Bước 1: Tạo Snapshot
Tạo snapshot của RDS Database như một biện pháp phòng ngừa. Điều này đảm bảo bạn có bản backup trong trường hợp có sự cố xảy ra.

### Bước 2: Bật Deletion Protection
Vào RDS console và **bảo vệ RDS Database khỏi bị xóa**. Điều này ngăn chặn nó bị xóa bất kể điều gì xảy ra với môi trường Beanstalk.

### Bước 3: Tạo Môi Trường Mới Không Có RDS
Tạo một môi trường Elastic Beanstalk mới, lần này **không có RDS**.

### Bước 4: Cấu Hình Kết Nối
Trỏ ứng dụng của bạn đến RDS Database hiện có bằng cách sử dụng biến môi trường hoặc connection string.

### Bước 5: Thực Hiện Chuyển Đổi Traffic
Thực hiện CNAME swap (triển khai Blue/Green) hoặc cập nhật DNS qua Route 53, sau đó xác nhận mọi thứ hoạt động chính xác.

### Bước 6: Kết Thúc Môi Trường Cũ
Kết thúc môi trường Beanstalk cũ. Vì RDS deletion protection đã được bật, RDS instance sẽ vẫn còn nguyên vẹn.

### Bước 7: Dọn Dẹp CloudFormation
CloudFormation stack đằng sau môi trường Elastic Beanstalk của bạn sẽ không thể xóa hoàn toàn và chuyển sang trạng thái **"Delete Failed"**. Bạn cần xóa CloudFormation stack đó theo cách thủ công thông qua CloudFormation console.

---

## Tổng Kết

Bằng cách tuân theo các chiến lược migration này, bạn có thể:

✅ Migration thành công giữa các loại Load Balancer khác nhau
✅ Tách RDS databases khỏi môi trường Elastic Beanstalk
✅ Duy trì tính độc lập của production database
✅ Đảm bảo migration không downtime bằng cách sử dụng các kỹ thuật chuyển đổi traffic

Những pattern này thường được kiểm tra trong các kỳ thi chứng chỉ AWS và là cần thiết cho các triển khai AWS cấp production.