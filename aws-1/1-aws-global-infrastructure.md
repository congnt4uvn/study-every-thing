# Tổng Quan Về Cơ Sở Hạ Tầng Toàn Cầu AWS

## Lịch Sử AWS Cloud

AWS (Amazon Web Services) được ra mắt vào năm **2002** nội bộ tại amazon.com khi họ nhận ra rằng các bộ phận CNTT có thể được cung cấp dưới dạng dịch vụ bên ngoài. Cơ sở hạ tầng của Amazon là một trong những thế mạnh cốt lõi của họ, và họ quyết định cung cấp dịch vụ CNTT cho người khác.

### Các Mốc Quan Trọng

- **2004**: Ra mắt dịch vụ công khai đầu tiên với **SQS** (Simple Queue Service)
- **2006**: Mở rộng dịch vụ với **SQS**, **S3**, và **EC2**
- **Mở rộng sang Châu Âu**: AWS vươn ra ngoài châu Mỹ để phục vụ thị trường toàn cầu
- **Ngày nay**: Cung cấp nền tảng cho các ứng dụng lớn bao gồm:
  - Dropbox
  - Netflix
  - Airbnb
  - NASA

## Vị Thế Thị Trường Của AWS Hiện Nay

Theo Magic Quadrant của Gartner, AWS được công nhận là nhà lãnh đạo và đã duy trì vị trí này trong nhiều năm.

### Thống Kê Chính (2023-2024)

- Doanh thu **90 tỷ USD** (năm 2023)
- Chiếm **31%** thị phần (Quý 1/2024)
- Microsoft đứng thứ hai với **25%** thị phần
- Tiên phong và dẫn đầu trong **13 năm liên tiếp**
- Hơn **1 triệu người dùng tích cực**

> Học AWS giúp bạn thành công trong thế giới điện toán đám mây.

## Bạn Có Thể Xây Dựng Gì Trên AWS?

AWS cho phép bạn xây dựng các ứng dụng phức tạp và có khả năng mở rộng, áp dụng cho nhiều ngành công nghiệp đa dạng. Mọi công ty đều có trường hợp sử dụng cho đám mây.

### Các Công Ty Sử Dụng AWS

- Netflix
- McDonald's
- 21st Century Fox
- Activision

### Các Trường Hợp Sử Dụng Phổ Biến

- **Di Chuyển CNTT Doanh Nghiệp**: Chuyển đổi cơ sở hạ tầng doanh nghiệp
- **Sao Lưu và Lưu Trữ**: Bảo vệ dữ liệu trên đám mây
- **Phân Tích Dữ Liệu Lớn**: Xử lý và phân tích tập dữ liệu lớn
- **Lưu Trữ Website**: Triển khai ứng dụng web
- **Backend Cho Mobile và Mạng Xã Hội**: Cung cấp nền tảng cho ứng dụng di động
- **Máy Chủ Game**: Lưu trữ toàn bộ cơ sở hạ tầng game

> Các ứng dụng là vô tận.

## Cơ Sở Hạ Tầng Toàn Cầu AWS

AWS là một dịch vụ thực sự toàn cầu với các thành phần sau:

- **AWS Regions** (Vùng AWS)
- **Availability Zones** (Vùng Khả Dụng)
- **Data Centers** (Trung Tâm Dữ Liệu)
- **Edge Locations** (Địa Điểm Biên)
- **Points of Presence** (Điểm Hiện Diện)

### Bản Đồ Cơ Sở Hạ Tầng AWS

AWS có nhiều vùng được phân bổ trên toàn cầu (hiển thị màu cam trên bản đồ cơ sở hạ tầng):
- Paris, Tây Ban Nha
- Ohio
- São Paulo
- Cape Town
- Mumbai
- Và nhiều nơi khác trên toàn thế giới

Mỗi vùng được kết nối thông qua **mạng riêng của AWS**, đảm bảo giao tiếp an toàn và nhanh chóng giữa các vùng.

## AWS Regions (Vùng AWS)

### Vùng Là Gì?

**Vùng (Region)** là một cụm trung tâm dữ liệu nằm trong một khu vực địa lý cụ thể (ví dụ: Ohio, Singapore, Sydney, Tokyo).

### Quy Ước Đặt Tên Vùng

- Các vùng có tên như: **us-east-1**, **eu-west-3**
- Ánh xạ tên vùng với mã có thể xem trong AWS Console

### Đặc Điểm Quan Trọng

- Hầu hết các dịch vụ AWS đều **có phạm vi theo vùng**
- Sử dụng dịch vụ ở một vùng độc lập với việc sử dụng nó ở vùng khác
- Nếu bạn sử dụng dịch vụ ở vùng khác, giống như bắt đầu từ đầu

## Làm Thế Nào Để Chọn Vùng AWS?

Khi khởi chạy ứng dụng mới, hãy xem xét các yếu tố sau:

### 1. **Tuân Thủ (Compliance)**

- Chính phủ có thể yêu cầu dữ liệu phải ở trong biên giới quốc gia
- Ví dụ: Dữ liệu ở Pháp có thể phải ở lại Pháp
- Triển khai ứng dụng của bạn trong vùng tuân thủ phù hợp

### 2. **Độ Trễ (Latency)**

- Triển khai gần người dùng để giảm độ trễ
- Ví dụ: Nếu người dùng ở Mỹ, hãy triển khai ở Mỹ
- Triển khai xa người dùng (ví dụ: Úc cho người dùng Mỹ) sẽ tăng độ trễ

### 3. **Tính Khả Dụng Của Dịch Vụ**

- Không phải tất cả các vùng đều có tất cả các dịch vụ
- Xác minh rằng các dịch vụ bạn cần có sẵn trong vùng bạn chọn
- Kiểm tra bảng vùng AWS về tính khả dụng của dịch vụ

### 4. **Giá Cả (Pricing)**

- Giá cả khác nhau giữa các vùng
- Tham khảo trang giá dịch vụ AWS để biết sự khác biệt theo vùng
- Chi phí có thể là yếu tố quan trọng trong quyết định triển khai

## Availability Zones - Vùng Khả Dụng (AZ)

### Tổng Quan

Mỗi vùng chứa nhiều **Vùng Khả Dụng**:
- **Tối thiểu**: 3 AZ mỗi vùng
- **Tối đa**: 6 AZ mỗi vùng
- **Thông thường**: 3 AZ mỗi vùng

### Ví Dụ: Vùng Sydney (ap-southeast-2)

Vùng Sydney có ba vùng khả dụng:
- **ap-southeast-2a**
- **ap-southeast-2b**
- **ap-southeast-2c**

### Đặc Điểm Của Vùng Khả Dụng

- Mỗi AZ bao gồm **một hoặc nhiều trung tâm dữ liệu riêng biệt**
- Mỗi AZ có **nguồn điện dự phòng, mạng và kết nối**
- Các AZ **được cách ly với nhau** để ngăn chặn thảm họa lan rộng
- Nếu một AZ bị lỗi (ví dụ: ap-southeast-2a), nó sẽ không ảnh hưởng đến các AZ khác (ap-southeast-2b, ap-southeast-2c)
- Các AZ được kết nối với **băng thông cao, mạng độ trễ cực thấp**
- Cùng nhau, các AZ được liên kết tạo thành một **vùng**

## Points of Presence - Điểm Hiện Diện (Edge Locations)

AWS duy trì mạng lưới biên rộng lớn để phân phối nội dung:

### Thống Kê Mạng Lưới Biên Toàn Cầu

- Hơn **400** điểm hiện diện
- Hơn **90** thành phố
- Hơn **40** quốc gia

### Mục Đích

Các địa điểm biên phân phối nội dung đến người dùng cuối với **độ trễ thấp nhất có thể**, điều này sẽ được đề cập chi tiết trong phần dịch vụ toàn cầu của các khóa học AWS.

## Phạm Vi Dịch Vụ AWS

### Dịch Vụ Toàn Cầu

Các dịch vụ có sẵn trên tất cả các vùng:
- **IAM** (Identity and Access Management - Quản Lý Danh Tính và Truy Cập)
- **Route 53** (Dịch Vụ DNS)
- **CloudFront** (CDN - Mạng Phân Phối Nội Dung)
- **WAF** (Web Application Firewall - Tường Lửa Ứng Dụng Web)

### Dịch Vụ Theo Phạm Vi Vùng

Các dịch vụ hoạt động trong các vùng cụ thể:
- **Amazon EC2** (Elastic Compute Cloud - Đám Mây Tính Toán Đàn Hồi)
- **Elastic Beanstalk**
- **Lambda**
- **Rekognition**

## Kiểm Tra Tính Khả Dụng Của Dịch Vụ

Để xác định xem dịch vụ có khả dụng trong vùng của bạn không, hãy tham khảo **Bảng Vùng AWS** có sẵn trên trang web AWS.

---

*Tài liệu này dựa trên nội dung giáo dục AWS và cung cấp tổng quan về cơ sở hạ tầng toàn cầu AWS và các khái niệm chính cho triển khai đám mây.*