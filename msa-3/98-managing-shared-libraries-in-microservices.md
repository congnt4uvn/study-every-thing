# Quản Lý Thư Viện Dùng Chung Trong Microservices

## Tổng Quan

Một trong những thách thức phổ biến trong phát triển microservices là xử lý việc trùng lặp code giữa nhiều dịch vụ. Tài liệu này khám phá các cách tiếp cận khác nhau để quản lý thư viện dùng chung và cung cấp hướng dẫn về thời điểm và cách triển khai chúng một cách hiệu quả.

## Vấn Đề: Trùng Lặp Code

Trong kiến trúc microservices, các developer thường viết code trùng lặp trên nhiều dịch vụ. Ví dụ, một class `ErrorResponseDto` có thể được nhân bản trên tất cả các microservices nghiệp vụ như accounts, cards và loans. Mặc dù các dịch vụ hỗ trợ (Eureka server, Config server, Gateway server) có thể không cần các DTO như vậy, nhưng các microservices nghiệp vụ thường chia sẻ nhiều class chung.

Khi hệ sinh thái microservices của bạn phát triển, sự trùng lặp này trở nên rõ ràng hơn và khó duy trì hơn.

## Cách Tiếp Cận 1: Dự Án Maven Dùng Chung Duy Nhất

### Mô Tả
Tạo một dự án Maven dùng chung chứa tất cả các dependency và code chung, bao gồm:
- Các class tiện ích (Utility classes)
- Cấu hình (Configurations)
- Logic ghi log (Logging)
- Triển khai bảo mật (Security)
- Bất kỳ chức năng chung nào khác

### Nhược Điểm
- **Vấn Đề Fat JAR**: Thư viện trở thành một file JAR lớn, nguyên khối
- **Dependency Không Cần Thiết**: Các dịch vụ phải bao gồm tất cả code, ngay cả chức năng chúng không sử dụng
- **Docker Image Cồng Kềnh**: Docker images chứa logic không sử dụng, tăng kích thước
- **Không Được Khuyến Nghị**: Cách tiếp cận này không phải là best practice

## Cách Tiếp Cận 2: Nhiều Thư Viện Nhỏ Hơn

### Mô Tả
Tách code dùng chung thành nhiều thư viện nhỏ, tập trung:
- Thư viện tiện ích
- Thư viện bảo mật
- Thư viện ghi log
- Các thư viện tập trung khác

### Ưu Điểm
- Các dịch vụ có thể chọn lọc dependency họ cần
- Kích thước thư viện nhỏ hơn, dễ quản lý hơn

### Nhược Điểm
- **Độ Phức Tạp Quản Lý**: Dự án lớn có thể có 20-30+ dự án Maven khác nhau
- **Quản Lý Phiên Bản**: Khó duy trì versioning trên nhiều thư viện
- **Overhead Pull Request**: Quy trình phức tạp cho thay đổi code và phê duyệt
- **Thách Thức Xuất Bản**: Quản lý nhiều releases rất phức tạp
- **Không Được Khuyến Nghị**: Chi phí quản lý lớn hơn lợi ích

## Cách Tiếp Cận 3: Dự Án Maven Multi-Module (BOM) ✅ Được Khuyến Nghị

### Mô Tả
Tạo một dự án cha Bill of Materials (BOM) với nhiều submodules, trong đó mỗi module tập trung vào một chức năng cụ thể:
- Module ghi log
- Module bảo mật
- Module kiểm toán (Auditing)
- Các module chức năng khác

Tất cả các submodules chia sẻ một file BOM cha chung.

### Ưu Điểm
- **Repository Duy Nhất**: Tất cả thư viện chung tồn tại trong một GitHub repository
- **Versioning Đơn Giản**: Dễ dàng duy trì số phiên bản trên tất cả modules
- **Quản Lý Dễ Dàng**: Quy trình pull request và code review đơn giản
- **Dependency Chọn Lọc**: Các dịch vụ vẫn chọn modules họ cần
- **Best Practice**: Giải quyết các thách thức từ cách tiếp cận trước

### Triển Khai
Cách tiếp cận BOM cung cấp sự linh hoạt của nhiều thư viện với sự đơn giản quản lý của một cấu trúc dự án duy nhất.

## Cân Nhắc Quan Trọng: Khi Nào Nên Sử Dụng Thư Viện Dùng Chung

### Cuộc Tranh Luận
Chia sẻ code giữa các microservices là một chủ đề gây tranh cãi trong cộng đồng phát triển. Không có câu trả lời đúng duy nhất - nó phụ thuộc vào tình huống cụ thể của bạn.

### Hướng Dẫn Quyết Định

#### ✅ Sử Dụng Thư Viện Dùng Chung Khi:
- Code chung không tạo ra sự ghép nối chặt chẽ giữa các dịch vụ
- Triển khai vẫn đơn giản và độc lập
- Gánh nặng duy trì của sự trùng lặp là đáng kể
- Logic dùng chung thực sự ổn định và không có khả năng phân kỳ

#### ❌ Tránh Thư Viện Dùng Chung Khi:
- Chúng tạo ra sự ghép nối chặt chẽ giữa các microservices
- Chúng làm phức tạp quy trình triển khai
- Các dịch vụ cần phát triển độc lập
- Code dùng chung có khả năng phân kỳ theo thời gian

### Cách Tiếp Cận Thực Dụng
Nếu việc duy trì code trùng lặp trong nhiều microservices đơn giản hơn việc quản lý thư viện dùng chung, **hãy giữ sự trùng lặp**. Mục tiêu của microservices là tính độc lập và đơn giản - đừng hy sinh những nguyên tắc này vì DRY (Don't Repeat Yourself).

## Kết Luận

Cách tiếp cận Multi-Module Maven Project (BOM) là giải pháp được khuyến nghị để quản lý thư viện dùng chung trong microservices. Tuy nhiên, hãy luôn đánh giá xem thư viện dùng chung có thực sự cần thiết cho trường hợp sử dụng của bạn hay không. Đôi khi, chấp nhận một số trùng lặp code là lựa chọn tốt hơn để duy trì tính độc lập và sự đơn giản trong triển khai microservices.

## Điểm Chính Cần Nhớ

1. **Dự án dùng chung duy nhất** tạo ra fat JARs với các dependency không cần thiết
2. **Nhiều thư viện nhỏ** khó quản lý ở quy mô lớn
3. **Dự án BOM multi-module** cung cấp sự cân bằng tốt nhất giữa tính linh hoạt và khả năng quản lý
4. **Đánh giá cẩn thận** xem thư viện dùng chung có thực sự mang lại lợi ích cho kiến trúc của bạn
5. **Ưu tiên tính độc lập** hơn việc loại bỏ tất cả sự trùng lặp

---

*Tài liệu này dựa trên các best practices cho kiến trúc microservices sử dụng Java và Spring Boot.*