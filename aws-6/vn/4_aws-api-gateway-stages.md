# AWS API Gateway - Các Giai Đoạn Triển Khai và Biến Giai Đoạn

## Tổng Quan
Tài liệu này đề cập đến các giai đoạn triển khai (deployment stages) và biến giai đoạn (stage variables) của API Gateway, những khái niệm thiết yếu để quản lý các phiên bản khác nhau của API.

## Các Giai Đoạn Triển Khai (Deployment Stages)

### Khái Niệm Chính
- **Thay đổi chỉ có hiệu lực sau khi triển khai**: Khi bạn sửa đổi cấu hình API Gateway, bạn phải triển khai (deploy) các thay đổi để chúng có hiệu lực
- **Lỗi thường gặp**: Quên triển khai thay đổi sau khi cập nhật cấu hình
- **Nhiều giai đoạn**: Bạn có thể tạo bao nhiêu giai đoạn tùy thích với quy ước đặt tên tùy chỉnh
  - Ví dụ: `dev`, `test`, `prod`
  - Ví dụ: `v1`, `v2`, `v3`

### Tính Năng của Stage
- Mỗi giai đoạn có các tham số cấu hình riêng
- Khả năng rollback liền mạch
- Lịch sử triển khai hoàn chỉnh được duy trì
- Mỗi giai đoạn có một URL duy nhất

### Trường Hợp Sử Dụng: Quản Lý Thay Đổi API Phá Vỡ Tương Thích

**Tình Huống**: Bạn cần triển khai phiên bản Lambda mới phá vỡ tương thích với v1

**Giải Pháp**: Tạo các giai đoạn riêng biệt
```
v1 Stage → v1 Lambda Function → api.example.com/v1
v2 Stage → v2 Lambda Function → api.example.com/v2
```

**Lợi Ích**:
- v1 và v2 có thể tồn tại đồng thời
- Di chuyển client dần dần từ v1 sang v2
- Không có downtime trong quá trình chuyển đổi
- Tắt v1 khi không còn cần thiết

## Biến Giai Đoạn (Stage Variables)

### Định Nghĩa
Biến giai đoạn giống như biến môi trường (environment variables) nhưng dành riêng cho các giai đoạn của API Gateway.

### Mục Đích
- Thay đổi giá trị cấu hình mà không cần triển khai lại API
- Quản lý cấu hình động

### Trường Hợp Sử Dụng Phổ Biến
1. **Cấu hình Lambda function ARN**
2. **Cấu hình HTTP endpoint**
3. **Parameter mapping templates**
4. **Các endpoint theo môi trường** (dev, test, prod)
5. **Truyền cấu hình cho Lambda functions**
6. **Trỏ đến các phiên bản Lambda function khác nhau**

### Truy Cập Biến Giai Đoạn

**Trong API Gateway**: 
```
$stageVariables.variableName
```

**Trong Lambda Function**: Biến giai đoạn được truyền trong đối tượng context

## Mẫu Nâng Cao: Lambda Aliases với Stage Variables

### Ví Dụ Kiến Trúc

```
dev Stage → stageVariable: lambdaAlias=dev
  ↓
dev Alias → 100% lưu lượng đến Lambda phiên bản mới nhất

test Stage → stageVariable: lambdaAlias=test
  ↓
test Alias → 100% lưu lượng đến Lambda v2

prod Stage → stageVariable: lambdaAlias=prod
  ↓
prod Alias → 95% lưu lượng đến v1, 5% lưu lượng đến v2
```

### Lợi Ích
- Biến giai đoạn chỉ định Lambda alias nào cần gọi
- API Gateway tự động gọi đúng Lambda function
- Cập nhật tỷ lệ phần trăm Lambda alias mà không cần sửa API Gateway
- Cho phép canary deployments và triển khai dần dần
- Mỗi giai đoạn duy trì logic định tuyến riêng

## Thực Hành Tốt Nhất

1. ✅ **Luôn triển khai** sau khi thay đổi API Gateway
2. ✅ **Sử dụng tên giai đoạn có ý nghĩa** (dev, test, prod hoặc v1, v2, v3)
3. ✅ **Tận dụng biến giai đoạn** cho cấu hình theo môi trường
4. ✅ **Sử dụng Lambda aliases** với biến giai đoạn để quản lý phiên bản
5. ✅ **Giữ lịch sử triển khai** để dễ dàng rollback
6. ✅ **Test ở các giai đoạn thấp hơn** trước khi đưa lên production

## Lưu Ý Quan Trọng

⚠️ **Quan Trọng**: Các thay đổi đối với API Gateway KHÔNG có hiệu lực cho đến khi bạn triển khai chúng lên một giai đoạn

⚠️ **Mẫu Phổ Biến**: Sử dụng biến giai đoạn để trỏ đến Lambda aliases cho quản lý phiên bản linh hoạt mà không cần triển khai lại API Gateway

---

**Mẹo Học Tập**: Mẫu này (API Gateway Stages → Stage Variables → Lambda Aliases → Lambda Versions) rất phổ biến trong AWS và thường xuất hiện trong các kỳ thi chứng chỉ.
