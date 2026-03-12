# Ứng Dụng Cloud Native - Định Nghĩa

## Tổng Quan

Bài giảng này giới thiệu các khái niệm cơ bản về ứng dụng cloud native, bao gồm định nghĩa, đặc điểm và mối quan hệ với kiến trúc microservices. Hiểu những khái niệm này là rất quan trọng đối với bất kỳ developer microservice nào, vì chúng tạo nền tảng cho việc xây dựng các ứng dụng hiện đại, có khả năng mở rộng.

## Các Chủ Đề Được Đề Cập

- Định nghĩa về Ứng dụng Cloud Native
- Đặc điểm của Ứng dụng Cloud Native
- Giới thiệu về Phương pháp luận 12 Factor và 15 Factor
- Mối quan hệ giữa Ứng dụng Cloud Native và Microservices

## Ứng Dụng Cloud Native Là Gì?

### Định Nghĩa Đơn Giản (Phi Kỹ Thuật)

Ứng dụng Cloud Native là các ứng dụng phần mềm được thiết kế và phát triển đặc biệt để tận dụng các nguyên tắc điện toán đám mây và khai thác tối đa các công nghệ và dịch vụ cloud native.

Những ứng dụng này:
- Được xây dựng và tối ưu hóa để chạy trong bất kỳ môi trường cloud nào
- Được thiết kế để tận dụng các lợi thế của cloud như:
  - **Khả năng mở rộng (Scalability)** - khả năng phát triển theo nhu cầu
  - **Tính đàn hồi (Elasticity)** - khả năng tự động giảm hoặc tăng tài nguyên
  - **Tính linh hoạt (Flexibility)** - khả năng thích nghi với các yêu cầu thay đổi

> **Nói một cách đơn giản**: Ứng dụng cloud native được xây dựng cho môi trường cloud để các tổ chức có thể tận dụng hoàn toàn các dịch vụ và công nghệ của nhà cung cấp cloud.

### Định Nghĩa Chính Thức (Kỹ Thuật)

Theo **Cloud Native Computing Foundation (CNCF)**:

> *"Các công nghệ cloud native trao quyền cho các tổ chức xây dựng và chạy các ứng dụng có khả năng mở rộng trong các môi trường động hiện đại như public cloud, private cloud và hybrid cloud."*

## Các Công Nghệ Chính Trong Ứng Dụng Cloud Native

Ứng dụng cloud native tận dụng một số công nghệ chính:

1. **Containers** - Đóng gói ứng dụng nhẹ, dễ di chuyển
2. **Service Meshes** - Lớp cơ sở hạ tầng cho giao tiếp giữa các service
3. **Microservices** - Phong cách kiến trúc với các service kết nối lỏng lẻo
4. **Immutable Infrastructure** - Cơ sở hạ tầng được thay thế thay vì sửa đổi
5. **Declarative APIs** - APIs mô tả trạng thái mong muốn của hệ thống

## Tính Linh Hoạt Của Môi Trường Cloud

Ứng dụng cloud native có thể chạy trên bất kỳ loại môi trường cloud nào:

- **Public Cloud** (AWS, Azure, GCP)
- **Private Cloud** (Trung tâm dữ liệu tại chỗ)
- **Hybrid Cloud** (Kết hợp public và private)

Tính linh hoạt này ngăn chặn việc **bị khóa với nhà cung cấp** (vendor lock-in) cụ thể nào.

## Lợi Ích Của Ứng Dụng Cloud Native

### 1. Hệ Thống Có Khả Năng Phục Hồi (Resilient)
- Có thể chịu đựng các lỗi
- Khả năng tự phục hồi
- Tính khả dụng cao

### 2. Hệ Thống Dễ Quản Lý (Manageable)
- Dễ dàng triển khai và cập nhật
- Đơn giản để giám sát và bảo trì
- Hoạt động tự động

### 3. Hệ Thống Có Thể Quan Sát (Observable)
- Khả năng hiển thị hoàn toàn về hành vi ứng dụng
- Giám sát và ghi log thời gian thực
- Số liệu và truy vết toàn diện

### 4. Kiến Trúc Kết Nối Lỏng Lẻo (Loosely Coupled)
- Các service độc lập có thể phát triển riêng biệt
- Dễ dàng kiểm tra từng thành phần
- Giảm sự phụ thuộc giữa các thành phần

## Lợi Ích Trong Phát Triển

Với các công nghệ cloud native và tự động hóa mạnh mẽ, các tổ chức đạt được:

- **Triển Khai Thường Xuyên** - Phát hành thay đổi nhanh chóng và an toàn
- **Thay Đổi Có Thể Dự Đoán** - Quy trình triển khai nhất quán
- **Giảm Thiểu Công Việc Thủ Công** - Giảm công việc thủ công thông qua tự động hóa
- **Thay Đổi Tác Động Cao** - Khả năng đổi mới nhanh chóng
- **Giảm Lỗi** - Kiểm tra và cô lập tốt hơn ngăn chặn các vấn đề hồi quy

## Khả Năng Cải Tiến Nhanh Chóng

Ứng dụng cloud native cho phép các developer:
- Thực hiện các thay đổi nhỏ mà không ảnh hưởng đến toàn bộ hệ thống
- Phát triển các cải tiến mới một cách nhanh chóng
- Triển khai cập nhật với rủi ro tối thiểu
- Kiểm tra các thay đổi một cách độc lập

Điều này có thể thực hiện được nhờ tính chất kết nối lỏng lẻo của kiến trúc.

## Điểm Chính Cần Nhớ

Khi giải thích về ứng dụng cloud native:

- **Đối với đối tượng phi kỹ thuật**: Sử dụng định nghĩa đơn giản tập trung vào tối ưu hóa cloud và các lợi thế
- **Đối với đối tượng kỹ thuật**: Tham khảo định nghĩa chính thức của CNCF và đề cập đến các công nghệ cụ thể

## Nội Dung Tiếp Theo

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá:
- Ứng dụng cloud native liên quan đến microservices như thế nào
- Phương pháp luận 12 Factor và 15 Factor
- Các phương pháp hay nhất để xây dựng ứng dụng cloud native
- Triển khai thực tế với Spring Boot

---

## Tóm Tắt

Ứng dụng cloud native đại diện cho một cách tiếp cận hiện đại trong việc xây dựng phần mềm, tận dụng tối đa khả năng của điện toán đám mây. Bằng cách sử dụng các công nghệ như containers, microservices và declarative APIs, những ứng dụng này đạt được khả năng phục hồi, khả năng quản lý và khả năng quan sát trong khi vẫn duy trì tính linh hoạt trên các môi trường cloud khác nhau. Hiểu những nguyên tắc này là rất quan trọng để phát triển các hệ thống dựa trên microservices thành công.