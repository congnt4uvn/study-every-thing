# Quản Lý Cấu Hình Trong Microservices

## Giới Thiệu

Quản lý cấu hình là một trong những thách thức quan trọng khi xây dựng microservices hoặc ứng dụng cloud-native. Phần này khám phá các thách thức, giải pháp có sẵn và các phương pháp tốt nhất để quản lý cấu hình trong kiến trúc microservices.

## Các Thách Thức Chính

### 1. Tách Biệt Cấu Hình Khỏi Logic Nghiệp Vụ

**Câu hỏi:** Làm thế nào để tách biệt các cấu hình hoặc thuộc tính khỏi logic nghiệp vụ trong microservices?

**Tại sao điều này quan trọng:**
- Không tách biệt thì không thể tái sử dụng cùng một Docker image cho nhiều môi trường
- Gộp logic nghiệp vụ và cấu hình lại với nhau đòi hỏi phải tạo Docker image riêng cho mỗi môi trường
- Phương pháp này không được khuyến nghị và trở nên khó quản lý với nhiều môi trường

**Phương pháp tốt nhất:** Sử dụng cùng một Docker image cho tất cả môi trường, bao gồm cả production, bằng cách đưa cấu hình ra bên ngoài.

### 2. Tiêm Cấu Hình Tại Runtime

**Câu hỏi:** Làm thế nào để tiêm các cấu hình hoặc thuộc tính tại runtime trong quá trình khởi động microservice?

**Các điểm cần xem xét:**
- Các thuộc tính nhạy cảm như thông tin xác thực không thể được hardcode trong cấu hình hoặc logic nghiệp vụ
- Cấu hình phải được tiêm vào microservices trong quá trình khởi động service
- Bảo mật và tính linh hoạt là tối quan trọng

### 3. Kho Lưu Trữ Cấu Hình Tập Trung

**Câu hỏi:** Làm thế nào để duy trì các cấu hình trong kho lưu trữ tập trung với quản lý phiên bản?

**Vấn đề:**
- Ứng dụng monolithic thường chỉ có 1-2 ứng dụng, giúp việc quản lý cấu hình thủ công khả thi
- Với hàng trăm microservices, quản lý cấu hình thủ công trở nên cực kỳ phức tạp
- Kiểm soát phiên bản và khả năng kiểm tra là thiết yếu

**Giải pháp:** Duy trì tất cả thuộc tính trong kho lưu trữ tập trung với hỗ trợ quản lý phiên bản phù hợp.

## Các Giải Pháp Có Sẵn

Hệ sinh thái Spring Boot cung cấp nhiều giải pháp cho quản lý cấu hình:

### 1. Cấu Hình Spring Boot Cơ Bản
- Cấu hình Spring Boot với các thuộc tính liên quan
- Sử dụng Spring Profiles cho các cấu hình theo môi trường cụ thể
- **Cấp độ:** Giải pháp cơ bản

### 2. Cấu Hình Bên Ngoài
- Áp dụng cấu hình bên ngoài cho ứng dụng Spring Boot
- Cấu hình được lưu trữ bên ngoài ứng dụng
- **Cấp độ:** Giải pháp trung gian

### 3. Spring Cloud Config Server
- Triển khai một configuration server riêng biệt
- Sử dụng dự án Spring Cloud Config Server
- **Cấp độ:** Giải pháp nâng cao và được khuyến nghị

## Phương Pháp Truyền Thống vs. Microservices

### Cấu Hình Ứng Dụng Truyền Thống

**Đặc điểm:**
- Source code và file cấu hình được đóng gói cùng nhau
- Cần rebuild cho mỗi môi trường với các cấu hình khác nhau
- Không đảm bảo hành vi nhất quán giữa các môi trường
- Logic nghiệp vụ có thể khác nhau giữa các môi trường

**Hạn chế:**
- Hoạt động cho ứng dụng monolithic với một ứng dụng
- Không mở rộng được cho kiến trúc microservices
- Nhiều lần build tạo ra sự phức tạp và không nhất quán

### Cấu Hình Microservices (Phương Pháp 15-Factor)

**Nguyên tắc:** Tất cả các cấu hình thay đổi giữa các lần deployment phải được cung cấp bên ngoài build component.

**Ví dụ về Cấu Hình Bên Ngoài:**
- Thông tin xác thực
- URL của các service
- Resource handles
- Cài đặt theo môi trường cụ thể

**Lợi ích:**
- Các artifact của ứng dụng vẫn bất biến trên tất cả môi trường
- Sử dụng một Docker image duy nhất trên tất cả môi trường
- Cấu hình được tiêm từ các vị trí bên ngoài tại runtime

## Quy Trình Được Khuyến Nghị

### Quy Trình Build và Deployment

```
1. Source Code (GitHub Repository)
   ↓
2. Biên dịch & Đóng gói (Build chung)
   ↓
3. Tạo Docker Image (Artifact bất biến)
   ↓
4. Tiêm Cấu Hình tại Runtime
   ↓
5. Triển khai đến Môi trường Đích
```

### Deployment Theo Môi Trường Cụ Thể

**Môi Trường Development:**
- Sử dụng cùng Docker image
- Tiêm cấu hình development tại runtime
- Triển khai đến hạ tầng development

**Môi Trường QA:**
- Sử dụng cùng Docker image
- Tiêm cấu hình QA tại runtime
- Triển khai đến hạ tầng QA

**Môi Trường Production:**
- Sử dụng cùng Docker image
- Tiêm cấu hình production tại runtime
- Triển khai đến hạ tầng production

## Những Điểm Chính Cần Ghi Nhớ

1. **Tách biệt là Quan trọng:** Luôn tách cấu hình khỏi logic nghiệp vụ
2. **Tính Bất Biến:** Build một lần, deploy mọi nơi với cùng một artifact
3. **Tiêm từ Bên Ngoài:** Tiêm cấu hình tại runtime dựa trên môi trường đích
4. **Quản Lý Tập Trung:** Sử dụng kho lưu trữ tập trung cho tất cả cấu hình
5. **Kiểm Soát Phiên Bản:** Duy trì versioning cho tất cả thay đổi cấu hình
6. **Bảo Mật:** Xử lý dữ liệu nhạy cảm thông qua runtime injection, không bao giờ hardcode

## Các Bước Tiếp Theo

Phần này sẽ đề cập:
- Trình diễn chi tiết về tất cả các phương pháp cấu hình
- Ưu điểm và nhược điểm của từng phương pháp
- Các phương pháp hay nhất và khuyến nghị
- Thay đổi code thực tế trong các microservices accounts, loans và cards

## Kết Luận

Quản lý cấu hình là thiết yếu để xây dựng microservices có khả năng mở rộng và dễ bảo trì. Bằng cách tuân theo phương pháp 15-factor và đưa cấu hình ra bên ngoài, chúng ta đảm bảo tính nhất quán, bảo mật và hiệu quả hoạt động trên tất cả các môi trường.

---

**Ghi chú:** Tài liệu này là một phần của khóa học microservices toàn diện sử dụng Spring Boot, bao gồm các triển khai thực tế và các thách thức trong thực tế.