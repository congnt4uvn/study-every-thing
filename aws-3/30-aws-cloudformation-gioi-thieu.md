# Giới Thiệu AWS CloudFormation

## AWS CloudFormation là gì?

AWS CloudFormation là một trong những dịch vụ mạnh mẽ nhất trong AWS, cho phép bạn mô tả cơ sở hạ tầng AWS của mình cho bất kỳ tài nguyên nào chỉ bằng code.

### Ví dụ Trường Hợp Sử Dụng

Trong một CloudFormation template, bạn có thể khai báo:
- Một security group
- Hai EC2 instances sử dụng security group
- Elastic IPs cho các EC2 instances này
- Một S3 bucket
- Một load balancer đặt trước các EC2 instances

Bằng cách khai báo những gì bạn muốn và cách chúng nên được liên kết với nhau, CloudFormation sẽ tự động tạo chúng cho bạn theo đúng thứ tự với cấu hình chính xác mà bạn chỉ định.

Điều này loại bỏ mọi nhu cầu cấu hình thủ công và làm việc thủ công - tất cả tài nguyên đều được cung cấp thông qua CloudFormation.

## Infrastructure as Code (Hạ tầng dưới dạng mã)

CloudFormation template là code mô tả một cách khai báo những gì bạn muốn cơ sở hạ tầng của mình bao gồm. Bạn có thể trực quan hóa cơ sở hạ tầng này bằng **Infrastructure Composer** để xem cách các thành phần liên quan với nhau trong CloudFormation.

## Tại Sao Nên Sử Dụng AWS CloudFormation?

### Infrastructure as Code
- **Không tạo thủ công**: Không có tài nguyên nào được tạo thủ công, điều này rất tốt cho việc kiểm soát
- **Quản lý phiên bản**: Tất cả CloudFormation templates có thể được quản lý phiên bản bằng Git
- **Code review**: Mọi thay đổi đối với cơ sở hạ tầng của bạn đều được xem xét thông qua thay đổi code

### Quản Lý Chi Phí
- **Tài nguyên được gắn thẻ**: Tất cả tài nguyên trong CloudFormation stack của bạn được gắn thẻ với một mã định danh để bạn có thể dễ dàng xem chi phí
- **Ước tính chi phí**: Bạn có thể ước tính chi phí của các tài nguyên từ CloudFormation templates
- **Chiến lược tiết kiệm**: Tự động xóa templates lúc 5:00 chiều và tạo lại chúng lúc 8:00 sáng trong môi trường phát triển

### Năng Suất
- **Hủy và tạo lại**: Khả năng hủy và tạo lại cơ sở hạ tầng trên cloud một cách nhanh chóng
- **Tận dụng sức mạnh cloud**: Tạo và xóa mọi thứ khi cần và chỉ trả tiền theo mức sử dụng
- **Sơ đồ tự động**: Tự động tạo sơ đồ cho templates của bạn
- **Lập trình khai báo**: Không cần tìm ra thứ tự tạo tài nguyên và điều phối

### Tách Biệt Mối Quan Tâm
Bạn có thể tạo nhiều CloudFormation stacks cho nhiều ứng dụng và lớp:
- Stacks cho mạng và VPCs của bạn
- Stacks cho các ứng dụng của bạn
- Và nhiều hơn nữa...

### Khả Năng Tái Sử Dụng
Đừng tái phát minh bánh xe - tận dụng các templates hiện có trên web và tài liệu để nhanh chóng viết CloudFormation templates của bạn.

## CloudFormation Hoạt Động Như Thế Nào?

### Upload Template và Tạo Stack
1. Templates phải được upload lên Amazon S3
2. Tham chiếu template từ CloudFormation
3. Một stack sẽ được tạo

### CloudFormation Stack
CloudFormation stack được tạo thành từ các tài nguyên AWS - nó có thể là bất kỳ loại tài nguyên nào bạn có thể tạo trên AWS.

### Cập Nhật Templates
- Bạn không thể chỉnh sửa template trước đó
- Bạn phải upload lại phiên bản mới của template lên AWS
- Sau đó cập nhật stack của bạn

### Quản Lý Stack
- Stacks được xác định bằng tên trong region
- Nếu bạn xóa một CloudFormation stack, mọi artifact và tài nguyên được tạo bởi CloudFormation sẽ bị xóa

## Triển Khai CloudFormation Templates

### Cách Thủ Công
- Sử dụng Infrastructure Composer hoặc code editor để tạo CloudFormation templates
- Sử dụng console để nhập parameters
- Được khuyến nghị cho mục đích học tập

### Cách Tự Động
- Chỉnh sửa templates trong file YAML
- Sử dụng CLI để triển khai templates
- Sử dụng công cụ continuous delivery để triển khai tự động trên cloud
- Được khuyến nghị để tự động hóa hoàn toàn quy trình triển khai của bạn

## Các Thành Phần Cơ Bản Của CloudFormation

CloudFormation template được tạo thành từ các thành phần khác nhau:

### Các Thành Phần Template

1. **AWSTemplateFormatVersion**: Xác định phiên bản cách đọc templates (cho mục đích nội bộ của AWS)

2. **Description**: Nhận xét về template

3. **Resources** (Bắt buộc): Định nghĩa tất cả các tài nguyên AWS được khai báo trong template

4. **Parameters**: Đầu vào động cho template của bạn

5. **Mappings**: Biến tĩnh cho template của bạn

6. **Outputs**: Tham chiếu đến những gì đã được tạo trong template của bạn

7. **Conditionals**: Danh sách các điều kiện để thực hiện tạo tài nguyên

8. **Template Helpers**: Tham chiếu và hàm

## Tổng Kết

AWS CloudFormation là một dịch vụ Infrastructure as Code mạnh mẽ cho phép bạn:
- Tự động hóa việc cung cấp cơ sở hạ tầng
- Quản lý cơ sở hạ tầng thông qua code
- Kiểm soát chi phí hiệu quả
- Cải thiện năng suất
- Duy trì tính nhất quán trên các môi trường

Trong các phần tiếp theo, chúng ta sẽ khám phá tất cả các thành phần này với các ví dụ code chi tiết.