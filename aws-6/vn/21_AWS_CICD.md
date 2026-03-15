# AWS CI/CD - Tích hợp Liên tục và Phân phối Liên tục

## Tổng quan

CI/CD (Continuous Integration/Continuous Delivery - Tích hợp Liên tục/Phân phối Liên tục) là một khái niệm quan trọng trong phát triển AWS, giúp tự động hóa quy trình triển khai, kiểm thử và phân phối mã nguồn. Phương pháp này giúp các lập trình viên làm việc hiệu quả hơn và giảm thiểu lỗi thủ công.

## Tại sao CI/CD quan trọng

- **Tự động hóa**: Loại bỏ các bước triển khai thủ công
- **An toàn**: Đảm bảo mã được kiểm thử trước khi triển khai
- **Tốc độ**: Chu kỳ phân phối nhanh hơn
- **Độ tin cậy**: Quy trình triển khai nhất quán giữa các môi trường
- **Phát hiện lỗi sớm**: Các vấn đề được tìm thấy và khắc phục nhanh chóng

## Các dịch vụ AWS CI/CD

### 1. **CodeCommit**
- Dịch vụ lưu trữ mã nguồn của AWS
- Tương tự như GitHub hoặc Bitbucket
- Lưu trữ và quản lý mã nguồn một cách bảo mật

### 2. **CodePipeline**
- Tự động hóa toàn bộ pipeline triển khai
- Điều phối luồng từ mã nguồn đến sản xuất
- Kết nối các giai đoạn khác nhau của quy trình triển khai

### 3. **CodeBuild**
- Xây dựng và kiểm thử mã tự động
- Chạy kiểm thử ngay khi mã được đẩy lên
- Cung cấp phản hồi về kết quả build thành công hay thất bại

### 4. **CodeDeploy**
- Triển khai ứng dụng lên các EC2 instances
- Tự động hóa việc triển khai lên các tài nguyên AWS khác nhau
- Có thể triển khai mà không cần sử dụng Elastic Beanstalk

### 5. **CodeStar**
- Giao diện thống nhất để quản lý phát triển phần mềm
- Tích hợp CodeCommit, CodePipeline, CodeBuild và CodeDeploy
- Nơi duy nhất để quản lý toàn bộ quy trình làm việc

### 6. **CodeArtifact**
- Lưu trữ, xuất bản và chia sẻ các gói phần mềm
- Giải pháp quản lý phụ thuộc
- Hoạt động với các trình quản lý gói phổ biến

### 7. **CodeGuru**
- Đánh giá mã tự động bằng machine learning
- Xác định các vấn đề quan trọng và cơ hội tối ưu hóa
- Cung cấp các đề xuất thông minh

## Tích hợp Liên tục (CI)

### Cách hoạt động:

1. **Lập trình viên đẩy mã** thường xuyên lên repository trung tâm (CodeCommit, GitHub, hoặc Bitbucket)
2. **Build server** (CodeBuild hoặc Jenkins) tự động tải và kiểm thử mã
3. **Lập trình viên nhận phản hồi** về kết quả kiểm thử ngay lập tức

### Lợi ích:

- ✅ Phát hiện lỗi sớm và sửa chữa nhanh chóng
- ✅ Không cần kiểm thử mã thủ công trên máy cá nhân
- ✅ Phân phối mã nhanh hơn
- ✅ Khả năng triển khai thường xuyên
- ✅ Chu kỳ phát triển lành mạnh hơn
- ✅ Lập trình viên hạnh phúc hơn

## Phân phối Liên tục (CD)

### Luồng triển khai:

```
Lập trình viên → Repository mã nguồn → Build/Test Server → Deployment Server → Application Servers
```

### Quy trình:

1. Lập trình viên đẩy mã lên repository
2. Build server kiểm thử mã (giai đoạn CI)
3. Nếu kiểm thử thành công (build xanh), deployment server kích hoạt
4. Ứng dụng được tự động triển khai lên các server đích

## Các môi trường triển khai

Pipeline CI/CD thường hỗ trợ nhiều giai đoạn:

- **Development**: Cho phát triển và kiểm thử tích cực
- **Test**: Cho kiểm thử tích hợp
- **Staging (Pre-prod)**: Môi trường giống production để xác thực cuối cùng
- **Production**: Môi trường trực tiếp phục vụ người dùng cuối

### Phê duyệt thủ công

Đối với triển khai production, có thể thêm các cổng phê duyệt thủ công để đảm bảo giám sát của con người trước khi phát hành quan trọng.

## Những điểm chính cần nhớ

- CI/CD tự động hóa toàn bộ quy trình phân phối phần mềm
- Giảm lỗi thủ công và tăng độ tin cậy khi triển khai
- Thiết yếu cho phát triển ứng dụng dựa trên cloud hiện đại
- AWS cung cấp một bộ công cụ hoàn chỉnh để triển khai CI/CD
- Chủ đề quan trọng cho các kỳ thi chứng chỉ AWS

## Thực hành tốt nhất

1. Đẩy mã thường xuyên để duy trì các thay đổi nhỏ, dễ quản lý
2. Tự động hóa kiểm thử ở mọi giai đoạn
3. Sử dụng nhiều môi trường để xác thực các thay đổi
4. Triển khai giám sát và ghi log phù hợp
5. Thêm cổng phê duyệt thủ công cho triển khai production
6. Duy trì quy trình triển khai nhất quán
