# AWS CodeArtifact - Tài Liệu Học Tập

## Tổng Quan

**AWS CodeArtifact** là dịch vụ lưu trữ artifact được quản lý hoàn toàn, giúp các tổ chức dễ dàng lưu trữ, xuất bản và chia sẻ các gói phần mềm được sử dụng trong quá trình phát triển phần mềm một cách an toàn.

## Quản Lý Artifact Là Gì?

- Khi xây dựng phần mềm, code của bạn phụ thuộc vào các thư viện và gói phần mềm khác (gọi là **code dependencies** - phụ thuộc code)
- Các phụ thuộc này thường được lưu trữ trong các repository
- Toàn bộ mạng lưới phụ thuộc được gọi là **artifact management** (quản lý artifact)
- Theo cách truyền thống, việc thiết lập và duy trì hệ thống quản lý artifact của riêng bạn có thể rất phức tạp

## Lợi Ích Chính

1. **Bảo mật** - Artifacts được lưu trong VPC của bạn trên AWS
2. **Khả năng mở rộng** - Được quản lý bởi AWS, tự động scale
3. **Tiết kiệm chi phí** - Chỉ trả tiền cho những gì bạn sử dụng
4. **Tích hợp** - Hoạt động liền mạch với các công cụ quản lý phụ thuộc phổ biến

## Các Package Manager Được Hỗ Trợ

CodeArtifact tích hợp với các công cụ quản lý phụ thuộc phổ biến:

- **Maven** (Java)
- **Gradle** (Java/Kotlin)
- **npm** (JavaScript/Node.js)
- **yarn** (JavaScript/Node.js)
- **pip** (Python)
- **twine** (Python)
- **NuGet** (.NET)

## Kiến Trúc

### Domains và Repositories

- CodeArtifact tổ chức artifacts sử dụng **domains** (miền)
- Mỗi domain chứa một tập hợp các **repositories** (kho lưu trữ)
- Tất cả artifacts nằm trong VPC của bạn trên AWS

### Cách Hoạt Động

#### 1. Proxy cho Public Repositories

Thay vì developers truy cập trực tiếp vào public artifact repositories, CodeArtifact hoạt động như một **proxy** (máy chủ trung gian):

```
Developer → CodeArtifact → Public Artifact Repository
```

**Lợi ích:**
- **Bảo mật mạng**: Developers chỉ tương tác với CodeArtifact
- **Caching**: Các phụ thuộc được lưu cache trong CodeArtifact
- **Tính khả dụng**: Ngay cả khi một phụ thuộc biến mất khỏi public repo, bạn vẫn giữ bản sao đã cache

**Các ngôn ngữ được hỗ trợ:**
- JavaScript (npm/yarn)
- Python (pip)
- .NET (NuGet)
- Java (Maven/Gradle)

#### 2. Xuất Bản Artifact Riêng Tư

- Developers và teams có thể xuất bản các gói của riêng họ lên CodeArtifact
- Các artifacts nội bộ được phê duyệt và chia sẻ giữa các teams
- Tất cả artifacts được tập trung ở một nơi trong VPC của bạn

#### 3. Tích Hợp với AWS CodeBuild

- CodeBuild có thể lấy dependencies trực tiếp từ CodeArtifact
- Không cần truy cập public repositories trong quá trình build
- Quá trình build nhanh hơn, an toàn hơn và đáng tin cậy hơn

## Tích Hợp Event-Driven

### Tích Hợp EventBridge

Các sự kiện của CodeArtifact kích hoạt các dịch vụ AWS downstream:

**Các loại sự kiện:**
- Package được tạo
- Package được sửa đổi
- Package bị xóa

**Các dịch vụ được kích hoạt:**
- AWS Lambda functions
- AWS Step Functions
- Amazon SNS (Simple Notification Service)
- Amazon SQS (Simple Queue Service)
- AWS CodePipeline

### Ví Dụ Use Case

Khi phiên bản package được cập nhật trong CodeArtifact:
1. Sự kiện được phát ra EventBridge
2. EventBridge kích hoạt CodePipeline
3. CodePipeline tự động bắt đầu quá trình build/deployment

## Tóm Tắt Các Khái Niệm Chính

| Khái niệm | Mô tả |
|-----------|-------|
| **Artifact** | Một gói phần mềm hoặc thư viện |
| **Domain** | Nhóm logic của các repositories |
| **Repository** | Vị trí lưu trữ cho artifacts |
| **Proxy** | CodeArtifact lấy từ public repos thay bạn |
| **Caching** | Các phụ thuộc được lưu cục bộ để đảm bảo độ tin cậy |
| **EventBridge** | Dịch vụ AWS cho tích hợp event-driven |

## Mẹo Học Tập

1. Hiểu sự khác biệt giữa public và private repositories
2. Biết cách CodeArtifact cải thiện bảo mật thông qua proxying
3. Nhớ các package managers được hỗ trợ
4. Hiểu cách CodeArtifact tích hợp với CodeBuild và CodePipeline
5. Quen thuộc với các mẫu tích hợp EventBridge

## Chuẩn Bị Thi

**Các điểm chính cần nhớ:**
- ✅ CodeArtifact là **dịch vụ artifact repository được quản lý**
- ✅ Hỗ trợ các package managers phổ biến (Maven, Gradle, npm, yarn, pip, NuGet)
- ✅ Hoạt động như **proxy** cho public repositories với caching
- ✅ Tích hợp với **CodeBuild** cho CI/CD pipelines
- ✅ Phát ra events tới **EventBridge** cho automation
- ✅ Tất cả artifacts được lưu trữ an toàn trong **VPC** của bạn
