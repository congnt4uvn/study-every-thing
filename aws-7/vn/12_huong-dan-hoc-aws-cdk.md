# Tài Liệu Học AWS CDK

## AWS CDK Là Gì?
AWS CDK (Cloud Development Kit) cho phép bạn định nghĩa hạ tầng cloud bằng ngôn ngữ lập trình, sau đó chuyển thành template AWS CloudFormation.

## Các Lệnh CDK Quan Trọng

### 1. Cài CDK CLI và thư viện
Cần cài AWS CDK CLI và thư viện theo ngôn ngữ bạn dùng để bắt đầu viết CDK stack.

### 2. `cdk init`
Khởi tạo ứng dụng CDK từ một template có sẵn.
Bạn có thể chọn Python, JavaScript, v.v.

### 3. `cdk synth`
Tổng hợp mã CDK và in ra template CloudFormation.
Đây là bước chuyển từ code hạ tầng sang CloudFormation.

### 4. `cdk bootstrap`
Chuẩn bị môi trường AWS trước khi deploy bằng cách tạo các tài nguyên cần thiết.
(Chi tiết ở phần bên dưới.)

### 5. `cdk deploy`
Triển khai stack đã tổng hợp lên AWS thông qua CloudFormation.

### 6. `cdk diff`
So sánh khác biệt giữa mã CDK local và stack đang deploy trên CloudFormation.
Rất hữu ích để kiểm tra thay đổi trước khi deploy.

### 7. `cdk destroy`
Xóa các CDK stack đã triển khai cùng tài nguyên liên quan.

## Giải Thích `cdk bootstrap`
Bootstrapping là quá trình cấp phát tài nguyên tiền đề cho CDK trước khi bạn deploy ứng dụng vào môi trường AWS.

Trong CDK, một **môi trường** là tổ hợp của:
- AWS account
- AWS region

Vì vậy, mỗi cặp account+region mới đều cần bootstrap.

Lệnh sử dụng:

```bash
cdk bootstrap aws://<aws_account>/<aws_region>
```

Lệnh này sẽ tạo CloudFormation stack tên **CDKToolkit** với các thành phần cần thiết như:
- Một S3 bucket
- Một IAM role

Đây là các điều kiện bắt buộc để deploy CDK stack trong môi trường đó.

## Nếu Không Bootstrap Thì Sao?
Nếu môi trường chưa bootstrap, lệnh deploy có thể lỗi, thường liên quan đến IAM principal hoặc policy không hợp lệ.

## Lộ Trình Học Đề Xuất
1. Cài công cụ CDK.
2. Tạo app bằng `cdk init`.
3. Chạy `cdk synth` để xem template sinh ra.
4. Chạy `cdk bootstrap` cho account/region mục tiêu.
5. Deploy bằng `cdk deploy`.
6. Dùng `cdk diff` để kiểm tra thay đổi ở các lần cập nhật sau.
7. Dọn tài nguyên bằng `cdk destroy` khi không cần nữa.

## Tóm Tắt Nhanh
- Code CDK -> `cdk synth` -> CloudFormation template
- Chuẩn bị môi trường -> `cdk bootstrap`
- Triển khai -> `cdk deploy`
- So sánh thay đổi -> `cdk diff`
- Dọn dẹp -> `cdk destroy`
