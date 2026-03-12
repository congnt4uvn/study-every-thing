# AWS Elastic Load Balancer - Sticky Sessions (Session Affinity)

## Tổng Quan

Sticky sessions, còn được gọi là session affinity (ái lực phiên), là một tính năng cho phép các yêu cầu từ client được định tuyến nhất quán đến cùng một instance backend thông qua Elastic Load Balancer.

## Cách Hoạt Động của Sticky Sessions

Khi sticky sessions được kích hoạt:
- Client thực hiện các yêu cầu đến load balancer sẽ nhận được phản hồi từ cùng một EC2 instance backend
- Ví dụ, với một ALB và hai EC2 instances:
  - Yêu cầu đầu tiên của Client 1 đi đến Instance 1
  - Các yêu cầu tiếp theo của Client 1 tiếp tục đến Instance 1
  - Tất cả yêu cầu của Client 2 đều đi đến Instance 2
  - Các yêu cầu của Client 3 vẫn nhất quán với instance được chỉ định

Điều này khác với hành vi mặc định của load balancer, vốn phân tán các yêu cầu đều khắp tất cả các EC2 instances có sẵn.

## Các Load Balancer Được Hỗ Trợ

Sticky sessions có thể được kích hoạt cho:
- Classic Load Balancer (CLB)
- Application Load Balancer (ALB)
- Network Load Balancer (NLB)

## Triển Khai Dựa Trên Cookie

Sticky sessions hoạt động thông qua cookies được gửi giữa client và load balancer:
- Cookie chứa thông tin về tính dính (stickiness)
- Cookie có ngày hết hạn
- Khi cookie hết hạn, client có thể được chuyển hướng đến EC2 instance khác

## Trường Hợp Sử Dụng

Trường hợp sử dụng chính của sticky sessions là duy trì dữ liệu phiên người dùng:
- Bảo toàn thông tin phiên trên cùng một backend instance
- Ngăn chặn mất mát dữ liệu quan trọng như thông tin đăng nhập của người dùng
- Đảm bảo tính liên tục của phiên cho người dùng

## Những Điều Cần Lưu Ý

**Mất Cân Bằng Tải Tiềm Ẩn:**
Việc kích hoạt stickiness có thể gây ra phân phối tải không đều trên các EC2 instances backend, đặc biệt nếu một số người dùng "dính" rất lâu với các instances cụ thể.

## Các Loại Cookie

### 1. Application-Based Cookies (Cookie Dựa Trên Ứng Dụng)

**Custom Cookie (Cookie Tùy Chỉnh):**
- Được tạo bởi target (ứng dụng của bạn)
- Có thể bao gồm bất kỳ thuộc tính tùy chỉnh nào mà ứng dụng yêu cầu
- Tên cookie phải được chỉ định riêng cho từng target group
- **Tên dành riêng (KHÔNG sử dụng):**
  - `AWSALB`
  - `AWSALBAPP`
  - `AWSALBTG`

**Application Cookie (Cookie Ứng Dụng):**
- Được tạo bởi chính load balancer
- Tên cookie cho ALB: `AWSALBAPP`

### 2. Duration-Based Cookies (Cookie Dựa Trên Thời Lượng)

- Được tạo bởi load balancer
- Tên cookies:
  - ALB: `AWSALB`
  - CLB: `AWSELB`
- Hết hạn dựa trên một thời lượng cụ thể
- Thời lượng được xác định bởi load balancer

**Sự Khác Biệt Chính:**
- Application-based cookies: Thời lượng được chỉ định bởi ứng dụng
- Duration-based cookies: Thời lượng được chỉ định bởi load balancer

## Hướng Dẫn Thực Hành

### Kích Hoạt Sticky Sessions

1. Điều hướng đến target group của bạn
2. Nhấp vào **Actions**
3. Chọn **Edit attributes**
4. Cuộn xuống **Target selection configuration**
5. Bật **Stickiness**

### Các Tùy Chọn Stickiness

**Tùy Chọn 1: Load Balancer Generated Cookie**
- Đặt thời lượng từ 1 giây đến 7 ngày
- Mặc định: 1 ngày

**Tùy Chọn 2: Application-Based Cookie**
- Cài đặt thời lượng tương tự
- Yêu cầu tên cookie ứng dụng tùy chỉnh (ví dụ: `MYCUSTOMCOOKIEAPP`)
- Tên này giúp load balancer áp dụng stickiness một cách chính xác

### Xác Minh Sticky Sessions

1. Mở công cụ dành cho nhà phát triển của trình duyệt (tab Network)
2. Làm mới trang nhiều lần
3. Quan sát rằng các yêu cầu luôn đi đến cùng một instance
4. Kiểm tra request headers:
   - **Response cookie:** Hiển thị thời gian hết hạn và giá trị của cookie
   - **Request cookie:** Hiển thị cookie được gửi với mỗi yêu cầu

### Vô Hiệu Hóa Sticky Sessions

1. Quay lại target group của bạn
2. Chỉnh sửa attributes
3. Tắt stickiness
4. Lưu thay đổi để khôi phục hành vi cân bằng tải bình thường

## Công Cụ Dành Cho Nhà Phát Triển Trình Duyệt

Để truy cập công cụ dành cho nhà phát triển web:
- Nhấp vào **Web Developer** → **Web Developer Tools**
- Hoặc sử dụng phím tắt (giống nhau cho Chrome và Firefox)
- Điều hướng đến tab **Network**
- Xem thông tin request/response bao gồm cookies

## Tóm Tắt

- Sticky sessions định tuyến các yêu cầu của client đến cùng một backend instance
- Được triển khai bằng cookies với ngày hết hạn
- Hai loại cookie chính: dựa trên ứng dụng và dựa trên thời lượng
- Hữu ích cho việc duy trì dữ liệu phiên nhưng có thể gây mất cân bằng tải
- Có thể dễ dàng kích hoạt/vô hiệu hóa ở cấp độ target group
- Hoạt động với CLB, ALB và NLB