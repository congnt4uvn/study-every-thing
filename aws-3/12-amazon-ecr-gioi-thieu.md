# Giới Thiệu Amazon ECR

## Tổng Quan

Amazon ECR (Elastic Container Registry) là dịch vụ được sử dụng để lưu trữ và quản lý Docker images trên AWS. Trong khi bạn có thể sử dụng các kho lưu trữ trực tuyến như Docker Hub, Amazon ECR cho phép bạn lưu trữ images của riêng mình trực tiếp trên hạ tầng AWS.

## Các Tùy Chọn Repository của ECR

Amazon ECR cung cấp hai loại repository:

- **Private Repository**: Lưu trữ images riêng tư cho tài khoản hoặc tổ chức của bạn
- **Public Repository**: Công khai images lên Amazon ECR public gallery để mọi người có thể truy cập

## Tích Hợp với Amazon ECS

Amazon ECR được tích hợp hoàn toàn với Amazon ECS (Elastic Container Service). Các điểm chính về tích hợp này:

- ECR repository có thể chứa nhiều Docker images khác nhau
- ECS cluster của bạn (ví dụ: các EC2 instances) có thể pull các images này
- Images được lưu trữ phía sau bởi Amazon S3
- IAM roles phải được gán cho các EC2 instances để cho phép chúng pull Docker images
- Tất cả quyền truy cập vào ECR đều được bảo vệ bởi IAM

### Cách Hoạt Động

1. Docker images được lưu trữ trong ECR repository của bạn
2. Các EC2 instances trong ECS cluster cần pull các images này
3. Một IAM role được gán cho EC2 instance với các quyền phù hợp
4. EC2 instance pull Docker images từ ECR
5. Containers được khởi động trên EC2 instance

> **Lưu ý**: Nếu bạn gặp lỗi về quyền truy cập với ECR, hãy kiểm tra IAM policies của bạn trước tiên.

## Các Tính Năng Chính

Amazon ECR cung cấp một số tính năng quan trọng:

- **Image Vulnerability Scanning**: Tự động quét images để tìm các lỗ hổng bảo mật
- **Versioning**: Duy trì các phiên bản khác nhau của images
- **Image Tags**: Tổ chức và nhận diện images bằng cách sử dụng tags
- **Image Lifecycle**: Quản lý chính sách vòng đời của image để tự động hóa việc dọn dẹp và lưu giữ

## Mẹo Cho Kỳ Thi

Đối với các kỳ thi chứng chỉ AWS, hãy nhớ quy tắc đơn giản này:

> **Mỗi khi bạn thấy "storing Docker images" → nghĩ ngay đến ECR**

Đây là khái niệm chính cần nhớ khi gặp các câu hỏi liên quan đến ECR trong kỳ thi.