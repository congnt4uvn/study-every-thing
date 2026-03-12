# Hướng Dẫn Thực Hành AWS CloudFormation

## Giới Thiệu

Hướng dẫn này cung cấp bài thực hành chi tiết về AWS CloudFormation. Bạn sẽ học cách tạo CloudFormation stack đầu tiên và triển khai EC2 instance sử dụng Infrastructure as Code (IaC).

## Yêu Cầu Trước Khi Bắt Đầu

### Chọn Region
**Quan trọng:** Trước khi bắt đầu, hãy đảm bảo bạn chọn region **US East (Northern Virginia) - us-east-1**.

**Tại sao phải dùng us-east-1?**
- Tất cả các template đã được thiết kế đặc biệt cho region này
- AMI ID là duy nhất cho từng region
- Điều này đảm bảo tính nhất quán cho mục đích học tập

## Bắt Đầu Với CloudFormation

### Hiểu Về Dịch Vụ CloudFormation

CloudFormation là dịch vụ AWS cho phép bạn cung cấp và quản lý hạ tầng dưới dạng code. Khi bạn truy cập dịch vụ lần đầu:

- Ban đầu bạn có thể thấy không có stack nào
- Nếu bạn đã sử dụng Elastic Beanstalk hoặc các dịch vụ tương tự, bạn có thể đã có một số stack
- Số lượng stack hiện có không ảnh hưởng đến hướng dẫn này

## Khám Phá CloudFormation Với Sample Templates

### Tạo Stack Đầu Tiên

1. Điều hướng đến dịch vụ CloudFormation
2. Nhấp **Create Stack**
3. Bạn sẽ thấy một số tùy chọn:
   - Chọn template có sẵn
   - Sử dụng sample template
   - Xây dựng trực tiếp từ Application Composer

### Sử Dụng Application Composer

Trong hướng dẫn này, chúng ta sẽ sử dụng sample template để hiểu cấu trúc CloudFormation:

1. Chọn **Sample template**
2. Chọn **Multi_AZ_Simple WordPress blog** từ danh sách
3. Thay vì khởi chạy, hãy nhấp để **Xem trong Application Composer**

### Hiểu Về Cấu Trúc Template

#### Biểu Diễn Trực Quan

Application Composer cung cấp hai chế độ xem cho hạ tầng của bạn:

1. **Canvas View** - Biểu diễn trực quan hiển thị:
   - WebServerSecurityGroup
   - LaunchConfig
   - WebServerGroup
   - Database instance
   - Database security group
   - Và nhiều thành phần khác

2. **Code View** - Code template thực tế

#### Tùy Chọn Định Dạng Template

CloudFormation hỗ trợ hai định dạng:

- **YAML** (Được khuyến nghị vì dễ đọc)
- **JSON**

File template chứa tất cả cấu hình cần thiết để tạo các tài nguyên AWS của bạn. Ngay cả khi ban đầu bạn không hiểu tất cả, bạn sẽ học cách đọc và viết các template này khi tiến triển.

### Cách Template Hoạt Động

- Code tương ứng trực tiếp với các tài nguyên AWS
- Mỗi thành phần trong Canvas trực quan ánh xạ tới code trong template
- Nhấp vào các thành phần sẽ hiển thị cấu hình tài nguyên của chúng từ CloudFormation template

## Tạo EC2 Instance Đầu Tiên Với CloudFormation

### Hiểu Về File Template

Hãy xem xét một CloudFormation template đơn giản (`0-just-ec2.yaml`):

```yaml
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      AvailabilityZone: us-east-1a
      ImageId: ami-xxxxxxxxx
      InstanceType: t2.micro
```

#### Các Thành Phần Template

1. **Resources** (Phần bắt buộc)
   - Đây là phần bắt buộc trong mọi CloudFormation template
   - Chứa tất cả các tài nguyên cần được tạo

2. **Tên Resource**: `MyInstance`
   - Tên logic cho CloudFormation resource của bạn

3. **Type**: `AWS::EC2::Instance`
   - Chỉ định loại tài nguyên AWS

4. **Properties**:
   - `AvailabilityZone`: us-east-1a
   - `ImageId`: AMI ID cần sử dụng
   - `InstanceType`: t2.micro

**Điểm Quan Trọng:** Mọi thứ được định nghĩa trong code, không qua console!

### Triển Khai Template

#### Các Bước Triển Khai

1. Trong CloudFormation, nhấp **Create Stack**
2. Chọn **Upload a template file**
3. Chọn `0-just-ec2.yaml`
4. Đặt tên stack của bạn: `EC2InstanceDemo`
5. Nhấp **Next**

#### Tùy Chọn Cấu Hình (Bỏ Qua Bây Giờ)

Ở giai đoạn này, bạn có thể bỏ qua:
- Tags
- Permissions
- Advanced settings

Những phần này sẽ được đề cập trong các bài giảng sau.

#### Quy Trình Upload Template

- Khi bạn upload template, AWS tự động lưu trữ nó trong Amazon S3
- CloudFormation tham chiếu file S3 này để tạo stack

#### Các Bước Cuối Cùng

1. Xem lại cấu hình của bạn
2. Nhấp **Submit**
3. Quá trình tạo stack của bạn bắt đầu!

### Giám Sát Quá Trình Tạo Stack

#### Tab Events

Theo dõi quá trình tạo theo thời gian thực:

1. Sự kiện ban đầu: `Stack CREATE_IN_PROGRESS`
2. Sự kiện resource: `MyInstance CREATE_IN_PROGRESS`
3. Hoàn thành: `MyInstance CREATE_COMPLETE`

Quá trình tạo thường rất nhanh đối với một EC2 instance đơn lẻ.

### Truy Cập Các Tài Nguyên Đã Tạo

#### Tab Resources

1. Nhấp vào tab **Resources**
2. Bạn sẽ thấy một resource đã được tạo
3. **Physical ID** là EC2 instance ID thực tế
4. Nhấp vào Physical ID để điều hướng trực tiếp đến EC2 Console

### Xác Minh EC2 Instance

Trong EC2 Console, xác minh rằng instance của bạn khớp với thông số kỹ thuật template:

- **Instance Type**: t2.micro ✓
- **Availability Zone**: us-east-1a ✓
- **AMI**: Amazon Linux 2023 ✓

### Tags Được CloudFormation Thêm Vào

CloudFormation tự động gắn tag cho tài nguyên để theo dõi:

- **aws:cloudformation:stack-name**: EC2InstanceDemo
- **aws:cloudformation:logical-id**: MyInstance
- **aws:cloudformation:stack-id**: [Stack ID]

Các tag này giúp xác định tài nguyên nào thuộc về CloudFormation stack nào.

## Hiểu Về CloudFormation Console

### Các Tab Thông Tin Stack

1. **Stack Info**: Thông tin chung về stack của bạn
2. **Events**: Dòng thời gian của tất cả các sự kiện trong quá trình tạo stack
3. **Resources**: Danh sách tất cả các tài nguyên được tạo bởi stack
4. **Outputs**: Các giá trị output tùy chỉnh (không có trong ví dụ này)
5. **Parameters**: Các tham số đầu vào (không có trong ví dụ này)
6. **Template**: Template chính xác mà bạn đã upload

## Những Điểm Chính Cần Nhớ

✅ CloudFormation cho phép Infrastructure as Code (IaC)
✅ Template có thể được viết bằng YAML hoặc JSON
✅ Phần `Resources` là bắt buộc
✅ Template được lưu trữ trong S3 tự động
✅ CloudFormation tự động gắn tag cho tài nguyên
✅ Các công cụ trực quan như Application Composer giúp hiểu các template phức tạp
✅ Mọi thứ được định nghĩa thông qua code, không qua console

## Các Bước Tiếp Theo

Bây giờ bạn đã tạo thành công EC2 instance đầu tiên sử dụng CloudFormation, bạn đã sẵn sàng khám phá các khái niệm và template CloudFormation nâng cao hơn trong các bài giảng sắp tới.

---

*Hướng dẫn thực hành này trình bày các khái niệm cơ bản về AWS CloudFormation và cách triển khai hạ tầng sử dụng code thay vì cấu hình thủ công qua console.*