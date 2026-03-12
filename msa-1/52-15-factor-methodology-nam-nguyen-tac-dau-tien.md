# Phương Pháp Luận 15-Factor: Năm Nguyên Tắc Đầu Tiên

## Tổng Quan

Tài liệu này bao gồm năm nguyên tắc đầu tiên của phương pháp luận 15-factor để xây dựng microservices cloud-native với Spring Boot. Những hướng dẫn này giúp đảm bảo rằng các microservices có khả năng mở rộng, dễ bảo trì và tuân theo các thực tiễn tốt nhất trong ngành.

---

## 1. Một Codebase Cho Một Ứng Dụng

### Nguyên Tắc
Phải có sự tương ứng một-một giữa một ứng dụng và codebase của nó. Mỗi ứng dụng hoặc microservice nên có codebase riêng biệt.

### Các Điểm Chính
- **Repository Riêng Biệt**: Mỗi microservice nên có repository GitHub riêng hoặc codebase riêng trong hệ thống quản lý phiên bản
- **Quản Lý Code Chung**: Code chung cho nhiều microservices nên được:
  - Quản lý riêng như một thư viện, HOẶC
  - Triển khai như một dịch vụ độc lập (backing service)
- **Build Một Lần**: Bất kể bạn triển khai vào bao nhiêu môi trường, chỉ build và đóng gói codebase một lần duy nhất
- **Không Build Riêng Cho Từng Môi Trường**: Không build lại codebase cho mỗi môi trường (dev, QA, production)

### Lợi Ích
- Tổ chức code tốt hơn và linh hoạt hơn
- Cấu trúc code sạch hơn
- Dễ dàng theo dõi và kiểm soát phiên bản
- Triển khai artifact đơn lẻ trên tất cả môi trường

### Hình Dung
```
Codebase Đơn → Build Một Lần → Triển khai đến:
  ├── Development (Phát triển)
  ├── Testing (Kiểm thử)
  └── Production (Sản xuất)
```

### Thực Hành Tốt Nhất
- Cấu hình theo môi trường (chi tiết database, v.v.) nên được lưu trữ bên ngoài codebase
- Cấu hình được inject từ bên ngoài trong quá trình triển khai
- Cùng một Docker image/artifact được triển khai đến tất cả môi trường

---

## 2. API First (API Là Ưu Tiên)

### Nguyên Tắc
Luôn áp dụng tư duy "API First" khi thiết kế và phát triển ứng dụng cloud-native.

### Các Điểm Chính
- **Thiết Kế Với APIs**: Ngay từ đầu, thiết kế logic nghiệp vụ để được expose thông qua REST APIs
- **Giao Tiếp Microservices**: Mọi thứ trong microservices được phát triển dưới dạng REST APIs
- **Hợp Tác Nhóm**: Các nhóm khác nhau có thể làm việc độc lập trên các APIs khác nhau

### Lợi Ích
1. **Tính Linh Hoạt**: Logic nghiệp vụ có thể được gọi bởi các APIs hoặc microservices khác như backing services
2. **Tích Hợp Có Thể Kiểm Thử**: Viết các bài test tích hợp trong deployment pipeline trước khi triển khai
3. **Sửa Đổi Độc Lập**: Sửa đổi triển khai API bên trong mà không ảnh hưởng đến các ứng dụng phụ thuộc
4. **Phát Triển Song Song**: Nhiều nhóm có thể làm việc đồng thời trên các APIs khác nhau

### Thực Hành Tốt Nhất
Nghĩ "API First" xuyên suốt toàn bộ vòng đời phát triển, từ thiết kế đến triển khai.

---

## 3. Quản Lý Dependency (Phụ Thuộc)

### Nguyên Tắc
Khai báo rõ ràng tất cả các dependency của ứng dụng trong một file manifest duy nhất và đảm bảo chúng có thể truy cập được thông qua dependency manager.

### Các Điểm Chính
- **File Manifest**: Sử dụng `pom.xml` (Maven) hoặc `build.gradle` (Gradle) cho ứng dụng Java
- **Repository Trung Tâm**: Dependencies được tải về từ repository trung tâm (Maven Central)
- **Artifact Đơn Lẻ**: Tất cả dependency libraries được đóng gói thành một artifact duy nhất trong quá trình build

### Cách Hoạt Động

1. **Developer**: Định nghĩa dependencies trong `pom.xml`
2. **Build Tool (Maven/Gradle)**: Đọc file manifest
3. **Kiểm Tra Local**: Kiểm tra xem dependencies có tồn tại trong repository local không
4. **Tải Về**: Nếu không có ở local, tải về từ Maven Central Repository
5. **Lưu Trữ Local**: Lưu các JARs đã tải về trong repository local
6. **Đóng Gói**: Trong quá trình build, tất cả dependencies được đóng gói thành:
   - Một fat JAR duy nhất (Spring Boot), HOẶC
   - Một Docker image

### Lợi Ích
- Quản lý dependency rõ ràng và có kiểm soát
- Không cần tải dependency thủ công
- Build nhất quán trên các môi trường
- Đơn giản hóa quản lý microservices

### Anti-Pattern (Mẫu Không Nên Làm)
❌ **Không Nên**: Tải dependency thủ công và thêm vào classpath (cách làm cũ)
- Trở nên cực kỳ phức tạp với hàng trăm microservices
- Dễ gây lỗi và tốn thời gian

---

## 4. Design, Build, Release, Run (Thiết Kế, Build, Release, Chạy)

### Nguyên Tắc
Codebase của bạn phải tiến triển từ thiết kế đến production bằng cách tuân theo các giai đoạn riêng biệt và tách biệt.

### Bốn Giai Đoạn

#### 1. Giai Đoạn Design (Thiết Kế)
- Xác định các công nghệ, dependencies và công cụ cần thiết
- Bao gồm phát triển và unit testing
- Định nghĩa tất cả yêu cầu kỹ thuật cho microservice

#### 2. Giai Đoạn Build
- Biên dịch và đóng gói codebase với các dependencies
- Tạo một **artifact bất biến** (immutable)
- Gán một số định danh duy nhất (phiên bản: 1.0, 2.0, 3.0, v.v.)
- **Không sửa đổi thủ công** artifact đã đóng gói

#### 3. Giai Đoạn Release
- Kết hợp build artifact với các cấu hình triển khai theo môi trường
- Ví dụ: thông tin database, cấu trúc thư mục, thuộc tính server
- Tạo một release component bất biến
- Gán định danh duy nhất (ví dụ: phiên bản 6.1.5 hoặc timestamp)
- Lưu trữ trong repository trung tâm để dễ dàng rollback

#### 4. Giai Đoạn Run (Chạy)
- Triển khai và chạy ứng dụng trong môi trường được chỉ định
- Sử dụng release artifact cụ thể
- **Không sửa đổi code trong runtime**

### Các Quy Tắc Chính
- ✅ **Duy trì sự tách biệt nghiêm ngặt** giữa các giai đoạn
- ✅ **Artifacts bất biến** - không thay đổi sau khi build
- ✅ **Khả năng tái tạo** - cùng artifact = cùng hành vi
- ❌ **Không sửa đổi runtime** để tránh không khớp

### Lợi Ích
- Dễ dàng rollback về phiên bản trước
- Hành vi nhất quán trên các môi trường
- Deployment pipeline rõ ràng
- Builds có thể tái tạo

---

## 5. Configuration, Credentials và Code (Cấu Hình, Thông Tin Xác Thực và Code)

### Nguyên Tắc
Cấu hình nên được lưu trữ riêng biệt với code và không bao giờ nhúng trong codebase.

### Configuration Là Gì?
Configuration bao gồm các yếu tố thay đổi giữa các lần triển khai:
- Thuộc tính database
- Thuộc tính hệ thống message
- Thông tin xác thực API của bên thứ ba
- Feature flags
- Bất kỳ cài đặt theo môi trường nào

### Các Điểm Chính
- **Lưu Trữ Riêng Biệt**: Duy trì cấu hình trong một codebase riêng
- **Không Có Dữ Liệu Nhạy Cảm Trong Code**: Không bao giờ expose thông tin nhạy cảm trong code repository
- **Runtime Injection**: Inject cấu hình vào thời điểm triển khai dựa trên môi trường
- **Sửa Đổi Độc Lập**: Thay đổi cấu hình mà không cần rebuild ứng dụng

### Các Loại Configuration
1. **Cấu Hình Mặc Định**: Có thể được đóng gói trong ứng dụng
2. **Cấu Hình Theo Môi Trường**: Phải được externalize
   - Cài đặt Development
   - Cài đặt QA
   - Cài đặt Production

### Ví Dụ Configuration
- Username và password database
- Connection strings
- API keys và credentials
- Service endpoints
- Feature flags theo môi trường

### Cách Hoạt Động
```
Codebase Đơn → Build Một Lần → Docker Image
                                    ↓
Triển khai đến Môi trường + Inject Cấu hình Runtime:
  ├── Development (cấu hình dev)
  ├── Testing (cấu hình QA)
  └── Production (cấu hình prod)
```

### Giải Pháp Spring Boot
**Spring Cloud Config Server**: Một project riêng trong hệ sinh thái Spring giúp triển khai hướng dẫn này trong microservices.

### Lợi Ích
- Docker image đơn lẻ cho tất cả môi trường
- Không cần rebuild khi thay đổi môi trường
- Xử lý dữ liệu nhạy cảm an toàn
- Đơn giản hóa quản lý hàng trăm microservices
- Dễ dàng cập nhật cấu hình mà không cần redeploy

### Thực Hành Tốt Nhất
- Lưu trữ cấu hình trong một configuration server tập trung
- Sử dụng các tiêu chuẩn externalization cho dữ liệu nhạy cảm
- Không bao giờ commit thông tin xác thực nhạy cảm vào version control

---

## Tóm Tắt

Năm nguyên tắc đầu tiên này của phương pháp luận 15-factor cung cấp nền tảng vững chắc để xây dựng microservices cloud-native:

1. **Một Codebase** - Một repository cho mỗi microservice
2. **API First** - Thiết kế mọi thứ như APIs
3. **Quản Lý Dependency** - Sử dụng Maven/Gradle để kiểm soát dependency rõ ràng
4. **Design, Build, Release, Run** - Tuân theo các giai đoạn riêng biệt, bất biến
5. **Quản Lý Configuration** - Externalize các cấu hình theo môi trường

Bằng cách tuân theo các hướng dẫn này, bạn đảm bảo rằng microservices của bạn:
- ✅ Có khả năng mở rộng
- ✅ Dễ bảo trì
- ✅ Có thể tái tạo
- ✅ Dễ dàng triển khai trên nhiều môi trường
- ✅ An toàn

---

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ thảo luận về các nguyên tắc còn lại của phương pháp luận 15-factor để hoàn thiện hiểu biết của chúng ta về các thực tiễn tốt nhất cho microservices cloud-native.