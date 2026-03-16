# Tích Hợp AWS SAM và CodeDeploy

## Tổng Quan

Tài liệu này trình bày cách AWS CodeDeploy tích hợp với Serverless Application Model (SAM) framework để triển khai và cập nhật Lambda functions một cách an toàn sử dụng tính năng chuyển đổi lưu lượng.

## Các Khái Niệm Chính

### CodeDeploy với SAM Framework

SAM sử dụng CodeDeploy để cập nhật Lambda functions, tận dụng:
- **Chuyển đổi lưu lượng** (Traffic shifting) với Lambda aliases
- **Pre và post-traffic hooks** sử dụng Lambda functions để xác thực triển khai
- **Tự động rollback** được kích hoạt bởi CloudWatch alarms

### Quy Trình Triển Khai

1. **Trạng thái ban đầu**: Lambda alias trỏ đến phiên bản v1 của function
2. **Kích hoạt triển khai**: Thông qua CI/CD pipeline hoặc SAM framework
3. **Pre-Traffic Hook** (Tùy chọn): Lambda function chạy các test trước khi chuyển đổi lưu lượng
4. **Chuyển đổi lưu lượng**: Chuyển dần lưu lượng từ v1 sang v2 theo chiến lược
5. **Giám sát** (Tùy chọn): CloudWatch alarms giám sát tình trạng triển khai
6. **Post-Traffic Hook** (Tùy chọn): Lambda function chạy các test sau khi chuyển đổi lưu lượng
7. **Hoàn thành**: Alias trỏ hoàn toàn đến v2, v1 được loại bỏ

## Cấu Hình SAM

### Các Thành Phần YAML Chính

#### AutoPublishAlias

```yaml
AutoPublishAlias: live
```

- Giúp SAM phát hiện khi code mới được triển khai
- Tạo một phiên bản Lambda mới với code mới nhất
- Tự động cập nhật alias để trỏ đến phiên bản mới

#### DeploymentPreference

Kiểm soát chiến lược triển khai và giám sát:

```yaml
DeploymentPreference:
  Type: Canary10Percent10Minutes
  Alarms:
    - MyCloudWatchAlarm
  Hooks:
    PreTraffic: !Ref PreTrafficHookFunction
    PostTraffic: !Ref PostTrafficHookFunction
```

### Các Loại Triển Khai

1. **Canary**: Chuyển một phần trăm lưu lượng, sau đó chờ trước khi chuyển phần còn lại
   - Ví dụ: `Canary10Percent10Minutes` - 10% lưu lượng trong 10 phút, sau đó 100%

2. **Linear**: Tăng dần lưu lượng theo khoảng thời gian đều đặn
   - Ví dụ: `Linear10PercentEvery10Minutes` - tăng 10% mỗi 10 phút

3. **AllAtOnce**: Chuyển ngay lập tức toàn bộ lưu lượng sang phiên bản mới

### Các Thành Phần

#### Alarms (Cảnh Báo)
- Danh sách các CloudWatch alarms để giám sát trong quá trình triển khai
- Có thể kích hoạt rollback tự động nếu vượt ngưỡng
- Ví dụ: Giám sát tỷ lệ lỗi trên phiên bản mới

#### Hooks
- **PreTraffic**: Lambda function thực thi trước khi bắt đầu chuyển đổi lưu lượng
- **PostTraffic**: Lambda function thực thi sau khi hoàn thành chuyển đổi lưu lượng
- Được sử dụng cho xác thực và kiểm thử tùy chỉnh

## Triển Khai Thực Tế

### Các Bước Thiết Lập

1. Tạo thư mục SAM application:
   ```bash
   mkdir sam-codedeploy
   cd sam-codedeploy
   ```

2. Khởi tạo SAM application:
   ```bash
   sam init
   ```
   - Chọn Python runtime (ví dụ: Python 3.7)
   - Chọn template "Hello World Example"
   - Đặt tên project (ví dụ: sam-app)

3. Build SAM application:
   ```bash
   cd sam-app
   sam build
   ```

4. Cấu hình CodeDeploy trong `template.yaml`:
   - Thêm thuộc tính `AutoPublishAlias`
   - Cấu hình các thiết lập `DeploymentPreference`
   - Định nghĩa alarms và hooks nếu cần

### Cấu Trúc Template

SAM template bao gồm:
- Định nghĩa resource `Serverless::Function`
- Function handler (ví dụ: `app.py` trả về "hello world")
- Outputs cho function ARN và API endpoints
- Cấu hình CodeDeploy được tích hợp vào định nghĩa function

## Thực Hành Tốt Nhất

- **Sử dụng Alarms**: Luôn cấu hình CloudWatch alarms để giám sát tình trạng triển khai
- **Test Hooks**: Triển khai pre và post-traffic hooks cho các ứng dụng quan trọng
- **Chọn chiến lược phù hợp**: Lựa chọn loại triển khai dựa trên mức độ rủi ro có thể chấp nhận
- **Giám sát Metrics**: Theo dõi lỗi, độ trễ và throttling trong quá trình triển khai
- **Lên kế hoạch Rollback**: Đảm bảo cơ chế rollback được kiểm thử và hoạt động

## Lợi Ích

- **Triển khai an toàn**: Chuyển đổi lưu lượng dần dần giảm rủi ro
- **Tự động kiểm thử**: Hooks cho phép xác thực tự động
- **Rollback nhanh chóng**: Tự động rollback khi alarm được kích hoạt
- **Kiểm soát phiên bản**: Duy trì nhiều phiên bản Lambda trong quá trình chuyển đổi
- **Tích hợp giám sát**: CloudWatch alarms cung cấp khả năng hiển thị triển khai

## Tóm Tắt

Tích hợp SAM và CodeDeploy cung cấp một framework mạnh mẽ để triển khai cập nhật Lambda function một cách an toàn với quản lý lưu lượng tích hợp, testing hooks, và khả năng rollback tự động. Cách tiếp cận này giảm thiểu rủi ro triển khai và đảm bảo tính ổn định của ứng dụng trong quá trình cập nhật.
