# AWS Application Load Balancer - Các Khái Niệm Nâng Cao: Bảo Mật và Quy Tắc

## Tổng Quan

Hướng dẫn này đề cập đến các khái niệm nâng cao cho AWS Application Load Balancer (ALB), tập trung vào hai lĩnh vực chính:
1. Bảo mật mạng với security groups
2. Các quy tắc listener của Application Load Balancer

## Bảo Mật Mạng cho Load Balancers

### Hiểu về Kiến Trúc Bảo Mật

Khi làm việc với Application Load Balancers, bạn có nhiều lớp bảo mật:
- **Load Balancer Security Group**: Kiểm soát quyền truy cập vào chính load balancer
- **EC2 Instance Security Groups**: Kiểm soát quyền truy cập vào các EC2 instances của bạn

### Vấn Đề: Truy Cập Trực Tiếp EC2 Instance

Theo mặc định, nếu các EC2 instances của bạn có quy tắc security group cho phép lưu lượng HTTP từ mọi nơi, người dùng có thể truy cập trực tiếp chúng bằng địa chỉ IP công khai, bỏ qua hoàn toàn load balancer.

### Giải Pháp: Hạn Chế Lưu Lượng Chỉ Qua Load Balancer

Để đảm bảo tất cả lưu lượng đi qua load balancer của bạn:

#### Bước 1: Điều Hướng đến EC2 Security Groups

1. Truy cập EC2 instances của bạn
2. Chọn **Security Groups**
3. Tìm security group của instance (ví dụ: `launch-wizard-1`)

#### Bước 2: Chỉnh Sửa Inbound Rules

1. Nhấp **Edit inbound rules**
2. Tìm quy tắc HTTP
3. Xóa quy tắc hiện có cho phép lưu lượng từ `0.0.0.0/0` (mọi nơi)

#### Bước 3: Thêm Load Balancer Security Group

1. Thêm một quy tắc mới
2. Chọn **HTTP** làm loại
3. Thay vì chọn CIDR block, chọn **Security Group** làm nguồn
4. Chọn security group của load balancer từ danh sách thả xuống
5. Lưu quy tắc

### Kết Quả

- **Truy cập trực tiếp vào EC2 instances**: Sẽ timeout và thất bại
- **Truy cập qua load balancer**: Sẽ tiếp tục hoạt động bình thường

Cấu hình này đảm bảo rằng các EC2 instances của bạn chỉ chấp nhận lưu lượng từ Application Load Balancer, cải thiện đáng kể tính bảo mật.

## Quy Tắc Listener của Application Load Balancer

### Hiểu về Listener Rules

Listener rules cho phép bạn định tuyến các yêu cầu đến các target groups khác nhau dựa trên nhiều điều kiện khác nhau. Điều này cho phép các mẫu định tuyến lưu lượng phức tạp trong một load balancer duy nhất.

### Quy Tắc Mặc Định

Mỗi listener có một quy tắc mặc định chuyển tiếp tất cả các yêu cầu đến một target group được chỉ định. Đây là quy tắc bắt tất cả cho các yêu cầu không khớp với bất kỳ quy tắc nào khác.

### Tạo Quy Tắc Tùy Chỉnh

#### Bước 1: Truy Cập Cấu Hình Listener

1. Điều hướng đến ALB của bạn
2. Vào tab **Listeners**
3. Nhấp vào listener của bạn
4. Cuộn xuống **Listener rules**

#### Bước 2: Thêm Quy Tắc Mới

1. Nhấp **Add rules**
2. Đặt tên cho quy tắc của bạn (ví dụ: `DemoRule`)

#### Bước 3: Định Nghĩa Điều Kiện

Bạn có thể lọc các yêu cầu dựa trên nhiều điều kiện:

- **Host header**: Khớp với các domain cụ thể (ví dụ: `*.example.com`, `myapp.example.com`)
- **Path**: Khớp với đường dẫn URL (ví dụ: `/error`, `/api/*`)
- **HTTP request method**: Khớp với các phương thức cụ thể (GET, POST, v.v.)
- **Source IP**: Khớp với các yêu cầu từ địa chỉ IP cụ thể
- **Query string**: Khớp với các tham số truy vấn cụ thể
- **HTTP headers**: Khớp với các giá trị header cụ thể

**Ví dụ**: Tạo quy tắc dựa trên path với điều kiện `/error`

#### Bước 4: Định Nghĩa Hành Động

Sau khi một điều kiện được khớp, bạn có thể thực hiện một số hành động:

1. **Forward to target groups**: Định tuyến đến một hoặc nhiều target groups
2. **Redirect**: Chuyển hướng đến URL khác với tùy chỉnh:
   - Các thành phần URI hoặc URL đầy đủ
   - Giao thức (HTTP/HTTPS)
   - Mã trạng thái
   - Tùy chỉnh host, path và query

3. **Return fixed response**: Trả về phản hồi tùy chỉnh (ví dụ của chúng ta)
   - Mã trạng thái: `404`
   - Loại nội dung: `text/plain`
   - Nội dung phản hồi: `Not found, custom error`

#### Bước 5: Đặt Độ Ưu Tiên

- Các quy tắc được đánh giá theo thứ tự ưu tiên (1 đến 50,000)
- Số thấp hơn = ưu tiên cao hơn
- Quy tắc khớp đầu tiên được áp dụng
- **Ví dụ**: Đặt độ ưu tiên là `5`

#### Bước 6: Xem Xét và Tạo

Xem xét cấu hình quy tắc của bạn và tạo nó.

### Kiểm Tra Quy Tắc

1. Sao chép tên DNS của load balancer
2. Thêm `/error` vào URL
3. Truy cập URL
4. Kết quả mong đợi: `Not found, custom error` với mã trạng thái 404

Điều này xác nhận rằng:
- Yêu cầu khớp với mẫu path `/error`
- Hành động fixed response được kích hoạt
- Phản hồi 404 với văn bản tùy chỉnh được trả về

## Những Điểm Chính Cần Nhớ

1. **Thực Hành Bảo Mật Tốt Nhất**: Cấu hình security groups để đảm bảo EC2 instances chỉ chấp nhận lưu lượng từ load balancer
2. **Định Tuyến Linh Hoạt**: Sử dụng listener rules để tạo logic định tuyến phức tạp dựa trên nhiều thuộc tính yêu cầu khác nhau
3. **Độ Ưu Tiên Quy Tắc**: Hiểu rằng các quy tắc được đánh giá theo thứ tự ưu tiên, với quy tắc khớp đầu tiên được áp dụng
4. **Nhiều Hành Động**: Tận dụng các loại hành động khác nhau (forward, redirect, fixed response) cho các trường hợp sử dụng khác nhau

## Kết Luận

Các tính năng ALB nâng cao này cho phép bạn xây dựng kiến trúc an toàn, linh hoạt và có khả năng mở rộng. Bằng cách cấu hình đúng security groups và listener rules, bạn có thể kiểm soát luồng lưu lượng và triển khai logic định tuyến phức tạp mà không cần sửa đổi mã ứng dụng của bạn.