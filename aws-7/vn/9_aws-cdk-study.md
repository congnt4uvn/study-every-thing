# AWS Cloud Development Kit (CDK) - Tài Liệu Học Tập

## Tổng Quan

**AWS Cloud Development Kit (CDK)** là một framework cho phép bạn định nghĩa hạ tầng đám mây bằng các ngôn ngữ lập trình quen thuộc thay vì sử dụng các file cấu hình khai báo.

### Ngôn Ngữ Được Hỗ Trợ
- JavaScript/TypeScript
- Python
- Java
- .NET

## Khái Niệm Chính

### CDK Là Gì?

CDK cho phép bạn định nghĩa hạ tầng đám mây bằng ngôn ngữ lập trình, mang lại nhiều lợi ích so với các template YAML của CloudFormation truyền thống:

- **Kiểm tra kiểu dữ liệu**: Code phải compile được trước khi tạo template
- **Phát hiện lỗi**: Phát hiện lỗi trong quá trình phát triển, không phải khi triển khai
- **Linh hoạt**: Sử dụng đầy đủ tính năng của ngôn ngữ lập trình
- **Tái sử dụng**: Tạo và chia sẻ các component có thể tái sử dụng

### Mối Quan Hệ với CloudFormation

CDK **thay thế nâng cấp** CloudFormation bằng cách:
- Compile thành các template CloudFormation (JSON hoặc YAML)
- Cung cấp các abstraction cấp cao hơn (constructs)
- Duy trì tính tương thích với CloudFormation ở backend

## Constructs (Cấu Trúc)

**Constructs** là các component cấp cao trong CDK, đóng gói các tài nguyên AWS với các cấu hình được định nghĩa sẵn.

### Ví Dụ: Định Nghĩa Hạ Tầng Bằng TypeScript

```typescript
// 1. Tạo VPC với 3 Availability Zones
const vpc = new VPC(this, 'MyVPC', {
  maxAzs: 3
});

// 2. Tạo ECS Cluster
const cluster = new ECS.Cluster(this, 'MyCluster', {
  vpc: vpc
});

// 3. Tạo Application Load-Balanced Fargate Service
const fargateService = new ApplicationLoadBalancedFargateService(this, 'MyService', {
  cluster: cluster,
  cpu: 512,
  desiredCount: 6,
  taskImageOptions: { /* config */ },
  memoryLimitMiB: 2048,
  publicLoadBalancer: true
});
```

## Quy Trình Làm Việc với CDK

1. **Viết Code**: Định nghĩa hạ tầng bằng ngôn ngữ lập trình
2. **Compile**: Đảm bảo code typesafe và không có lỗi
3. **Synthesize**: Sử dụng CDK CLI để tạo template CloudFormation
4. **Deploy**: Áp dụng template thông qua CloudFormation

```
Application Constructs (Lambda, DynamoDB, S3, ECS, Step Functions)
         ↓
Ngôn Ngữ Lập Trình (Python, TypeScript, Java, .NET)
         ↓
CDK CLI (cdk synth)
         ↓
CloudFormation Template
         ↓
Triển Khai Hạ Tầng
```

## Các Trường Hợp Sử Dụng

CDK đặc biệt tốt cho:
- **Lambda Functions**: Triển khai hạ tầng và code cùng lúc
- **Docker Containers**: Triển khai ECS và EKS
- **Hạ tầng phức tạp**: Kiến trúc đa dịch vụ
- **Application Runtime**: Kết hợp code hạ tầng và ứng dụng

## So Sánh CDK vs SAM

### SAM (Serverless Application Model)
- **Tập trung**: Serverless và Lambda functions
- **Định dạng**: Template JSON/YAML khai báo
- **Phù hợp cho**: Bắt đầu nhanh với Lambda
- **Backend**: Sử dụng CloudFormation

### CDK (Cloud Development Kit)
- **Tập trung**: Tất cả các dịch vụ AWS (superset của CloudFormation)
- **Định dạng**: Ngôn ngữ lập trình (TypeScript, Python, Java, .NET)
- **Phù hợp cho**: Hạ tầng phức tạp với type safety
- **Backend**: Tạo ra các template CloudFormation

## Tích Hợp CDK + SAM

Bạn có thể kết hợp CDK và SAM để test local:

1. Chạy `cdk synth` để tạo template CloudFormation từ CDK app
2. Sử dụng SAM CLI để test local ứng dụng CDK
3. Tận dụng khả năng test local của SAM với định nghĩa hạ tầng của CDK

## Lợi Ích Chính

✅ **Type Safety**: Kiểm tra lỗi tại compile-time  
✅ **Hỗ trợ IDE**: Auto-completion và tài liệu inline  
✅ **Component tái sử dụng**: Tạo và chia sẻ constructs  
✅ **Ngôn ngữ quen thuộc**: Sử dụng công cụ và pattern bạn đã biết  
✅ **Sức mạnh CloudFormation**: Hỗ trợ đầy đủ các dịch vụ AWS  
✅ **Linh hoạt**: Kết hợp code hạ tầng và ứng dụng  

## Các Lệnh Cơ Bản

- `cdk synth`: Tổng hợp CDK app thành template CloudFormation
- `cdk deploy`: Triển khai hạ tầng lên AWS
- `cdk diff`: So sánh stack đã deploy với trạng thái hiện tại
- `cdk destroy`: Xóa các tài nguyên đã triển khai

---

**Mẹo Học Tập**: Thực hành bằng cách chuyển đổi các template CloudFormation đơn giản thành code CDK để hiểu được sự khác biệt và lợi ích của việc sử dụng ngôn ngữ lập trình.
