# Định nghĩa và Tổng quan về Microservices

## Giới thiệu

Trong bài giảng này, chúng ta sẽ khám phá định nghĩa chính thức về microservices, cung cấp cho bạn một giải thích rõ ràng và súc tích mà bạn có thể sử dụng khi giao tiếp với cả các bên liên quan kỹ thuật và phi kỹ thuật.

## Định nghĩa Chính thức

Định nghĩa về microservices, được đưa ra bởi **James Lewis và Martin Fowler** trong bài viết blog có ảnh hưởng của họ, phát biểu rằng:

> **Microservices là một cách tiếp cận để phát triển một ứng dụng đơn lẻ như một bộ các dịch vụ nhỏ.**

### Các Đặc điểm Chính

1. **Bộ các Dịch vụ Nhỏ**
   - Một ứng dụng đơn lẻ được chia nhỏ thành nhiều dịch vụ nhỏ, tập trung
   - Ví dụ: Ứng dụng web EasyBank có thể được phát triển thành các dịch vụ riêng biệt:
     - Dịch vụ Tài khoản (Accounts)
     - Dịch vụ Vay vốn (Loans)
     - Dịch vụ Thẻ (Cards)

2. **Các Tiến trình Độc lập**
   - Mỗi dịch vụ chạy trong tiến trình riêng của nó
   - Các dịch vụ được cách ly và tự chứa

3. **Giao tiếp Nhẹ**
   - Các dịch vụ giao tiếp bằng cách sử dụng các cơ chế nhẹ
   - Các giao thức phổ biến bao gồm REST APIs
   - Cho phép giao tiếp liền mạch giữa các dịch vụ

4. **Thiết kế Hướng Nghiệp vụ**
   - Microservices được xây dựng xung quanh các khả năng nghiệp vụ
   - Mỗi dịch vụ đại diện cho một lĩnh vực nghiệp vụ cụ thể
   - Phù hợp với cấu trúc tổ chức và chức năng kinh doanh

5. **Triển khai Độc lập**
   - Các dịch vụ có thể được triển khai độc lập
   - Máy móc triển khai tự động hoàn toàn
   - Không cần triển khai lại toàn bộ ứng dụng cho các thay đổi trong một dịch vụ

## Tự động hóa và CI/CD

Một trong những lợi thế quan trọng nhất của microservices là khả năng tự động hóa toàn bộ quy trình triển khai:

- **Tự động Build**: Ngay khi một lập trình viên commit code vào kho lưu trữ của microservice, quá trình build được kích hoạt tự động
- **Tích hợp Liên tục**: Các bản build tự động được triển khai đến môi trường phát triển và UAT
- **Triển khai Liên tục**: Triển khai production cũng có thể được tự động hóa bằng cách sử dụng khái niệm CI/CD
- **Hiệu quả**: Giảm can thiệp thủ công và tăng tốc chu kỳ phát hành

## Tóm tắt Lợi ích

Kiến trúc Microservices mang lại nhiều lợi thế:

- **Khả năng Mở rộng**: Các dịch vụ riêng lẻ có thể được mở rộng độc lập
- **Linh hoạt**: Ngăn xếp công nghệ có thể thay đổi cho từng dịch vụ
- **Khả năng Phục hồi**: Lỗi trong một dịch vụ không làm sập toàn bộ ứng dụng
- **Phát triển Nhanh hơn**: Các nhóm có thể làm việc trên các dịch vụ khác nhau đồng thời
- **Bảo trì Dễ dàng**: Codebase nhỏ hơn dễ hiểu và bảo trì hơn

## Tham khảo Nhanh

Khi được hỏi "Microservices là gì?" bạn có thể sử dụng định nghĩa súc tích này:

*"Microservices là một cách tiếp cận để phát triển ứng dụng như một bộ các dịch vụ nhỏ, độc lập chạy trong các tiến trình riêng của chúng, giao tiếp qua các cơ chế nhẹ, được xây dựng xung quanh các khả năng nghiệp vụ và có thể được triển khai độc lập thông qua các quy trình triển khai tự động."*

## Kết luận

Định nghĩa này cung cấp một nền tảng vững chắc để hiểu kiến trúc microservices. Cho dù bạn đang giải thích khái niệm này cho người dùng nghiệp vụ, khách hàng hay các thành viên nhóm kỹ thuật, định nghĩa chính thức này bao gồm tất cả các khía cạnh thiết yếu của microservices.

---

**Bối cảnh Khóa học**: Bài giảng này là một phần của khóa học toàn diện về kiến trúc microservices sử dụng Java và Spring Boot, nơi chúng ta sẽ đi sâu hơn vào các chi tiết triển khai và các phương pháp hay nhất.