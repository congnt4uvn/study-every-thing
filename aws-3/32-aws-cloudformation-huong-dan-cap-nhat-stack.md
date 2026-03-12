# AWS CloudFormation: Hướng Dẫn Cập Nhật Stack

## Tổng Quan

Hướng dẫn này trình bày cách cập nhật AWS CloudFormation stack, làm việc với change sets và dọn dẹp tài nguyên đúng cách. Bạn sẽ học cách CloudFormation quản lý các thay đổi hạ tầng thông qua templates và xử lý các phụ thuộc tài nguyên một cách tự động.

## Cập Nhật CloudFormation Stack

### Thay Thế Template

Sau khi đã tạo CloudFormation stack, bạn có thể cập nhật nó bằng cách:

1. Click vào **Update** trong CloudFormation console
2. Chọn **replace the current template** (thay thế template hiện tại) bằng template mới
3. Nếu bạn chọn "use the current template", bạn không thể chỉnh sửa - nó sẽ sử dụng template giống như trước

### Cấu Trúc Template Đã Cập Nhật

Trong ví dụ này, chúng ta sẽ cập nhật stack sử dụng template `EC2-with-SG-EIP.YAML`, bao gồm:

- **Parameters**: Cho phép cấu hình tại runtime (ví dụ: mô tả security group)
- **EC2 Instance**: Với security groups đính kèm
- **Elastic IP**: Gắn vào EC2 instance
- **Security Groups**: Hai security groups (SSH và Server)

Template này minh họa việc tham chiếu tài nguyên - các security groups được tham chiếu trong định nghĩa EC2 instance trước khi chúng được tạo trong template.

## Quy Trình Cập Nhật Từng Bước

### 1. Tải Lên Template Mới

1. Điều hướng đến CloudFormation stack của bạn
2. Click **Update**
3. Chọn **Replace current template**
4. Tải lên file `SG-EIP.YAML`
5. Click **Next**

### 2. Cung Cấp Parameters

Bạn sẽ được yêu cầu nhập các giá trị parameter:

- **Security Group Description**: Nhập mô tả (ví dụ: "This is a cool security group")
- Giá trị parameter này sẽ được sử dụng tại runtime để cấu hình security group
- Click **Next** để tiếp tục

### 3. Xem Xét Change Set Preview

Trước khi áp dụng thay đổi, CloudFormation hiển thị **Change Set Preview** - danh sách tất cả các thay đổi sẽ xảy ra:

| Hành Động | Loại Tài Nguyên | Chi Tiết |
|-----------|----------------|----------|
| Add | Elastic IP | Tạo tài nguyên mới |
| Add | SSH Security Group | Security group mới |
| Add | Server Security Group | Security group mới |
| Replace | EC2 Instance | `replacement: true` |

**Quan trọng**: Khi `replacement: true` xuất hiện, điều đó có nghĩa:
- Tài nguyên hiện tại sẽ bị terminate
- Tài nguyên mới sẽ được tạo để thay thế
- Khi `replacement: false`, tài nguyên có thể được sửa đổi tại chỗ

CloudFormation xác định tính cần thiết của việc thay thế dựa trên các thay đổi bạn đã thực hiện trong template.

### 4. Gửi Cập Nhật

Click **Submit** để bắt đầu quá trình cập nhật.

## Hiểu Về Quy Trình Cập Nhật

### Thứ Tự Tạo Tài Nguyên

CloudFormation tự động xác định thứ tự chính xác để tạo và cập nhật tài nguyên:

1. **Security Groups Được Tạo Trước**
   - Server Security Group
   - SSH Security Group

2. **EC2 Instance Được Cập Nhật**
   - Thông báo: "The requested update requires the creation of a new physical resource; hence creating one"
   - Do `replacement: true`
   - Instance cũ vẫn chạy trong khi instance mới được tạo
   - Instance mới chuyển sang trạng thái "pending" sau đó "running"

3. **Elastic IP Được Tạo**
   - Được tạo sau EC2 instance
   - Tự động được tag bởi CloudFormation với:
     - Logical ID
     - Stack ID
     - Stack Name

4. **Tài Nguyên Được Liên Kết**
   - Elastic IP được gắn vào EC2 instance mới
   - Instance cũ bị terminate và xóa
   - Public IP của instance mới khớp với địa chỉ Elastic IP

## Xác Minh Cập Nhật

### Xác Minh EC2 Instance

Điều hướng đến EC2 Console:
- Instance mới đang chạy
- Public IP khớp với địa chỉ Elastic IP
- Instance ID khớp với associated instance trong chi tiết Elastic IP

### Xác Minh Security Groups

Kiểm tra các security groups được gắn vào instance của bạn:

**SSH Security Group:**
- Inbound rule trên port 22
- Được tag bởi CloudFormation

**Server Security Group:**
- Inbound rules cho SSH và HTTP
- Mô tả: "This is a cool security group" (từ parameter)
- Được tag bởi CloudFormation

Parameter bạn cung cấp đã được chèn thành công làm mô tả security group tại runtime - thể hiện sức mạnh của CloudFormation parameters.

### Tài Nguyên CloudFormation

Trong CloudFormation stack của bạn, bạn sẽ thấy:
- Tổng cộng 4 tài nguyên
- Tất cả tài nguyên được tag và quản lý đúng cách
- Trạng thái: **Update Complete**

## Sức Mạnh Của Parameters

Parameters trong CloudFormation cho phép bạn:
- Tùy chỉnh hành vi stack tại runtime
- Tái sử dụng templates với các cấu hình khác nhau
- Cung cấp các giá trị động (như mô tả security group trong ví dụ này)

## Dọn Dẹp Tài Nguyên

### Tại Sao Xóa Thủ Công Gây Vấn Đề

Nếu bạn xóa tài nguyên thủ công:
- Chỉ xóa EC2 instance để lại các tài nguyên mồ côi
- Security groups vẫn còn
- Elastic IP vẫn còn
- Bạn phải theo dõi và xóa từng tài nguyên một cách riêng lẻ

### Xóa CloudFormation Stack

Cách đúng để dọn dẹp:

1. Điều hướng đến CloudFormation stack của bạn
2. Click **Delete**
3. Xác nhận xóa

**Điều Gì Xảy Ra:**
- CloudFormation xóa TẤT CẢ tài nguyên trong stack
- Tự động xác định thứ tự xóa chính xác:
  1. Elastic IP được xóa trước
  2. EC2 instance bị terminate và xóa
  3. Security groups được xóa cuối cùng
- Dọn dẹp hoàn toàn chỉ với một hành động

CloudFormation xử lý các phụ thuộc và đảm bảo tài nguyên được xóa theo đúng thứ tự để tránh xung đột.

## Những Điểm Chính Cần Nhớ

### Khả Năng CloudFormation

1. **Create**: Định nghĩa hạ tầng dưới dạng code
2. **Update**: Sửa đổi hạ tầng thông qua thay đổi template
3. **Delete**: Dọn dẹp tất cả tài nguyên trong một thao tác

### Lợi Ích

- **Tự động hóa**: Không cần quản lý tài nguyên thủ công
- **Nhất quán**: Hạ tầng khớp với định nghĩa template
- **Quản lý phụ thuộc**: Tự động sắp xếp thứ tự các thao tác
- **Xem trước thay đổi**: Xem những gì sẽ thay đổi trước khi áp dụng
- **Rollback**: Khả năng dọn dẹp và rollback dễ dàng
- **Tagging**: Tự động tag tài nguyên để theo dõi

### Thực Hành Tốt Nhất

- Luôn sử dụng CloudFormation delete để dọn dẹp
- Xem xét change sets trước khi áp dụng cập nhật
- Hiểu rõ ý nghĩa của replacement
- Sử dụng parameters cho tùy chỉnh runtime
- Để CloudFormation quản lý các phụ thuộc tài nguyên

## Kết Luận

CloudFormation cung cấp khả năng infrastructure-as-code mạnh mẽ cho AWS. Bằng cách cập nhật templates và để CloudFormation xử lý việc thực thi, bạn có thể quản lý các thay đổi hạ tầng phức tạp một cách an toàn và hiệu quả. Các tính năng tự động giải quyết phụ thuộc và xem trước thay đổi giúp bạn dễ dàng hiểu và kiểm soát các sửa đổi hạ tầng.

Trong bài giảng tiếp theo, chúng ta sẽ khám phá các tính năng nâng cao và thực hành tốt nhất của CloudFormation.