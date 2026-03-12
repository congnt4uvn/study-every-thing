# Tổng Quan về AWS RDS

## Giới Thiệu về AWS RDS

**RDS** là viết tắt của **Relational Database Service** (Dịch vụ Cơ sở Dữ liệu Quan hệ). Đây là một dịch vụ cơ sở dữ liệu được quản lý cho các cơ sở dữ liệu sử dụng SQL làm ngôn ngữ truy vấn. SQL là ngôn ngữ có cấu trúc được thiết kế để truy vấn cơ sở dữ liệu, được thích ứng tốt và chạy trên nhiều engine khác nhau.

RDS cho phép bạn tạo các cơ sở dữ liệu trên đám mây được quản lý bởi AWS, mang lại nhiều lợi ích.

## Các Database Engine Được Hỗ Trợ

AWS RDS hỗ trợ các database engine sau:

- **PostgreSQL**
- **MySQL**
- **MariaDB**
- **Oracle**
- **Microsoft SQL Server**
- **IBM DB2**
- **Amazon Aurora** (cơ sở dữ liệu độc quyền của AWS)

## Tại Sao Nên Sử Dụng RDS Thay Vì EC2?

Mặc dù bạn có thể triển khai dịch vụ cơ sở dữ liệu của riêng mình trên EC2 instance, RDS là một **dịch vụ được quản lý** cung cấp nhiều lợi thế đáng kể:

### Lợi Ích Chính của RDS

- **Cung Cấp Tự Động**: Việc cung cấp cơ sở dữ liệu được tự động hóa hoàn toàn, bao gồm cả việc vá lỗi hệ điều hành cơ bản
- **Sao Lưu Liên Tục**: Tự động sao lưu với khả năng Point in Time Restore để khôi phục về một thời điểm cụ thể
- **Dashboard Giám Sát**: Xem hiệu suất của cơ sở dữ liệu
- **Read Replicas**: Cải thiện hiệu suất đọc với các bản sao đọc chuyên dụng
- **Thiết Lập Multi-AZ**: Kích hoạt khả năng khôi phục thảm họa
- **Cửa Sổ Bảo Trì**: Lên lịch các cửa sổ nâng cấp
- **Khả Năng Mở Rộng**:
  - **Mở Rộng Dọc**: Tăng loại instance
  - **Mở Rộng Ngang**: Thêm read replicas
- **Lưu Trữ EBS**: Lưu trữ được hỗ trợ bởi Amazon EBS

### Hạn Chế

- **Không Có Quyền Truy Cập SSH**: Bạn không thể SSH vào các RDS instances vì đây là dịch vụ được quản lý hoàn toàn

Tuy nhiên, hạn chế này được bù đắp bởi tất cả các tính năng tự động mà AWS cung cấp, mà nếu không bạn phải tự thiết lập trên EC2.

## RDS Storage Auto Scaling

### Tổng Quan

RDS Storage Auto Scaling là một tính năng có thể xuất hiện trong các kỳ thi AWS. Khi bạn tạo một cơ sở dữ liệu RDS, bạn chỉ định dung lượng lưu trữ ban đầu (ví dụ: 20 GB). Nếu cơ sở dữ liệu của bạn được sử dụng nhiều và sắp hết dung lượng lưu trữ, RDS có thể tự động mở rộng dung lượng lưu trữ mà không cần can thiệp thủ công.

### Cách Hoạt Động

1. Ứng dụng của bạn thực hiện nhiều thao tác đọc và ghi vào cơ sở dữ liệu RDS
2. Khi đạt đến các ngưỡng nhất định, dung lượng lưu trữ tự động mở rộng
3. Không có thời gian chết hoặc thao tác thủ công nào được yêu cầu

### Cấu Hình

Để sử dụng tính năng này:

- **Đặt Ngưỡng Lưu Trữ Tối Đa**: Xác định giới hạn tối đa cho việc tăng trưởng lưu trữ để ngăn việc mở rộng vô hạn
- **Kích Hoạt Tự Động Khi**:
  - Dung lượng lưu trữ trống nhỏ hơn 10% dung lượng đã phân bổ
  - Tình trạng dung lượng thấp kéo dài hơn 5 phút
  - Ít nhất 6 giờ đã trôi qua kể từ lần sửa đổi cuối cùng

### Trường Hợp Sử Dụng

Tính năng này đặc biệt hữu ích cho:
- Các ứng dụng có khối lượng công việc không thể đoán trước
- Tránh các thao tác mở rộng lưu trữ cơ sở dữ liệu thủ công
- Được hỗ trợ bởi tất cả các database engine của RDS

## Tổng Kết

AWS RDS là một dịch vụ cơ sở dữ liệu được quản lý mạnh mẽ, giúp đơn giản hóa việc quản trị cơ sở dữ liệu trong khi cung cấp tính khả dụng cao, sao lưu tự động và khả năng mở rộng liền mạch. Hiểu về RDS và các tính năng của nó là điều cần thiết cho các kỳ thi chứng chỉ AWS và triển khai đám mây thực tế.