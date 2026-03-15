# AWS DynamoDB Accelerator (DAX)

## Tổng quan
DAX (DynamoDB Accelerator) là dịch vụ bộ nhớ đệm được quản lý hoàn toàn, có tính khả dụng cao cho Amazon DynamoDB. Nó cung cấp độ trễ ở mức microsecond cho dữ liệu được lưu trong cache.

## Tạo DAX Cluster

### Bước 1: Truy cập DAX Console
- Điều hướng đến DynamoDB console
- Tìm DAX ở menu bên trái
- **Lưu ý**: DAX **không thuộc gói miễn phí** - việc tạo DAX cluster sẽ phát sinh chi phí

### Bước 2: Cấu hình Cluster

#### Tên Cluster
- Ví dụ: `DemoDAX`

#### Lựa chọn Node Family
Bạn có thể chọn giữa hai loại node chính:

**T-types (Hiệu suất có thể tăng đột biến)**
- Được khuyến nghị cho các trường hợp sử dụng có thông lượng thấp hơn
- Tiết kiệm chi phí cho việc phát triển và thử nghiệm
- Ví dụ: `t2.small`

**R-types (Tối ưu hóa bộ nhớ)**
- Được thiết kế cho khả năng luôn sẵn sàng
- Tốt hơn cho các workload sản xuất với thông lượng cao ổn định
- Ví dụ: `r5.large`, `r5.4xlarge`

### Bước 3: Kích thước Cluster
- **Phạm vi**: 1 đến 11 nodes
- **1 node**: Phù hợp cho single AZ hoặc môi trường phát triển
  - ⚠️ Có thể gặp vấn đề về tính khả dụng giảm
- **2 nodes**: Vẫn có thể gặp vấn đề về tính khả dụng giảm
- **3 nodes**: Cung cấp cấu hình multi-AZ cho tính khả dụng cao

### Bước 4: Cấu hình Mạng

#### Subnet Group
- Chọn hoặc tạo subnet group cho DAX cluster của bạn
- Ví dụ: `demosubnetgroup`
- Phải tồn tại trong một VPC cụ thể
- Chọn subnets dựa trên yêu cầu về tính khả dụng:
  - 3 subnets = hỗ trợ cho cấu hình 3 node có tính khả dụng cao

#### Kiểm soát Truy cập
- Cấu hình security group để kiểm soát quyền truy cập vào DAX cluster
- **Cổng yêu cầu**: 
  - Cổng **8111** (kết nối tiêu chuẩn)
  - Cổng **9111** (nếu sử dụng mã hóa trong quá trình truyền)
- Có thể tạo security group từ EC2 console
- Default security group có thể được sử dụng để demo

### Bước 5: Phân bổ Availability Zone
- Chọn giữa:
  - **Tự động**: AWS tự động phân phối các nodes qua các AZs
  - **Thủ công**: Chỉ định vị trí AZ cho từng node

## Thực hành Tốt nhất
✅ Sử dụng 3 hoặc nhiều nodes hơn cho môi trường production
✅ Bật mã hóa trong quá trình truyền cho dữ liệu nhạy cảm
✅ Đặt các nodes trên nhiều AZs để có tính khả dụng cao
✅ Cấu hình security groups phù hợp để hạn chế quyền truy cập
⚠️ Nhớ rằng DAX không đủ điều kiện cho gói miễn phí - theo dõi chi phí

## Những điểm chính cần nhớ
- DAX giảm đáng kể độ trễ đọc cho DynamoDB
- Kích thước cluster phù hợp ảnh hưởng đến cả tính khả dụng và chi phí
- Triển khai multi-AZ yêu cầu cấu hình subnet phù hợp
- Security groups phải cho phép traffic trên các cổng chuyên dụng của DAX
