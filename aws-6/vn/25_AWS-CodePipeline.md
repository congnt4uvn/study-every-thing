# AWS CodePipeline - Tài Liệu Học Tập

## Tổng Quan
CodePipeline là công cụ quy trình làm việc trực quan giúp điều phối CI/CD (Tích hợp Liên tục/Triển khai Liên tục) trong AWS.

## Các Giai Đoạn Pipeline

### 1. Giai Đoạn Source (Nguồn)
CodePipeline có thể tích hợp với nhiều kho lưu trữ mã nguồn:
- **Dịch vụ AWS:**
  - CodeCommit (kho Git được quản lý bởi AWS)
  - Amazon ECR (Docker images)
  - Amazon S3 (mã nguồn được lưu trong S3 buckets)
- **Công Cụ Bên Ngoài:**
  - Bitbucket
  - GitHub

### 2. Giai Đoạn Build (Xây Dựng)
Sau khi lấy mã nguồn, giai đoạn build có thể sử dụng:
- CodeBuild (dịch vụ gốc của AWS)
- Jenkins
- CloudBees
- TeamCity

### 3. Giai Đoạn Test (Kiểm Thử)
Sau khi xây dựng, bạn có thể kiểm thử mã nguồn bằng:
- CodeBuild (cho các bài test chung)
- AWS Device Farm (cho ứng dụng iOS và Android)
- Các công cụ kiểm thử của bên thứ ba

### 4. Giai Đoạn Deploy (Triển Khai)
Các tùy chọn triển khai cuối cùng bao gồm:
- CodeDeploy
- Elastic Beanstalk
- CloudFormation
- Amazon ECS
- Amazon S3
- Lambda functions
- Step Functions

## Cấu Trúc Pipeline

### Các Hành Động Tuần Tự và Song Song
- Mỗi giai đoạn có thể chứa **các hành động tuần tự** (thực thi lần lượt)
- Mỗi giai đoạn cũng có thể có **các hành động song song** (thực thi đồng thời)

### Ví Dụ Luồng Pipeline
```
Source → Build → Test → Deploy to Staging → Load Testing → Deploy to Production
```

### Phê Duyệt Thủ Công
- Bạn có thể định nghĩa **các bước phê duyệt thủ công** ở bất kỳ giai đoạn nào
- Trường hợp sử dụng phổ biến: Yêu cầu kiểm tra của con người trước khi triển khai lên production
- Ví dụ: Xem xét kết quả load testing trước khi triển khai production

## Cách CodePipeline Hoạt Động Bên Trong

### Quản Lý Artifact
1. **Artifacts** là các đầu ra được tạo bởi mỗi giai đoạn pipeline
2. Tất cả artifacts được lưu trữ trong **Amazon S3 buckets**
3. Artifacts được truyền từ giai đoạn này sang giai đoạn khác thông qua S3

### Ví Dụ Quy Trình Làm Việc
```
Developer → Push code lên CodeCommit
         ↓
CodePipeline trích xuất code → Tạo artifact → Lưu vào S3
         ↓
CodeBuild nhận artifact từ S3 → Build code → Tạo deployment artifact
         ↓
Artifact được lưu vào S3 → Truyền tới CodeDeploy
         ↓
CodeDeploy triển khai artifact
```

**Điểm Quan Trọng:** Các giai đoạn tương tác với nhau thông qua Amazon S3, không trực tiếp. CodePipeline điều phối luồng dữ liệu giữa các giai đoạn.

## Khắc Phục Sự Cố

### Giám Sát với CloudWatch Events / EventBridge
Bạn có thể giám sát việc thực thi pipeline bằng CloudWatch Events để theo dõi:
- Thay đổi trạng thái hành động pipeline
- Thay đổi trạng thái thực thi giai đoạn
- Pipelines thất bại
- Các giai đoạn bị hủy

**Các Hành Động Phổ Biến:**
- Tạo các quy tắc sự kiện cho pipelines thất bại
- Thiết lập thông báo email cho các lỗi pipeline

### Khả Năng Hiển Thị trên Console
- Các lỗi pipeline được hiển thị trực quan trong AWS Console
- Bạn có thể xem thông tin chi tiết về lỗi của từng giai đoạn
- Mỗi giai đoạn thất bại hiển thị thông tin lỗi

### Quyền IAM
Nếu CodePipeline không thể thực hiện các hành động cụ thể (ví dụ: gọi CodeBuild, lấy code từ CodeCommit), hãy kiểm tra:
- **IAM service role** được gắn với CodePipeline
- Xác minh rằng role có các quyền phù hợp cho tất cả các dịch vụ tích hợp

## Điểm Chính Cần Nhớ
✓ CodePipeline điều phối toàn bộ quy trình CI/CD
✓ Rất linh hoạt với nhiều tùy chọn tích hợp
✓ Sử dụng S3 làm cơ chế lưu trữ artifact trung tâm
✓ Hỗ trợ cả quy trình phê duyệt tự động và thủ công
✓ Cung cấp khả năng giám sát và khắc phục sự cố toàn diện
