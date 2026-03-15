# AWS CodeBuild - Tài Liệu Học Tập

## Tổng Quan
AWS CodeBuild là dịch vụ tích hợp liên tục (CI) được quản lý hoàn toàn, biên dịch mã nguồn, chạy kiểm thử và tạo ra các gói phần mềm sẵn sàng để triển khai.

## Khái Niệm Chính

### Hỗ Trợ Nguồn Mã
CodeBuild có thể lấy mã nguồn từ:
- **AWS CodeCommit**
- **Amazon S3**
- **Bitbucket**
- **GitHub**

### File buildspec.yml ⭐ QUAN TRỌNG CHO KỲ THI
- **Tên file**: `buildspec.yml`
- **Vị trí**: Phải ở **thư mục gốc (root) của mã nguồn**
- **Cách khác**: Có thể nhập hướng dẫn build thủ công trong console, nhưng best practice là dùng buildspec.yml
- **Trọng Tâm Thi**: Phải nhớ tên file và yêu cầu về vị trí

## Đầu Ra & Giám Sát

### Logs (Nhật Ký)
- Output logs được lưu trữ tại:
  - **Amazon S3**
  - **CloudWatch Logs**

### Giám Sát & Cảnh Báo
- **CloudWatch Metrics**: Xem thống kê build
- **EventBridge**: Phát hiện build thất bại và kích hoạt thông báo
- **CloudWatch Alarms**: Cảnh báo khi có quá nhiều lỗi

## Build Projects (Dự Án Build)
Build Projects có thể được định nghĩa trong:
- **CodeBuild** trực tiếp
- **CodePipeline** (cũng có thể gọi các CodeBuild project có sẵn)

## Môi Trường Được Hỗ Trợ

### Các Image Có Sẵn Cho:
- Java
- Ruby
- Python
- Go
- Node.js
- Android
- .NET Core
- PHP

### Môi Trường Tùy Chỉnh
- Mở rộng Docker image để hỗ trợ bất kỳ ngôn ngữ/môi trường nào khác
- Bạn tự duy trì và hỗ trợ môi trường tùy chỉnh của mình

## Cách CodeBuild Hoạt Động

### Quy Trình
1. **Lấy Mã (Fetch Code)**: CodeBuild lấy mã nguồn (ví dụ: từ CodeCommit) bao gồm cả buildspec.yml
2. **Tạo Container**: CodeBuild kéo Docker image (AWS cung cấp sẵn hoặc tùy chỉnh)
3. **Môi Trường Build**: Container được tạo với môi trường đã chọn (Java, Go, v.v.)
4. **Load Mã**: Container load mã nguồn và buildspec.yml
5. **Thực Thi Lệnh**: Chạy tất cả các lệnh từ buildspec.yml
6. **Caching (Tùy Chọn)**: Các file có thể được cache trong S3 bucket để tái sử dụng giữa các lần build
7. **Logging**: Tất cả logs được gửi đến CloudWatch Logs và S3 (nếu được bật)
8. **Artifacts**: Artifacts đầu ra cuối cùng được trích xuất và lưu trong S3 bucket

## Cấu Trúc buildspec.yml

### Các Phần Chính

#### **Environment (Môi Trường)**
Định nghĩa biến môi trường:
- **Biến dạng plain text**
- **SSM Parameter Store** values
- **Secrets Manager** secrets (cho mật khẩu, thông tin xác thực, v.v.)

#### **Phases (Các Giai Đoạn)**
- **install**: Lệnh để cài đặt các gói cần thiết
- **pre_build**: Lệnh thực thi trước khi build
- **build**: Các lệnh build thực sự ⭐ QUAN TRỌNG
- **post_build**: Hoàn thiện và dọn dẹp

### Lưu Ý Quan Trọng
- Không bao giờ lưu mật khẩu dạng plaintext trong buildspec.yml
- Sử dụng SSM Parameter Store hoặc Secrets Manager cho dữ liệu nhạy cảm
- File phải ở thư mục gốc (root) của code directory

## Mẹo Cho Kỳ Thi
✅ Nhớ: Tên file là `buildspec.yml`
✅ Vị trí: Thư mục gốc (root) của code directory
✅ Best practice: Sử dụng file buildspec.yml (không nhập thủ công trong console)
✅ Hiểu rõ quy trình build hoàn chỉnh
✅ Biết logs được lưu ở đâu (S3, CloudWatch)
✅ Nhận biết các ngôn ngữ lập trình được hỗ trợ

## Từ Vựng Quan Trọng
- **Build**: Biên dịch, xây dựng
- **Artifacts**: Sản phẩm đầu ra, kết quả build
- **Cache**: Bộ nhớ đệm
- **Container**: Vùng chứa, môi trường chạy độc lập
- **Logs**: Nhật ký, ghi chú hoạt động

---
*Ngày Học: Tháng 3, 2026*
