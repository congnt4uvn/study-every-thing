# Hướng Dẫn AWS CloudFormation Mappings

## Giới Thiệu

Mappings trong CloudFormation là các biến cố định trong các template CloudFormation của bạn. Chúng rất hữu ích khi bạn muốn phân biệt giữa các môi trường khác nhau, các vùng (regions), hoặc các biến khác có giá trị được xác định trước.

## Mappings Là Gì?

Mappings là các cặp key-value được hardcode cho phép bạn:

- Phân biệt giữa các môi trường khác nhau (ví dụ: dev vs prod)
- Xử lý sự khác biệt theo vùng (ví dụ: các vùng AWS)
- Quản lý các loại AMI và các giá trị cụ thể theo kiến trúc
- Cung cấp khả năng kiểm soát an toàn hơn đối với các giá trị template

Tất cả các giá trị có thể có đều được hardcode trong template, giúp chúng có thể dự đoán và kiểm soát được.

## Cấu Trúc Mapping

Đây là một ví dụ về RegionMap minh họa định dạng của mappings:

```yaml
Mappings:
  RegionMap:
    us-east-1:
      HVM64: ami-0ff8a91507f77f867
      HVMG2: ami-0a584ac55a7631c0c
    us-west-1:
      HVM64: ami-0bdb828fd58c52235
      HVMG2: ami-066ee5fd4a9ef77f1
    eu-west-1:
      HVM64: ami-047bb4163c506cd98
      HVMG2: ami-0a7c483d527806435
```

Trong ví dụ này:
- **Region** (us-east-1, us-west-1, eu-west-1) là key cấp cao nhất
- **Kiến trúc** (HVM64, HVMG2) là key cấp thứ hai
- **AMI ID** là giá trị được trả về

Đây là một ứng cử viên tuyệt vời cho mapping vì AMI là đặc thù theo vùng, và bạn cần các AMI ID khác nhau cho mỗi kết hợp vùng và kiến trúc.

## Truy Cập Giá Trị Mapping

Để truy cập các giá trị mapping, hãy sử dụng hàm `FindInMap`. Đây là một ví dụ với EC2 instance:

```yaml
Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: !FindInMap
        - RegionMap
        - !Ref AWS::Region
        - HVM64
```

### Cách Hoạt Động Của FindInMap

Hàm `FindInMap` nhận ba tham số:

1. **Tên Map**: Tên của mapping (ví dụ: `RegionMap`)
2. **Key Cấp Cao**: Thường sử dụng pseudo parameter `AWS::Region` để tự động phát hiện vùng hiện tại
3. **Key Cấp Hai**: Giá trị cụ thể bạn muốn (ví dụ: `HVM64` cho loại kiến trúc)

Khi bạn khởi chạy template này:
- Ở **us-east-1**, nó sẽ resolve thành AMI của us-east-1
- Ở **us-west-1**, nó tự động resolve thành AMI của us-west-1

Pseudo parameter `AWS::Region` tự động resolve thành vùng nơi template được khởi chạy.

## Mappings vs Parameters

### Khi Nào Sử Dụng Mappings

Sử dụng mappings khi:
- Bạn biết **trước** tất cả các giá trị có thể có
- Các giá trị có thể được **suy ra từ các biến** như:
  - Region (Vùng)
  - Availability Zone (Vùng khả dụng)
  - AWS Account (Tài khoản AWS)
  - Environment (Môi trường - dev vs prod)
- Bạn muốn **kiểm soát an toàn hơn** đối với template
- Các giá trị là **cố định và có thể dự đoán**

### Khi Nào Sử Dụng Parameters

Sử dụng parameters khi:
- Các giá trị phụ thuộc vào **đầu vào của người dùng**
- Bạn muốn cung cấp cho người dùng **sự tự do tối đa** tại runtime
- Các giá trị **không thể dự đoán** trước
- Người dùng cần **đưa ra quyết định** khi khởi chạy stack

## Thực Hành Tốt Nhất

1. **Sử dụng mappings cho các tài nguyên đặc thù theo vùng**: AMIs, availability zones và các tài nguyên theo vùng khác
2. **Giữ mappings có tổ chức**: Nhóm các giá trị liên quan lại với nhau
3. **Ghi chú cho mappings của bạn**: Thêm comments để giải thích mục đích của mỗi mapping
4. **Kết hợp với parameters**: Sử dụng cả mappings và parameters để có templates linh hoạt nhưng vẫn được kiểm soát

## Kết Luận

Mappings là một tính năng mạnh mẽ trong CloudFormation cung cấp tính linh hoạt được kiểm soát. Chúng hoạt động tuyệt vời cho các giá trị được biết trước và có thể được suy ra từ các biến môi trường. Bằng cách sử dụng mappings một cách phù hợp, bạn có thể tạo các template CloudFormation dễ bảo trì và an toàn hơn.

## Những Điểm Chính Cần Nhớ

- Mappings là các biến cố định được hardcode trong templates
- Hoàn hảo cho các giá trị đặc thù theo vùng như AMIs
- Sử dụng hàm `FindInMap` để truy cập các giá trị
- Kết hợp với pseudo parameters để tự động resolve
- Chọn mappings thay vì parameters khi các giá trị được xác định trước