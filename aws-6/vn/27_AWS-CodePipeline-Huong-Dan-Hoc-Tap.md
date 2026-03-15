# Hướng Dẫn Học Tập AWS CodePipeline

## Tổng Quan
Hướng dẫn này trình bày cách tạo một pipeline để triển khai code từ GitHub đến Elastic Beanstalk sử dụng AWS CodePipeline.

## Tạo Pipeline Tùy Chỉnh

### Bước 1: Cấu Hình Pipeline
1. **Tên Pipeline**: MyFirstPipeline
2. **Chế Độ Thực Thi**: Queued (cài đặt mặc định)
3. **Service Role**: Tạo service role mới
   - Role này cho phép CodePipeline thực hiện các thao tác cần thiết
   - Rất quan trọng cho chức năng của pipeline

### Bước 2: Artifact Store và Encryption
- Để nguyên cài đặt mặc định cho:
  - Artifact store
  - Encryption key
  - Không cần biến số (variables)

## Cấu Hình Source Provider

### Các Source Provider Có Sẵn
- **CodeCommit** (đã ngừng sử dụng)
- **Amazon ECR**
- **Amazon S3**
- **Bitbucket** (Git provider)
- **GitHub** (phiên bản 1 và phiên bản 2)
- **GitHub Enterprise Server**
- **GitLab** và **GitLab Self-Managed**

### Khuyến Nghị: GitHub Phiên Bản 2

#### Thiết Lập Kết Nối GitHub
1. Tạo kết nối có tên "MyGitHubConnection"
2. Click "Connect to GitHub"
3. Ủy quyền AWS connector cho GitHub
4. Cài đặt GitHub app:
   - Chọn repositories (có thể chọn tất cả repositories)
   - Nhập mã bảo mật nếu yêu cầu
   - Bạn sẽ nhận được GitHub app ID

5. Đợi cho đến khi trạng thái kết nối hiển thị "Available"

#### Cấu Hình Repository
- **Tên Repository**: Chọn ứng dụng Node.js của bạn (hoặc ứng dụng của bạn)
- **Branch Mặc Định**: main
- **Output Artifact Format**: CodePipeline default

### Triggers Pipeline
Cấu hình trigger để khởi động pipeline:
- **Loại Trigger**: Push to branch
- **Tên Branch**: main
- Pipeline tự động khởi động khi code được push lên branch main

## Build Provider

Các tùy chọn có sẵn:
- **CodeBuild**
- **Jenkins**

*Lưu ý: Có thể bỏ qua ban đầu và thêm vào sau*

## Giai Đoạn Deploy

### Deploy Provider: AWS Elastic Beanstalk

Cấu hình:
1. **Tên Application**: Chọn application đã tạo của bạn
2. **Environment**: Chọn environment của bạn (ví dụ: "env")

Pipeline sẽ gửi code từ GitHub trực tiếp đến ứng dụng Elastic Beanstalk của bạn.

## Quan Trọng: Quyền Service Role

### Thêm Quyền Beanstalk
1. Vào **Settings** cho pipeline của bạn
2. Click vào **Service Role**
3. Bạn sẽ thấy hai policies đã được đính kèm
4. Thêm quyền còn thiếu cho Beanstalk:
   - Click **Attach Policy**
   - Tìm kiếm "Beanstalk"
   - Thêm **AdministratorAccess-AWSElasticBeanstalk**
   - *(Lưu ý: Chỉ cho mục đích demo; sử dụng policies hạn chế hơn trong môi trường production)*

## Điểm Chính Cần Nhớ
- CodePipeline tự động hóa triển khai từ nguồn đến production
- Khuyến nghị sử dụng tích hợp GitHub Version 2
- Quyền service role phù hợp là rất quan trọng
- Pipeline có thể tùy chỉnh với các giai đoạn build và deploy
- Hỗ trợ nhiều source providers và deployment targets

## Thực Hành Tốt Nhất
- Sử dụng triggers branch cụ thể để kiểm soát khi nào triển khai xảy ra
- Xem xét và điều chỉnh quyền service role cho môi trường production
- Test pipeline với môi trường non-production trước
- Giám sát việc thực thi pipeline để phát hiện lỗi hoặc vấn đề
