# AWS Lambda Best Practices - Thực Hành Tốt Nhất

## Tổng Quan
Tài liệu này bao gồm các thực hành tốt nhất cho AWS Lambda, rất quan trọng cho kỳ thi chứng chỉ AWS.

## Các Thực Hành Tốt Nhất

### 1. Tối Ưu Hiệu Suất Function Handler
**Các công việc nặng nên được thực hiện bên ngoài function handler** để giảm thiểu thời gian thực thi.

Bao gồm:
- **Kết nối cơ sở dữ liệu** - Khởi tạo kết nối bên ngoài handler
- **Khởi tạo AWS SDK** - Thiết lập SDK clients bên ngoài handler
- **Dependencies và datasets** - Build và load các thành phần này bên ngoài handler

**Tại sao?** Lambda tái sử dụng môi trường thực thi, nên code bên ngoài handler chỉ chạy một lần trong cold start, cải thiện hiệu suất tổng thể.

### 2. Sử Dụng Environment Variables (Biến Môi Trường)
Environment variables nên được dùng cho các giá trị thay đổi theo thời gian:
- Chuỗi kết nối cơ sở dữ liệu
- Tên S3 bucket
- Các tham số cấu hình
- Bất kỳ giá trị động nào

**Quan trọng:** Không bao giờ hardcode các giá trị này trong code!

### 3. Bảo Mật Dữ Liệu Nhạy Cảm
Đối với mật khẩu và các giá trị nhạy cảm:
- Sử dụng environment variables
- **Mã hóa chúng bằng AWS KMS** để tăng cường bảo mật
- Không bao giờ lưu credentials dưới dạng plain text

### 4. Giảm Thiểu Kích Thước Deployment Package
Giữ deployment package nhỏ nhất có thể:
- Chỉ bao gồm những gì cần thiết cho runtime
- Chia nhỏ các functions lớn thành các functions nhỏ hơn
- Nhớ các giới hạn kích thước package của Lambda
- Sử dụng **Lambda Layers** để tái sử dụng các thư viện chung cho nhiều functions

### 5. Tránh Code Đệ Quy (Recursive Code)
**Không bao giờ để Lambda function tự gọi chính nó!**
- Có thể dẫn đến thực thi không kiểm soát được
- Gây ra chi phí rất cao
- Có thể nhanh chóng cạn kiệt giới hạn concurrency
- Được coi là tình huống thảm họa

## Tóm Tắt
Tuân theo các thực hành tốt nhất này sẽ giúp bạn:
- Cải thiện hiệu suất Lambda
- Giảm chi phí
- Tăng cường bảo mật
- Vượt qua kỳ thi chứng chỉ AWS

## Mẹo Cho Kỳ Thi
- Hiểu lý do đằng sau mỗi thực hành tốt nhất
- Biết khi nào sử dụng Lambda Layers
- Nhớ tầm quan trọng của mã hóa KMS cho dữ liệu nhạy cảm
- Biết về các giới hạn và ràng buộc của Lambda
