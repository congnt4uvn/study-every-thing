# AWS CloudFormation: Giới Thiệu Về YAML

## Tổng Quan

Trong bài học này, chúng ta sẽ tìm hiểu về YAML (YAML Ain't Markup Language), định dạng được ưa chuộng để viết các template AWS CloudFormation. Mặc dù CloudFormation hỗ trợ cả YAML và JSON, nhưng YAML mang lại khả năng đọc hiểu tốt hơn và dễ sử dụng hơn, khiến nó trở thành lựa chọn được khuyến nghị cho việc phát triển template.

## Tại Sao Chọn YAML Thay Vì JSON?

YAML được sử dụng rộng rãi trong các template CloudFormation vì một số lý do quan trọng:

- **Dễ Đọc Hơn**: Cú pháp rõ ràng của YAML giúp template dễ đọc và hiểu hơn
- **Dễ Xây Dựng Hơn**: Việc viết template trở nên đơn giản hơn với cấu trúc trực quan của YAML
- **Giảm Độ Phức Tạp**: Không giống JSON, YAML giảm thiểu việc nội suy chuỗi và quản lý dấu ngoặc
- **Thân Thiện Với Con Người**: Cấu trúc dựa trên thụt lề tự nhiên hơn cho con người làm việc

## Kiến Thức Cơ Bản Về YAML

### Cặp Khóa-Giá Trị

Các tài liệu YAML được xây dựng dựa trên các cặp khóa-giá trị. Dưới đây là một ví dụ cơ bản:

```yaml
invoice: 34843
date: 2001-01-23
```

### Đối Tượng Lồng Nhau

YAML hỗ trợ các đối tượng lồng nhau thông qua thụt lề:

```yaml
bill-to:
  given: Chris
  family: Dumars
  address:
    lines: |
      458 Walkman Dr.
      Suite #292
    city: Royal Oak
    state: MI
    postal: 48046
```

Dấu hai chấm (`:`) theo sau bởi thụt lề phù hợp tạo ra cấu trúc đối tượng lồng nhau.

### Mảng

Mảng trong YAML được biểu diễn bằng dấu trừ (`-`):

```yaml
products:
  - sku: BL394D
    quantity: 4
    description: Basketball
    price: 450.00
  - sku: BL4438H
    quantity: 1
    description: Super Hoop
    price: 2392.00
```

Mỗi phần tử trong mảng bắt đầu bằng dấu gạch ngang và có thể chứa các cặp khóa-giá trị riêng.

### Chuỗi Nhiều Dòng

Dấu gạch dọc (`|`) cho phép bạn viết chuỗi nhiều dòng:

```yaml
address:
  lines: |
    458 Walkman Dr.
    Suite #292
    Ann Arbor, MI 48103
```

### Chú Thích

Chú thích trong YAML bắt đầu bằng ký hiệu thăng (`#`):

```yaml
# Đây là một chú thích
Type: AWS::EC2::Instance  # Đây cũng là một chú thích
```

## YAML Trong CloudFormation Templates

### Cấu Trúc CloudFormation Cơ Bản

Dưới đây là cách YAML trông như thế nào trong một template CloudFormation:

```yaml
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      AvailabilityZone: us-east-1a
      ImageId: ami-a4c7edb2
      InstanceType: t2.micro
```

**Các thành phần chính:**
- `Resources`: Khóa cấp cao nhất để định nghĩa tài nguyên AWS
- `MyInstance`: Tên logic cho tài nguyên
- `Type`: Chỉ định loại tài nguyên AWS
- `Properties`: Chi tiết cấu hình cho tài nguyên

### Làm Việc Với Danh Sách

Các template CloudFormation thường sử dụng danh sách cho nhiều giá trị:

```yaml
SecurityGroups:
  - sg-12345678  # Security group thứ nhất
  - sg-87654321  # Security group thứ hai

SecurityGroupIds:
  - !Ref SSHSecurityGroup
  - !Ref ServerSecurityGroup
```

### Thuộc Tính Lồng Nhau

Các tài nguyên phức tạp yêu cầu thuộc tính lồng nhau:

```yaml
Resources:
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-a4c7edb2
      InstanceType: t2.micro
      SecurityGroups:
        - !Ref SSHSecurityGroup
      Tags:
        - Key: Name
          Value: MyInstance
```

## Thực Hành Tốt Nhất

1. **Sử Dụng Thụt Lề Nhất Quán**: Luôn sử dụng khoảng trắng (thường là 2 hoặc 4) cho thụt lề, không bao giờ dùng tab
2. **Thêm Chú Thích**: Ghi chú các template của bạn với các chú thích rõ ràng giải thích các phần phức tạp
3. **Tận Dụng Chuỗi Nhiều Dòng**: Sử dụng toán tử `|` để văn bản dài dễ đọc hơn
4. **Tổ Chức Hợp Lý**: Nhóm các tài nguyên và thuộc tính liên quan lại với nhau
5. **Sử Dụng Danh Sách Phù Hợp**: Khi cần nhiều giá trị, sử dụng cú pháp mảng với dấu gạch ngang

## Ưu Điểm Trong CloudFormation

Sử dụng YAML cho các template CloudFormation mang lại:

- **Template Sạch Hơn**: Ít lộn xộn hơn so với dấu ngoặc và dấu ngoặc kép của JSON
- **Bảo Trì Dễ Dàng Hơn**: Các thay đổi đơn giản hơn để triển khai và xem xét
- **Kiểm Soát Phiên Bản Tốt Hơn**: Git diffs dễ đọc hơn với YAML
- **Giảm Lỗi**: Định dạng có cấu trúc giảm thiểu lỗi cú pháp
- **Hỗ Trợ Chú Thích Tự Nhiên**: Ghi chú hạ tầng dưới dạng code trực tiếp trong template

## Kết Luận

YAML là lựa chọn tuyệt vời để viết các template CloudFormation. Khả năng đọc hiểu, dễ sử dụng và các tính năng mạnh mẽ của nó làm cho nó vượt trội hơn JSON cho hạ tầng dưới dạng code. Một khi bạn làm quen với cú pháp YAML - bao gồm các cặp khóa-giá trị, đối tượng lồng nhau, mảng và chuỗi nhiều dòng - bạn sẽ có thể tận dụng toàn bộ sức mạnh của AWS CloudFormation một cách hiệu quả.

Bằng cách thành thạo YAML, bạn sẽ có thể đọc, hiểu và viết các template CloudFormation một cách tự tin, cho phép bạn định nghĩa và quản lý hạ tầng AWS của mình một cách hiệu quả.