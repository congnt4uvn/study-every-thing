# AWS RDS: Read Replicas và Multi-AZ

## Tổng Quan

Hiểu được sự khác biệt giữa RDS Read Replicas và Multi-AZ là vô cùng quan trọng cho các kỳ thi AWS. Hướng dẫn này trình bày các trường hợp sử dụng, cấu hình và thực hành tốt nhất của chúng.

## RDS Read Replicas

### Read Replicas Là Gì?

Read Replicas giúp bạn mở rộng khả năng đọc dữ liệu bằng cách tạo các instance cơ sở dữ liệu bổ sung có thể xử lý lưu lượng đọc. Điều này hữu ích khi instance cơ sở dữ liệu chính của bạn nhận quá nhiều yêu cầu đọc và không thể mở rộng đủ.

### Tính Năng Chính

- **Khả năng mở rộng**: Tạo tối đa **15 Read Replicas**
- **Tùy chọn triển khai**:
  - Trong cùng một availability zone
  - Cross availability zone (giữa các AZ)
  - Cross region (giữa các vùng)

### Cơ Chế Nhân Bản

- **Nhân bản bất đồng bộ (Asynchronous Replication)**: Dữ liệu được nhân bản bất đồng bộ giữa instance cơ sở dữ liệu RDS chính và các Read Replicas
- **Eventually Consistent (Nhất quán cuối cùng)**: Các thao tác đọc là nhất quán cuối cùng, nghĩa là nếu ứng dụng của bạn đọc từ Read Replica trước khi nó nhân bản dữ liệu mới nhất, bạn có thể nhận được dữ liệu cũ

### Thăng Cấp Thành Cơ Sở Dữ Liệu Độc Lập

Read Replicas có thể được thăng cấp thành cơ sở dữ liệu độc lập:
- Sau khi thăng cấp, replica thoát khỏi cơ chế nhân bản
- Nó trở thành cơ sở dữ liệu độc lập với vòng đời riêng
- Sau đó nó có thể chấp nhận các thao tác ghi

### Yêu Cầu Triển Khai

Để sử dụng Read Replicas hiệu quả:
- Cập nhật connection string của ứng dụng để tận dụng tất cả Read Replicas
- Phân phối lưu lượng đọc trên các replica

## Trường Hợp Sử Dụng: Phân Tích và Báo Cáo

### Tình Huống

Một cơ sở dữ liệu production đang xử lý tải bình thường với các thao tác đọc và ghi. Một nhóm mới muốn chạy báo cáo và phân tích trên dữ liệu.

### Vấn Đề

Kết nối ứng dụng báo cáo trực tiếp vào instance cơ sở dữ liệu RDS chính sẽ:
- Làm quá tải cơ sở dữ liệu
- Làm chậm ứng dụng production

### Giải Pháp

1. Tạo một Read Replica
2. Nhân bản bất đồng bộ xảy ra giữa cơ sở dữ liệu chính và Read Replica
3. Ứng dụng báo cáo thực hiện đọc từ Read Replica
4. Ứng dụng production không bị ảnh hưởng

### Ràng Buộc Quan Trọng

Read Replicas chỉ hỗ trợ **các câu lệnh SELECT** (thao tác đọc):
- ✅ **Được phép**: Các truy vấn SELECT
- ❌ **Không được phép**: Các thao tác INSERT, UPDATE, DELETE

## Chi Phí Mạng Cho Read Replicas

### Nhân Bản Trong Cùng Region

**Không tính phí bổ sung** khi Read Replica ở cùng region nhưng khác availability zone:
- Ví dụ: Instance RDS ở `us-east-1a` với Read Replica ở `us-east-1b`
- Lưu lượng nhân bản là **miễn phí** vì RDS là dịch vụ được quản lý
- Truyền dữ liệu giữa các AZ được bao gồm miễn phí

### Nhân Bản Cross-Region

**Phát sinh chi phí mạng** khi Read Replica ở region khác:
- Ví dụ: Instance RDS ở `us-east-1` với Read Replica ở `eu-west-1`
- Lưu lượng nhân bản cross-region sẽ phát sinh phí nhân bản

## RDS Multi-AZ

### Mục Đích

Multi-AZ chủ yếu được sử dụng cho **Disaster Recovery (Khôi phục thảm họa)** và **tính sẵn sàng cao**, không phải để mở rộng quy mô.

### Kiến Trúc

- **Master Database**: Nằm ở Availability Zone A
- **Standby Database**: Nằm ở Availability Zone B
- **Nhân bản đồng bộ (Synchronous Replication)**: Mọi thay đổi ở Master được nhân bản đồng bộ sang Standby

### Cách Hoạt Động

1. Ứng dụng thực hiện đọc và ghi vào Master database
2. Các thay đổi được nhân bản đồng bộ sang Standby instance
3. Cả Master và Standby chia sẻ **một tên DNS**
4. Trong trường hợp lỗi, tự động failover sang Standby database

### Các Tình Huống Failover

Failover tự động xảy ra trong trường hợp:
- Mất toàn bộ availability zone
- Lỗi mạng
- Lỗi instance
- Lỗi storage trên Master database

### Đặc Điểm Chính

- **Failover không downtime**: Ứng dụng tự động kết nối lại qua tên DNS
- **Không cần can thiệp thủ công**: Failover hoàn toàn tự động
- **Không phải để mở rộng**: Standby database:
  - Không thể đọc từ nó
  - Không thể ghi vào nó
  - Chỉ tồn tại cho mục đích failover

## Kết Hợp Read Replicas và Multi-AZ

### Câu Hỏi

Có thể thiết lập Read Replicas với Multi-AZ cho Disaster Recovery không?

### Trả Lời

**Có!** Bạn có thể cấu hình Read Replicas của mình với Multi-AZ được bật. Đây là một câu hỏi thi phổ biến.

## Chuyển Đổi Từ Single-AZ Sang Multi-AZ

### Thao Tác Không Downtime

Chuyển đổi cơ sở dữ liệu RDS từ Single-AZ sang Multi-AZ là **thao tác không downtime**:
- Không cần dừng cơ sở dữ liệu
- Chỉ cần nhấp "Modify" cho cơ sở dữ liệu và bật Multi-AZ

### Quy Trình Diễn Ra Phía Sau

1. **Tạo Snapshot**: RDS tự động tạo snapshot của cơ sở dữ liệu chính
2. **Khôi phục**: Snapshot được khôi phục để tạo Standby database mới
3. **Đồng bộ hóa**: Thiết lập đồng bộ hóa giữa Master và Standby
4. **Catch-up**: Standby database bắt kịp Master database
5. **Hoàn tất**: Thiết lập Multi-AZ sẵn sàng

## Bảng Tóm Tắt Sự Khác Biệt

| Tính Năng | Read Replicas | Multi-AZ |
|-----------|--------------|----------|
| **Mục đích chính** | Mở rộng thao tác đọc | Khôi phục thảm họa & tính sẵn sàng cao |
| **Loại nhân bản** | Bất đồng bộ | Đồng bộ |
| **Số lượng instances** | Tối đa 15 replicas | 1 standby instance |
| **Thao tác đọc** | Có - trường hợp sử dụng chính | Không - standby là passive |
| **Thao tác ghi** | Không (trừ khi được thăng cấp) | Chỉ trên Master |
| **Failover tự động** | Không | Có |
| **Trường hợp sử dụng** | Workload nặng về đọc, phân tích | Tính sẵn sàng cao, chịu lỗi |
| **Tùy chọn triển khai** | Cùng AZ, Cross-AZ, Cross-Region | Chỉ Cross-AZ |

## Mẹo Cho Kỳ Thi

1. **Hiểu rõ sự khác biệt** giữa Read Replicas (mở rộng) và Multi-AZ (khôi phục thảm họa)
2. **Ghi nhớ**: Read Replicas sử dụng nhân bản bất đồng bộ; Multi-AZ sử dụng đồng bộ
3. **Biết rằng**: Chuyển đổi sang Multi-AZ là thao tác không downtime
4. **Nhớ**: Có thể tạo tối đa 15 Read Replicas
5. **Quan trọng**: Read Replicas có thể được cấu hình với Multi-AZ được bật
6. **Nhận thức về chi phí**: Read Replicas cùng region không có chi phí nhân bản; cross-region thì có

## Kết Luận

Hiểu về RDS Read Replicas và Multi-AZ là rất quan trọng cho kỳ thi AWS. Hãy nhớ rằng Read Replicas dùng để mở rộng khả năng đọc, trong khi Multi-AZ dùng cho khôi phục thảm họa. Cả hai có thể được sử dụng cùng nhau để tạo kiến trúc cơ sở dữ liệu có tính sẵn sàng cao và khả năng mở rộng.