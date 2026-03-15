# Các Phương Án Lưu Trữ Session State trên AWS

## Tổng Quan

Tài liệu này bao gồm các dịch vụ AWS khác nhau có thể được sử dụng để lưu trữ trạng thái phiên (session states) trong ứng dụng web, cùng với các trường hợp sử dụng và sự khác biệt của chúng.

## Các Phương Án Lưu Trữ Session States

### 1. **DynamoDB**

- **Loại**: Cơ sở dữ liệu NoSQL serverless
- **Kiểu lưu trữ**: Key/value store
- **Đặc điểm**:
  - Kiến trúc serverless
  - Tự động mở rộng quy mô (automatic scaling)
  - Lưu trữ bền vững (không hoàn toàn trong bộ nhớ)
  - Có thể chia sẻ thông tin đăng nhập người dùng giữa các ứng dụng web backend
  
**Tốt nhất cho**: Các tình huống yêu cầu tự động mở rộng và giải pháp serverless

### 2. **ElastiCache**

- **Loại**: Dịch vụ caching trong bộ nhớ
- **Kiểu lưu trữ**: Key/value store
- **Đặc điểm**:
  - Hoàn toàn trong bộ nhớ (in-memory)
  - Truy cập rất nhanh
  - Có thể chia sẻ session states giữa các instances
  
**Tốt nhất cho**: Các tình huống yêu cầu lưu trữ session trong bộ nhớ để đạt hiệu suất tối đa

### 3. **Amazon EFS (Elastic File System)**

- **Loại**: Hệ thống file mạng
- **Kiểu lưu trữ**: File system
- **Đặc điểm**:
  - Phải được gắn vào các EC2 instances như một ổ đĩa mạng
  - Có thể được chia sẻ giữa nhiều EC2 instances
  - Lưu trữ trên đĩa
  
**Tốt nhất cho**: Khi bạn cần chia sẻ dữ liệu trên đĩa giữa nhiều EC2 instances

### 4. **EBS Volumes & EC2 Instance Store** ❌

- **Loại**: Lưu trữ cục bộ
- **Hạn chế**: Chỉ gắn với một EC2 instance duy nhất
- **Trường hợp sử dụng**: Chỉ cho caching cục bộ, KHÔNG cho caching chia sẻ
  
**Không phù hợp cho**: Chia sẻ session states giữa nhiều instances

### 5. **Amazon S3** ❌

- **Loại**: Object storage
- **Hạn chế**: Độ trễ cao hơn
- **Được thiết kế cho**: Các file lớn, không phải các object nhỏ
  
**Không phù hợp cho**: Lưu trữ session state (không tối ưu cho trường hợp này)

## Bảng So Sánh

| Dịch vụ | Loại | Bộ nhớ/Đĩa | Chia sẻ giữa Instances | Trường hợp sử dụng tốt nhất |
|---------|------|-------------|------------------------|------------------------------|
| **DynamoDB** | Database | Serverless | ✅ Có | Tự động mở rộng, serverless |
| **ElastiCache** | Cache | In-memory | ✅ Có | Trong bộ nhớ, hiệu năng cao |
| **EFS** | File System | Đĩa | ✅ Có | Lưu trữ hệ thống file chia sẻ |
| **EBS/Instance Store** | Local Storage | Đĩa | ❌ Không | Chỉ caching cục bộ |
| **S3** | Object Storage | Đĩa | ✅ Có | File lớn (không phải session states) |

## Mẹo Quan Trọng Cho Kỳ Thi

### DynamoDB so với ElastiCache

- **ElastiCache**: Chọn khi đề thi đề cập đến yêu cầu "in-memory"
- **DynamoDB**: Chọn khi đề thi đề cập đến "automatic scaling" hoặc "serverless"
- Cả hai đều là key/value stores và phù hợp cho session states

### Các Phương Án Tốt Nhất Cho Session States

**Top 3 lựa chọn**:
1. DynamoDB
2. ElastiCache  
3. EFS

**Ưu tiên**: DynamoDB và ElastiCache là hai phương án tốt nhất

## Tóm Tắt

Khi lưu trữ session states trên AWS:
- ✅ **Sử dụng DynamoDB** cho các giải pháp serverless, tự động mở rộng
- ✅ **Sử dụng ElastiCache** cho nhu cầu hoàn toàn trong bộ nhớ, hiệu năng cao
- ✅ **Sử dụng EFS** khi bạn cần một hệ thống file chia sẻ
- ❌ **Tránh EBS/Instance Store** cho session states chia sẻ
- ❌ **Tránh S3** cho lưu trữ session state (độ trễ cao cho các object nhỏ)
