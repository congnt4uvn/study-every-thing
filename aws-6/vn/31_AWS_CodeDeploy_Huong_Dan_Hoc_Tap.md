# AWS CodeDeploy - Hướng Dẫn Học Tập

## Tổng Quan
AWS CodeDeploy là dịch vụ triển khai tự động giúp bạn triển khai ứng dụng trên nhiều nền tảng điện toán khác nhau.

## Các Tính Năng Chính

### 1. **AWS CodeDeploy là gì?**
- Dịch vụ triển khai tự động hóa việc triển khai ứng dụng
- Cho phép nâng cấp từ phiên bản 1 lên phiên bản 2 tự động
- Hỗ trợ nhiều mục tiêu triển khai khác nhau

### 2. **Mục Tiêu Triển Khai**
CodeDeploy có thể triển khai đến:
- **EC2 instances** (Máy chủ ảo EC2)
- **On-premises servers** (Máy chủ tại chỗ)
- **Lambda functions** (Hàm Lambda)
- **ECS services** (Dịch vụ ECS)

*Lưu ý: EC2 instances và on-premises servers sử dụng cùng phương pháp triển khai*

### 3. **Khả Năng Chính**
- ✅ Cập nhật ứng dụng
- ✅ Tự động rollback (quay lại phiên bản cũ) khi thất bại
- ✅ Rollback được kích hoạt bởi cảnh báo
- ✅ Kiểm soát tốc độ triển khai
- ✅ Cấu hình triển khai thông qua file `appspec.yml`

## Nền Tảng EC2/On-Premises

### Các Loại Triển Khai

#### 1. **In-Place Deployment (Triển Khai Tại Chỗ)**
- Cập nhật các instance hiện có trong cùng môi trường
- Các instance được dừng, cập nhật, và khởi động lại

#### 2. **Blue/Green Deployment (Triển Khai Xanh/Lục)**
- Tạo các instance mới (green) cùng với các instance cũ (blue)
- Traffic được chuyển sang các instance mới
- Các instance cũ bị xóa sau khi triển khai thành công

### Điều Kiện Tiên Quyết
- **CodeDeploy Agent** phải được cài đặt trên các instance đích
- Agent thực hiện việc cập nhật thực tế trên các instance
- Có thể cài đặt thông qua:
  - Lệnh Linux trực tiếp
  - Systems Manager (để cài đặt tự động)

### Yêu Cầu IAM
- EC2 instances cần quyền IAM đủ để truy cập Amazon S3
- S3 lưu trữ các file phiên bản ứng dụng

## Tùy Chọn Tốc Độ Triển Khai

| Tùy Chọn | Mô Tả | Tác Động Downtime | Trường Hợp Sử Dụng |
|----------|-------|-------------------|---------------------|
| **AllAtOnce** | Cập nhật tất cả instances cùng lúc | Downtime cao nhất | Triển khai nhanh, testing |
| **HalfAtATime** | Cập nhật 50% instances một lúc | Downtime trung bình | Cách tiếp cận cân bằng |
| **OneAtATime** | Cập nhật từng instance một | Downtime thấp nhất | Production, hệ thống quan trọng |
| **Custom** | Tự định nghĩa tốc độ triển khai | Có thể thay đổi | Yêu cầu cụ thể |

## Ví Dụ In-Place Deployment (HalfAtATime)

**Tình huống:** 4 EC2 instances đang chạy v1

1. **Bước 1:** Hai instances được dừng để bảo trì
2. **Bước 2:** Agent dừng ứng dụng trên hai instances đó
3. **Bước 3:** Agent nâng cấp chúng lên phiên bản 2
4. **Bước 4:** Nửa còn lại được dừng
5. **Bước 5:** Các instances còn lại được nâng cấp lên phiên bản 2

**Kết quả:** Tất cả instances hiện chạy v2 với downtime tối thiểu

## Quy Trình Blue/Green Deployment

1. **Trạng Thái Ban Đầu:** Application Load Balancer → v1 Auto Scaling Group
2. **Tạo ASG Mới:** CodeDeploy tạo Auto Scaling Group mới (thủ công hoặc tự động)
3. **Triển Khai v2:** Các instance mới được khởi chạy với phiên bản 2
4. **Chuyển Traffic:** Load Balancer được chuyển hướng đến v2 Auto Scaling Group
5. **Dọn Dẹp:** v1 Auto Scaling Group bị xóa

**Lợi Ích:**
- Không có downtime
- Dễ dàng rollback (giữ v1 chạy tạm thời)
- Instance mới = môi trường sạch

## File Cấu Hình Quan Trọng

### appspec.yml
- Định nghĩa cách triển khai sẽ diễn ra
- Kiểm soát hành vi triển khai
- Phải được bao gồm trong phiên bản ứng dụng

## Thực Hành Tốt Nhất

1. ✅ Luôn test triển khai trong môi trường non-production trước
2. ✅ Cấu hình cảnh báo phù hợp để tự động rollback
3. ✅ Chọn tốc độ triển khai dựa trên tính quan trọng của ứng dụng
4. ✅ Đảm bảo CodeDeploy Agent được cài đặt và chạy đúng cách
5. ✅ Thiết lập IAM roles và permissions phù hợp
6. ✅ Lưu trữ phiên bản ứng dụng an toàn trong S3
7. ✅ Sử dụng blue/green deployments cho các hệ thống production quan trọng

## Những Điểm Chính Cần Nhớ

- 🎯 CodeDeploy tự động hóa triển khai và rollback
- 🎯 Hỗ trợ nhiều mục tiêu triển khai
- 🎯 Hai chiến lược triển khai chính: In-Place và Blue/Green
- 🎯 CodeDeploy Agent là thiết yếu cho triển khai EC2/on-premises
- 🎯 Tốc độ triển khai có thể được kiểm soát và tùy chỉnh
- 🎯 Các phiên bản ứng dụng được lưu trữ trong Amazon S3

## Thuật Ngữ Quan Trọng

- **Deployment** - Triển khai
- **Rollback** - Quay lại phiên bản trước
- **Instance** - Máy chủ ảo/Thực thể
- **Auto Scaling Group** - Nhóm tự động mở rộng
- **Load Balancer** - Bộ cân bằng tải
- **Downtime** - Thời gian ngừng hoạt động
- **Agent** - Tác nhân/Phần mềm đại diện
- **Application Revision** - Phiên bản ứng dụng

---

*Mẹo Học Tập: Thực hành thiết lập CodeDeploy với một ứng dụng đơn giản để hiểu rõ quy trình triển khai thực tế.*
