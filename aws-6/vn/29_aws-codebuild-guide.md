# Hướng Dẫn Học AWS CodeBuild

## Tổng Quan
AWS CodeBuild là dịch vụ tích hợp liên tục (continuous integration) được quản lý hoàn toàn, dùng để biên dịch mã nguồn, chạy kiểm thử và tạo ra các gói phần mềm sẵn sàng để triển khai.

## Khái Niệm Chính

### CodeBuild Là Gì?
- Dịch vụ build được quản lý trên cloud
- Biên dịch mã nguồn và chạy các bài kiểm thử
- Không cần cung cấp, quản lý hoặc mở rộng máy chủ build
- Tích hợp với các dịch vụ AWS khác và hệ thống quản lý mã nguồn phổ biến

## Tạo Dự Án CodeBuild

### 1. Cấu Hình Dự Án
- **Tên Dự Án**: Chọn tên mô tả rõ ràng (ví dụ: "MyFirstBuild")
- **Mô Tả**: Mô tả dự án (tùy chọn)
- **Build Badge**: Huy hiệu trạng thái (tùy chọn)
- **Tags**: Thẻ metadata (tùy chọn)

### 2. Cấu Hình Nguồn

#### Các Nhà Cung Cấp Nguồn Được Hỗ Trợ:
- Amazon S3
- AWS CodeCommit
- GitHub
- Bitbucket
- GitHub Enterprise
- GitLab
- GitLab Self-Managed

#### Tích Hợp GitHub:
1. Chọn GitHub làm nhà cung cấp nguồn
2. Kết nối sử dụng OAuth
3. Cho phép AWS CodeSuite truy cập repository của bạn
4. Chọn repository (ví dụ: nodejs-app)
5. Chọn nhánh (mặc định: main)

#### Trigger Build:
- **Rebuild khi có thay đổi code**: Tự động khởi chạy build khi code được push
- **Single Build**: Thực hiện một build cho mỗi trigger
- **Các Loại Sự Kiện**:
  - PUSH: Build khi code được push
  - Pull Request: Build khi PR được tạo
  - Release: Build khi release được tạo

### 3. Cấu Hình Môi Trường

#### Tùy Chọn Compute:
- **Managed Image**: Amazon Linux hoặc Ubuntu
- **Runtime**: Standard
- **Phiên Bản Image**: Latest (ví dụ: standard 7.0)

#### Service Role:
- Tạo service role mới (ví dụ: "CodeBuildDemoServiceRole")
- Cấp các quyền cần thiết cho hoạt động của CodeBuild

#### Cấu Hình Bổ Sung:
- **Timeout**: Thời gian build tối đa (mặc định: 1 giờ, có thể điều chỉnh xuống thời gian ngắn hơn như 10 phút)
- **VPC**: Tùy chọn - chọn VPC để truy cập tài nguyên riêng tư (database, dịch vụ nội bộ)
- **Compute Size**: 
  - 3 GB bộ nhớ
  - 2 vCPUs
  - (Có thể điều chỉnh dựa trên nhu cầu)
- **Environment Variables**: Định nghĩa biến cho quá trình build

### 4. Cấu Hình Buildspec

#### Buildspec Là Gì?
- File YAML định nghĩa các lệnh build và cài đặt
- Phải được đặt tên là `buildspec.yaml` (hoặc `buildspec.yml`)
- Nằm trong thư mục gốc của mã nguồn

#### Tùy Chọn Buildspec:
1. **Sử dụng file buildspec**: Tham chiếu buildspec.yaml trong repository
2. **Chèn lệnh build**: Định nghĩa lệnh trực tiếp trong console

**Quan Trọng**: Nếu sử dụng file buildspec, đảm bảo file tồn tại trong thư mục gốc của repository. Build sẽ thất bại nếu thiếu file này.

### 5. Artifacts (Tùy Chọn)
- Lưu trữ đầu ra build trong Amazon S3
- Hữu ích cho các file nhị phân đã biên dịch, package hoặc artifact triển khai
- Không bắt buộc đối với build chỉ để kiểm thử

### 6. Logs
- **CloudWatch Logs**: Stream log đến CloudWatch
- **Amazon S3**: Lưu trữ log trong S3 bucket

## Chạy Build

### Quy Trình Build:
1. CodeBuild pull mã nguồn từ repository
2. Thiết lập môi trường build
3. Thực thi các lệnh được định nghĩa trong buildspec.yaml
4. Chạy kiểm thử hoặc biên dịch code
5. Tạo artifacts (nếu được cấu hình)
6. Báo cáo thành công hoặc thất bại

### Nguyên Nhân Thất Bại Thường Gặp:
- Thiếu file buildspec.yaml
- Cú pháp buildspec không chính xác
- Lệnh build thất bại
- Kiểm thử thất bại
- Quyền không đủ

## Best Practices (Thực Hành Tốt Nhất)

1. **Version Control**: Luôn lưu buildspec.yaml trong repository của bạn
2. **Timeouts**: Đặt timeout phù hợp để tránh chi phí không cần thiết
3. **Cấu Hình VPC**: Sử dụng VPC để truy cập tài nguyên riêng tư
4. **Environment Variables**: Lưu trữ secrets trong AWS Systems Manager Parameter Store hoặc Secrets Manager
5. **Build Triggers**: Cấu hình trigger phù hợp (PUSH, PR, Release) dựa trên workflow
6. **Compute Size**: Chọn tài nguyên compute phù hợp dựa trên độ phức tạp của build
7. **Logs**: Bật CloudWatch Logs để debug và giám sát

## Các Trường Hợp Sử Dụng

- **Continuous Integration**: Tự động build và test code mỗi lần commit
- **Continuous Testing**: Chạy test suite trên pull request
- **Tạo Package**: Biên dịch và đóng gói ứng dụng để triển khai
- **Build Đa Môi Trường**: Build cho các môi trường khác nhau (dev, staging, prod)

## Tích Hợp Với Các Dịch Vụ AWS

- **CodePipeline**: Điều phối workflow build, test và deployment
- **CodeCommit**: Sử dụng Git repository gốc của AWS
- **S3**: Lưu trữ artifacts và logs
- **CloudWatch**: Giám sát build và xem logs
- **IAM**: Quản lý quyền và kiểm soát truy cập

## Tóm Tắt

AWS CodeBuild loại bỏ nhu cầu quản lý các máy chủ build trong khi cung cấp giải pháp có khả năng mở rộng, bảo mật và tích hợp để build và test code. Bằng cách cấu hình đúng tích hợp nguồn, cài đặt môi trường và file buildspec, bạn có thể tạo ra workflow CI/CD tự động giúp cải thiện chất lượng code và tốc độ triển khai.
