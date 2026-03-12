# Giao Tiếp Heartbeat và Eureka Server trong Microservice

## Tổng Quan

Tài liệu này trình bày cách các microservice gửi tín hiệu heartbeat đến Eureka Server và cách thức hoạt động tự động của quá trình đăng ký, cơ chế heartbeat, và hủy đăng ký trong kiến trúc microservices Spring Boot.

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ khám phá demo về các tín hiệu heartbeat được gửi bởi các microservice đến Eureka Server. Đây là một thành phần quan trọng của service discovery và giám sát sức khỏe trong hệ sinh thái microservices.

## Khởi Động Các Microservice

Để bắt đầu với demonstration này, chúng ta cần đảm bảo tất cả các microservice được khởi động theo thứ tự sau:

1. **Microservice Loans (Khoản vay)**
2. **Microservice Cards (Thẻ)**
3. **Microservice Accounts (Tài khoản)**

Khi các microservice này khởi động thành công, chúng sẽ tự động đăng ký thông tin instance của mình với Eureka Server ở chế độ nền.

## Xác Thực Đăng Ký

Bạn có thể xác thực việc đăng ký bằng cách truy cập dashboard Eureka:

1. Điều hướng đến dashboard Eureka
2. Làm mới trang
3. Xác minh rằng tất cả các instance hiện đang được đăng ký với Eureka

## Hiểu Về Cơ Chế Heartbeat

### Chu Kỳ Heartbeat Mặc Định

Các microservice cố gắng gửi tín hiệu heartbeat mỗi **30 giây** (chu kỳ mặc định) đến Eureka Server. Điều này đảm bảo Eureka Server chỉ duy trì thông tin của các instance khỏe mạnh.

### Demonstration Hành Vi Heartbeat

Để demonstration cơ chế heartbeat:

1. **Làm sạch console** của tất cả các microservice (accounts, loans, và cards)
2. **Dừng Eureka Server**
3. **Chờ 30 giây**
4. **Quan sát các exception** trong console của các microservice

## Hành Vi Mong Đợi Khi Eureka Server Bị Dừng

Khi Eureka Server bị dừng, bạn sẽ thấy các exception trong console của các microservice cho biết chúng đang cố gắng gửi heartbeat nhưng Eureka Server không phản hồi.

### Ví Dụ Về Log Messages

Trong console **AccountsApplication**, bạn sẽ tìm thấy:

- Các exception mới liên quan đến lỗi heartbeat
- Thông báo như: "was unable to send Heartbeat to Eureka Server"
- Các request PUT cố gắng cập nhật thông tin heartbeat tại URL của Eureka Server
- Lỗi do Eureka Server bị dừng

Hành vi tương tự có thể được quan sát thấy trong:
- Console **LoansApplication**
- Console **CardsApplication**

## Quản Lý Vòng Đời Service Tự Động

Tích hợp Eureka cung cấp quản lý tự động vòng đời của service:

### 1. Đăng Ký (Khởi Động)
- Trong quá trình khởi động, các microservice tự động đăng ký với Eureka Server
- Không cần can thiệp thủ công

### 2. Heartbeat (Thời Gian Chạy)
- Khi các service đã khởi động, heartbeat được gửi mỗi 30 giây
- Đảm bảo Eureka Server chỉ duy trì thông tin của các instance khỏe mạnh
- Giám sát sức khỏe tự động

### 3. Hủy Đăng Ký (Tắt)
- Trong quá trình shutdown, các microservice tự động hủy đăng ký
- Loại bỏ sạch sẽ khỏi service registry

## Điểm Chính Cần Nhớ

- **Giao Tiếp Tự Động**: Giao tiếp giữa các microservice và Eureka Server diễn ra tự động mà không cần can thiệp thủ công
- **Agent Service Discovery**: Eureka Server hoạt động như một agent service discovery
- **Service Registry**: Các microservice truyền thông tin instance của chúng đến Eureka Service Registry
- **Giám Sát Sức Khỏe**: Cơ chế heartbeat đảm bảo chỉ các service khỏe mạnh được duy trì trong registry

## Các Bước Tiếp Theo

Bây giờ chúng ta đã có:
- Eureka Server hoạt động như một agent service discovery
- Các microservice truyền thông tin instance của chúng đến Eureka Service Registry

Bước tiếp theo là hiểu:
- Cách một microservice có thể dựa vào Eureka Server để khám phá thông tin của các service khác
- Cách load balancing được thực hiện trong quá trình này

Các chủ đề này sẽ được đề cập trong bài giảng tiếp theo.

## Kết Luận

Tích hợp Eureka Server trong microservices Spring Boot cung cấp một cơ chế tự động mạnh mẽ cho việc đăng ký service, giám sát sức khỏe thông qua heartbeat, và hủy đăng ký. Nền tảng này là thiết yếu để xây dựng các kiến trúc microservices có khả năng mở rộng và linh hoạt.