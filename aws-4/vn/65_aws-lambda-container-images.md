# AWS Lambda Container Images

## Tổng Quan

AWS Lambda hiện đã hỗ trợ **container images** như một phương thức triển khai, cho phép bạn deploy Lambda Functions dưới dạng container images với dung lượng lên đến **10 GB** từ Amazon ECR (Elastic Container Registry).

## Tính Năng Chính

### Hỗ Trợ Container Image
- Deploy Lambda Functions dưới dạng container images
- Kích thước tối đa: 10 GB từ ECR
- Đóng gói các dependencies phức tạp và lớn trong containers
- Quy trình thống nhất cho việc triển khai container

### Tích Hợp Docker
Docker cho phép bạn đóng gói cùng nhau:
- Mã nguồn ứng dụng
- Các dependencies
- Bộ dữ liệu cần thiết
- Base image (phải implement Lambda Runtime API)

## Yêu Cầu Lambda Runtime API

**Quan trọng**: Base image **phải implement Lambda Runtime API** để Lambda có thể chạy container.

### Base Images Được Hỗ Trợ

AWS cung cấp base images cho nhiều ngôn ngữ:
- Python
- Node.js
- Java
- .NET
- Go
- Ruby

### Custom Base Images
Bạn có thể tạo Lambda base image của riêng mình, nhưng phải implement Lambda Runtime API. Tham khảo tài liệu AWS để biết chi tiết kỹ thuật.

## Kiểm Thử

Sử dụng **Lambda Runtime Interface Emulator** để kiểm thử containers locally trước khi triển khai.

## Quy Trình Thống Nhất

Container images cho Lambda cho phép quy trình thống nhất để publish ứng dụng:
- Build containers theo cùng một cách cho ECS hoặc Lambda
- Publish containers lên Amazon ECR
- Deploy từ ECR sang Lambda

## Ví Dụ: Lambda Container Image

```dockerfile
# Chọn base image implement Lambda Runtime API
FROM amazon/aws-lambda-nodejs:12

# Copy mã nguồn và files
COPY app.js package.json ./

# Cài đặt dependencies
RUN npm install

# Chỉ định function nào sẽ chạy
CMD ["app.handler"]
```

## Các Bước Thực Hiện

1. **Chọn Base Image**: Chọn image implement Lambda Runtime API
2. **Copy Code**: Thêm mã nguồn và các files cấu hình
3. **Cài Đặt Dependencies**: Chạy các lệnh cài đặt cần thiết (ví dụ: npm install)
4. **Định Nghĩa Handler**: Chỉ định function sẽ thực thi
5. **Build & Push**: Build image và push lên Amazon ECR
6. **Deploy**: Deploy từ ECR sang Lambda

## Lợi Ích

- ✅ Hỗ trợ dependencies phức tạp
- ✅ Gói dependencies lớn (lên đến 10 GB)
- ✅ Quy trình triển khai nhất quán giữa các services
- ✅ Khả năng kiểm thử local
- ✅ Sử dụng các công cụ Docker quen thuộc

## Ghi Chú

- Không phải bất kỳ Docker container nào cũng hoạt động được
- Base image phải implement Lambda Runtime API
- Containers chạy trong Lambda virtual machines
- Yêu cầu tích hợp ECR để triển khai
