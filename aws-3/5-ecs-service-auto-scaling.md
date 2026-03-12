# Tự Động Mở Rộng ECS Service (ECS Service Auto Scaling)

## Tổng Quan

Tự động mở rộng ECS Service cho phép bạn tự động tăng hoặc giảm số lượng task trong dịch vụ ECS của mình. Mặc dù bạn có thể điều chỉnh số lượng task theo cách thủ công, việc tận dụng AWS Application Auto Scaling cung cấp khả năng mở rộng động và tự động.

## Các Chỉ Số Mở Rộng

AWS Application Auto Scaling hỗ trợ ba chỉ số chính để mở rộng ECS Service:

1. **CPU Utilization (Sử dụng CPU)** - Mở rộng dựa trên mức sử dụng CPU của ECS Service
2. **Memory Utilization (Sử dụng bộ nhớ)** - Mở rộng dựa trên mức sử dụng RAM của ECS Service
3. **ALB Request Count Per Target (Số lượng yêu cầu ALB trên mỗi đích)** - Mở rộng dựa trên các chỉ số từ Application Load Balancer

## Các Loại Tự Động Mở Rộng

Bạn có thể cấu hình các loại tự động mở rộng khác nhau cho ECS Service:

### Target Tracking (Theo Dõi Mục Tiêu)
Theo dõi một giá trị mục tiêu cụ thể cho ba chỉ số đã đề cập ở trên. Dịch vụ tự động điều chỉnh công suất để duy trì mục tiêu.

### Step Scaling (Mở Rộng Theo Bước)
Xác định các điều chỉnh mở rộng dựa trên các cảnh báo CloudWatch vượt qua ngưỡng đã định.

### Scheduled Scaling (Mở Rộng Theo Lịch)
Mở rộng ECS Service của bạn trước thời gian dựa trên các thay đổi có thể dự đoán được về nhu cầu.

## Các Lưu Ý Quan Trọng

### Mở Rộng ECS Service vs. Mở Rộng EC2 Cluster

**Lưu ý quan trọng**: Mở rộng ECS Service ở cấp độ task **không bằng** với việc mở rộng cluster các instance EC2 khi sử dụng EC2 launch type.

- **Không có EC2 instances** (Fargate): Tự động mở rộng service dễ dàng hơn nhiều vì mọi thứ đều là serverless
- **Có EC2 instances** (EC2 launch type): Bạn cần các cơ chế bổ sung để mở rộng hạ tầng EC2 bên dưới

> **Mẹo Thi**: AWS khuyến khích sử dụng Fargate để mở rộng dễ dàng hơn và vận hành serverless.

## Mở Rộng EC2 Instances Trong EC2 Launch Type

Khi sử dụng EC2 launch type, bạn có hai tùy chọn để mở rộng các EC2 instance bên dưới:

### Tùy Chọn 1: Auto Scaling Group (ASG) Scaling
- Mở rộng ASG dựa trên các chỉ số như CPU Utilization
- Các EC2 instance được thêm vào theo thời gian khi mức sử dụng CPU tăng
- Yêu cầu cấu hình thủ công

### Tùy Chọn 2: ECS Cluster Capacity Provider (Khuyến Nghị)
- Cách tiếp cận **thông minh và tiên tiến hơn**
- Tự động ghép nối với Auto Scaling Group
- Mở rộng ASG một cách thông minh khi cần công suất cho các task mới
- Giám sát khả năng sẵn có của RAM và CPU
- Tự động cung cấp các EC2 instance khi tài nguyên không đủ

> **Thực Hành Tốt Nhất**: Luôn sử dụng **ECS Cluster Capacity Provider** thay vì mở rộng ASG truyền thống cho triển khai EC2 launch type.

## Cách Hoạt Động: Tự Động Mở Rộng Trong Thực Tế

### Ví Dụ Kịch Bản

1. **Trạng Thái Ban Đầu**: Service A đang chạy với 2 task
2. **Tăng Tải**: Nhiều người dùng truy cập ứng dụng hơn, khiến mức sử dụng CPU tăng đột biến
3. **Giám Sát CloudWatch**: CloudWatch Metric giám sát mức sử dụng CPU ở cấp độ ECS service
4. **Kích Hoạt Cảnh Báo**: Mức sử dụng CPU cao kích hoạt CloudWatch Alarm
5. **Hoạt Động Mở Rộng**: Cảnh báo kích hoạt AWS Application Auto Scaling
6. **Tăng Công Suất**: Công suất mong muốn cho ECS Service của bạn tăng lên
7. **Tạo Task Mới**: Một task mới được khởi chạy để xử lý tải tăng thêm
8. **Mở Rộng EC2 Tùy Chọn**: Nếu sử dụng EC2 launch type, ECS Capacity Providers tự động mở rộng EC2 cluster để hỗ trợ các task bổ sung

## Tóm Tắt

- **ECS Service Auto Scaling** quản lý số lượng task
- **AWS Application Auto Scaling** cung cấp cơ chế mở rộng
- **Fargate** đơn giản hóa việc mở rộng bằng cách loại bỏ quản lý EC2
- **ECS Cluster Capacity Provider** là cách tiếp cận được khuyến nghị cho EC2 launch type
- Việc mở rộng được kích hoạt bởi các chỉ số và cảnh báo CloudWatch