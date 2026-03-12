# Tổng Quan về AWS Network Load Balancer (NLB)

## Giới Thiệu

Network Load Balancer (NLB) là giải pháp cân bằng tải mạnh mẽ của AWS hoạt động ở tầng 4 của mô hình OSI, xử lý lưu lượng TCP và UDP với hiệu năng vượt trội.

## Tính Năng Chính

### Cân Bằng Tải Tầng 4

- **Hỗ trợ Giao thức**: Xử lý lưu lượng TCP và UDP
- **Mức thấp hơn**: Hoạt động ở Layer 4 (Tầng Giao vận), khác với Application Load Balancer hoạt động ở Layer 7 (HTTP/HTTPS)
- **Trường hợp sử dụng**: Khi bạn thấy yêu cầu về UDP hoặc TCP trong bài thi, hãy nghĩ đến Network Load Balancer

### Hiệu Năng Cao

- **Hiệu năng cực cao**: Có khả năng xử lý hàng triệu yêu cầu mỗi giây
- **Độ trễ cực thấp**: Độ trễ tối thiểu trong xử lý yêu cầu
- **Tốt nhất cho**: Ứng dụng yêu cầu hiệu năng cao với giao thức TCP hoặc UDP

### Địa Chỉ IP Tĩnh

- **Một IP tĩnh cho mỗi Availability Zone**: Mỗi AZ có một địa chỉ IP tĩnh riêng
- **Gán Elastic IP**: Bạn có thể gán Elastic IP cho mỗi AZ
- **Trường hợp sử dụng**: Hoàn hảo khi ứng dụng của bạn cần được truy cập thông qua một tập hợp địa chỉ IP cố định (1, 2 hoặc 3 IP cụ thể)

## Kiến Trúc và Target Groups

### Cách Hoạt Động

Network Load Balancer hoạt động tương tự như Application Load Balancer:
1. Tạo các target groups
2. NLB chuyển hướng lưu lượng đến các target groups này
3. Hỗ trợ lưu lượng TCP trên cả frontend và backend
4. Có thể sử dụng các giao thức khác nhau (ví dụ: TCP ở frontend, GTP ở backend)

### Các Tùy Chọn Target Group

Network Load Balancer hỗ trợ hai loại targets:

#### 1. EC2 Instances
- Định tuyến trực tiếp đến các EC2 instances
- Gửi lưu lượng TCP hoặc UDP đến các instances đã đăng ký

#### 2. Địa Chỉ IP (Chỉ Private IPs)
- **Địa chỉ IP riêng được mã hóa cứng**
- Có thể bao gồm:
  - Private IPs của các EC2 instances của bạn
  - Private IPs của các server trong data center của bạn
- Cho phép kiến trúc hybrid cloud với tích hợp on-premises

### Cấu Hình Nâng Cao: Kết Hợp NLB + ALB

Bạn có thể đặt Network Load Balancer phía trước Application Load Balancer:

**Lợi ích:**
- **Từ NLB**: Địa chỉ IP cố định cho client truy cập
- **Từ ALB**: Các quy tắc xử lý và định tuyến lưu lượng HTTP nâng cao
- **Kết quả**: Một sự kết hợp hợp lệ và mạnh mẽ cho các kiến trúc phức tạp

## Health Checks

Target groups của Network Load Balancer hỗ trợ health checks sử dụng ba giao thức:

1. **Giao thức TCP**
2. **Giao thức HTTP**
3. **Giao thức HTTPS**

Nếu ứng dụng backend của bạn hỗ trợ HTTP hoặc HTTPS, bạn có thể cấu hình health checks sử dụng các giao thức này.

## Khi Nào Sử Dụng Network Load Balancer

Chọn Network Load Balancer khi bạn cần:

- ✅ **Hiệu năng cực cao**: Hàng triệu yêu cầu mỗi giây
- ✅ **Giao thức TCP/UDP**: Xử lý lưu lượng mạng mức thấp
- ✅ **Yêu cầu IP tĩnh**: Địa chỉ IP cố định (bao gồm Elastic IPs)
- ✅ **Độ trễ cực thấp**: Yêu cầu độ trễ tối thiểu
- ✅ **Kiến trúc Hybrid**: Tích hợp với data center on-premises

## Mẹo Thi

- **Lưu lượng UDP** → Nghĩ đến Network Load Balancer
- **Lưu lượng TCP** → Cân nhắc Network Load Balancer
- **Yêu cầu Static/Elastic IP** → Network Load Balancer
- **Nhu cầu hiệu năng cao** → Network Load Balancer
- **HTTP/HTTPS với IP cố định** → Kết hợp NLB + ALB

## Tóm Tắt

Network Load Balancer là giải pháp cân bằng tải Layer 4 hiệu năng cao của AWS, được thiết kế cho các kịch bản hiệu năng cực cao yêu cầu xử lý lưu lượng TCP/UDP và địa chỉ IP tĩnh. Khả năng xử lý hàng triệu yêu cầu mỗi giây với độ trễ cực thấp làm cho nó trở nên lý tưởng cho các ứng dụng quan trọng về hiệu năng.