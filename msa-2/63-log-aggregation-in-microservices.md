# Tập Trung Hóa Log trong Kiến Trúc Microservices

## Giới Thiệu

Trong kiến trúc microservices, khả năng quan sát (observability) và giám sát (monitoring) được xây dựng dựa trên ba trụ cột cơ bản:
- **Logging** (Ghi nhật ký)
- **Metrics** (Số liệu)
- **Traces** (Theo dấu)

Để giám sát microservices hiệu quả, chúng ta phải triển khai các khái niệm này để tạo ra dữ liệu giúp hiểu được trạng thái nội bộ của các dịch vụ.

## Hiểu Về Logs

### Logs Là Gì?

Logs là các bản ghi rời rạc về các sự kiện xảy ra trong một ứng dụng phần mềm theo thời gian. Mỗi mục log thường chứa:

- **Timestamp** (Dấu thời gian): Cho biết khi nào sự kiện xảy ra
- **Thông tin sự kiện**: Chi tiết về những gì đã xảy ra
- **Ngữ cảnh**: Dữ liệu ngữ cảnh bổ sung (ID luồng, người dùng, tenant, v.v.)

### Các Câu Hỏi Chính Mà Logs Giúp Trả Lời

- Điều gì đã xảy ra tại một thời điểm cụ thể?
- Luồng (thread) nào đang xử lý sự kiện?
- Người dùng hoặc tenant nào đang trong ngữ cảnh?

### Các Mức Độ Nghiêm Trọng Của Log

Logs được phân loại theo mức độ nghiêm trọng để kiểm soát độ chi tiết trong các môi trường khác nhau:

- **TRACE**: Thông tin chi tiết nhất
- **DEBUG**: Thông tin gỡ lỗi chi tiết
- **INFO**: Thông báo thông tin chung
- **WARN**: Thông báo cảnh báo
- **ERROR**: Sự kiện lỗi

## Thực Hành Tốt Nhất Về Logging

### Logging Dựa Trên Môi Trường

- **Production (Sản xuất)**: Chỉ ghi lại các sự kiện nghiêm trọng (WARN, ERROR) để giảm thiểu tác động hiệu suất
- **Development/Testing (Phát triển/Kiểm thử)**: Sử dụng logging chi tiết hơn (DEBUG, INFO) để có cái nhìn sâu sắc

### Tránh Ghi Log Quá Mức

Ghi log quá nhiều có thể dẫn đến:
- Giảm hiệu suất
- Vấn đề lưu trữ
- Khó tìm thông tin liên quan

**Khuyến nghị**: Ghi lại exceptions và lỗi nghiêm trọng trong production; sử dụng logging toàn diện trong môi trường không phải production.

## Thách Thức Trong Logging Microservices

### Ứng Dụng Nguyên Khối vs Microservices

**Ứng Dụng Nguyên Khối (Monolithic):**
- Tất cả code trong một codebase duy nhất
- Logs được lưu trữ tại một vị trí/máy chủ duy nhất
- Dễ dàng tìm kiếm và khắc phục sự cố

**Kiến Trúc Microservices:**
- Mỗi dịch vụ có logs riêng
- Logs phân tán trên nhiều container và vị trí
- Nhà phát triển phải kiểm tra logs từ nhiều nguồn để gỡ lỗi
- Khắc phục sự cố phức tạp và tốn thời gian

## Giải Pháp Tập Trung Hóa Log

### Tập Trung Hóa Log Là Gì?

Tập trung hóa log là thực hành thu thập logs từ tất cả các dịch vụ và lưu trữ chúng tại một vị trí tập trung duy nhất.

### Lợi Ích

- **Đơn Giản Hóa Khắc Phục Sự Cố**: Nhà phát triển chỉ cần tìm ở một nơi thay vì hàng trăm dịch vụ
- **Giải Quyết Vấn Đề Nhanh Hơn**: Truy cập nhanh vào tất cả logs liên quan
- **Cải Thiện Khả Năng Quan Sát**: Cái nhìn toàn diện về toàn bộ hệ thống

### Các Phương Pháp Triển Khai

#### Phương Pháp Do Developer Xử Lý (Không Khuyến Nghị)

Nhà phát triển viết logic tùy chỉnh để truyền logs từ container đến vị trí tập trung.

**Nhược Điểm:**
- Lãng phí thời gian của nhà phát triển vào logic không liên quan đến business
- Tăng độ phức tạp trong code microservice
- Chuyển hướng sự tập trung khỏi việc giải quyết các vấn đề business thực sự

#### Phương Pháp Khuyến Nghị

Sử dụng các công cụ tập trung hóa log chuyên dụng thực hiện việc tập trung hóa **mà không yêu cầu thay đổi code microservice**.

Phương pháp này cho phép nhà phát triển tập trung vào:
- Các vấn đề của khách hàng
- Logic nghiệp vụ
- Chức năng cốt lõi

## Các Bước Tiếp Theo

Trong các phần tiếp theo, chúng ta sẽ khám phá các sản phẩm và công cụ tập trung hóa log hiện đại cung cấp khả năng logging tập trung sẵn có cho kiến trúc microservices.

## Tài Nguyên Bổ Sung

Để có hướng dẫn chi tiết về triển khai logging trong ứng dụng Spring Boot, bao gồm:
- Thiết lập các mức độ nghiêm trọng khác nhau
- Cấu hình dựa trên môi trường
- Các thực hành tốt nhất về logging

Hãy tham khảo các khóa học Spring Boot toàn diện có phần riêng về triển khai logging.

---

**Điểm Chính**: Tập trung hóa log là điều thiết yếu cho khả năng quan sát microservices. Chọn các công cụ xử lý tập trung hóa log tự động, cho phép team phát triển tập trung vào việc mang lại giá trị business.