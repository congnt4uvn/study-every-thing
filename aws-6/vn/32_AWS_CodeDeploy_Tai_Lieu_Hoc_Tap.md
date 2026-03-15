# Tài Liệu Học Tập AWS CodeDeploy

## Tổng Quan
AWS CodeDeploy là dịch vụ triển khai ứng dụng tự động đến các dịch vụ máy tính như Amazon EC2, AWS Lambda và các máy chủ on-premises.

## Các Khái Niệm Chính

### 1. Triển Khai Trên EC2 Instance

#### Tệp AppSpec.yml
- Nằm ở thư mục gốc của mã nguồn
- Định nghĩa các hành động triển khai và lifecycle event hooks
- Thiết yếu cho cấu hình triển khai

#### Chiến Lược Triển Khai
- **In-Place Updates** (Cập nhật tại chỗ): Cập nhật các EC2 instance hiện có
- Ví dụ: Triển khai từng nửa (Half-at-a-time)
  - Nửa đầu được tắt và nâng cấp lên phiên bản 2
  - Nửa sau được tắt và nâng cấp lên phiên bản 2
  - Không tạo instance mới

### 2. Triển Khai Trên Auto Scaling Group (ASG)

CodeDeploy cung cấp hai loại triển khai cho ASG:

#### A. In-Place Deployment (Triển khai tại chỗ)
- Cập nhật các EC2 instance hiện có trong ASG
- Các EC2 instance mới được tạo bởi ASG tự động nhận triển khai
- Không tạo ASG mới

#### B. Blue/Green Deployment (Triển khai xanh/lục)
- Tạo một Auto Scaling Group mới
- Sao chép cài đặt từ ASG gốc
- Quy trình:
  1. ELB định hướng traffic đến các instance gốc (Blue - V1)
  2. Tạo ASG mới với launch template cập nhật (Green - V2)
  3. CodeDeploy triển khai ứng dụng lên các instance mới
  4. ELB nhận traffic từ cả instance V1 và V2
  5. Sau khi kiểm tra sức khỏe thành công, instance V1 bị chấm dứt
  6. Traffic được chuyển hoàn toàn sang instance V2

**Ưu điểm chính**: Bạn có thể chọn thời gian giữ ASG cũ trước khi xóa

### 3. Deployment Hooks (Móc Triển Khai)
- Được thiết lập trong tệp appspec.yml
- Dùng để xác minh triển khai sau mỗi giai đoạn
- Cho phép kiểm tra và xác thực trong quá trình triển khai

### 4. Triển Khai Lại và Rollback (Quay Lui)

#### Rollback là gì?
- Triển khai lại một phiên bản ứng dụng đã thành công trước đó
- "Quay ngược thời gian" về trạng thái tốt đã biết

#### Các Phương Thức Kích Hoạt Rollback

**Rollback Tự Động:**
- Phát hiện lỗi triển khai
- CloudWatch Alarm được kích hoạt báo hiệu vấn đề triển khai

**Rollback Thủ Công:**
- Do người vận hành/quản trị viên khởi tạo
- Có thể vô hiệu hóa nếu cần

#### Quan Trọng: Cách Rollback Hoạt Động
⚠️ **Lưu Ý Thi**: CodeDeploy KHÔNG khôi phục phiên bản trước. Thay vào đó:
- Nó triển khai lại phiên bản tốt cuối cùng như một **triển khai MỚI**
- Tạo phiên bản triển khai mới (không hoàn nguyên)
- Sử dụng mã nguồn của lần triển khai thành công cuối cùng

### 5. Tích Hợp Elastic Load Balancer (ELB)
- Định tuyến traffic giữa phiên bản cũ và mới trong triển khai blue/green
- Cho phép triển khai không downtime
- Chuyển dần traffic từ target group cũ sang mới

## Mẹo Học Tập
- Hiểu sự khác biệt giữa triển khai in-place và blue/green
- Nhớ rằng rollback tạo triển khai MỚI, không phải thao tác khôi phục
- Biết vai trò của appspec.yml trong quá trình triển khai
- Quen thuộc với các trigger rollback tự động và thủ công

## Trọng Tâm Cho Kỳ Thi
✓ Cơ chế rollback (triển khai mới vs khôi phục)
✓ Sự khác biệt giữa blue/green và in-place deployment
✓ Khả năng triển khai trên ASG
✓ Vị trí và mục đích của tệp AppSpec.yml
✓ Hooks triển khai và xác thực
