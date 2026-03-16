# Tài liệu học AWS CDK Constructs

## Tổng quan

Trong AWS CDK, **Construct** là khối xây dựng cốt lõi để định nghĩa hạ tầng cloud. Mỗi construct đóng gói toàn bộ cấu hình mà CDK cần để sinh ra CloudFormation stack cuối cùng.

Một construct có thể đại diện cho:

- Một tài nguyên AWS đơn lẻ, ví dụ S3 bucket
- Một nhóm tài nguyên liên quan, ví dụ hệ thống worker dùng SQS và dịch vụ compute

CDK cung cấp constructs thông qua:

- **Construct Library**, nơi chứa các construct cho tài nguyên AWS
- **Construct Hub**, nơi có thêm construct từ AWS, bên thứ ba và cộng đồng mã nguồn mở

## 3 cấp độ Construct

### Level 1: L1 Constructs

L1 là cấp độ construct cơ bản nhất.

- Còn được gọi là **CFN Resources**
- Ánh xạ trực tiếp tới tài nguyên trong CloudFormation
- Thường bắt đầu bằng `Cfn`, ví dụ `s3.CfnBucket`
- Yêu cầu khai báo thuộc tính gần với cú pháp CloudFormation thuần

#### Khi nào nên dùng L1

- Khi cần kiểm soát chi tiết toàn bộ thuộc tính của CloudFormation
- Khi muốn chuyển đổi dần từ template CloudFormation sang CDK
- Khi construct cấp cao hơn không hỗ trợ một thuộc tính thấp cấp mà bạn cần

#### Ví dụ

```ts
new s3.CfnBucket(this, 'MyBucket', {
  bucketName: 'my-bucket'
});
```

#### Ý chính

L1 rất mạnh nhưng ở mức thấp. Nó gần với cách khai báo hạ tầng bằng CloudFormation thuần.

### Level 2: L2 Constructs

L2 là các construct ở mức trừu tượng cao hơn cho tài nguyên AWS.

- Đại diện cho tài nguyên AWS với trải nghiệm phát triển tốt hơn
- **Không** bắt đầu bằng `Cfn`, ví dụ `s3.Bucket`
- Có sẵn cấu hình mặc định hợp lý và các helper methods
- Giúp diễn đạt ý định thiết kế rõ ràng hơn

#### Lợi ích của L2

- Ít boilerplate hơn
- Cấu hình dễ hơn
- Có thêm helper methods
- Dễ đọc và dễ bảo trì hơn

#### Ví dụ

```ts
const bucket = new s3.Bucket(this, 'MyBucket', {
  versioned: true,
  encryption: s3.BucketEncryption.KMS
});
```

Với L2, bạn cũng có thể dùng các helper methods như cấu hình lifecycle thay vì tự viết toàn bộ chi tiết của CloudFormation.

#### Ý chính

L2 thường cho kết quả hạ tầng tương tự L1 nhưng thuận tiện hơn và dễ bảo trì hơn.

### Level 3: L3 Constructs

L3 còn được gọi là **Patterns**.

- Kết hợp nhiều tài nguyên liên quan thành một giải pháp có thể tái sử dụng
- Tập trung vào các kiến trúc AWS phổ biến
- Giảm độ phức tạp khi phải ghép nhiều dịch vụ thủ công

#### Ví dụ

- Mẫu Lambda REST API
- ECS kết hợp Application Load Balancer và Fargate Service

#### Vì sao L3 hữu ích

Một số kiến trúc AWS rất phức tạp nếu viết bằng CloudFormation thuần vì cần nhiều tài nguyên liên kết với nhau, ví dụ:

- Load balancer
- Dịch vụ compute
- Security groups
- Listener
- Tích hợp giữa các dịch vụ

L3 che giấu phần lớn công việc cấu hình đó và cho phép bạn tập trung vào kiến trúc mong muốn.

#### Ý chính

L3 phù hợp để xây dựng nhanh các giải pháp AWS phổ biến với ít cấu hình thủ công hơn.

## So sánh nhanh

| Cấp độ | Tên | Phạm vi | Lợi ích chính | Ví dụ |
| --- | --- | --- | --- | --- |
| L1 | CFN Resource | Một tài nguyên CloudFormation | Kiểm soát tối đa | `s3.CfnBucket` |
| L2 | AWS Resource Construct | Một tài nguyên AWS | Có mặc định tốt và helper methods | `s3.Bucket` |
| L3 | Pattern | Nhiều tài nguyên liên quan | Tạo kiến trúc nhanh hơn | Lambda REST API pattern |

## Cách nhận biết từng cấp độ

- Nếu tên construct bắt đầu bằng `Cfn` thì thường là **L1**
- Nếu nó mô hình hóa một tài nguyên AWS đơn lẻ theo cách thân thiện hơn thì thường là **L2**
- Nếu nó tạo ra cả một kiến trúc hoặc một mẫu giải pháp hoàn chỉnh thì thường là **L3**

## Ghi chú học tập

- **Construct** là abstraction cốt lõi của AWS CDK
- CDK chuyển constructs thành CloudFormation
- **L1** gần nhất với CloudFormation thuần
- **L2** là cấp độ được dùng nhiều nhất trong phát triển hằng ngày
- **L3** giúp xây dựng nhanh các kiến trúc phổ biến
- Construct Hub mở rộng số lượng construct ngoài thư viện có sẵn của AWS

## Trọng tâm cho thi cử và phỏng vấn

Hãy chuẩn bị giải thích:

1. Construct là gì trong AWS CDK
2. Sự khác nhau giữa L1, L2 và L3
3. Vì sao L2 và L3 thường được ưu tiên hơn L1 về năng suất
4. Khi nào L1 vẫn cần thiết
5. Sự khác nhau giữa Construct Library và Construct Hub

## Tóm tắt ngắn

AWS CDK constructs là các khối xây dựng có thể tái sử dụng để định nghĩa hạ tầng dưới dạng code. L1 ánh xạ trực tiếp tới CloudFormation, L2 cung cấp abstraction mức cao hơn cho từng tài nguyên, còn L3 đóng gói các mẫu kiến trúc phổ biến. Cấp độ càng cao thì càng có nhiều tiện ích và mức trừu tượng lớn hơn.