# Hướng Dẫn Thực Hành Amazon ElastiCache

## Giới Thiệu

Trong hướng dẫn thực hành này, chúng ta sẽ thực hành sử dụng Amazon ElastiCache bằng cách tạo và cấu hình một Redis cluster. Hướng dẫn này sẽ đưa bạn qua tất cả các tùy chọn cấu hình có sẵn khi thiết lập ElastiCache.

## Bắt Đầu

Khi bạn bắt đầu tạo ElastiCache cluster, bạn sẽ thấy một số engine được khuyến nghị:

- **Valkey** - Sự thay thế cho Redis (tùy chọn được khuyến nghị)
- **Memcached**
- **Redis OSS**

Trong hướng dẫn này, chúng ta sẽ sử dụng **Redis** vì nó cung cấp các tùy chọn giống như Valkey.

## Tùy Chọn Triển Khai

ElastiCache cung cấp hai tùy chọn triển khai:

1. **Serverless** - Tùy chọn được quản lý hoàn toàn
2. **Node-based cluster** - Kiểm soát nhiều hơn về cấu hình

Chúng ta sẽ chọn **node-based cluster** để hiểu chính xác cách mọi thứ hoạt động.

## Phương Pháp Cấu Hình

Bạn có thể cấu hình cluster của mình theo nhiều cách:

- **Restore from backup** - Sử dụng bản sao lưu hiện có
- **Easy create** - Sử dụng các phương pháp hay nhất được khuyến nghị
  - Cấu hình Production
  - Cấu hình Dev/Test
  - Cấu hình Demo
- **Custom configuration** - Cấu hình thủ công mọi thứ

Trong hướng dẫn này, chúng ta sẽ sử dụng **custom configuration** để xem tất cả các tùy chọn có sẵn.

## Chế Độ Cluster

### Chế Độ Cluster Bị Vô Hiệu Hóa (Cluster Mode Disabled)
- Một shard duy nhất với một primary node
- Lên đến 5 read replica
- Phù hợp cho các triển khai đơn giản hơn

### Chế Độ Cluster Được Kích Hoạt (Cluster Mode Enabled)
- Nhiều shard trên nhiều server
- Tốt hơn cho khả năng mở rộng

Trong hướng dẫn này, chúng ta sẽ sử dụng **cluster mode disabled**.

## Cấu Hình Cơ Bản

### Cài Đặt Cluster
- **Tên Cluster**: DemoCluster
- **Vị trí**: AWS Cloud (cũng có thể chạy on-premises sử dụng AWS Outpost)

### Tùy Chọn Tính Khả Dụng Cao
- **Multi-AZ**: Vô hiệu hóa (để giảm chi phí cho demo này)
  - Cung cấp tính khả dụng cao và failover
  - Hữu ích trong trường hợp primary node lỗi
- **Auto-failover**: Được kích hoạt

### Cấu Hình Engine
- Phiên bản engine (chỉ định theo nhu cầu)
- Cấu hình cổng
- Parameter groups

## Chọn Loại Node

Trong hướng dẫn này, chúng ta sẽ sử dụng **micro instance type**:

- **t2.micro** (Đủ điều kiện Free tier)
- **t3.micro** (Đủ điều kiện Free tier)
- **t4g.micro**

Chúng ta sẽ chọn **t2.micro** để tối ưu hóa chi phí.

## Cấu Hình Replica

- **Số lượng replica**: 0 (để tiết kiệm chi phí)
- Lưu ý: Khi sử dụng Multi-AZ, bạn nên có nhiều replica hơn để có tính khả dụng tốt hơn

## Cấu Hình Mạng

### Subnet Group
- **Tên**: my-first-subnet-group
- Chỉ ra subnet nào mà ElastiCache có thể chạy
- Chọn VPC
- Subnet được chọn tự động (có thể chỉ định thủ công)

### Vị Trí Availability Zone
- Chỉ định replica nào đi đến AZ nào
- Không quan trọng khi không chạy chế độ Multi-AZ

## Cấu Hình Bảo Mật

### Mã Hóa Khi Lưu Trữ (Encryption at Rest)
- Kích hoạt/vô hiệu hóa theo nhu cầu
- Yêu cầu chỉ định key nếu được kích hoạt

### Mã Hóa Khi Truyền Tải (Encryption in Transit)
- Mã hóa dữ liệu giữa client và server
- Kích hoạt tính năng kiểm soát truy cập khi được bật:
  - **Redis AUTH**: Chỉ định password/AUTH token để kết nối
  - **User group access control list**: Tạo user group từ ElastiCache console

Trong hướng dẫn này, chúng ta sẽ **vô hiệu hóa encryption in transit**.

### Security Groups
- Quản lý ứng dụng nào có quyền truy cập mạng vào cluster của bạn

## Cấu Hình Sao Lưu

- Kích hoạt hoặc vô hiệu hóa sao lưu tự động
- Cấu hình thời gian lưu trữ backup theo nhu cầu

## Cấu Hình Bảo Trì

- **Maintenance windows**: Lên lịch cho các bản nâng cấp phiên bản nhỏ
- **Logs**: Cấu hình slow logs hoặc engine logs
  - Có thể được gửi đến CloudWatch Logs

## Gắn Tag

- Thêm tag để tổ chức tài nguyên và theo dõi chi phí

## Tạo Cluster

Sau khi xem xét tất cả các tùy chọn cấu hình:

1. Xem lại tất cả các cài đặt
2. Nhấp **Create** để tạo cache

## Sử Dụng ElastiCache Cluster

Khi ElastiCache database của bạn được tạo:

1. Nhấp vào cluster để xem chi tiết
2. Sử dụng **primary endpoint** cho các thao tác ghi
3. Sử dụng **reader endpoint** cho các thao tác đọc (nếu sử dụng read replica)

## Tính Năng Console

Từ AWS ElastiCache console, bạn có thể xem:

- Chi tiết cluster
- Thông tin nodes
- Metrics
- Logs
- Cài đặt bảo mật mạng

Giao diện console tương tự như RDS, vì ElastiCache chia sẻ nhiều khái niệm với RDS nhưng được thiết kế đặc biệt cho Redis và Memcached.

## Kết Nối Đến Redis

**Lưu ý**: Kết nối đến Redis cache yêu cầu viết mã ứng dụng và nằm ngoài phạm vi của hướng dẫn dựa trên console này. Tuy nhiên, bạn sẽ sử dụng các endpoint được cung cấp trong console để thiết lập kết nối từ ứng dụng của bạn.

## Dọn Dẹp

Để xóa Redis cluster của bạn:

1. Chọn cluster
2. Nhấp **Actions** → **Delete**
3. Chọn có tạo backup cuối cùng hay không (Không cho demo này)
4. Nhập tên cluster để xác nhận
5. Nhấp **Delete**

## Kết Luận:

Hướng dẫn thực hành này đã đề cập đến tất cả các tùy chọn cấu hình thiết yếu để tạo Amazon ElastiCache cluster. Dịch vụ này tương tự như RDS nhưng được tối ưu hóa cho bộ nhớ đệm in-memory với Redis và Memcached engines.

## Những Điểm Chính Cần Nhớ

- ElastiCache hỗ trợ nhiều engine: Valkey, Redis, và Memcached
- Cluster mode có thể bị vô hiệu hóa (single shard) hoặc được kích hoạt (multiple shards)
- Multi-AZ cung cấp tính khả dụng cao nhưng tăng chi phí
- Các tùy chọn mã hóa có sẵn cho cả at rest và in transit
- Security groups và access control lists quản lý quyền truy cập
- Giao diện console tương tự như RDS
- Luôn nhớ xóa tài nguyên khi hoàn thành để tránh chi phí không cần thiết