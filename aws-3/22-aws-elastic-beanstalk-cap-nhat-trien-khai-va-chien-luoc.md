# AWS Elastic Beanstalk - Cập Nhật Triển Khai và Chiến Lược

## Giới Thiệu

Hướng dẫn này bao gồm các chiến lược triển khai AWS Elastic Beanstalk, bao gồm các chính sách triển khai khác nhau, cập nhật cấu hình và kỹ thuật hoán đổi môi trường.

## Cấu Hình Triển Khai

### Truy Cập Cài Đặt Triển Khai

1. Điều hướng đến **Configuration** (Cấu hình) trong menu bên trái
2. Chọn môi trường production của bạn
3. Cuộn xuống **Updates, Monitoring, and Logging** (Cập nhật, Giám sát và Ghi log)
4. Nhấp vào **Edit** (Chỉnh sửa)
5. Tìm phần **Rolling Updates and Deployments** (Cập nhật và Triển khai Tuần tự)

## Các Chính Sách Triển Khai Ứng Dụng

### 1. All at Once (Tất Cả Cùng Lúc)

- **Mô tả**: Triển khai cập nhật code đến tất cả các instance đồng thời
- **Downtime**: Có - các instance sẽ ngừng hoạt động trong quá trình triển khai
- **Tốc độ**: Phương pháp triển khai nhanh nhất
- **Cài đặt**: Các tùy chọn Fixed và Percentage bị vô hiệu hóa (không áp dụng)
- **Trường hợp sử dụng**: Môi trường phát triển hoặc khi có thể chấp nhận downtime

### 2. Rolling (Tuần Tự)

- **Mô tả**: Tắt một số instance, nâng cấp chúng, sau đó chuyển sang batch tiếp theo
- **Downtime**: Một phần - một số instance vẫn khả dụng
- **Tùy chọn Batch Size**:
  - **Percentage** (Phần trăm): ví dụ, 30% instance mỗi lần
  - **Fixed** (Cố định): ví dụ, 1 instance mỗi lần
- **Trường hợp sử dụng**: Môi trường production với lưu lượng truy cập vừa phải

### 3. Rolling with Additional Batch (Tuần Tự với Batch Bổ Sung)

- **Mô tả**: Thêm các EC2 instance tạm thời, triển khai lên chúng, sau đó tiếp tục với các batch
- **Dung lượng**: Duy trì đầy đủ dung lượng trong suốt quá trình triển khai
- **Chi phí**: Tăng chi phí do các instance bổ sung tạm thời
- **Cài đặt**: Có thể đặt kích thước batch theo percentage hoặc fixed
- **Trường hợp sử dụng**: Môi trường production yêu cầu dung lượng đầy đủ trong quá trình cập nhật

### 4. Immutable (Bất Biến)

- **Mô tả**: Tạo một bộ instance hoàn toàn mới, triển khai lên chúng, sau đó xóa các instance cũ
- **Downtime**: Không có downtime
- **Quy trình**:
  1. Tạo Auto Scaling Group tạm thời
  2. Khởi chạy các instance mới với ứng dụng đã cập nhật
  3. Xác minh tình trạng của các instance mới
  4. Thêm các instance mới vào load balancer
  5. Tách các instance khỏi ASG tạm thời
  6. Gắn các instance vào ASG vĩnh viễn
  7. Kết thúc các instance cũ
- **Cài đặt**: Các tùy chọn Fixed và Percentage không áp dụng
- **Trường hợp sử dụng**: Môi trường production quan trọng yêu cầu zero downtime

### 5. Traffic Splitting (Phân Chia Lưu Lượng)

- **Mô tả**: Phân chia lưu lượng đến một phần trăm phiên bản ứng dụng mới trong một khoảng thời gian xác định trước khi nâng cấp hoàn toàn
- **Trường hợp sử dụng**: Kiểm thử Canary và triển khai dần dần

## Cập Nhật Cấu Hình

Cập nhật cấu hình áp dụng khi:
- Cập nhật cấu hình EC2 instance
- Sửa đổi cấu hình VPC
- Thực hiện các thay đổi cơ sở hạ tầng khác yêu cầu thay thế instance

**Các Tùy Chọn Khả Dụng**:
- Rolling (Tuần tự)
- Immutable (Bất biến)

> **Lưu ý**: Kỳ thi tập trung chủ yếu vào các chính sách triển khai ứng dụng thay vì cập nhật cấu hình.

## Thực Hành: Triển Khai với Chiến Lược Immutable

### Bước 1: Chuẩn Bị Ứng Dụng

1. Tải xuống ứng dụng Node.js mẫu từ hướng dẫn AWS
2. Cấu trúc ứng dụng bao gồm:
   - `index.html` - Trang chào mừng với styling
   - `app.js` - Cấu hình server Node.js
   - `cron.yaml` - Lập lịch tác vụ (tùy chọn)
   - `.ebextensions/` - Thư mục tùy chỉnh Elastic Beanstalk
   - `.gitignore` - File ignore Git

### Bước 2: Tùy Chỉnh Ứng Dụng

Sửa đổi màu nền trong `index.html`:
```html
<!-- Thay đổi background-color từ xanh lá sang xanh dương -->
<style>
  background-color: blue;
  /* các style khác */
</style>
```

### Bước 3: Đóng Gói Ứng Dụng

Tạo file zip chứa tất cả các file ứng dụng. Đảm bảo đóng gói đúng cách để tránh các vấn đề tương thích với Elastic Beanstalk.

### Bước 4: Triển Khai Ứng Dụng

1. Nhấp vào **Upload and Deploy** (Tải lên và Triển khai)
2. Chọn file ứng dụng (ví dụ: `nodejs-v2-blue.zip`)
3. Nhập nhãn phiên bản (ví dụ: "MyApplication-Blue")
4. Chọn tùy chọn triển khai: **Immutable** (hoặc ghi đè bằng các tùy chọn khác)
5. Nhấp vào **Submit** (Gửi)

### Bước 5: Theo Dõi Tiến Trình Triển Khai

Quy trình triển khai theo các bước sau:

1. **Khởi chạy instance xác minh**: Tạo một instance với cài đặt mới để xác minh tình trạng
2. **Tạo Auto Scaling Group tạm thời**: Chứa instance mới
3. **Kiểm tra tình trạng**: Chờ instance vượt qua kiểm tra tình trạng load balancer
4. **Gắn vào load balancer**: Thêm instance mới vào load balancer
5. **Tách khỏi ASG tạm thời**: Loại bỏ các instance khỏi Auto Scaling Group tạm thời
6. **Gắn vào ASG vĩnh viễn**: Thêm các instance vào Auto Scaling Group vĩnh viễn
7. **Cấu hình sau triển khai**: Áp dụng các cấu hình cuối cùng
8. **Kết thúc các instance cũ**: Loại bỏ các instance cũ và ASG tạm thời
9. **Hoàn thành triển khai**: Phiên bản mới được triển khai hoàn toàn

## Hoán Đổi Môi Trường

### Các Trường Hợp Sử Dụng

- Triển khai Blue/Green
- Kiểm thử các phiên bản mới trong môi trường giống production
- Cập nhật lớn không có downtime

### Quy Trình

1. **Sao chép môi trường**: Tạo bản sao của môi trường production
2. **Triển khai lên môi trường mới**: Triển khai và kiểm thử phiên bản ứng dụng mới (ví dụ: "prod-v2")
3. **Hoán đổi domain môi trường**: Trao đổi URL giữa các môi trường
4. **Kết quả**: Phiên bản mới trở thành production, phiên bản cũ trở thành staging/backup

### Cách Hoán Đổi Môi Trường

1. Chọn môi trường nguồn (ví dụ: prod)
2. Nhấp vào **Actions** → **Swap Environment URLs** (Hoán đổi URL Môi trường)
3. Chọn môi trường đích (ví dụ: dev)
4. Nhấp vào **Swap** (Hoán đổi)
5. Chờ cập nhật DNS lan truyền (có thể mất vài phút)

### Ví Dụ Kịch Bản

**Trước Khi Hoán Đổi**:
- Môi trường Prod: Phiên bản Blue
- Môi trường Dev: Phiên bản Green

**Sau Khi Hoán Đổi**:
- Môi trường Prod: Phiên bản Green
- Môi trường Dev: Phiên bản Blue

> **Lưu ý**: Việc lan truyền DNS có thể gây ra sự chậm trễ tạm thời trong việc phản ánh các thay đổi.

## Các Phương Pháp Hay Nhất

1. **Sử dụng triển khai Immutable** cho các môi trường production yêu cầu zero downtime
2. **Kiểm thử trong môi trường đã sao chép** trước khi hoán đổi sang production
3. **Theo dõi các sự kiện triển khai** để theo dõi tiến trình và xác định vấn đề
4. **Hiểu về độ trễ lan truyền DNS** khi hoán đổi môi trường
5. **Chọn kích thước batch phù hợp** cho các triển khai tuần tự dựa trên các mẫu lưu lượng
6. **Xem xét chi phí** khi sử dụng triển khai batch bổ sung

## Tóm Tắt

AWS Elastic Beanstalk cung cấp nhiều chiến lược triển khai để phù hợp với các yêu cầu khác nhau:

- **All at Once**: Nhanh nhất, nhưng gây ra downtime
- **Rolling**: Cập nhật dần dần với tính khả dụng một phần
- **Rolling with Additional Batch**: Duy trì dung lượng nhưng tăng chi phí
- **Immutable**: Zero downtime với làm mới hoàn toàn cơ sở hạ tầng
- **Traffic Splitting**: Triển khai dần dần với kiểm thử canary

Hoán đổi môi trường cho phép triển khai blue/green và cập nhật production an toàn thông qua chuyển đổi URL.

## Tài Nguyên Bổ Sung

- [Tài Liệu AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/)
- [Chính Sách và Cài Đặt Triển Khai](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.rolling-version-deploy.html)
- [Cấu Hình Môi Trường](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customize-containers.html)