# Hướng Dẫn AWS CloudFormation Conditions

## Giới Thiệu về Conditions

Conditions (Điều kiện) trong AWS CloudFormation cho phép bạn kiểm soát việc tạo resources hoặc outputs dựa trên các điều kiện cụ thể. Điều này mang lại sự linh hoạt để tạo các cấu hình stack khác nhau tùy thuộc vào môi trường hoặc các tiêu chí khác.

## Các Trường Hợp Sử Dụng Conditions

Conditions thường được sử dụng cho:

- **Resources dựa trên môi trường**: Chỉ tạo một số resources nhất định trong môi trường phát triển (Dev Stack) và các resources khác trong môi trường production (Prod Stack)
- **Cấu hình theo khu vực**: Điều chỉnh resources dựa trên AWS region
- **Quyết định dựa trên tham số**: Kiểm soát việc tạo resource dựa trên giá trị parameter

### Ví Dụ Kịch Bản

Bạn có thể có một cấu hình stack với EBS volume được gắn kèm và một cấu hình khác không có nó, tùy thuộc vào việc bạn đang triển khai lên production hay development.

## Cách Hoạt Động của Conditions

Mỗi condition có thể:
- Tham chiếu đến các conditions khác
- Tham chiếu đến giá trị parameter
- Tham chiếu đến giá trị mapping

## Tạo Conditions

Để định nghĩa một condition, bạn sử dụng phần `Conditions` trong CloudFormation template. Dưới đây là một ví dụ:

```yaml
Conditions:
  CreateProdResources: !Equals 
    - !Ref EnvType
    - prod
```

Trong ví dụ này:
- Condition được đặt tên là `CreateProdResources`
- Nó đánh giá xem parameter `EnvType` có bằng "prod" hay không
- Nếu đúng, các resources có condition này sẽ được tạo
- Nếu sai, những resources đó sẽ bị bỏ qua

## Các Hàm Condition

CloudFormation cung cấp một số hàm nội tại để tạo conditions:

- **Fn::And**: Trả về true nếu tất cả các điều kiện đều đúng
- **Fn::Equals**: So sánh hai giá trị để kiểm tra sự bằng nhau
- **Fn::If**: Trả về một giá trị nếu đúng, giá trị khác nếu sai
- **Fn::Not**: Phủ định một điều kiện
- **Fn::Or**: Trả về true nếu bất kỳ điều kiện nào đúng

## Áp Dụng Conditions cho Resources

Sau khi đã định nghĩa một condition, bạn có thể áp dụng nó cho resources hoặc outputs:

```yaml
Resources:
  MountPoint:
    Type: AWS::EC2::VolumeAttachment
    Condition: CreateProdResources
    Properties:
      # ... thuộc tính của resource
```

Trong ví dụ này:
- Resource `MountPoint` có loại `EC2::VolumeAttachment`
- Nó có condition `CreateProdResources` được áp dụng
- Nếu condition đánh giá là true, resource sẽ được tạo
- Nếu condition đánh giá là false, resource sẽ bị bỏ qua

## Góc Nhìn Từ Kỳ Thi

Từ góc độ kỳ thi chứng chỉ AWS:
- Bạn không cần biết cách viết các conditions phức tạp (quá nâng cao)
- Bạn cần hiểu rằng conditions tồn tại và khi nào nên sử dụng chúng
- Nắm được khái niệm cơ bản về việc tạo resource có điều kiện

## Tóm Tắt

CloudFormation Conditions cung cấp một cách mạnh mẽ để tạo các templates động có thể thích ứng với các môi trường, regions hoặc giá trị parameters khác nhau. Bằng cách sử dụng conditions hiệu quả, bạn có thể duy trì một template duy nhất hoạt động trên nhiều kịch bản triển khai mà không cần sao chép code.