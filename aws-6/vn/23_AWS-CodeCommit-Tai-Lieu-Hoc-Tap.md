# Tài Liệu Học Tập AWS CodeCommit

## Tổng Quan
AWS CodeCommit là dịch vụ kiểm soát mã nguồn được quản lý hoàn toàn, lưu trữ các repository Git an toàn. Đây là một phần của bộ công cụ AWS Developer Tools, bao gồm CodeBuild, CodeDeploy và CodePipeline.

## Các Khái Niệm Chính

### CodeCommit là gì?
- Dịch vụ kiểm soát mã nguồn được quản lý hoàn toàn
- Repository dựa trên Git
- Tích hợp với các dịch vụ AWS DevOps khác
- An toàn và có khả năng mở rộng

## Bắt Đầu Với CodeCommit

### Tạo Repository
1. Mở console CodeCommit
2. Điều hướng đến menu bên trái để truy cập:
   - CodeCommit
   - CodeBuild
   - CodeDeploy
   - CodePipeline
3. Nhấp "Create repository" (Tạo repository)
4. Nhập tên repository (ví dụ: `my-nodejs-app`)
5. Thêm mô tả và tags (tùy chọn)
6. Nhấp "Create" (Tạo)

### Phương Thức Kết Nối
CodeCommit hỗ trợ ba phương thức kết nối:
- **HTTPS** - Xác thực dựa trên HTTP tiêu chuẩn
- **SSH** - Xác thực Secure Shell
- **HTTPS GRC** - Git Remote CodeCommit

**Lưu Ý Quan Trọng**: Tùy chọn SSH chỉ khả dụng khi sử dụng IAM Users. Nếu kết nối với tài khoản root, SSH sẽ không xuất hiện.

## Làm Việc Với Files

### Tải Files Lên
1. Điều hướng đến repository
2. Nhấp "Add file" → "Upload file"
3. Chọn file để tải lên (một file tại một thời điểm)
4. Nhập chi tiết commit:
   - Tên tác giả
   - Địa chỉ email
   - Thông điệp commit
5. Nhấp "Commit changes" (Commit thay đổi)

### Ví Dụ Tải Lên
- File: `index.html`
- Tác giả: Stephane
- Email: stephane@example.com
- Thông điệp commit: "first commit"

## Tính Năng Repository

### Xem Code
- Duyệt các files trong repository
- Xem nội dung file
- Tạo và tải lên files
- Xem lịch sử commit

### Branches (Nhánh)
- **Master Branch**: Nhánh mặc định được tạo tự động
- **Nhiều Branches**: Hỗ trợ phát triển cộng tác
- **Tạo Branch**: Có thể tạo thêm các nhánh (dev, test, v.v.)
- **Branch From**: Chỉ định nhánh nguồn cho các nhánh mới

### Pull Requests (Yêu Cầu Kéo)
- Cho phép developers merge thay đổi từ các nhánh khác nhau
- Merge vào master hoặc các nhánh đích khác
- Cần thiết cho kiến thức kỳ thi DevOps
- Cho phép xem xét code và cộng tác

### Commits
- **Xem Commits**: Xem tất cả các commits của repository
- **Commit Visualizer**: Biểu diễn trực quan lịch sử commit
- **So Sánh Commits**: So sánh thay đổi giữa các nhánh hoặc commits
- **Duyệt Repository**: Xem trạng thái repository tại commit cụ thể

### Git Tags
- Được sử dụng để đánh dấu các điểm cụ thể trong lịch sử repository
- Thường được sử dụng cho các phiên bản phát hành

### Settings (Cài Đặt)
Thông tin repository bao gồm:
- Tên repository
- ID repository
- ARN (Amazon Resource Name)
- Mô tả

## Thực Hành Tốt Nhất
1. Sử dụng IAM Users thay vì tài khoản root
2. Cung cấp thông điệp commit có ý nghĩa
3. Sử dụng branches cho công việc phát triển
4. Sử dụng pull requests để xem xét code
5. Gắn tags cho các bản phát hành một cách phù hợp

## Tích Hợp Với Các Dịch Vụ Khác
CodeCommit tích hợp liền mạch với:
- **AWS CodeBuild**: Dịch vụ build tự động
- **AWS CodeDeploy**: Dịch vụ triển khai tự động
- **AWS CodePipeline**: Tích hợp và phân phối liên tục
- **AWS Elastic Beanstalk**: Triển khai ứng dụng

## Mẹo Thi Cử
- Hiểu sự khác biệt giữa xác thực HTTPS và SSH
- Biết khi nào SSH khả dụng (chỉ với IAM Users)
- Hiểu pull requests trong bối cảnh DevOps
- Quen thuộc với các chiến lược branching
- Biết cách CodeCommit tích hợp với các dịch vụ AWS khác

## Tóm Tắt
AWS CodeCommit cung cấp dịch vụ lưu trữ repository dựa trên Git an toàn, có khả năng mở rộng, tích hợp với các công cụ AWS DevOps. Nó hỗ trợ các thao tác Git tiêu chuẩn, nhiều phương thức xác thực và các tính năng phát triển cộng tác như branches và pull requests.
