
================================================================================
FILE: 1-aws-global-infrastructure.md
================================================================================

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



================================================================================
FILE: 10-aws-password-policy-and-mfa-setup.md
================================================================================

# Hướng Dẫn Thiết Lập Chính Sách Mật Khẩu và MFA trên AWS

## Tổng Quan

Hướng dẫn này bao gồm hai biện pháp bảo mật thiết yếu cho tài khoản AWS:
1. Thiết lập chính sách mật khẩu
2. Cấu hình xác thực đa yếu tố (MFA) cho tài khoản root

## Thiết Lập Chính Sách Mật Khẩu

### Truy Cập Cài Đặt Chính Sách Mật Khẩu

1. Điều hướng đến **Account Settings** (Cài đặt tài khoản) ở phía bên trái của bảng điều khiển IAM
2. Tìm mục **Password Policy** (Chính sách mật khẩu)
3. Nhấp **Edit** (Chỉnh sửa) để thay đổi chính sách

### Các Tùy Chọn Chính Sách Mật Khẩu

Bạn có hai tùy chọn chính:

#### Tùy Chọn 1: Chính Sách Mật Khẩu Mặc Định của IAM
Sử dụng chính sách mật khẩu mặc định được cấu hình sẵn của AWS với các yêu cầu tiêu chuẩn.

#### Tùy Chọn 2: Chính Sách Mật Khẩu Tùy Chỉnh
Tùy chỉnh các yêu cầu mật khẩu của bạn với các tùy chọn sau:

- **Độ dài tối thiểu của mật khẩu**
- **Yêu cầu chữ in hoa**
- **Yêu cầu chữ thường**
- **Yêu cầu số**
- **Yêu cầu ký tự đặc biệt** (không phải chữ và số)
- **Thời hạn mật khẩu** (ví dụ: hết hạn sau 90 ngày)
- **Yêu cầu đặt lại bởi quản trị viên** cho mật khẩu hết hạn
- **Cho phép người dùng thay đổi mật khẩu của họ**
- **Ngăn chặn tái sử dụng mật khẩu**

Chính sách mật khẩu có thể được chỉnh sửa trực tiếp từ bảng điều khiển IAM, cung cấp lớp bảo mật đầu tiên cho tài khoản.

## Cấu Hình Xác Thực Đa Yếu Tố (MFA)

### Tại Sao MFA Quan Trọng

Xác thực đa yếu tố thêm một lớp bảo mật bổ sung cho tài khoản root của bạn, đây là tài khoản quan trọng nhất trong môi trường AWS của bạn.

### ⚠️ Cảnh Báo Quan Trọng

**Trước khi tiếp tục**: Một số người dùng đã bị khóa tài khoản sau khi mất quyền truy cập vào thiết bị MFA của họ. Nếu bạn lo ngại về việc mất điện thoại hoặc thiết bị MFA:
- Cân nhắc chỉ xem hướng dẫn này mà không thực hiện
- Đảm bảo bạn có thể duy trì quyền truy cập vào thiết bị MFA của mình
- Nhớ rằng bạn có thể xóa thiết bị MFA sau khi kích hoạt nếu cần

### Thiết Lập MFA

#### Bước 1: Truy Cập Thông Tin Bảo Mật

1. Nhấp vào **tên tài khoản** của bạn ở thanh điều hướng trên cùng
2. Chọn **Security Credentials** (Thông tin bảo mật)
3. Nếu đăng nhập bằng tài khoản root, bạn sẽ thấy "My security credentials root user"

#### Bước 2: Gán Thiết Bị MFA

1. Nhấp vào **Assign MFA device** (Gán thiết bị MFA)
2. Đặt tên cho thiết bị của bạn (ví dụ: "my iPhone")
3. Chọn loại thiết bị MFA:
   - **Authenticator app** (Ứng dụng xác thực) - khuyến nghị cho hầu hết người dùng
   - **Security key** (Khóa bảo mật)
   - **Hardware TOTP token** (Token TOTP phần cứng)

#### Bước 3: Cấu Hình Ứng Dụng Xác Thực

1. AWS cung cấp danh sách các ứng dụng tương thích cho cả Android và iOS
2. Ứng dụng được khuyến nghị: **Twilio Authenticator** (hoặc các ứng dụng tương tự như Google Authenticator, Microsoft Authenticator)
3. Nhấp **Show QR code** (Hiển thị mã QR)

#### Bước 4: Quét Mã QR

1. Mở ứng dụng xác thực trên điện thoại của bạn
2. Thêm tài khoản mới
3. Quét mã QR hiển thị trên bảng điều khiển AWS
4. Lưu tài khoản trong ứng dụng của bạn

#### Bước 5: Xác Minh Cài Đặt

1. Ứng dụng xác thực sẽ tạo mã 6 chữ số thay đổi định kỳ
2. AWS yêu cầu hai mã liên tiếp để xác minh cài đặt đúng:
   - Nhập **mã MFA thứ nhất** (ví dụ: 301935)
   - Đợi mã thay đổi
   - Nhập **mã MFA thứ hai** (ví dụ: 792843)
3. Nhấp **Add MFA** (Thêm MFA)

### Quản Lý Thiết Bị MFA

- Bạn có thể thêm tối đa **8 thiết bị MFA** cho mỗi tài khoản
- Xem tất cả các thiết bị MFA đã cấu hình trong phần thông tin bảo mật
- Xóa thiết bị MFA nếu cần bằng cách chọn chúng từ danh sách

## Sử Dụng MFA Để Đăng Nhập

Sau khi thiết lập MFA, quy trình đăng nhập của bạn sẽ thay đổi:

1. Điều hướng đến trang đăng nhập AWS
2. Nhập **email tài khoản root và mật khẩu** của bạn
3. Sau khi xác thực thành công, bạn sẽ được nhắc nhập **mã MFA**
4. Mở ứng dụng xác thực của bạn
5. Nhập mã 6 chữ số hiện tại
6. Nhấp **Submit** (Gửi)

Bây giờ bạn sẽ được đăng nhập với mức độ bảo mật được nâng cao trên tài khoản của mình.

## Kết Luận

Bằng cách triển khai cả chính sách mật khẩu mạnh và MFA, bạn đã cải thiện đáng kể tư thế bảo mật của tài khoản AWS. Đây là những thực hành bảo mật cơ bản nên được triển khai trên tất cả các tài khoản AWS, đặc biệt là những tài khoản có quyền truy cập root.

## Các Bước Tiếp Theo

- Cân nhắc triển khai MFA cho tất cả người dùng IAM, không chỉ tài khoản root
- Thường xuyên xem xét và cập nhật chính sách mật khẩu của bạn
- Giữ thiết bị MFA của bạn an toàn và có sao lưu
- Ghi chép thiết lập MFA của bạn cho mục đích khắc phục thảm họa



================================================================================
FILE: 11-aws-access-methods-cli-sdk.md
================================================================================

# Các Phương Thức Truy Cập AWS: Management Console, CLI và SDK

## Tổng Quan

AWS cung cấp ba phương thức khác nhau để truy cập và tương tác với các dịch vụ của mình. Mỗi phương thức phục vụ các trường hợp sử dụng khác nhau và được bảo vệ bởi các cơ chế xác thực cụ thể.

## Ba Cách Truy Cập AWS

### 1. AWS Management Console

**Management Console** là giao diện web cho AWS mà chúng ta thường sử dụng.

**Bảo Mật:**
- Được bảo vệ bằng tên người dùng và mật khẩu
- Tùy chọn bảo mật bằng Xác Thực Đa Yếu Tố (MFA)
- Phù hợp nhất cho việc quản lý tài nguyên tương tác, trực quan

### 2. AWS Command Line Interface (CLI)

**CLI** là công cụ được cài đặt trên máy tính cá nhân cho phép bạn tương tác với các dịch vụ AWS bằng các lệnh dòng lệnh.

**Bảo Mật:**
- Được bảo vệ bằng access keys (khóa truy cập)
- Access keys là thông tin xác thực được tải xuống từ AWS
- Cho phép tương tác với AWS qua terminal

**Tính Năng Chính:**
- Truy cập trực tiếp vào API công khai của các dịch vụ AWS
- Cho phép phát triển script để quản lý tài nguyên
- Tự động hóa các tác vụ lặp đi lặp lại
- Mã nguồn mở (có sẵn trên GitHub)
- Là giải pháp thay thế cho việc sử dụng Management Console

**Ví Dụ Sử Dụng:**
```bash
aws s3 cp file.txt s3://my-bucket/
```

### 3. AWS Software Development Kit (SDK)

**SDK** là tập hợp các thư viện theo từng ngôn ngữ lập trình cho phép truy cập theo chương trình vào các dịch vụ AWS.

**Bảo Mật:**
- Được bảo vệ bằng cùng access keys như CLI
- Được nhúng vào trong mã ứng dụng của bạn

**Ngôn Ngữ Được Hỗ Trợ:**
- JavaScript
- Python
- PHP
- .NET
- Ruby
- Java
- Go
- Node.js
- C++
- SDK di động (Android, iOS)
- SDK thiết bị IoT

**Trường Hợp Sử Dụng:**
- Tích hợp các dịch vụ AWS trực tiếp vào ứng dụng của bạn
- Xây dựng các giải pháp tùy chỉnh tương tác với AWS API
- Ví dụ: AWS CLI được xây dựng bằng AWS SDK cho Python (Boto)

## Access Keys: Những Lưu Ý Bảo Mật Quan Trọng

### Access Keys Là Gì?

Access keys bao gồm hai thành phần:
1. **Access Key ID** - Tương tự như tên người dùng
2. **Secret Access Key** - Tương tự như mật khẩu

### Tạo Access Keys

- Được tạo thông qua AWS Management Console
- Mỗi người dùng chịu trách nhiệm về access keys của riêng mình
- Có thể tải xuống ngay lập tức sau khi tạo

### Thực Hành Bảo Mật Tốt Nhất

⚠️ **QUAN TRỌNG:** Xử lý access keys như thông tin xác thực cực kỳ nhạy cảm

- **Không bao giờ chia sẻ access keys** của bạn với đồng nghiệp
- Giữ chúng riêng tư và an toàn
- Mỗi người dùng nên tạo access keys của riêng mình
- Xử lý Access Key ID như tên người dùng của bạn
- Xử lý Secret Access Key như mật khẩu của bạn
- Không commit chúng vào hệ thống kiểm soát phiên bản

## Khi Nào Sử Dụng Từng Phương Thức

| Phương Thức | Phù Hợp Nhất Cho |
|-------------|------------------|
| **Management Console** | Quản lý trực quan, khám phá dịch vụ, cấu hình một lần |
| **CLI** | Script tự động hóa, quy trình DevOps, thao tác dòng lệnh nhanh |
| **SDK** | Xây dựng ứng dụng, quản lý tài nguyên theo chương trình, tích hợp |

## Tóm Tắt

Hiểu ba phương thức truy cập này là nền tảng để làm việc hiệu quả với AWS:

- **Management Console** cung cấp giao diện web thân thiện với người dùng
- **CLI** cho phép tự động hóa mạnh mẽ thông qua các công cụ dòng lệnh
- **SDK** cho phép tích hợp liền mạch các dịch vụ AWS vào ứng dụng của bạn

Cả ba phương thức hoạt động cùng nhau để cung cấp bộ công cụ toàn diện cho việc quản lý và tương tác với các dịch vụ AWS, mỗi phương thức phục vụ các tình huống và sở thích người dùng khác nhau.



================================================================================
FILE: 12-installing-aws-cli-on-windows.md
================================================================================

# Cài Đặt AWS CLI Trên Windows

## Tổng Quan

Hướng dẫn này sẽ giúp bạn cài đặt AWS Command Line Interface (CLI) phiên bản 2 trên Windows bằng trình cài đặt MSI.

## Yêu Cầu

- Hệ điều hành Windows
- Kết nối Internet để tải trình cài đặt
- Quyền quản trị viên để cài đặt

## Các Bước Cài Đặt

### 1. Tìm Kiếm Trình Cài Đặt AWS CLI

1. Mở trình duyệt web của bạn
2. Tìm kiếm "aws CLI install windows" trên Google
3. Tìm trang cài đặt AWS CLI phiên bản 2 cho Windows

### 2. Tải Trình Cài Đặt MSI

1. Truy cập trang tài liệu chính thức của AWS
2. Cuộn xuống phần "Install on Windows"
3. Nhấp vào liên kết tải xuống trình cài đặt MSI
4. Trình cài đặt sẽ được tải xuống máy tính của bạn

### 3. Chạy Trình Cài Đặt

1. Tìm và chạy trình cài đặt MSI đã tải xuống
2. Nhấp **Next** trên màn hình chào mừng
3. Chấp nhận các điều khoản của thỏa thuận cấp phép
4. Nhấp **Next** để tiếp tục
5. Nhấp **Install** để bắt đầu cài đặt
6. Nếu được nhắc bởi User Account Control, nhấp **Yes** để cho phép cài đặt
7. Đợi quá trình cài đặt hoàn tất
8. Nhấp **Finish** khi hoàn tất

### 4. Xác Minh Cài Đặt

1. Mở Command Prompt (tìm kiếm "Command Prompt" trong Windows)
2. Gõ lệnh sau và nhấn Enter:
   ```bash
   aws --version
   ```
3. Bạn sẽ thấy kết quả tương tự như:
   ```
   aws-cli/2.x.x Python/x.x.x Windows/x.x.x
   ```

Nếu bạn thấy phiên bản bắt đầu bằng "2", AWS CLI của bạn đã được cài đặt đúng cách và sẵn sàng sử dụng.

## Nâng Cấp AWS CLI

Để nâng cấp AWS CLI lên phiên bản mới nhất:

1. Tải trình cài đặt MSI mới nhất từ trang web AWS
2. Chạy trình cài đặt
3. Quá trình cài đặt sẽ tự động nâng cấp phiên bản hiện tại của bạn

## Có Gì Mới Trong Phiên Bản 2

AWS CLI phiên bản 2 cung cấp một số cải tiến so với phiên bản 1:

- **Hiệu Suất Được Cải Thiện**: Tốc độ thực thi và hiệu quả tốt hơn
- **Khả Năng Nâng Cao**: Các tính năng và chức năng bổ sung
- **API Giống Nhau**: Cấu trúc lệnh vẫn giống như phiên bản 1
- **Trình Cài Đặt Tốt Hơn**: Quá trình cài đặt đơn giản hơn

## Kết Luận

Bạn đã cài đặt thành công AWS CLI trên Windows và giờ đây đã sẵn sàng tương tác với các dịch vụ AWS từ dòng lệnh. Bạn có thể tiếp tục cấu hình thông tin xác thực AWS và bắt đầu sử dụng các lệnh AWS CLI.

## Các Bước Tiếp Theo

- Cấu hình AWS CLI với thông tin xác thực của bạn
- Học các lệnh AWS CLI cơ bản
- Khám phá các lệnh dành riêng cho dịch vụ AWS



================================================================================
FILE: 13-installing-aws-cli-on-macos.md
================================================================================

# Cài đặt AWS CLI trên macOS

## Tổng quan
Hướng dẫn này sẽ giúp bạn thực hiện các bước cài đặt AWS CLI phiên bản 2 trên macOS sử dụng trình cài đặt đồ họa.

## Các bước cài đặt

### Bước 1: Tìm hướng dẫn cài đặt
1. Truy cập Google và tìm kiếm "installing the AWS CLI version 2 on macOS"
2. Đảm bảo chọn link tài liệu chính thức của AWS

### Bước 2: Tải xuống trình cài đặt
1. Cuộn xuống để tìm hướng dẫn cài đặt
2. Tải xuống file `.pkg` (trình cài đặt đồ họa)

### Bước 3: Chạy trình cài đặt đồ họa
1. Mở file `.pkg` vừa tải xuống
2. Nhấn **Continue** qua các màn hình ban đầu
3. Nhấn **Agree** để chấp nhận thỏa thuận giấy phép
4. Chọn "Install for all the users on this computer" (Cài đặt cho tất cả người dùng trên máy tính này)
5. Nhấn **Continue**
6. Nhấn **Install** để bắt đầu cài đặt
7. Đợi quá trình ghi các file hoàn tất
8. Sau khi cài đặt thành công, di chuyển trình cài đặt vào thùng rác

### Bước 4: Xác minh cài đặt
1. Mở ứng dụng terminal trên macOS
   - Gõ "terminal" trong thanh tìm kiếm Spotlight
   - Hoặc bạn có thể sử dụng iTerm (một ứng dụng terminal miễn phí cho macOS)

2. Chạy lệnh sau để xác minh cài đặt:
   ```bash
   aws --version
   ```

3. Nếu mọi thứ được cài đặt đúng, bạn sẽ thấy kết quả tương tự:
   ```
   AWS CLI 2.0.10
   ```

## Khắc phục sự cố
Trong trường hợp gặp bất kỳ vấn đề nào trong quá trình cài đặt, vui lòng tham khảo hướng dẫn cài đặt AWS CLI chính thức cho macOS. Hướng dẫn này chứa thông tin khắc phục sự cố chi tiết và câu trả lời cho các vấn đề thường gặp.

## Các bước tiếp theo
Sau khi đã cài đặt thành công AWS CLI, bạn có thể tiến hành cấu hình nó với thông tin xác thực AWS của mình và bắt đầu sử dụng để tương tác với các dịch vụ AWS.



================================================================================
FILE: 14-installing-aws-cli-on-linux.md
================================================================================

# Cài Đặt AWS CLI Trên Linux

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thực hiện quá trình cài đặt AWS CLI Version 2 trên hệ thống Linux bằng phương pháp cài đặt chính thức.

## Yêu Cầu Trước Khi Cài Đặt

- Hệ thống Linux có quyền truy cập terminal
- Quyền `sudo` để thực hiện cài đặt
- Kết nối Internet để tải xuống bộ cài đặt

## Các Bước Cài Đặt

### Bước 1: Tải Xuống Bộ Cài Đặt AWS CLI

Đầu tiên, tải xuống gói cài đặt AWS CLI:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

Lệnh này sẽ tải xuống bộ cài đặt AWS CLI Version 2 mới nhất dưới dạng file ZIP.

### Bước 2: Giải Nén Bộ Cài Đặt

Sau khi quá trình tải xuống hoàn tất, giải nén nội dung của file ZIP:

```bash
unzip awscliv2.zip
```

Lệnh này sẽ giải nén gói cài đặt và chuẩn bị cho quá trình cài đặt.

### Bước 3: Chạy Bộ Cài Đặt

Cài đặt AWS CLI bằng cách chạy bộ cài đặt với quyền root:

```bash
sudo ./aws/install
```

Bạn sẽ được yêu cầu nhập mật khẩu. Sau khi nhập mật khẩu, quá trình cài đặt sẽ tự động tiến hành.

## Kiểm Tra Cài Đặt

Sau khi quá trình cài đặt hoàn tất, hãy kiểm tra xem AWS CLI đã được cài đặt chính xác bằng cách kiểm tra phiên bản:

```bash
aws --version
```

Bạn sẽ thấy kết quả tương tự như:

```
AWS CLI/2.x.x Python/3.x.x Linux/x.x.x botocore/x.x.x
```

Các số phiên bản cụ thể sẽ khác nhau tùy thuộc vào thời điểm bạn thực hiện cài đặt.

## Bước Tiếp Theo

Sau khi AWS CLI đã được cài đặt thành công và lệnh kiểm tra phiên bản hoạt động, bạn có thể tiếp tục với việc cấu hình và sử dụng các lệnh AWS CLI.

## Xử Lý Sự Cố

Nếu bạn gặp bất kỳ vấn đề nào trong quá trình cài đặt, vui lòng tham khảo tài liệu chính thức của AWS CLI để biết các bước xử lý sự cố chi tiết và giải pháp.

---

*Lưu ý: Đảm bảo rằng `/usr/local/bin` nằm trong PATH của bạn để có thể chạy lệnh `aws` từ bất kỳ đâu trong terminal.*



================================================================================
FILE: 15-aws-cli-access-keys-configuration.md
================================================================================

# Hướng Dẫn Cấu Hình AWS CLI Access Keys

## Tổng Quan

Hướng dẫn này trình bày cách tạo và cấu hình AWS access keys cho truy cập CLI, bao gồm thiết lập thông tin xác thực AWS CLI và hiểu về quyền IAM.

## Tạo Access Keys

### Bước 1: Truy Cập Security Credentials

1. Click vào tên người dùng của bạn trong AWS Console
2. Chọn **Security credentials** (Thông tin xác thực bảo mật)
3. Cuộn xuống để tìm phần access keys

### Bước 2: Tạo Access Key

1. Click vào **Create access key** (Tạo access key)
2. Chọn trường hợp sử dụng của bạn (ví dụ: truy cập CLI)
3. AWS sẽ đưa ra các khuyến nghị thay thế dựa trên lựa chọn của bạn:
   - Cho CLI: CloudShell (được khuyến nghị)
   - Cho CLI: CLI V2 với xác thực IAM Identity Center
   - Cho ứng dụng code cục bộ chạy bên ngoài AWS
   - Cho ứng dụng chạy trong AWS

> **Lưu ý**: Vì mục đích học tập, chúng ta sẽ tiếp tục với access keys truyền thống để hiểu cách chúng hoạt động, mặc dù có các khuyến nghị khác.

4. Đánh dấu vào ô xác nhận: "I understand the above recommendation" (Tôi hiểu các khuyến nghị trên)
5. Click **Create access key** (Tạo access key)

### Bước 3: Lưu Thông Tin Xác Thực

⚠️ **Quan trọng**: Đây là **lần duy nhất** bạn có thể xem cả hai thông tin:
- Access Key ID
- Secret Access Key

Hãy chắc chắn lưu các thông tin xác thực này một cách an toàn trước khi đóng hộp thoại.

## Cấu Hình AWS CLI

### Cấu Hình Ban Đầu

Mở terminal và chạy lệnh:

```bash
aws configure
```

Bạn sẽ được yêu cầu nhập các thông tin sau:

1. **AWS Access Key ID**: Nhập access key ID của bạn
2. **AWS Secret Access Key**: Nhập secret access key của bạn
3. **Default region name**: Chọn region gần với bạn (ví dụ: `eu-west-1`)
   - Bạn có thể tìm mã region trong menu dropdown region của AWS Console
4. **Default output format**: Nhấn Enter để sử dụng mặc định

### Ví Dụ Cấu Hình

```bash
$ aws configure
AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
Default region name [None]: eu-west-1
Default output format [None]: 
```

## Kiểm Tra Cấu Hình

### Xác Minh Quyền Truy Cập CLI

Kiểm tra cấu hình của bạn bằng cách liệt kê các IAM users:

```bash
aws iam list-users
```

Lệnh này sẽ trả về thông tin về tất cả users trong tài khoản của bạn, bao gồm:
- Tên người dùng
- User ID
- ARN (Amazon Resource Name)
- Ngày tạo
- Ngày sử dụng mật khẩu lần cuối

Kết quả từ CLI sẽ tương tự như thông tin hiển thị trong IAM Management Console.

## Hiểu Về Quyền IAM

### Kiểm Tra Thay Đổi Quyền

Để minh họa cách quyền IAM hoạt động:

1. **Xóa user khỏi nhóm admin** (sử dụng tài khoản root):
   - Điều hướng đến IAM Groups
   - Chọn nhóm admin
   - Xóa user của bạn khỏi nhóm

2. **Kiểm tra quyền truy cập trong Management Console**:
   - Refresh trang IAM
   - Bạn sẽ nhận được lỗi cho biết không đủ quyền

3. **Kiểm tra quyền truy cập qua CLI**:
   ```bash
   aws iam list-users
   ```
   - Lệnh sẽ bị từ chối (không có phản hồi)
   - Quyền CLI khớp chính xác với quyền IAM Console

### Khôi Phục Quyền

⚠️ **Quan trọng**: Đừng quên khôi phục quyền của bạn!

1. Vào **IAM Groups**
2. Chọn nhóm **admin**
3. Thêm user của bạn trở lại vào nhóm
4. Quyền administrator của bạn đã được khôi phục

## Những Điểm Chính

- AWS có thể được truy cập thông qua:
  - **Management Console** (giao diện web)
  - **AWS CLI** (giao diện dòng lệnh sử dụng access keys)
  
- Access keys bao gồm:
  - **Access Key ID** (giống như tên người dùng)
  - **Secret Access Key** (giống như mật khẩu)

- **Thực Hành Bảo Mật Tốt Nhất**:
  - Lưu trữ access keys một cách an toàn
  - Không bao giờ chia sẻ secret access key của bạn
  - Xoay vòng access keys thường xuyên
  - Sử dụng IAM roles khi có thể cho các ứng dụng chạy trên AWS

- Quyền CLI giống hệt với quyền Management Console
- IAM policies kiểm soát quyền truy cập cho cả hai giao diện một cách bình đẳng

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá:
- AWS CloudShell như một giải pháp thay thế cho CLI cục bộ
- Các thực hành bảo mật bổ sung
- IAM roles và thông tin xác thực tạm thời

---

*Hướng dẫn này là một phần của loạt bài AWS IAM cơ bản*



================================================================================
FILE: 16-aws-cloudshell-guide.md
================================================================================

# Hướng Dẫn AWS CloudShell

## Giới Thiệu

AWS CloudShell là một giải pháp thay thế cho việc sử dụng terminal để thực thi các lệnh với AWS. Nó cung cấp một môi trường shell dựa trên trình duyệt được tích hợp trực tiếp vào AWS Management Console.

## Truy Cập CloudShell

CloudShell có thể được truy cập thông qua biểu tượng ở góc trên bên phải của AWS Console. Tuy nhiên, cần lưu ý rằng **CloudShell không khả dụng ở tất cả các vùng (regions)**.

### Tính Khả Dụng Theo Vùng

Trước khi sử dụng CloudShell, hãy kiểm tra các vùng hỗ trợ CloudShell trong tài liệu FAQ. Tính đến thời điểm ghi hình, CloudShell chỉ khả dụng ở một số vùng được chọn. Nếu bạn muốn theo dõi các tính năng CloudShell, nên sử dụng một trong các vùng được hỗ trợ.

**Lưu ý:** Nếu CloudShell không khả dụng ở vùng của bạn hoặc không hoạt động, bạn vẫn có thể sử dụng terminal cục bộ đã được cấu hình với AWS CLI. Cả hai phương pháp đều hoạt động tốt cho khóa học.

## Các Tính Năng Chính

### 1. AWS CLI Được Cấu Hình Sẵn

CloudShell đi kèm với AWS CLI được cài đặt sẵn. Bạn có thể xác minh điều này bằng cách chạy:

```bash
aws --version
```

Môi trường thường chạy AWS CLI phiên bản 2.x.

### 2. Xác Thực Tự Động

Khi sử dụng CloudShell, các lệnh CLI tự động sử dụng thông tin xác thực của tài khoản bạn đang đăng nhập vào console. Điều này có nghĩa là bạn không cần phải cấu hình access keys thủ công.

Ví dụ:
```bash
aws iam list-users
```

Lệnh này sẽ hoạt động ngay lập tức mà không cần thiết lập xác thực bổ sung.

### 3. Cấu Hình Vùng Mặc Định

Vùng mặc định cho các API call của CloudShell được tự động đặt thành vùng bạn đang đăng nhập trong AWS Console. Bạn có thể ghi đè điều này bằng cách sử dụng tham số `--region` khi cần.

### 4. Lưu Trữ Bền Vững

CloudShell cung cấp lưu trữ bền vững cho các tệp của bạn. Bất kỳ tệp nào bạn tạo trong môi trường CloudShell sẽ vẫn khả dụng ngay cả sau khi bạn khởi động lại CloudShell.

Ví dụ:
```bash
echo "test" > demo.txt
```

Tệp này sẽ được giữ lại qua các phiên CloudShell.

### 5. Quản Lý Tệp

CloudShell cung cấp khả năng tải lên và tải xuống tệp thuận tiện:

- **Tải xuống tệp:** Điều hướng đến Actions → Download file, sau đó chỉ định đường dẫn tệp
  ```bash
  # Lấy đường dẫn đầy đủ đến tệp của bạn
  pwd
  # Ví dụ: /home/cloudshell-user/demo.txt
  ```

- **Tải lên tệp:** Sử dụng tùy chọn upload để chuyển tệp từ máy cục bộ sang CloudShell

### 6. Tùy Chọn Tùy Chỉnh

Bạn có thể tùy chỉnh môi trường CloudShell của mình:

- **Kích thước phông chữ:** Nhỏ, Trung bình hoặc Lớn
- **Giao diện:** Chế độ Sáng hoặc Tối
- **Safe paste:** Bật hoặc tắt

### 7. Nhiều Terminal

CloudShell hỗ trợ nhiều phiên terminal:

- Mở tab mới
- Chia thành các cột để hiển thị terminal song song
- Nhiều terminal được kết nối đồng thời

## Thực Hành Tốt Nhất

1. **Chọn các vùng hỗ trợ CloudShell** khi có thể để có trải nghiệm đầy đủ
2. **Sử dụng tính năng upload/download** để quản lý tệp dễ dàng
3. **Tận dụng lưu trữ bền vững** cho các script và tệp cấu hình
4. **Sử dụng nhiều terminal** cho các quy trình làm việc phức tạp

## Giải Pháp Thay Thế: Terminal Cục Bộ

Nếu CloudShell không khả dụng hoặc không hoạt động cho bạn, việc sử dụng terminal cục bộ được cấu hình đúng cách với AWS CLI hoàn toàn ổn và sẽ hoạt động cho tất cả các bài tập trong khóa học.

## Tóm Tắt

CloudShell là một terminal miễn phí, dựa trên trình duyệt trong đám mây AWS, cung cấp:
- AWS CLI được cấu hình sẵn
- Quản lý xác thực tự động
- Lưu trữ tệp bền vững
- Khả năng tải lên/tải xuống tệp
- Giao diện tùy chỉnh
- Hỗ trợ nhiều terminal

Đây là một công cụ mạnh mẽ cho người dùng AWS chuyên nghiệp, nhưng việc sử dụng terminal cục bộ cũng hoàn toàn hiệu quả khi làm việc với AWS CLI.



================================================================================
FILE: 17-aws-iam-roles.md
================================================================================

# AWS IAM Roles

## Giới Thiệu

IAM Roles là thành phần chính cuối cùng của AWS Identity and Access Management (IAM). Chúng cung cấp một cách an toàn để cấp quyền cho các dịch vụ AWS thực hiện các hành động thay mặt bạn trong tài khoản AWS của bạn.

## IAM Roles Là Gì?

IAM Roles tương tự như IAM Users ở chỗ cả hai đều có các chính sách quyền (permissions policies) được gán cho chúng. Tuy nhiên, có một sự khác biệt cơ bản:

- **IAM Users:** Dành cho con người thực tế cần truy cập tài nguyên AWS
- **IAM Roles:** Dành cho các dịch vụ AWS cần thực hiện các hành động thay mặt bạn

## Tại Sao Chúng Ta Cần IAM Roles?

Các dịch vụ AWS mà bạn khởi chạy trong hành trình điện toán đám mây của mình sẽ cần thực hiện nhiều hành động khác nhau trên tài khoản của bạn. Giống như người dùng, các dịch vụ này cần quyền để thực thi các hành động này. IAM Roles cung cấp một cơ chế an toàn để gán các quyền này cho dịch vụ AWS mà không cần nhúng thông tin xác thực.

## Cách Hoạt Động Của IAM Roles

Khi một dịch vụ AWS cần truy cập tài nguyên AWS:

1. Bạn tạo một IAM Role với các quyền cụ thể
2. Bạn gán role này cho dịch vụ AWS
3. Dịch vụ và role cùng nhau tạo thành một thực thể
4. Khi dịch vụ cố gắng truy cập tài nguyên AWS, nó sử dụng IAM Role
5. Nếu role có quyền chính xác, API call sẽ thành công

### Quy Trình Ví Dụ

Hãy xem xét một EC2 Instance (máy chủ ảo trong AWS):

```
EC2 Instance + IAM Role → Truy cập Tài nguyên AWS
```

1. Bạn tạo một EC2 Instance
2. Bạn gán một IAM Role với các quyền cụ thể cho instance
3. EC2 Instance giờ có thể thực hiện các hành động trên AWS dựa trên quyền của role
4. Nếu chính sách quyền đúng, instance sẽ truy cập thành công các tài nguyên AWS cần thiết

## Các Trường Hợp Sử Dụng Phổ Biến Cho IAM Roles

Trong hành trình AWS của bạn, bạn sẽ gặp một số kịch bản phổ biến mà IAM Roles là thiết yếu:

### 1. EC2 Instance Roles
- Cho phép các máy chủ ảo EC2 truy cập các dịch vụ AWS khác
- Trường hợp sử dụng phổ biến nhất cho IAM Roles
- Ví dụ: EC2 instance truy cập S3 buckets hoặc DynamoDB tables

### 2. Lambda Function Roles
- Cho phép các hàm AWS Lambda tương tác với các dịch vụ AWS khác
- Bắt buộc cho các ứng dụng serverless

### 3. CloudFormation Roles
- Cho phép CloudFormation tạo và quản lý tài nguyên AWS thay mặt bạn
- Thiết yếu cho infrastructure as code

## Các Khái Niệm Chính

### Lợi Ích Về Bảo Mật
- **Không có thông tin xác thực hardcoded:** Dịch vụ không cần access keys nhúng trong code
- **Thông tin xác thực tạm thời:** Roles cung cấp security credentials tạm thời
- **Đặc quyền tối thiểu:** Chỉ gán quyền cần thiết cho nhiệm vụ

### Thực Hành Tốt Nhất
1. Tạo các role cụ thể cho các mục đích cụ thể
2. Tuân theo nguyên tắc đặc quyền tối thiểu (least privilege)
3. Thường xuyên xem xét và kiểm toán quyền của role
4. Sử dụng roles thay vì chia sẻ thông tin xác thực người dùng

## Bắt Đầu

Trong bài giảng tiếp theo, chúng ta sẽ thực hành các bước tạo IAM Role trong AWS Console. Mặc dù chúng ta sẽ tạo role, nhưng chúng ta sẽ chưa sử dụng nó ngay lập tức—nó sẽ trở nên hữu ích khi chúng ta bắt đầu làm việc với EC2 Instances trong phần tiếp theo.

## Tóm Tắt

- **IAM Roles** cấp quyền cho các dịch vụ AWS, không phải người dùng thực tế
- Các dịch vụ sử dụng roles để thực hiện các hành động trên tài khoản AWS của bạn
- Các ví dụ phổ biến bao gồm EC2 Instance Roles, Lambda Function Roles và CloudFormation Roles
- Roles cung cấp một cách an toàn để quản lý quyền dịch vụ mà không cần thông tin xác thực hardcoded
- Hiểu về roles là thiết yếu để xây dựng kiến trúc AWS an toàn

## Các Bước Tiếp Theo

Trong bài giảng sau, bạn sẽ học cách tạo IAM Role thông qua thực hành. Kiến thức nền tảng này sẽ rất quan trọng khi chúng ta tiến xa hơn trong khóa học và bắt đầu khởi chạy các dịch vụ AWS yêu cầu quyền dựa trên role.



================================================================================
FILE: 18-aws-iam-roles-hands-on.md
================================================================================

# AWS IAM Roles - Thực Hành

## Giới Thiệu

Trong bài thực hành này, chúng ta sẽ thực hành sử dụng IAM roles trong AWS. Roles là một cách thiết yếu để cấp quyền cho các thực thể AWS thực hiện các hành động trên các dịch vụ AWS.

## Truy Cập IAM Roles

1. Trong bảng điều khiển AWS IAM, nhấp vào **Roles** ở menu bên trái
2. Bạn có thể thấy một số roles đã được tạo sẵn cho tài khoản của bạn (2 hoặc nhiều hơn - điều này không quan trọng)

## Tạo IAM Role Mới

### Bước 1: Chọn Loại Role

Chúng ta sẽ tạo role của riêng mình. Có năm loại role khác nhau bạn có thể tạo, nhưng loại quan trọng nhất cho bài thực hành và kỳ thi là:

- **AWS Service Role** - Cho phép các dịch vụ AWS thực hiện các hành động thay mặt bạn

### Bước 2: Chọn Dịch Vụ

Trong hướng dẫn này, chúng ta sẽ tạo một role cho **EC2 instance**:

1. Chọn **EC2** từ các dịch vụ thường dùng (bạn cũng sẽ thấy Lambda và roles cho hầu hết mọi dịch vụ trên AWS)
2. Chọn use case: **EC2**
3. Bỏ qua các tùy chọn khác
4. Nhấp **Next**

### Bước 3: Gắn Policy Quyền

Bây giờ chúng ta cần gắn một policy để xác định role này sẽ có quyền gì:

1. Tìm kiếm và chọn **IAMReadOnlyAccess**
2. Policy này cho phép EC2 instance đọc thông tin từ IAM
3. Nhấp **Next**

### Bước 4: Cấu Hình Chi Tiết Role

1. Nhập tên role: `DemoRoleForEC2`
2. Xem lại phần **Trusted entities**:
   - Phần này cho thấy role có thể được sử dụng bởi dịch vụ EC2
   - Đây là điều xác định nó như một role cho Amazon EC2
3. Xác minh quyền hiển thị **IAMReadOnlyAccess**
4. Nhấp **Create role**

## Xác Minh

Sau khi tạo:
- Role sẽ xuất hiện trong danh sách roles của bạn
- Bạn có thể xác minh rằng các quyền đã được cấu hình chính xác cho role này
- Role hiện đã sẵn sàng để gắn vào các EC2 instances

## Lưu Ý Quan Trọng

- Chúng ta không thể sử dụng role này ngay lập tức trong phần này
- Chúng ta sẽ áp dụng role này cho EC2 instance khi đến phần EC2 của khóa học
- Đây là một mô hình rất phổ biến trong AWS và quan trọng để hiểu cho kỳ thi

## Tóm Tắt

Bạn đã học cách:
- Tạo một IAM role cho Amazon EC2
- Gắn các quyền phù hợp cho role
- Xác minh cấu hình role

Role này sẽ được sử dụng trong các bài giảng sắp tới khi chúng ta làm việc với EC2 instances.



================================================================================
FILE: 19-iam-security-tools-overview.md
================================================================================

# Tổng quan về Công cụ Bảo mật IAM

## Giới thiệu

Chúng ta sắp kết thúc phần này, nhưng trước tiên hãy nói về các loại công cụ bảo mật mà chúng ta có trong IAM.

## Báo cáo Thông tin Xác thực IAM (IAM Credentials Report)

Chúng ta có thể tạo một **Báo cáo Thông tin Xác thực IAM** và đây là công cụ ở cấp độ tài khoản.

Báo cáo này sẽ chứa tất cả người dùng trong tài khoản của bạn và trạng thái của các thông tin xác thực khác nhau của họ. Chúng ta sẽ thực sự tạo nó ngay bây giờ và xem xét nó.

### Tính năng chính:
- **Phạm vi**: Cấp độ tài khoản
- **Nội dung**: Tất cả người dùng và trạng thái thông tin xác thực của họ
- **Mục đích**: Giám sát và kiểm toán việc sử dụng thông tin xác thực trên tất cả người dùng

## Cố vấn Truy cập IAM (IAM Access Advisor)

Công cụ bảo mật thứ hai mà chúng ta sẽ sử dụng trong IAM được gọi là **Cố vấn Truy cập IAM**.

Công cụ này ở cấp độ người dùng và Cố vấn Truy cập sẽ hiển thị các quyền dịch vụ được cấp cho người dùng và thời điểm các dịch vụ đó được truy cập lần cuối.

### Tính năng chính:
- **Phạm vi**: Cấp độ người dùng
- **Nội dung**: Quyền truy cập dịch vụ và thời gian truy cập cuối cùng
- **Mục đích**: Xác định các quyền không được sử dụng

### Lợi ích:
Điều này sẽ rất hữu ích vì chúng ta đang nói về **nguyên tắc đặc quyền tối thiểu**, và do đó, sử dụng công cụ này, chúng ta có thể xem quyền nào không được sử dụng và giảm quyền mà người dùng có thể nhận được để phù hợp với nguyên tắc đặc quyền tối thiểu.

## Bước tiếp theo

Vì vậy, tôi sẽ gặp bạn trong bài giảng tiếp theo để chỉ cho bạn cách sử dụng các công cụ bảo mật.



================================================================================
FILE: 2-aws-ui-change-note.md
================================================================================

# Thông Báo Về Thay Đổi Giao Diện AWS Console

## Tổng Quan

Trước khi bắt đầu khóa học này, điều quan trọng là bạn cần lưu ý về những thay đổi giao diện người dùng gần đây trong AWS Console.

## Các Thay Đổi Giao Diện

### Tính Năng Giao Diện Mới
- **Nền màu trắng sáng** - Giao diện sạch sẽ và sáng hơn
- **Nút bo tròn** - Thiết kế nút hiện đại với các góc bo tròn
- **Màu xanh dương tươi sáng** - Màu xanh dương nổi bật
- **Diện mạo hiện đại** - Tổng thể có vẻ ngoài đương đại hơn

### Đặc Điểm Giao Diện Cũ
- **Màu xám** - Tông màu xám trầm hơn
- **Màu xanh nhạt** - Màu xanh dương nhẹ nhàng hơn
- **Nút vuông** - Thiết kế nút truyền thống hình vuông
- **Diện mạo cổ điển** - Giao diện truyền thống hơn

## Lưu Ý Quan Trọng

### Trực Quan vs. Khả Năng Sử Dụng
Mặc dù giao diện mới có thể trông khác về mặt trực quan, nhưng **khả năng sử dụng vẫn hoàn toàn giống nhau**. Chức năng và vị trí của các tính năng phải giống hệt nhau giữa giao diện cũ và mới.

### Video Khóa Học
Các video khóa học có thể hiển thị giao diện cũ hoặc mới. Mặc dù có sự khác biệt về hình ảnh, bạn vẫn có thể theo dõi với cả hai phiên bản vì chức năng không thay đổi.

### Thay Đổi Đáng Kể
Nếu bạn nhận thấy những thay đổi đáng kể khi các nút hoặc tính năng đã chuyển sang các vị trí khác nhau, vui lòng báo cáo để tài liệu khóa học có thể được cập nhật tương ứng.

## Kết Luận

Đừng lo lắng về những thay đổi trực quan - giao diện mới chỉ đơn giản là một bản cập nhật thẩm mỹ với màu sắc và hình dạng nút mới. Chức năng cơ bản và trải nghiệm người dùng vẫn nhất quán.

---

*Cảm ơn bạn rất nhiều, và hẹn gặp lại trong bài giảng tiếp theo!*



================================================================================
FILE: 20-aws-iam-security-tools-credentials-report-and-access-advisor.md
================================================================================

# Công cụ Bảo mật AWS IAM: Báo cáo Thông tin Xác thực và Access Advisor

## Tổng quan

AWS Identity and Access Management (IAM) cung cấp các công cụ bảo mật mạnh mẽ giúp bạn giám sát và quản lý quyền truy cập của người dùng. Hướng dẫn này trình bày hai công cụ bảo mật IAM thiết yếu: **Báo cáo Thông tin Xác thực (Credentials Report)** và **IAM Access Advisor**.

## Báo cáo Thông tin Xác thực IAM

### Báo cáo Thông tin Xác thực là gì?

Báo cáo Thông tin Xác thực là một tệp CSV toàn diện cung cấp thông tin chi tiết về tất cả người dùng IAM trong tài khoản AWS của bạn và trạng thái của các thông tin xác thực khác nhau của họ.

### Cách Tạo Báo cáo Thông tin Xác thực

1. Điều hướng đến bảng điều khiển IAM
2. Ở menu bên trái, nhấp vào **Credential report**
3. Nhấp **Download credential report**
4. Một tệp CSV sẽ được tạo và tải xuống

### Thông tin Có trong Báo cáo

Báo cáo Thông tin Xác thực cung cấp các thông tin sau cho mỗi người dùng:

- **Ngày tạo người dùng**: Khi tài khoản người dùng được tạo
- **Trạng thái mật khẩu**: Mật khẩu có được kích hoạt hay không
- **Mật khẩu được sử dụng lần cuối**: Khi mật khẩu được sử dụng lần cuối
- **Mật khẩu được thay đổi lần cuối**: Khi mật khẩu được sửa đổi lần cuối
- **Luân chuyển mật khẩu**: Ngày dự kiến cho lần luân chuyển mật khẩu tiếp theo (nếu được bật)
- **Trạng thái MFA**: Xác thực đa yếu tố có đang hoạt động hay không
- **Access keys (Khóa truy cập)**: 
  - Khóa truy cập đã được tạo chưa
  - Khi nào chúng được luân chuyển lần cuối
  - Khi nào chúng được sử dụng lần cuối
- **Thông tin xác thực bảo mật bổ sung**: Thông tin về các khóa truy cập và chứng chỉ khác

### Ví dụ Trường hợp Sử dụng

Trong một báo cáo thông tin xác thực điển hình, bạn có thể thấy:

- **Tài khoản root**: MFA đang hoạt động, không có khóa truy cập được tạo
- **Người dùng IAM (ví dụ: stephane)**: MFA chưa hoạt động, khóa truy cập đã được tạo

### Lợi ích của Việc Sử dụng Báo cáo Thông tin Xác thực

Báo cáo Thông tin Xác thực cực kỳ hữu ích cho:

- **Kiểm toán bảo mật**: Xác định người dùng chưa thay đổi mật khẩu gần đây
- **Phát hiện người dùng không hoạt động**: Tìm các tài khoản chưa được sử dụng
- **Tuân thủ**: Đảm bảo các phương pháp tốt nhất về bảo mật được tuân theo
- **Quản lý khóa truy cập**: Theo dõi việc sử dụng và luân chuyển khóa truy cập
- **Đánh giá rủi ro**: Xác định người dùng cần được chú ý từ góc độ bảo mật

## IAM Access Advisor

### IAM Access Advisor là gì?

IAM Access Advisor là công cụ hiển thị các dịch vụ AWS nào đã được người dùng IAM cụ thể truy cập và khi nào các dịch vụ đó được truy cập lần cuối.

### Cách Sử dụng IAM Access Advisor

1. Vào bảng điều khiển IAM
2. Điều hướng đến **Users**
3. Chọn người dùng bạn muốn phân tích (ví dụ: stephane)
4. Ở phía bên phải, nhấp vào **Access Advisor**

### Thông tin Được Cung cấp

Access Advisor hiển thị:

- **Các dịch vụ đã truy cập**: Danh sách các dịch vụ AWS mà người dùng đã truy cập
- **Thời gian truy cập lần cuối**: Khi mỗi dịch vụ được sử dụng lần cuối
- **Các dịch vụ chưa truy cập**: Các dịch vụ AWS mà người dùng có quyền nhưng chưa sử dụng

### Ví dụ Các Dịch vụ

Các dịch vụ có thể xuất hiện trong Access Advisor:

**Dịch vụ đã truy cập:**
- AWS Organizations
- AWS Health
- Identity and Access Management (IAM)
- Amazon EC2
- Resource Explorer

**Dịch vụ chưa truy cập:**
- Alexa for Business
- AWS App2Container
- Và nhiều dịch vụ khác...

### Phân tích Quyền

Access Advisor giúp bạn hiểu:

- Policy nào cấp quyền truy cập vào các dịch vụ cụ thể
- Ví dụ: nếu người dùng truy cập Amazon EC2, bạn có thể thấy policy "Administrator Access" đã cấp quyền truy cập đó

### Lợi ích của Việc Sử dụng IAM Access Advisor

IAM Access Advisor vô cùng có giá trị cho:

- **Nguyên tắc đặc quyền tối thiểu**: Đảm bảo người dùng chỉ có các quyền họ thực sự cần
- **Tinh chỉnh quyền**: Xác định các quyền không cần thiết có thể được loại bỏ
- **Tối ưu hóa bảo mật**: Giảm bề mặt tấn công bằng cách loại bỏ các quyền không sử dụng
- **Kiểm soát truy cập chi tiết**: Điều chỉnh chính xác quyền truy cập người dùng trên AWS
- **Tuân thủ**: Đáp ứng yêu cầu bảo mật về quyền truy cập tối thiểu cần thiết

### Ứng dụng Thực tế

Nếu Access Advisor hiển thị 37 trang dịch vụ nhưng người dùng chỉ truy cập một số ít, bạn có thể:

1. Xác định các dịch vụ cụ thể mà họ thực sự sử dụng
2. Sửa đổi quyền của họ để chỉ cấp quyền truy cập vào các dịch vụ đó
3. Loại bỏ các quyền không cần thiết để cải thiện tư thế bảo mật

## Các Phương pháp Tốt nhất

1. **Kiểm toán định kỳ**: Tạo Báo cáo Thông tin Xác thực thường xuyên để giám sát trạng thái bảo mật người dùng
2. **Xem xét Access Advisor**: Kiểm tra định kỳ Access Advisor cho mỗi người dùng
3. **Thực thi MFA**: Bật Xác thực Đa yếu tố cho tất cả người dùng
4. **Luân chuyển thông tin xác thực**: Triển khai chính sách luân chuyển mật khẩu và khóa truy cập
5. **Áp dụng đặc quyền tối thiểu**: Sử dụng Access Advisor để chỉ cấp các quyền cần thiết
6. **Loại bỏ người dùng không hoạt động**: Xác định và vô hiệu hóa hoặc xóa các tài khoản không sử dụng

## Kết luận

Cả Báo cáo Thông tin Xác thực và IAM Access Advisor đều là các công cụ thiết yếu để duy trì môi trường AWS an toàn. Báo cáo Thông tin Xác thực cung cấp tổng quan toàn diện về thông tin xác thực người dùng và trạng thái bảo mật của họ, trong khi Access Advisor giúp bạn triển khai nguyên tắc đặc quyền tối thiểu bằng cách hiển thị việc sử dụng dịch vụ thực tế. Cùng nhau, các công cụ này cho phép bạn đưa ra quyết định sáng suốt về quản lý quyền truy cập và quyền người dùng trong AWS.

---

*Hướng dẫn này dựa trên các phương pháp tốt nhất và khuyến nghị bảo mật của AWS IAM.*



================================================================================
FILE: 21-aws-iam-best-practices.md
================================================================================

# Các Phương Pháp Hay Nhất cho AWS IAM

## Tổng Quan

Tài liệu này bao gồm các hướng dẫn chung và phương pháp hay nhất cho AWS Identity and Access Management (IAM) để giúp bạn tránh các lỗi phổ biến khi sử dụng AWS.

## Các Phương Pháp Hay Nhất

### 1. Sử Dụng Tài Khoản Root

- **Không sử dụng tài khoản root** ngoại trừ khi bạn thiết lập tài khoản AWS
- Đến bây giờ bạn nên có hai tài khoản:
  - Một tài khoản root
  - Tài khoản cá nhân của riêng bạn

### 2. Một Người Dùng Cho Mỗi Người Thực

- Hãy nhớ: **Một người dùng AWS tương đương với một người thực**
- Nếu bạn bè muốn sử dụng AWS, đừng đưa thông tin đăng nhập của bạn cho họ
- Thay vào đó, hãy tạo một người dùng khác cho họ

### 3. Nhóm Người Dùng và Quyền

- Gán người dùng vào các nhóm
- Gán quyền cho nhóm để đảm bảo bảo mật được quản lý ở cấp độ nhóm
- Tạo một chính sách mật khẩu mạnh

### 4. Xác Thực Đa Yếu Tố (MFA)

- Sử dụng và thực thi MFA để đảm bảo rằng tài khoản của bạn được an toàn khỏi tin tặc
- MFA cung cấp một lớp bảo mật bổ sung

### 5. IAM Roles cho các Dịch Vụ AWS

- Tạo và sử dụng roles bất cứ khi nào bạn cấp quyền cho các dịch vụ AWS
- Điều này bao gồm các EC2 instances (máy chủ ảo)

### 6. Bảo Mật Access Keys

- Nếu bạn sử dụng AWS theo chương trình hoặc sử dụng CLI/SDK, bạn phải tạo access keys
- Access keys giống như mật khẩu - chúng rất bí mật
- Giữ chúng cho riêng bạn

### 7. Kiểm Tra Quyền của Bạn

- Sử dụng **IAM Credentials Report** để kiểm tra quyền
- Sử dụng tính năng **IAM Access Advisor** để xem xét các mẫu truy cập

### 8. Không Bao Giờ Chia Sẻ Thông Tin Đăng Nhập

- **Không bao giờ, không bao giờ, không bao giờ chia sẻ người dùng IAM và access keys của bạn**
- Điều này rất quan trọng cho bảo mật tài khoản

## Kết Luận

Tuân thủ các phương pháp hay nhất về IAM này sẽ giúp đảm bảo tài khoản AWS của bạn luôn an toàn và được quản lý đúng cách. Những hướng dẫn này tạo nền tảng cho bảo mật AWS.



================================================================================
FILE: 22-aws-iam-shared-responsibility-model.md
================================================================================

# Mô Hình Trách Nhiệm Chia Sẻ AWS IAM

## Tổng Quan

Trong suốt kỳ thi AWS Certified Cloud Practitioner (CCP), bạn sẽ gặp rất nhiều câu hỏi về **Mô Hình Trách Nhiệm Chia Sẻ** (Shared Responsibility Model). Hiểu rõ mô hình này là rất quan trọng vì nó xác định rõ ràng AWS chịu trách nhiệm về điều gì và bạn, với tư cách là khách hàng, chịu trách nhiệm về điều gì.

## Trách Nhiệm Của AWS

AWS chịu trách nhiệm về các khía cạnh nền tảng của hạ tầng đám mây:

- **Quản Lý Hạ Tầng**: AWS quản lý toàn bộ hạ tầng vật lý cung cấp sức mạnh cho các dịch vụ của họ
- **Bảo Mật Mạng Toàn Cầu**: Đảm bảo an toàn cho hạ tầng mạng lưới trên toàn thế giới
- **Cấu Hình và Phân Tích Lỗ Hổng**: Đánh giá và bảo trì thường xuyên các dịch vụ của họ
- **Xác Thực Tuân Thủ**: Đáp ứng các tiêu chuẩn và chứng nhận tuân thủ khác nhau mà AWS cam kết

## Trách Nhiệm Của Khách Hàng Đối Với IAM

Khi nói đến Quản Lý Danh Tính và Truy Cập (IAM), khách hàng phải chịu trách nhiệm đáng kể về bảo mật và cấu hình phù hợp:

### Quản Lý Người Dùng và Quyền Truy Cập
- **Tạo và Quản Lý Người Dùng**: Bạn phải tự tạo các IAM users, groups, roles và policies
- **Quản Lý Chính Sách**: Chịu trách nhiệm về việc quản lý và giám sát liên tục các chính sách này
- **Xem Xét Quyền Truy Cập**: Phân tích thường xuyên các mẫu truy cập và xem xét quyền hạn trên toàn bộ tài khoản của bạn

### Thực Hành Bảo Mật Tốt Nhất
- **Xác Thực Đa Yếu Tố (MFA)**: Bạn có trách nhiệm kích hoạt MFA trên tất cả các tài khoản và thực thi biện pháp bảo mật này trong toàn tổ chức
- **Luân Chuyển Khóa**: Đảm bảo rằng các access keys và credentials được luân chuyển thường xuyên
- **Quản Lý Quyền Hạn**: Sử dụng các công cụ IAM để áp dụng quyền hạn phù hợp dựa trên nguyên tắc đặc quyền tối thiểu

## Điểm Chính Cần Nhớ

Mô Hình Trách Nhiệm Chia Sẻ có thể được tóm tắt như sau:
- **AWS chịu trách nhiệm** bảo mật hạ tầng và chính đám mây
- **Bạn chịu trách nhiệm** về cách bạn sử dụng hạ tầng đó và bảo mật các tài nguyên của bạn trong đám mây

Đây là một khái niệm cơ bản xuất hiện xuyên suốt các kỳ thi chứng chỉ AWS và rất quan trọng để duy trì môi trường đám mây an toàn.

---

*Bài giảng này cung cấp sự hiểu biết cơ bản về Mô Hình Trách Nhiệm Chia Sẻ của AWS áp dụng cho Quản Lý Danh Tính và Truy Cập.*



================================================================================
FILE: 23-iam-summary.md
================================================================================

# Tóm Tắt IAM

## Tổng Quan

Tài liệu này cung cấp bản tóm tắt toàn diện về các khái niệm và tính năng chính của AWS Identity and Access Management (IAM).

## IAM Users (Người Dùng IAM)

Người dùng IAM nên được ánh xạ tới những người dùng thực tế trong tổ chức của bạn. Mỗi người dùng sẽ có:

- Mật khẩu để truy cập AWS Console
- Danh tính và thông tin xác thực riêng

## IAM Groups (Nhóm IAM)

Người dùng có thể được tổ chức thành các nhóm để quản lý dễ dàng hơn:

- Nhóm chỉ chứa người dùng
- Policies có thể được gán cho nhóm
- Người dùng kế thừa quyền từ nhóm của họ

## IAM Policies (Chính Sách IAM)

Policies là các tài liệu JSON xác định quyền hạn:

- Có thể được gán cho người dùng hoặc nhóm
- Quy định những hành động nào được phép hoặc bị từ chối
- Xác định mức độ truy cập vào các tài nguyên AWS

## IAM Roles (Vai Trò IAM)

Roles là các danh tính được thiết kế cho:

- Các EC2 instances
- Các dịch vụ AWS khác
- Ứng dụng cần truy cập tài nguyên AWS
- Các tình huống truy cập tạm thời

## Tính Năng Bảo Mật

### Xác Thực Đa Yếu Tố (MFA)

- Bật MFA để tăng cường bảo mật
- Thêm một lớp bảo vệ bổ sung ngoài mật khẩu

### Chính Sách Mật Khẩu

- Đặt các yêu cầu mật khẩu mạnh
- Xác định quy tắc độ phức tạp mật khẩu
- Thực thi việc thay đổi mật khẩu định kỳ

## Phương Thức Truy Cập

### AWS CLI (Giao Diện Dòng Lệnh)

- Quản lý dịch vụ AWS từ dòng lệnh
- Yêu cầu access keys để xác thực

### AWS SDK (Bộ Công Cụ Phát Triển Phần Mềm)

- Quản lý dịch vụ AWS bằng ngôn ngữ lập trình
- Truy cập lập trình vào tài nguyên AWS
- Yêu cầu access keys để xác thực

## Access Keys (Khóa Truy Cập)

Access keys được yêu cầu để sử dụng:

- AWS CLI
- AWS SDK
- Truy cập lập trình vào dịch vụ AWS

## Kiểm Toán và Giám Sát

### IAM Credentials Report (Báo Cáo Thông Tin Xác Thực IAM)

- Tạo báo cáo về việc sử dụng thông tin xác thực
- Xem xét tất cả người dùng IAM và trạng thái thông tin xác thực của họ

### IAM Access Advisor (Cố Vấn Truy Cập IAM)

- Giám sát việc truy cập dịch vụ của người dùng
- Xác định các quyền không được sử dụng
- Tối ưu hóa bảo mật bằng cách tuân theo nguyên tắc đặc quyền tối thiểu

## Kết Luận

IAM là một dịch vụ cơ bản để bảo mật môi trường AWS của bạn. Bằng cách triển khai đúng cách người dùng, nhóm, chính sách, vai trò và các tính năng bảo mật như MFA, bạn có thể duy trì một cơ sở hạ tầng đám mây mạnh mẽ và an toàn.



================================================================================
FILE: 24-aws-budgets-and-billing-management.md
================================================================================

# Quản Lý Ngân Sách và Thanh Toán AWS

## Tổng Quan

Hướng dẫn này sẽ chỉ cho bạn cách thiết lập ngân sách và cảnh báo trong AWS để giám sát và kiểm soát chi phí. Bằng cách làm theo các bước này, bạn có thể đảm bảo rằng mình không phải chịu các khoản phí bất ngờ khi sử dụng dịch vụ AWS.

## Truy Cập Bảng Điều Khiển Thanh Toán

### Vấn Đề Truy Cập Ban Đầu

Khi đăng nhập với tư cách người dùng IAM, bạn có thể gặp lỗi "Access Denied" (Truy cập bị từ chối) khi cố gắng truy cập Bảng điều khiển Thanh toán, ngay cả khi có quyền quản trị viên. Điều này là do quyền truy cập thông tin thanh toán cần được kích hoạt một cách rõ ràng.

### Kích Hoạt Quyền Truy Cập Thanh Toán Cho Người Dùng IAM

1. Đăng nhập vào **tài khoản gốc** (root account) của bạn (không phải người dùng IAM)
2. Nhấp vào tên tài khoản của bạn ở góc trên bên phải
3. Chọn **Account** (Tài khoản) từ menu thả xuống
4. Cuộn xuống để tìm **IAM user and role access to billing information** (Quyền truy cập thông tin thanh toán cho người dùng và vai trò IAM)
5. Nhấp **Edit** (Chỉnh sửa) và **Activate IAM access** (Kích hoạt truy cập IAM)

Điều này cho phép người dùng IAM có quyền quản trị truy cập thông tin thanh toán.

### Xem Bảng Điều Khiển Thanh Toán

Sau khi kích hoạt quyền truy cập và làm mới trang, bạn sẽ thấy:

- **Chi phí tính đến nay trong tháng** (Month-to-date costs)
- **Tổng chi phí dự báo** cho tháng hiện tại
- **Tổng chi phí tháng trước**
- **Phân tích chi phí theo tháng**

> **Lưu ý**: Nếu bạn thấy "Data unavailable exception" (Ngoại lệ dữ liệu không khả dụng) cho dự báo, điều này là do dữ liệu lịch sử không đủ và sẽ được giải quyết theo thời gian.

## Hiểu Hóa Đơn Của Bạn

### Truy Cập Chi Tiết Hóa Đơn

1. Điều hướng đến **Bills** (Hóa đơn) trong thanh bên trái
2. Chọn tháng bạn muốn xem lại (ví dụ: Tháng 12, 2023)
3. Cuộn xuống phần **Charges by service** (Chi phí theo dịch vụ)

### Ví Dụ Về Phân Tích Hóa Đơn

Bạn sẽ thấy:
- **Số lượng dịch vụ đang hoạt động** (ví dụ: 28 dịch vụ)
- **Phân tích chi phí theo dịch vụ**

**Ví dụ**: Đối với EC2 (Elastic Compute Cloud) tại EU Ireland:
- Tổng chi phí: $43
- Amazon Elastic Compute NatGateway: $35
- Chi phí EBS
- Chi phí Elastic IP
- Các khoản phí liên quan khác

Phân tích chi tiết này giúp bạn hiểu chính xác tiền của mình đang được chi tiêu ở đâu và xác định bất kỳ khoản phí bất ngờ nào.

## Giám Sát Sử Dụng Tầng Miễn Phí

### Truy Cập Bảng Điều Khiển Tầng Miễn Phí

1. Nhấp vào **Free Tier** (Tầng miễn phí) trong thanh bên trái
2. Xem:
   - Mức sử dụng hiện tại
   - Mức sử dụng dự báo
   - Giới hạn tầng miễn phí

### Hiểu Bảng Điều Khiển

- **Chỉ báo màu xanh lá**: Bạn đang nằm trong giới hạn tầng miễn phí
- **Chỉ báo màu đỏ**: Bạn được dự báo sẽ vượt quá giới hạn tầng miễn phí và sẽ bị tính phí

> **Quan trọng**: Nếu bạn thấy chỉ báo màu đỏ, hãy ngay lập tức tắt bất kỳ dịch vụ nào đang tiêu tốn tài nguyên để tránh phí.

## Thiết Lập Ngân Sách

### Tạo Ngân Sách Chi Tiêu Bằng Không

Ngân sách này cảnh báo bạn ngay khi bạn chi tiêu dù chỉ 1 xu.

**Các bước**:
1. Nhấp vào **Budgets** (Ngân sách) trong thanh bên trái
2. Nhấp **Create budget** (Tạo ngân sách)
3. Chọn **Use a template (simplified)** (Sử dụng mẫu đơn giản)
4. Chọn **Zero spend budget** (Ngân sách chi tiêu bằng không)
5. Tên: `My Zero Spend Budget` (Ngân sách chi tiêu bằng không của tôi)
6. Thêm địa chỉ email của bạn (ví dụ: stephane@example.com)
7. Nhấp **Create budget** (Tạo ngân sách)

### Tạo Ngân Sách Chi Phí Hàng Tháng

Đặt giới hạn chi tiêu tối đa hàng tháng (ví dụ: $10).

**Các bước**:
1. Tạo ngân sách mới bằng mẫu
2. Chọn **Monthly cost budget** (Ngân sách chi phí hàng tháng)
3. Đặt số tiền ngân sách: `$10`
4. Thêm người nhận email
5. Cấu hình cảnh báo:
   - Cảnh báo khi chi tiêu thực tế đạt **85%**
   - Cảnh báo khi chi tiêu thực tế đạt **100%**
   - Cảnh báo khi chi tiêu dự báo dự kiến đạt **100%**
6. Nhấp **Create budget** (Tạo ngân sách)

## Thực Hành Tốt Nhất Về Quản Lý Chi Phí

### Đối Với Khóa Học Này

- Nếu bạn làm theo hướng dẫn khóa học cẩn thận, bạn **không nên tốn tiền**
- Thiết lập ngân sách như một biện pháp an toàn trong trường hợp có sai sót
- Thường xuyên kiểm tra bảng điều khiển Tầng miễn phí
- Xem lại phân tích hóa đơn hàng tháng

### Gỡ Lỗi Vấn Đề Thanh Toán

Để khắc phục các chi phí bất ngờ:

1. **Truy cập Bills** (Hóa đơn) → Chọn tháng liên quan
2. **Xem lại Charges by service** (Chi phí theo dịch vụ) → Xác định dịch vụ nào đang tốn tiền
3. **Kiểm tra Free Tier** (Tầng miễn phí) → Xác minh xem bạn có vượt quá giới hạn không
4. **Xem lại Budgets** (Ngân sách) → Kiểm tra xem cảnh báo có được kích hoạt không

## Điểm Chính Cần Nhớ

- Kích hoạt quyền truy cập thanh toán cho người dùng IAM thông qua tài khoản gốc
- Thiết lập cả ngân sách chi tiêu bằng không và ngân sách chi phí hàng tháng
- Thường xuyên giám sát bảng điều khiển Tầng miễn phí
- Sử dụng tính năng phân tích hóa đơn để hiểu các khoản phí của bạn
- Các kỹ năng quản lý thanh toán này rất quan trọng đối với việc sử dụng AWS

## Kết Luận

Thiết lập giám sát ngân sách phù hợp và hiểu biết về thanh toán AWS là một kỹ năng quan trọng đối với bất kỳ người dùng AWS nào. Với các công cụ này, bạn có thể tự tin sử dụng các dịch vụ AWS trong khi vẫn duy trì kiểm soát chi tiêu của mình.



================================================================================
FILE: 25-amazon-ec2-introduction.md
================================================================================

# Giới Thiệu Amazon EC2

## Tổng Quan

Amazon EC2 (Elastic Compute Cloud) là một trong những dịch vụ phổ biến nhất của AWS và được sử dụng rộng rãi trong ngành công nghiệp. Nó đại diện cho phương pháp **Infrastructure as a Service (IaaS)** của AWS, cho phép bạn tạo trang web và ứng dụng đầu tiên trên AWS.

## Amazon EC2 Là Gì?

EC2 không chỉ là một dịch vụ đơn lẻ - nó được cấu thành từ nhiều thành phần hoạt động cùng nhau:

- **Máy Ảo**: Thuê các máy ảo được gọi là EC2 instances
- **Lưu Trữ**: Lưu trữ dữ liệu trên ổ đĩa ảo (EBS volumes)
- **Cân Bằng Tải**: Phân phối tải giữa các máy sử dụng Elastic Load Balancer (ELB)
- **Tự Động Mở Rộng**: Mở rộng dịch vụ sử dụng Auto Scaling Groups (ASG)

Hiểu về EC2 là nền tảng để nắm bắt cách thức hoạt động của cloud. Nguyên tắc cốt lõi của cloud là khả năng thuê tài nguyên tính toán bất cứ khi nào bạn cần, theo yêu cầu - và EC2 thể hiện hoàn hảo khái niệm này.

## Các Tùy Chọn Cấu Hình EC2 Instance

Khi tạo một EC2 instance, bạn có thể tùy chỉnh nhiều khía cạnh khác nhau:

### 1. Hệ Điều Hành
Chọn từ ba tùy chọn chính:
- **Linux** (lựa chọn phổ biến nhất)
- **Windows**
- **macOS**

### 2. Tài Nguyên Tính Toán
- **CPU**: Chọn lượng sức mạnh tính toán và số lượng lõi
- **RAM**: Chọn lượng bộ nhớ truy cập ngẫu nhiên cần thiết

### 3. Tùy Chọn Lưu Trữ
Bạn có sự linh hoạt trong việc chọn loại lưu trữ:
- **Lưu trữ gắn qua mạng**: EBS (Elastic Block Store) hoặc EFS (Elastic File System)
- **Lưu trữ gắn phần cứng**: EC2 Instance Store

### 4. Cấu Hình Mạng
- Tốc độ card mạng
- Loại địa chỉ IP công khai
- **Security Groups**: Quy tắc tường lửa cho EC2 instance của bạn

### 5. Bootstrap Script
- **EC2 User Data**: Script để cấu hình instance khi khởi động lần đầu

Sức mạnh của cloud nằm ở khả năng chọn chính xác cách bạn muốn cấu hình máy ảo và thuê nó từ AWS trong chớp mắt.

## EC2 User Data & Bootstrapping

### Bootstrapping Là Gì?

Bootstrapping đề cập đến việc thực thi các lệnh khi máy khởi động. Script EC2 User Data cho phép bạn tự động bootstrap các instances của mình.

### Đặc Điểm Chính:
- **Chỉ chạy một lần**: Thực thi khi instance khởi động lần đầu, không bao giờ chạy lại
- **Mục đích**: Tự động hóa các tác vụ khởi động
- **Quyền root**: Chạy với quyền người dùng root (quyền sudo)

### Các Tác Vụ Bootstrap Phổ Biến:
- Cài đặt các bản cập nhật hệ thống
- Cài đặt các gói phần mềm
- Tải xuống các tệp phổ biến từ internet
- Bất kỳ tác vụ cấu hình tùy chỉnh nào bạn cần

### Lưu Ý Quan Trọng:
Càng thêm nhiều tác vụ vào User Data script, instance của bạn sẽ càng mất nhiều thời gian để khởi động.

## Tóm Tắt

Amazon EC2 cung cấp một cách linh hoạt và mạnh mẽ để chạy các máy chủ ảo trên cloud. Với nhiều tùy chọn cấu hình đa dạng, từ hệ điều hành đến lưu trữ và mạng, bạn có thể điều chỉnh các instances để đáp ứng nhu cầu cụ thể của mình. Khả năng bootstrapping thông qua EC2 User Data càng tăng cường tự động hóa, giúp triển khai các instances đã được cấu hình một cách nhanh chóng hơn.

Trong các buổi thực hành sắp tới, chúng ta sẽ khám phá các khái niệm này một cách chi tiết và thực tế, xem cách làm việc trực tiếp với EC2 instances.



================================================================================
FILE: 26-launching-your-first-ec2-instance.md
================================================================================

# Khởi Chạy EC2 Instance Đầu Tiên Của Bạn

## Giới Thiệu

Trong hướng dẫn này, chúng ta sẽ khởi chạy EC2 instance đầu tiên chạy Amazon Linux. Bạn sẽ được tìm hiểu tổng quan về các tham số khác nhau khi khởi chạy một EC2 instance, và chúng ta sẽ triển khai một web server trực tiếp trên instance bằng cách sử dụng user data.

## Yêu Cầu Trước

- Tài khoản AWS có quyền truy cập vào EC2 Console
- Hiểu biết cơ bản về điện toán đám mây

## Hướng Dẫn Từng Bước

### 1. Truy Cập EC2 Console

1. Điều hướng đến **EC2 Console**
2. Nhấp vào **Instances**
3. Nhấp vào **Launch Instances**

### 2. Cấu Hình Tên và Tags cho Instance

- Nhập tên cho instance của bạn: `My First Instance`
- Điều này tạo ra một name tag cho instance
- Bạn có thể thêm các tag bổ sung nếu cần, nhưng name tag là đủ cho hiện tại

### 3. Chọn Amazon Machine Image (AMI)

1. Chọn **Amazon Linux 2 AMI** từ các tùy chọn Quick Start
2. AMI này được **free tier eligible** (đủ điều kiện miễn phí)
3. Chọn kiến trúc: **64-bit x86**
4. AWS cung cấp các image này làm quick starts để dễ dàng triển khai

### 4. Chọn Instance Type

- Chọn **t2.micro** (đủ điều kiện miễn phí)
- Instance type này cung cấp:
  - Công suất CPU đủ cho các workload cơ bản
  - Bộ nhớ đủ để test và phát triển
  - 750 giờ miễn phí mỗi tháng trong năm đầu tiên (tương đương chạy 24/7 trong một tháng)
- Nếu t2.micro không có sẵn ở region của bạn, t3.micro sẽ được đề xuất thay thế

**Lưu ý:** Bạn có thể so sánh các instance type khác nhau bằng cách nhấp vào link so sánh, hiển thị các cấu hình khác nhau với CPU, memory và giá cả khác nhau.

### 5. Tạo Key Pair để Truy Cập SSH

Key pair cần thiết để truy cập an toàn vào instance của bạn qua SSH.

1. Nhấp **Create a new key pair**
2. Đặt tên: `EC2 Tutorial`
3. Key pair type: **RSA**
4. Key pair format:
   - **PEM format**: Cho Mac, Linux, hoặc Windows 10+
   - **PPK format**: Cho Windows 7 hoặc Windows 8 (sử dụng với PuTTY)
5. Nhấp **Create** - key pair sẽ được tải xuống tự động

### 6. Cấu Hình Network Settings

#### Cấu Hình Security Group

Security group hoạt động như một tường lửa ảo kiểm soát lưu lượng đến và đi từ instance của bạn.

1. Console sẽ tạo một security group có tên `launch-wizard-1`
2. Cấu hình các inbound rule sau:
   - **Allow SSH traffic from anywhere** (Port 22) - để truy cập từ xa
   - **Allow HTTP traffic from the internet** (Port 80) - để truy cập web server
3. HTTPS không cần thiết cho hướng dẫn này
4. Instance của bạn sẽ nhận được public IP address tự động

### 7. Cấu Hình Storage

- Mặc định: **8 GB gp2 root volume**
- Free tier bao gồm tới **30 GB EBS general purpose SSD storage**
- **Delete on termination**: Được bật theo mặc định (volume sẽ bị xóa khi instance bị terminate)

### 8. Thêm User Data Script

User data cho phép bạn chạy các lệnh khi khởi chạy lần đầu tiên EC2 instance.

1. Cuộn xuống **Advanced details**
2. Tìm phần **User data** ở cuối
3. Dán script sau:

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
echo "<h1>Hello World from $(hostname -f)</h1>" > /var/www/html/index.html
```

**Script này làm gì:**
- Cập nhật các gói hệ thống
- Cài đặt Apache HTTP web server
- Khởi động và kích hoạt web server
- Tạo một file HTML đơn giản hiển thị "Hello World"

**Quan trọng:** Script này chỉ thực thi một lần trong lần khởi chạy đầu tiên của instance.

### 9. Review và Launch

1. Xem xét instance summary:
   - 1 instance loại t2.micro
   - Đủ điều kiện free tier (750 giờ mỗi tháng)
   - 30 GB EBS storage được bao gồm
2. Nhấp **Launch Instance**
3. Nhấp **View all Instances**

## Hiểu Về Instance Của Bạn

### Các Trạng Thái Instance

Instance của bạn sẽ trải qua nhiều trạng thái:

1. **Pending**: Instance đang được khởi chạy (mất 10-15 giây)
2. **Running**: Instance đang hoạt động và có thể truy cập
3. **Stopping**: Instance đang tắt
4. **Stopped**: Instance đã dừng (không tính phí compute, nhưng storage vẫn tính phí)
5. **Terminated**: Instance bị xóa vĩnh viễn

### Chi Tiết Instance

Khi instance đang chạy, bạn sẽ thấy:

- **Instance Name**: My First Instance
- **Instance ID**: Định danh duy nhất cho instance của bạn
- **Public IPv4 Address**: Được sử dụng để truy cập instance từ internet
- **Private IPv4 Address**: Được sử dụng cho giao tiếp mạng nội bộ AWS
- **Instance Type**: t2.micro
- **AMI**: Amazon Linux 2
- **Key Pair**: EC2 Tutorial

### Thông Tin Security Group

- **Name**: launch-wizard-1
- **Inbound Rules**:
  - Port 22 (SSH): Có thể truy cập từ mọi nơi
  - Port 80 (HTTP): Có thể truy cập từ mọi nơi
- **Outbound Rules**: Tất cả giao tiếp được cho phép (cho phép truy cập internet)

### Thông Tin Storage

- **Một volume**: 8 GB được gắn vào instance

## Truy Cập Web Server Của Bạn

### Phương Pháp 1: Sử Dụng Console

1. Tìm **Public IPv4 Address** trong chi tiết instance
2. Nhấp **Open Address** hoặc sao chép IP

### Phương Pháp 2: Nhập Thủ Công

1. Sao chép public IPv4 address
2. Mở trình duyệt web
3. Nhập: `http://[YOUR-PUBLIC-IP]`

**Quan trọng:** Đảm bảo sử dụng `http://` và KHÔNG dùng `https://`. Sử dụng HTTPS sẽ dẫn đến màn hình loading vô tận vì chúng ta chưa cấu hình SSL.

### Kết Quả Mong Đợi

Bạn sẽ thấy một trang hiển thị:
```
Hello World from [PRIVATE-IP-ADDRESS]
```

**Lưu ý:** IP được hiển thị là private IPv4 address, không phải public IP được sử dụng để truy cập trang.

### Xử Lý Sự Cố

Nếu trang không tải ngay lập tức:
- Đợi 5 phút để user data script hoàn thành
- Làm mới trang
- Xác minh bạn đang sử dụng `http://` không phải `https://`
- Kiểm tra trạng thái instance là "Running"

## Quản Lý Instance Của Bạn

### Dừng Instance

**Khi nào nên dừng:** Để tránh phí khi bạn không cần instance chạy.

1. Chọn instance của bạn
2. Đi tới **Instance State** → **Stop Instance**
3. Instance chuyển sang trạng thái "Stopping"
4. Khi đã dừng, bạn sẽ không bị tính phí cho thời gian compute (phí storage vẫn áp dụng)

**Quan trọng:** Khi bạn dừng rồi khởi động lại instance, public IPv4 address có thể thay đổi. Private IPv4 address vẫn giữ nguyên.

### Khởi Động Instance Đã Dừng

1. Chọn instance đã dừng của bạn
2. Đi tới **Instance State** → **Start Instance**
3. Đợi instance chuyển sang trạng thái "Running"
4. Ghi chú public IPv4 address mới
5. Truy cập web server của bạn bằng IP mới

### Terminate Instance

**Cảnh báo:** Terminate sẽ xóa vĩnh viễn instance và root volume của nó.

1. Chọn instance của bạn
2. Đi tới **Instance State** → **Terminate Instance**
3. Xác nhận hành động trong hộp thoại cảnh báo

**Hành động này không thể hoàn tác.**

## Những Điểm Chính Cần Nhớ

1. **Sức Mạnh Đám Mây**: Bạn có thể tạo instance trong vài giây mà không cần sở hữu server vật lý
2. **Khả Năng Mở Rộng**: Bạn có thể khởi chạy 1 hoặc 100 instance dễ dàng như nhau
3. **Linh Hoạt**: Start, stop và terminate instance theo nhu cầu
4. **Kiểm Soát Chi Phí**: Chỉ trả tiền cho các instance đang chạy (dừng khi không sử dụng)
5. **User Data**: Tự động hóa thiết lập ban đầu bằng script
6. **IP Động**: Public IPv4 address có thể thay đổi sau khi stop/start (private IP giữ nguyên)
7. **Free Tier**: 750 giờ t2.micro mỗi tháng trong năm đầu tiên

## Best Practices (Thực Hành Tốt Nhất)

- **Sử Dụng Tags**: Tag các instance để tổ chức và theo dõi chi phí tốt hơn
- **Bảo Mật**: Hạn chế truy cập SSH cho các IP range cụ thể trong môi trường production
- **Dừng Khi Không Dùng**: Dừng instance khi không sử dụng để giảm chi phí
- **Quản Lý Key**: Giữ các file private key của bạn an toàn
- **Cập Nhật Thường Xuyên**: Giữ instance của bạn được cập nhật với các bản vá bảo mật mới nhất

## Cân Nhắc Chi Phí

- **Free Tier**: 750 giờ t2.micro hàng tháng (12 tháng đầu)
- **Storage**: 30 GB EBS storage được bao gồm trong free tier
- **Stopped Instance**: Không có phí compute, nhưng phí storage vẫn áp dụng
- **Truyền Dữ Liệu**: Theo dõi truyền dữ liệu outbound để quản lý chi phí

## Bước Tiếp Theo

- Tìm hiểu về Elastic IP (địa chỉ public IP tĩnh)
- Khám phá các instance type khác nhau cho các workload khác nhau
- Hiểu về các mô hình định giá EC2 instance
- Thiết lập truy cập SSH vào instance của bạn
- Cấu hình các security group rule nâng cao

## Kết Luận

Bạn đã khởi chạy thành công EC2 instance đầu tiên và triển khai một web server! Điều này chứng minh sức mạnh cơ bản của điện toán đám mây: cung cấp nhanh chóng, linh hoạt và định giá theo mức sử dụng. Bây giờ bạn có thể start, stop và terminate instance bằng các API call đơn giản, cho bạn quyền kiểm soát hoàn toàn hạ tầng đám mây của mình.

---

*Hướng dẫn này là một phần của loạt bài AWS EC2 fundamentals.*



================================================================================
FILE: 27-ec2-instance-types.md
================================================================================

# Các Loại EC2 Instance

## Tổng Quan

EC2 instances có nhiều loại khác nhau được tối ưu hóa cho các trường hợp sử dụng khác nhau. AWS hiện tại cung cấp bảy danh mục khác nhau của EC2 instances, mỗi loại được thiết kế để đáp ứng các yêu cầu workload cụ thể.

## Quy Ước Đặt Tên Instance

AWS tuân theo quy ước đặt tên chuẩn hóa cho EC2 instances. Ví dụ: **m5.2xlarge**

- **m** = Lớp instance (ví dụ: general purpose - đa năng)
- **5** = Thế hệ của instance (cải tiến theo thời gian: m5 → m6 → m7...)
- **2xlarge** = Kích thước trong lớp instance (small → large → 2xlarge → 4xlarge...)

Kích thước càng lớn, instance càng có nhiều bộ nhớ và tài nguyên CPU.

## Các Loại EC2 Instance

### 1. General Purpose (Đa Năng)

**Đặc điểm:**
- Cân bằng giữa tài nguyên compute, memory và networking
- Phù hợp cho các workload đa dạng

**Trường hợp sử dụng:**
- Web servers
- Code repositories
- Hosting ứng dụng tổng quát

**Họ Instance:** T-series, M-series

**Ví dụ:** t2.micro (đủ điều kiện Free Tier)

### 2. Compute Optimized (Tối Ưu Hóa Tính Toán)

**Đặc điểm:**
- Được tối ưu hóa cho các tác vụ đòi hỏi tính toán cao
- Bộ xử lý hiệu năng cao

**Trường hợp sử dụng:**
- Xử lý hàng loạt (batch processing)
- Chuyển mã media (media transcoding)
- Web servers hiệu năng cao
- High-performance computing (HPC)
- Machine learning
- Game servers chuyên dụng

**Họ Instance:** C-series (C5, C6, v.v.)

### 3. Memory Optimized (Tối Ưu Hóa Bộ Nhớ)

**Đặc điểm:**
- Hiệu năng nhanh cho các workload xử lý tập dữ liệu lớn trong bộ nhớ
- Dung lượng RAM cao

**Trường hợp sử dụng:**
- Cơ sở dữ liệu quan hệ/phi quan hệ hiệu năng cao
- Cache store quy mô web phân tán (ví dụ: ElastiCache)
- Cơ sở dữ liệu trong bộ nhớ cho business intelligence (BI)
- Xử lý real-time dữ liệu lớn không có cấu trúc

**Họ Instance:** R-series (R viết tắt của RAM), X1, High Memory, Z1

### 4. Storage Optimized (Tối Ưu Hóa Lưu Trữ)

**Đặc điểm:**
- Được tối ưu hóa cho việc truy cập tần suất cao vào tập dữ liệu lớn trên bộ nhớ local
- Hiệu năng I/O cao

**Trường hợp sử dụng:**
- Hệ thống xử lý giao dịch trực tuyến tần suất cao (OLTP)
- Cơ sở dữ liệu quan hệ và NoSQL
- Cache cho cơ sở dữ liệu trong bộ nhớ (ví dụ: Redis)
- Ứng dụng kho dữ liệu (data warehousing)
- Hệ thống file phân tán

**Họ Instance:** I-series, D-series, H1

## Ví Dụ So Sánh Instance

| Loại Instance | vCPUs | Bộ nhớ | Tối ưu hóa |
|--------------|-------|---------|------------|
| t2.micro | 1 | 1 GB | Đa năng |
| r5.16xlarge | 16 | 512 GB | Bộ nhớ |
| c5d.4xlarge | 16 | 32 GB | Tính toán |

## Tài Nguyên Hữu Ích

**EC2Instances.info** - Website so sánh toàn diện cung cấp:
- Danh sách đầy đủ tất cả các loại instance AWS
- Thông tin giá cả (Linux On-Demand, chi phí Reserved)
- Thông số kỹ thuật Memory và vCPU
- Khả năng tìm kiếm và lọc
- Công cụ phân tích so sánh

## Điểm Chính Cần Nhớ

- Chọn loại instance dựa trên yêu cầu workload cụ thể của bạn
- Các họ instance phát triển với các thế hệ phần cứng mới
- Tham khảo tài liệu AWS và công cụ so sánh để có thông tin cập nhật
- Các loại instance khác nhau có mô hình giá khác nhau
- Free Tier bao gồm t2.micro instances cho workload đa năng



================================================================================
FILE: 28-ec2-security-groups-and-firewall-rules.md
================================================================================

# Nhóm Bảo Mật EC2 và Quy Tắc Tường Lửa

## Giới Thiệu Về Nhóm Bảo Mật (Security Groups)

Nhóm bảo mật là thành phần cơ bản để triển khai bảo mật mạng trong AWS cloud. Chúng hoạt động như tường lửa xung quanh các EC2 instance của bạn, kiểm soát cách lưu lượng truy cập được phép vào và ra khỏi các instance.

### Đặc Điểm Chính

- **Chỉ Có Quy Tắc Cho Phép**: Nhóm bảo mật chỉ chứa các quy tắc cho phép - bạn chỉ định những gì được phép vào và ra
- **Tham Chiếu Linh Hoạt**: Quy tắc có thể tham chiếu đến địa chỉ IP hoặc các nhóm bảo mật khác
- **Kiểm Soát Hai Chiều**: Quản lý cả lưu lượng vào và ra

## Cách Hoạt Động Của Nhóm Bảo Mật

Khi bạn đang ở trên máy tính của mình (internet công cộng) và cố gắng truy cập vào một EC2 instance, nhóm bảo mật hoạt động như một tường lửa xung quanh instance đó. Nhóm bảo mật chứa các quy tắc xác định:

- **Lưu Lượng Vào (Inbound)**: Liệu lưu lượng từ bên ngoài có thể đến EC2 instance hay không
- **Lưu Lượng Ra (Outbound)**: Liệu EC2 instance có thể giao tiếp với internet hay không

## Các Thành Phần Của Nhóm Bảo Mật

Nhóm bảo mật điều chỉnh quyền truy cập thông qua nhiều cơ chế:

### Các Yếu Tố Kiểm Soát Truy Cập

1. **Truy Cập Cổng**: Kiểm soát cổng nào có thể truy cập được
2. **Dải Địa Chỉ IP**: Cho phép các dải địa chỉ IPv4 hoặc IPv6 cụ thể
3. **Mạng Vào**: Kiểm soát lưu lượng từ bên ngoài vào instance
4. **Mạng Ra**: Kiểm soát lưu lượng từ instance ra bên ngoài

### Cấu Trúc Quy Tắc Nhóm Bảo Mật

Mỗi quy tắc bao gồm:
- **Loại**: Loại lưu lượng
- **Giao Thức**: TCP, UDP, v.v.
- **Phạm Vi Cổng**: Cổng nào lưu lượng có thể sử dụng trên instance
- **Nguồn**: Dải địa chỉ IP (ví dụ: `0.0.0.0/0` có nghĩa là tất cả, `/32` có nghĩa là một IP cụ thể)

## Ví Dụ Về Luồng Lưu Lượng

Xem xét một EC2 instance với nhóm bảo mật chứa các quy tắc vào và ra:

### Lưu Lượng Vào
- **Máy Tính Được Ủy Quyền**: Nếu máy tính của bạn được ủy quyền trên cổng 22, lưu lượng sẽ đi qua đến EC2 instance
- **Máy Tính Không Được Ủy Quyền**: Máy tính từ các địa chỉ IP khác sẽ bị chặn bởi tường lửa, dẫn đến timeout

### Lưu Lượng Ra
- **Hành Vi Mặc Định**: Theo mặc định, EC2 instance cho phép tất cả lưu lượng ra
- **Kết Nối Do Instance Khởi Tạo**: EC2 instance có thể truy cập trang web và khởi tạo kết nối mà không bị hạn chế

## Các Khái Niệm Quan Trọng Về Nhóm Bảo Mật

### Gắn Kết Đa Instance
- Nhóm bảo mật có thể được gắn vào nhiều instance (không phải quan hệ một-một)
- Một instance có thể có nhiều nhóm bảo mật

### Phạm Vi Khu Vực
- Nhóm bảo mật bị khóa với một tổ hợp region/VPC cụ thể
- Chuyển đổi region hoặc VPC yêu cầu tạo nhóm bảo mật mới

### Bên Ngoài EC2
- Nhóm bảo mật tồn tại bên ngoài EC2 instance
- Lưu lượng bị chặn không bao giờ đến được EC2 instance

### Thực Hành Tốt Nhất
- **Nhóm Bảo Mật SSH Riêng Biệt**: Duy trì một nhóm bảo mật riêng cho truy cập SSH, vì đây là điều quan trọng nhất cần cấu hình đúng

## Khắc Phục Sự Cố Kết Nối

### Lỗi Timeout
- **Triệu Chứng**: Ứng dụng không thể truy cập được, kết nối bị treo
- **Nguyên Nhân**: Vấn đề về nhóm bảo mật - lưu lượng đang bị chặn

### Lỗi Connection Refused
- **Triệu Chứng**: Nhận được thông báo "connection refused" rõ ràng
- **Nguyên Nhân**: Nhóm bảo mật đã hoạt động (lưu lượng đi qua), nhưng bản thân ứng dụng có lỗi hoặc không chạy

### Hành Vi Mặc Định
- **Tất cả lưu lượng vào**: Bị chặn theo mặc định
- **Tất cả lưu lượng ra**: Được cho phép theo mặc định

## Tính Năng Nâng Cao: Tham Chiếu Nhóm Bảo Mật

Nhóm bảo mật có thể tham chiếu đến các nhóm bảo mật khác trong quy tắc của chúng, điều này đặc biệt hữu ích cho load balancer.

### Cách Thức Hoạt Động

Nếu một EC2 instance có Security Group 1 với các quy tắc vào cho phép:
- Security Group 1
- Security Group 2

Thì:
- Bất kỳ EC2 instance nào có Security Group 2 đều có thể kết nối trực tiếp với các instance có Security Group 1
- Bất kỳ EC2 instance nào có Security Group 1 đều có thể giao tiếp với các instance khác cũng có Security Group 1
- EC2 instance có Security Group 3 sẽ bị từ chối truy cập

### Lợi Ích
- Không cần quản lý địa chỉ IP
- Giao tiếp instance động và linh hoạt
- Mẫu phổ biến cho cấu hình load balancer

## Các Cổng Cần Nhớ

### SSH (Cổng 22)
- **Mục Đích**: Đăng nhập vào EC2 instance trên Linux
- **Giao Thức**: Secure Shell

### FTP (Cổng 21)
- **Mục Đích**: Tải file lên file share
- **Giao Thức**: File Transfer Protocol

### SFTP (Cổng 22)
- **Mục Đích**: Tải file an toàn bằng SSH
- **Giao Thức**: Secure File Transfer Protocol

### HTTP (Cổng 80)
- **Mục Đích**: Truy cập trang web không bảo mật
- **Định Dạng**: `http://địa-chỉ-website`

### HTTPS (Cổng 443)
- **Mục Đích**: Truy cập trang web bảo mật (tiêu chuẩn hiện đại)
- **Định Dạng**: `https://địa-chỉ-website`

### RDP (Cổng 3389)
- **Mục Đích**: Đăng nhập vào Windows instance
- **Giao Thức**: Remote Desktop Protocol

## Tóm Tắt

| Cổng | Giao Thức | Trường Hợp Sử Dụng | Hệ Điều Hành |
|------|-----------|-------------------|--------------|
| 22 | SSH | Đăng nhập vào Linux instance | Linux |
| 22 | SFTP | Truyền file an toàn | Linux |
| 21 | FTP | Truyền file | Bất kỳ |
| 80 | HTTP | Truy cập web không bảo mật | Bất kỳ |
| 443 | HTTPS | Truy cập web bảo mật | Bất kỳ |
| 3389 | RDP | Đăng nhập vào Windows instance | Windows |

Nhóm bảo mật là nền tảng của bảo mật mạng EC2. Hiểu cách chúng kiểm soát luồng lưu lượng, hành vi mặc định và cách khắc phục các sự cố thường gặp là điều cần thiết để làm việc hiệu quả với AWS EC2 instance.



================================================================================
FILE: 29-ec2-security-groups-deep-dive.md
================================================================================

# Tìm Hiểu Sâu Về EC2 Security Groups

## Tổng Quan

Sau khi khởi chạy một EC2 instance, điều quan trọng là phải hiểu cách hoạt động của security groups để kiểm soát quyền truy cập vào instance của bạn. Hướng dẫn này cung cấp một cách thực hành về EC2 security groups, các quy tắc inbound/outbound và khắc phục các vấn đề kết nối phổ biến.

## Truy Cập Security Groups

Có hai cách để xem security groups cho EC2 instance của bạn:

1. **Xem Nhanh**: Nhấp vào tab "Security" trong trang chi tiết EC2 instance
   - Hiển thị tổng quan về các security groups được gắn kèm
   - Hiển thị các quy tắc inbound và outbound

2. **Xem Đầy Đủ**: Điều hướng đến trang Security Groups chuyên dụng
   - Vào menu bên trái
   - Trong mục "Networking and Security", nhấp "Security Groups"

## Hiểu Về Security Groups

### Khái Niệm Cơ Bản Về Security Group

Khi bạn tạo EC2 instance đầu tiên, bạn sẽ thấy ít nhất hai security groups trong console:

- **Default Security Group**: Được AWS tạo tự động
- **Launch Wizard Security Group**: Được tạo khi bạn khởi chạy EC2 instance đầu tiên (ví dụ: "launch-wizard-1")

Mỗi security group có một **Security Group ID** duy nhất, tương tự như cách EC2 instances có instance IDs.

### Quy Tắc Inbound

Quy tắc inbound kiểm soát kết nối **từ bên ngoài vào EC2 instance của bạn**.

#### Ví Dụ Cấu Hình Ban Đầu

Khi khởi chạy một EC2 instance, thông thường bạn có hai quy tắc inbound:

1. **Quy Tắc SSH**
   - Loại: SSH
   - Cổng: 22
   - Nguồn: 0.0.0.0/0 (bất kỳ đâu)

2. **Quy Tắc HTTP**
   - Loại: HTTP
   - Cổng: 80
   - Nguồn: 0.0.0.0/0 (bất kỳ đâu)

Quy tắc HTTP trên cổng 80 là điều cho phép bạn truy cập web server thông qua địa chỉ IPv4 công khai của instance qua trình duyệt.

## Thực Hành: Kiểm Tra Quy Tắc Security Group

### Xóa Quyền Truy Cập HTTP

Để hiểu cách hoạt động của security groups, hãy thực hiện một bài kiểm tra:

1. Chỉnh sửa các quy tắc inbound và **xóa quy tắc HTTP (cổng 80)**
2. Lưu các thay đổi
3. Thử truy cập EC2 instance của bạn qua HTTP trong trình duyệt

**Kết quả**: Trang sẽ hiển thị màn hình tải vô hạn và cuối cùng sẽ timeout. Điều này chứng minh rằng nếu không có quy tắc security group thích hợp, bạn không thể truy cập instance.

### Mẹo Khắc Phục Sự Cố Quan Trọng

**Nếu bạn gặp phải timeout khi kết nối với EC2 instance**, nguyên nhân **100% liên quan đến cấu hình security group**.

Các tình huống timeout phổ biến:
- Kết nối SSH timeout
- Yêu cầu HTTP/HTTPS timeout
- Bất kỳ nỗ lực kết nối nào khác timeout

**Giải pháp**: Kiểm tra các quy tắc security group của bạn và đảm bảo chúng được cấu hình đúng cho loại truy cập bạn cần.

### Khôi Phục Quyền Truy Cập HTTP

Để khắc phục vấn đề timeout:

1. Thêm lại quy tắc inbound HTTP
2. Chọn HTTP từ menu thả xuống loại (tự động đặt cổng 80)
3. Đặt nguồn thành 0.0.0.0/0 (bất kỳ đâu IPv4)
4. Lưu quy tắc

Sau khi thêm lại quy tắc, làm mới trình duyệt của bạn và trang web sẽ tải thành công.

## Cấu Hình Quy Tắc Inbound Tùy Chỉnh

Bạn có sự linh hoạt trong việc tạo các quy tắc inbound:

### Cấu Hình Cổng

- Xác định các cổng cụ thể (ví dụ: cổng 443 cho HTTPS)
- Xác định phạm vi cổng
- Sử dụng menu thả xuống loại cho các giao thức phổ biến:
  - HTTP → Cổng 80
  - HTTPS → Cổng 443
  - SSH → Cổng 22
  - Và nhiều hơn nữa...

### Cấu Hình Nguồn

Bạn có thể chỉ định nguồn lưu lượng được phép:

1. **CIDR Blocks**
   - Ký hiệu CIDR block tùy chỉnh
   - `0.0.0.0/0` = Bất kỳ đâu (tất cả địa chỉ IPv4)

2. **My IP**
   - Hạn chế truy cập chỉ cho địa chỉ IP hiện tại của bạn
   - **Cảnh báo**: Nếu địa chỉ IP của bạn thay đổi, bạn sẽ gặp timeout và mất quyền truy cập vào instance

3. **Security Groups** (sẽ được đề cập sau trong khóa học)

4. **Prefix Lists** (sẽ được đề cập sau trong khóa học)

## Quy Tắc Outbound

Quy tắc outbound kiểm soát lưu lượng **từ EC2 instance của bạn ra bên ngoài**.

### Cấu Hình Mặc Định

Theo mặc định, security groups cho phép:
- Tất cả lưu lượng trên tất cả các cổng
- Đến bất kỳ đích nào (0.0.0.0/0)
- Giao thức: Tất cả

Cấu hình này cung cấp cho EC2 instance của bạn kết nối internet đầy đủ.

## Các Khái Niệm Nâng Cao Về Security Group

### Nhiều Security Groups Trên Một Instance

Một EC2 instance có thể có nhiều security groups được gắn kèm:
- Bạn có thể gắn 1, 2, 3, 5 hoặc nhiều security groups vào một instance
- Các quy tắc từ tất cả các security groups được gắn kèm sẽ được kết hợp
- Các quy tắc có tính tích lũy (chúng cộng lại với nhau)

### Tái Sử Dụng Security Groups

Security groups là tài nguyên có thể tái sử dụng:
- Một security group (ví dụ: "launch-wizard-1") có thể được gắn vào nhiều EC2 instances
- Điều này thúc đẩy tính nhất quán và quản lý dễ dàng hơn trong cơ sở hạ tầng của bạn

### Tóm Tắt Về Tính Linh Hoạt

- **Nhiều security groups** → Một EC2 instance
- **Một security group** → Nhiều EC2 instances
- Kết hợp theo nhu cầu cho kiến trúc của bạn

## Điểm Chính Cần Nhớ

1. Security groups hoạt động như tường lửa ảo cho EC2 instances của bạn
2. Quy tắc inbound kiểm soát lưu lượng đến, quy tắc outbound kiểm soát lưu lượng đi
3. **Lỗi timeout = Cấu hình sai security group** (100% trường hợp)
4. Security groups có trạng thái (lưu lượng trả về được tự động cho phép)
5. Nhiều security groups có thể được gắn vào một instance
6. Security groups có thể được tái sử dụng trên nhiều instances
7. Luôn xác minh các quy tắc security group khi khắc phục sự cố kết nối

## Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá các cấu hình security group nâng cao hơn và các phương pháp tốt nhất để bảo mật cơ sở hạ tầng AWS của bạn.



================================================================================
FILE: 3-aws-console-navigation-guide.md
================================================================================

# Hướng Dẫn Điều Hướng AWS Console

## Giới Thiệu

Chào mừng bạn đến với Trang Chủ AWS Console. Hướng dẫn này sẽ giúp bạn làm quen với AWS Management Console và hiểu cách điều hướng cũng như sử dụng các tính năng khác nhau một cách hiệu quả.

## Lựa Chọn Region (Vùng)

### Hiểu Về AWS Regions

Ở góc trên bên phải màn hình của bạn, bạn sẽ tìm thấy **bộ chọn vùng** (regions selector). Đây là một thành phần quan trọng để quản lý tài nguyên AWS của bạn.

- **Hiển Thị Vùng Hiện Tại**: Bộ chọn hiển thị vùng bạn đang chọn (ví dụ: "Northern Virginia, US East 1")
- **Thực Hành Tốt Nhất**: Chọn một vùng gần với vị trí địa lý của bạn để có hiệu suất tối ưu
- **Ví Dụ**: Nếu bạn ở châu Âu, hãy cân nhắc chọn "EU West 1" (Ireland); nếu bạn ở châu Phi gần Cape Town, chọn vùng Cape Town

### Những Lưu Ý Quan Trọng Về Vùng

- Bạn không cần phải ở vị trí vật lý của vùng đó để sử dụng nó
- Chọn vùng phù hợp nhất với nhu cầu của bạn
- Chọn vùng gần hơn sẽ cho bạn độ trễ thấp nhất
- Quan trọng là bạn nên duy trì cùng một vùng trong suốt khóa học hoặc hướng dẫn của bạn

## Các Tính Năng Của Console Home

### Dịch Vụ Đã Truy Cập Gần Đây

Console hiển thị danh sách các dịch vụ bạn đã truy cập gần đây. Phần này sẽ trống khi bạn mới bắt đầu sử dụng AWS, nhưng sẽ được điền khi bạn điều hướng qua các dịch vụ khác nhau.

### Bảng Thông Tin

Ở cuối trang chủ, bạn sẽ tìm thấy:
- Thông tin chung về AWS
- Các vấn đề về tình trạng hệ thống (nếu có)
- Thông tin về chi phí và sử dụng cho tài khoản của bạn
- Các hướng dẫn để xây dựng giải pháp

**Lưu Ý**: Trang chủ AWS Console thay đổi thường xuyên. Nếu nó trông khác đáng kể so với những gì bạn thấy trong hướng dẫn, đừng lo lắng - chức năng cốt lõi vẫn giữ nguyên.

## Tìm Kiếm Dịch Vụ AWS

### Phương Pháp 1: Menu Services

1. Nhấp vào **Services** ở góc trên bên trái
2. Duyệt các dịch vụ theo hai cách:
   - **Thứ Tự Bảng Chữ Cái**: Xem tất cả các dịch vụ AWS được sắp xếp từ A-Z
   - **Theo Danh Mục**: Ví dụ, trong mục "Compute" bạn sẽ tìm thấy tất cả các dịch vụ liên quan đến điện toán

### Phương Pháp 2: Thanh Tìm Kiếm

Thanh tìm kiếm là một công cụ mạnh mẽ để nhanh chóng tìm kiếm dịch vụ:

1. Nhập tên dịch vụ (ví dụ: "Route 53")
2. Xem kết quả tìm kiếm bao gồm:
   - Các dịch vụ phù hợp (ví dụ: 4 dịch vụ)
   - Các tính năng trong những dịch vụ đó (ví dụ: 13 tính năng)
   - Liên kết trực tiếp đến các tính năng cụ thể (ví dụ: tên miền trong Route 53)
   - Các blog, bài viết kiến thức và tài liệu liên quan

## Hiểu Về Dịch Vụ Global và Regional

### Dịch Vụ Global (Toàn Cầu)

Một số dịch vụ AWS là **dịch vụ toàn cầu**, nghĩa là chúng không yêu cầu lựa chọn vùng.

**Ví Dụ: Route 53**
- Khi bạn truy cập Route 53, bạn sẽ thấy "Global" ở góc trên bên phải
- Bạn sẽ nhận được cùng một giao diện bất kể vùng bạn đã chọn
- Đây là ngoại lệ chứ không phải là quy tắc

### Dịch Vụ Regional (Theo Vùng)

Hầu hết các dịch vụ AWS là **dịch vụ theo vùng**, nghĩa là chúng hoạt động trong các vùng cụ thể.

**Ví Dụ: EC2**
- Khi bạn truy cập EC2, bạn sẽ thấy vùng đã chọn (ví dụ: "Ireland") ở góc trên bên phải
- Giao diện của bạn sẽ khác nhau dựa trên vùng đã chọn
- Các tài nguyên được tạo trong một vùng sẽ không xuất hiện khi xem vùng khác

## Cơ Sở Hạ Tầng Toàn Cầu AWS

### Tài Liệu Về Dịch Vụ Theo Vùng

Bạn có thể tìm thông tin chi tiết về các dịch vụ AWS theo vùng:

1. Tìm kiếm "AWS global infrastructure" trên Google
2. Điều hướng đến trang **AWS Regional Services**
3. Xem danh sách dịch vụ được sắp xếp theo vùng

### Kiểm Tra Tính Khả Dụng Của Dịch Vụ

Tài nguyên này đặc biệt hữu ích khi:
- Một dịch vụ được đề cập trong khóa học không có sẵn trong vùng của bạn
- Bạn cần xác minh dịch vụ nào có sẵn trong các vùng cụ thể
- Bạn đang lên kế hoạch triển khai tài nguyên trong một vùng mới

**Ví Dụ**: Bạn có thể kiểm tra dịch vụ nào có sẵn ở Cape Town hoặc bất kỳ vùng AWS nào khác.

### Lưu Ý Quan Trọng

Không phải tất cả các dịch vụ AWS đều có sẵn trong mọi vùng. Nếu bạn không thấy dịch vụ bạn cần:
- Kiểm tra trang AWS Regional Services
- Cân nhắc chuyển sang vùng có dịch vụ đó
- Lập kế hoạch kiến trúc của bạn cho phù hợp

## Kết Luận

Hiểu cách điều hướng AWS Console là nền tảng để làm việc hiệu quả với các dịch vụ AWS. Hãy dành thời gian làm quen với:
- Lựa chọn vùng và các tác động của nó
- Các phương pháp khác nhau để tìm dịch vụ
- Sự khác biệt giữa dịch vụ toàn cầu và dịch vụ theo vùng
- Cách xác minh tính khả dụng của dịch vụ trong vùng của bạn

Khi bạn tiếp tục làm việc với AWS, những kỹ năng điều hướng này sẽ trở nên tự nhiên, cho phép bạn tập trung vào việc xây dựng và quản lý cơ sở hạ tầng đám mây của mình một cách hiệu quả.



================================================================================
FILE: 30-connecting-to-ec2-instances-ssh-overview.md
================================================================================

# Kết Nối Đến EC2 Instances: Tổng Quan Về SSH

## Giới Thiệu

Một trong những phần khó khăn khi vận hành trên Cloud là hiểu cách kết nối vào bên trong máy chủ của bạn để thực hiện bảo trì hoặc các hành động khác. Đối với máy chủ Linux, chúng ta sử dụng SSH (Secure Shell) để kết nối an toàn đến các instances.

## Các Phương Thức Kết Nối Theo Hệ Điều Hành

Phương thức bạn sử dụng phụ thuộc vào hệ điều hành của bạn:

### Mac và Linux
- **SSH Command Line Interface**: Tiện ích tích hợp sẵn trên hệ thống Mac và Linux
- Cũng có sẵn trên Windows 10 và các phiên bản mới hơn

### Windows (Trước Phiên Bản 10)
- **PuTTY**: Một ứng dụng SSH client dành riêng cho Windows
- Cung cấp chức năng tương tự như SSH
- Tương thích với mọi phiên bản Windows

### Tất Cả Các Nền Tảng
- **EC2 Instance Connect**: Phương thức kết nối dựa trên trình duyệt web
- Hoạt động trên Mac, Linux và mọi phiên bản Windows
- Không cần cài đặt
- Hiện tại hỗ trợ các instances Amazon Linux 2

## Bạn Nên Sử Dụng Phương Thức Nào?

### Cho Người Dùng Mac hoặc Linux
Xem bài giảng SSH trên Mac/Linux để học cách sử dụng tiện ích SSH tích hợp sẵn.

### Cho Người Dùng Windows
Bạn có nhiều lựa chọn:
- **Windows 10 trở lên**: Sử dụng tiện ích SSH tích hợp sẵn (xem bài giảng SSH trên Windows 10)
- **Bất kỳ phiên bản Windows nào**: Sử dụng PuTTY (xem bài giảng PuTTY)

### Khuyến Nghị Cho Tất Cả Người Dùng
**EC2 Instance Connect** được khuyến nghị cao vì:
- Đơn giản và thân thiện với người dùng
- Không cần cài đặt
- Hoạt động thông qua trình duyệt web
- Không cần kiến thức về dòng lệnh
- Tương thích với mọi hệ điều hành

## Khắc Phục Sự Cố

Kết nối SSH là một trong những thách thức phổ biến nhất mà học viên gặp phải trong khóa học này. Nếu bạn gặp vấn đề:

1. **Xem lại bài giảng** - Bạn có thể đã bỏ lỡ một bước quan trọng
2. **Kiểm tra các vấn đề thường gặp**:
   - Quy tắc security group
   - Cú pháp lệnh
   - Lỗi chính tả trong thông tin kết nối
3. **Xem hướng dẫn khắc phục sự cố** được cung cấp sau các bài giảng này
4. **Thử EC2 Instance Connect** - Phương pháp này thường giải quyết được các vấn đề kết nối

## Lưu Ý Quan Trọng

- **Bạn chỉ cần MỘT phương thức hoạt động** - Nếu một phương thức kết nối hoạt động, bạn đã sẵn sàng
- **Đừng lo lắng nếu SSH không hoạt động** - Đây là khóa học giới thiệu và việc sử dụng SSH là tối thiểu
- **Hạn chế của EC2 Instance Connect** - Hiện tại chỉ hoạt động với Amazon Linux 2 (đây là lý do chúng ta sử dụng nó trong hướng dẫn này)

## Các Bước Tiếp Theo

Tìm bài giảng phù hợp với hệ điều hành và phương thức kết nối bạn ưa thích, và hẹn gặp lại bạn trong bài giảng tiếp theo!



================================================================================
FILE: 31-ssh-into-ec2-instance-linux-mac.md
================================================================================

# Kết nối SSH vào EC2 Instance (Linux/Mac)

## Giới thiệu

SSH (Secure Shell) là một trong những chức năng quan trọng nhất khi làm việc với Amazon Cloud. Nó cho phép bạn điều khiển một máy chủ từ xa bằng cách sử dụng terminal hoặc giao diện dòng lệnh của bạn.

## Cách SSH hoạt động với EC2

Khi bạn SSH vào một EC2 instance:

1. EC2 instance của bạn chạy Amazon Linux 2 và có địa chỉ IP công khai
2. Security group của bạn cho phép truy cập qua Port 22 (cổng SSH)
3. Máy tính cục bộ của bạn kết nối với EC2 instance qua web thông qua Port 22
4. Giao diện dòng lệnh của bạn hoạt động như thể bạn đang ở bên trong máy đó

## Yêu cầu trước khi bắt đầu

Trước khi bắt đầu, hãy đảm bảo bạn có:
- Một EC2 instance đang chạy với Amazon Linux 2
- File PEM đã tải xuống (ví dụ: `EC2Tutorial.pem`)
- Security group được cấu hình để cho phép SSH (Port 22) từ 0.0.0.0/0
- Địa chỉ IPv4 công khai của instance

## Hướng dẫn từng bước

### 1. Chuẩn bị file PEM

- Xóa bất kỳ khoảng trắng nào khỏi tên file (ví dụ: đổi tên `EC2 Tutorial.pem` thành `EC2Tutorial.pem`)
- Đặt file vào một thư mục bạn chọn (ví dụ: thư mục `aws-course`)

### 2. Lấy thông tin Instance

1. Điều hướng đến trang tổng quan EC2 instance
2. Tìm instance của bạn
3. Sao chép địa chỉ IPv4 công khai
4. Xác minh security group có quy tắc cho Port 22 (SSH) từ 0.0.0.0/0

### 3. Điều hướng đến đúng thư mục

Mở terminal và điều hướng đến nơi chứa file PEM của bạn:

```bash
# Kiểm tra thư mục hiện tại
pwd

# Liệt kê các file trong thư mục hiện tại
ls

# Chuyển đến thư mục chứa file PEM
cd aws-course

# Xác minh file PEM có mặt
ls
```

**Quan trọng**: Terminal của bạn phải ở cùng thư mục với file PEM để lệnh SSH hoạt động.

### 4. Thiết lập quyền đúng

Trước khi sử dụng file PEM, bạn cần thiết lập quyền chính xác:

```bash
chmod 0400 EC2Tutorial.pem
```

Lệnh này đảm bảo file khóa của bạn không thể xem công khai và bảo vệ nó khỏi truy cập trái phép.

### 5. Kết nối qua SSH

Sử dụng lệnh sau để kết nối với EC2 instance:

```bash
ssh -i EC2Tutorial.pem ec2-user@<IP_CONG_KHAI_CUA_BAN>
```

Thay thế `<IP_CONG_KHAI_CUA_BAN>` bằng địa chỉ IPv4 công khai của instance.

**Tại sao lại là `ec2-user`?** Amazon Linux 2 AMI đi kèm với một user được cấu hình sẵn tên là `ec2-user`.

### 6. Kết nối lần đầu

Lần kết nối đầu tiên, bạn có thể thấy một thông báo yêu cầu xác nhận tin cậy instance:
```
The authenticity of host '...' can't be established.
Are you sure you want to continue connecting (yes/no)?
```

Nhập `yes` và nhấn Enter.

## Làm việc với EC2 Instance

Sau khi kết nối, bạn có thể thực thi các lệnh trực tiếp trên EC2 instance:

```bash
# Kiểm tra user hiện tại
whoami

# Kiểm tra kết nối mạng
ping google.com
```

Để dừng một lệnh đang chạy, nhấn `Ctrl + C`.

## Ngắt kết nối khỏi Instance

Để thoát khỏi phiên SSH, bạn có thể:
- Nhập `exit` và nhấn Enter
- Nhấn `Ctrl + D`

## Kết nối lại

Để kết nối lại với instance sau này, sử dụng cùng lệnh SSH:

```bash
ssh -i EC2Tutorial.pem ec2-user@<IP_CONG_KHAI_CUA_BAN>
```

**Lưu ý quan trọng**: Nếu bạn dừng và sau đó khởi động lại EC2 instance, địa chỉ IP công khai có thể thay đổi. Hãy đảm bảo cập nhật địa chỉ IP trong lệnh SSH của bạn.

## Lỗi thường gặp và cách khắc phục

### "Too many authentication failures"
Điều này có nghĩa là bạn chưa chỉ định file khóa PEM. Sử dụng flag `-i` với file PEM của bạn.

### "Unprotected key file"
File PEM của bạn có quyền không chính xác. Chạy `chmod 0400 EC2Tutorial.pem` để khắc phục.

### "No such file or directory"
Terminal của bạn không ở đúng thư mục. Điều hướng đến thư mục chứa file PEM bằng lệnh `cd`.

## Tóm tắt

SSH cho phép bạn truy cập và điều khiển các EC2 instance từ xa một cách an toàn. Bằng cách làm theo các bước này, bạn có thể thiết lập kết nối đến Amazon Linux 2 instance và thực thi các lệnh như thể bạn đang sử dụng máy đó trực tiếp.



================================================================================
FILE: 32-ssh-into-ec2-instance-windows-putty.md
================================================================================

# SSH vào EC2 Instance sử dụng Windows với PuTTY

## Giới thiệu

SSH (Secure Shell) là một trong những chức năng quan trọng nhất khi làm việc với Amazon Cloud. Nó cho phép bạn điều khiển máy chủ từ xa bằng giao diện dòng lệnh.

## Tổng quan

Trong hướng dẫn này, bạn sẽ học cách:
- Kết nối đến EC2 instance đang chạy Amazon Linux 2
- Sử dụng PuTTY làm SSH client trên Windows
- Cấu hình xác thực sử dụng file khóa PPK

### SSH hoạt động như thế nào

Máy EC2 của bạn chạy Amazon Linux 2 với địa chỉ IP công khai. Với security group SSH được cấu hình cho phép SSH trên cổng 22, máy Windows của bạn có thể kết nối qua internet trực tiếp đến EC2 instance và điều khiển nó bằng dòng lệnh.

## Yêu cầu

- Windows 7, Windows 8, hoặc Windows 10
- EC2 instance với security group SSH đã được cấu hình (cổng 22 mở)
- File key pair EC2 (định dạng .pem)

## Bước 1: Tải và Cài đặt PuTTY

PuTTY là SSH client miễn phí cho Windows.

1. Tải PuTTY từ trang web chính thức
2. Chọn bản cài đặt 64-bit (khuyến nghị)
3. Chạy file cài đặt và hoàn tất quá trình cài đặt
4. Click qua các bước cài đặt (Next → Next → Yes → Install)

Sau khi cài đặt, bạn sẽ có hai ứng dụng quan trọng:
- **PuTTY**: SSH client
- **PuTTYgen**: Công cụ chuyển đổi khóa

## Bước 2: Chuyển đổi PEM sang định dạng PPK (nếu cần)

Nếu bạn đã tải key pair EC2 ở định dạng PEM, bạn cần chuyển đổi nó sang định dạng PPK cho PuTTY.

1. Mở **PuTTYgen**
2. Click **Load**
3. Điều hướng đến vị trí file khóa của bạn (ví dụ: Desktop)
4. Thay đổi bộ lọc file thành "All Files (*.*)" ở góc dưới bên phải
5. Chọn file `.pem` của bạn (ví dụ: `EC2tutorial.pem`)
6. Click **Open** - bạn sẽ thấy thông báo thành công
7. Click **Save private key**
8. Khi được hỏi về passphrase, click **Yes** (nếu bạn không muốn đặt passphrase)
9. Lưu file dưới tên `EC2tutorial.ppk`

File PEM của bạn đã được chuyển đổi thành công sang định dạng PPK.

## Bước 3: Cấu hình Kết nối PuTTY

1. Mở ứng dụng **PuTTY**
2. Trong danh mục Session:
   - Nhập địa chỉ IPv4 công khai của EC2 instance vào trường "Host Name"
   - Định dạng: `ec2-user@<địa-chỉ-ip-công-khai>`
   - Ví dụ: `ec2-user@54.123.45.67`
   - Đảm bảo loại kết nối là **SSH**
   - Port phải là **22**
3. Lưu phiên này:
   - Nhập tên trong "Saved Sessions" (ví dụ: "EC2 Instance")
   - Click **Save**

## Bước 4: Cấu hình Xác thực

1. Trong cửa sổ PuTTY Configuration, điều hướng đến:
   - **Connection** → **SSH** → **Auth**
2. Click **Browse** bên cạnh "Private key file for authentication"
3. Điều hướng đến vị trí file `.ppk` của bạn
4. Chọn file PPK của bạn (ví dụ: `EC2tutorial.ppk`)
5. Quay lại danh mục **Session**
6. Click **Save** một lần nữa để lưu profile hoàn chỉnh

## Bước 5: Kết nối đến EC2 Instance

1. Trong PuTTY, chọn phiên đã lưu của bạn (ví dụ: "EC2 Instance")
2. Click **Load**
3. Click **Open**
4. Ở lần kết nối đầu tiên, chấp nhận cảnh báo bảo mật bằng cách click **Yes**
5. Bây giờ bạn đã được kết nối đến Amazon Linux 2 instance

## Xác minh Kết nối

Sau khi kết nối, bạn có thể xác minh kết nối với các lệnh sau:

```bash
whoami
# Output: ec2-user

ping google.com
# Nhấn Ctrl+C để dừng
```

## Mẹo

- **Saved Sessions**: Sau khi cấu hình, bạn chỉ cần load phiên đã lưu và click Open cho các lần kết nối sau
- **Thoát**: Gõ `exit` hoặc đơn giản đóng cửa sổ PuTTY để kết thúc phiên
- **Dừng Lệnh**: Nhấn `Ctrl+C` để dừng các lệnh đang chạy

## Xử lý Sự cố

Nếu bạn gặp vấn đề xác thực:
1. Xác minh file PPK được cấu hình đúng trong SSH → Auth
2. Đảm bảo username `ec2-user` được bao gồm trong hostname
3. Kiểm tra security group EC2 cho phép SSH (cổng 22) từ IP của bạn
4. Xác minh bạn đang sử dụng đúng key pair được liên kết với instance

## Các Bước Tiếp theo

- Đối với người dùng Windows 10, có phương pháp SSH thay thế sử dụng SSH client tích hợp của Windows
- Thực hành chạy các lệnh Linux cơ bản trên EC2 instance
- Tìm hiểu về các phương pháp bảo mật tốt nhất của EC2

## Tóm tắt

Bạn đã học thành công cách:
- Cài đặt PuTTY trên Windows
- Chuyển đổi khóa PEM sang định dạng PPK sử dụng PuTTYgen
- Cấu hình và lưu profile kết nối PuTTY
- SSH vào EC2 instances sử dụng PuTTY

Bất cứ khi nào khóa học đề cập đến "SSH vào instance", người dùng Windows nên sử dụng PuTTY để kết nối.



================================================================================
FILE: 33-ssh-into-ec2-instance-windows-10.md
================================================================================

# SSH vào EC2 Instance trên Windows 10

## Tổng quan

Hướng dẫn này trình bày cách kết nối đến Amazon EC2 instance sử dụng SSH trên Windows 10, bao gồm cả cách khắc phục các vấn đề về quyền truy cập với file PEM.

## Yêu cầu

- Windows 10 có sẵn lệnh SSH
- EC2 instance đang chạy trên AWS
- File khóa PEM đã tải xuống từ AWS
- Security group có mở cổng 22 cho SSH

## Kiểm tra SSH có sẵn

### Sử dụng Windows PowerShell

1. Mở Windows PowerShell
2. Gõ `ssh` và nhấn Enter
3. Nếu bạn thấy văn bản trợ giúp SSH, lệnh đã có sẵn

### Sử dụng Command Prompt

1. Mở Command Prompt
2. Gõ `ssh` và nhấn Enter
3. Nếu bạn thấy văn bản trợ giúp SSH, lệnh đã có sẵn

**Lưu ý:** Nếu lệnh SSH không có sẵn, bạn phải sử dụng phương pháp PuTTY thay thế.

## Kết nối đến EC2 Instance

### Bước 1: Di chuyển đến thư mục chứa file PEM

```powershell
# Di chuyển đến thư mục chứa file PEM của bạn
cd .\Desktop

# Liệt kê các file để xác nhận vị trí file PEM
ls
```

### Bước 2: Thực thi lệnh SSH

```powershell
ssh -i EC2Tutorial.pem ec2-user@<PUBLIC_IP>
```

**Giải thích lệnh:**
- `-i`: Chỉ định file khóa (identity file)
- `EC2Tutorial.pem`: Tên file khóa PEM của bạn
- `ec2-user`: Tên người dùng mặc định cho Amazon Linux instances
- `<PUBLIC_IP>`: Địa chỉ IP công khai của EC2 instance

### Bước 3: Chấp nhận xác thực host

Khi được nhắc "The authenticity of the host cannot be trusted, do you want to continue?", gõ `yes`.

## Khắc phục vấn đề quyền truy cập

Nếu bạn gặp lỗi quyền truy cập với file PEM, thực hiện các bước sau:

### Cấu hình quyền truy cập file

1. **Tìm file PEM của bạn**
   - Di chuyển đến thư mục chứa file PEM (ví dụ: Desktop)

2. **Truy cập thuộc tính bảo mật**
   - Nhấp chuột phải vào file PEM
   - Chọn "Properties"
   - Vào tab "Security"
   - Nhấp "Advanced"

3. **Đặt chủ sở hữu file**
   - Đảm bảo chủ sở hữu là bạn
   - Nếu không, nhấp "Change"
   - Trong "Object types", chọn loại người dùng của bạn
   - Đảm bảo "Locations" được đặt ở máy tính của bạn
   - Gõ tên người dùng của bạn và nhấp "Check Names"
   - Nhấp "OK" để xác nhận

4. **Xóa quyền thừa kế**
   - Nhấp "Disable inheritance"
   - Chọn "Remove all inherited permissions from this object"

5. **Xóa các thực thể không cần thiết**
   - Xóa các mục "SYSTEM" và "Administrators"
   - Các thực thể này không cần quyền truy cập vào file PEM của bạn

6. **Thêm người dùng của bạn với quyền Full Control**
   - Nhấp "Add"
   - Nhấp "Select a principal"
   - Gõ tên người dùng của bạn và nhấp "Check Names"
   - Nhấp "OK"
   - Cấp quyền "Full control"
   - Nhấp "OK" để lưu

7. **Xác minh quyền truy cập**
   - Nhấp "OK" trên tất cả các hộp thoại
   - Nhấp chuột phải vào file PEM lại và chọn "Properties"
   - Trong tab "Security", xác minh chỉ có tên người dùng của bạn xuất hiện với quyền đầy đủ

### Thử lại kết nối SSH

Sau khi sửa quyền truy cập, chạy lại lệnh SSH:

```powershell
ssh -i EC2Tutorial.pem ec2-user@<PUBLIC_IP>
```

Bạn sẽ không còn nhận được lỗi quyền truy cập hoặc nhắc xác thực host nữa.

## Sử dụng Command Prompt

Lệnh SSH tương tự hoạt động trong Command Prompt:

1. Mở Command Prompt
2. Di chuyển đến thư mục chứa file PEM
3. Thực thi lệnh SSH

```cmd
cd Desktop
ssh -i EC2Tutorial.pem ec2-user@<PUBLIC_IP>
```

## Ngắt kết nối khỏi EC2 Instance

Để thoát khỏi phiên SSH:

- Gõ `exit` và nhấn Enter, hoặc
- Nhấn `Ctrl + D`

## Mẹo

- Sử dụng phím Tab để tự động hoàn thành khi gõ tên file
- Đảm bảo security group của EC2 có quy tắc inbound cho phép SSH (cổng 22)
- Giữ file PEM của bạn an toàn và không bao giờ chia sẻ
- File `.ppk` chỉ cần thiết cho kết nối PuTTY

## Thực hành tốt về bảo mật

- Chỉ cấp quyền truy cập cho chính bạn đối với file PEM
- Lưu trữ file PEM ở vị trí an toàn
- Không bao giờ commit file PEM vào hệ thống quản lý phiên bản
- Sử dụng file PEM riêng biệt cho các môi trường khác nhau
- Thường xuyên thay đổi SSH keys

## Các vấn đề thường gặp

### Không tìm thấy lệnh SSH
- Cài đặt OpenSSH client từ Windows Features
- Thay thế: Sử dụng PuTTY cho kết nối SSH

### Timeout kết nối
- Xác minh security group cho phép inbound SSH (cổng 22)
- Kiểm tra EC2 instance đang chạy
- Xác minh bạn đang sử dụng đúng public IP

### Permission Denied (Từ chối quyền truy cập)
- Đảm bảo file PEM có quyền truy cập đúng (làm theo các bước sửa quyền)
- Xác minh bạn đang sử dụng đúng tên người dùng (ec2-user cho Amazon Linux)
- Xác nhận bạn đang sử dụng đúng file PEM cho instance

## Kết luận

Bây giờ bạn có thể SSH vào EC2 instance thành công trực tiếp từ Windows 10 sử dụng PowerShell hoặc Command Prompt. Với quyền truy cập file PEM được cấu hình đúng, bạn sẽ có quyền truy cập liền mạch vào cơ sở hạ tầng AWS của mình.



================================================================================
FILE: 34-ssh-troubleshooting-guide.md
================================================================================

# Hướng Dẫn Khắc Phục Sự Cố SSH

Hướng dẫn này bao gồm các vấn đề kết nối SSH phổ biến khi kết nối đến AWS EC2 instances và cách giải quyết.

## 1) Lỗi Connection Timeout (Hết Thời Gian Kết Nối)

**Vấn đề:** Bị lỗi timeout khi cố gắng kết nối qua SSH.

**Giải pháp:** Đây là vấn đề về security group. Bất kỳ lỗi timeout nào (không chỉ SSH) đều liên quan đến security groups hoặc firewall. Đảm bảo security group của bạn được cấu hình đúng và được gán chính xác cho EC2 instance.

**Các điểm chính:**
- Kiểm tra cấu hình security group của EC2
- Xác minh inbound rules cho phép SSH (cổng 22) từ địa chỉ IP của bạn
- Đảm bảo security group được gắn vào EC2 instance của bạn

## 2) Lỗi Connection Timeout Vẫn Tiếp Diễn

**Vấn đề:** Lỗi timeout vẫn tiếp tục mặc dù đã cấu hình security groups đúng.

**Giải pháp:** Nếu security group đã được cấu hình đúng và vẫn còn vấn đề timeout, có thể firewall của công ty hoặc firewall cá nhân đang chặn kết nối.

**Khuyến nghị:** Sử dụng EC2 Instance Connect như một phương pháp thay thế để truy cập instance.

## 3) Lệnh SSH Không Hoạt Động Trên Windows

**Vấn đề:** Thông báo lỗi "ssh command not found" xuất hiện trên Windows.

**Giải pháp:** Điều này có nghĩa là bạn cần sử dụng PuTTY thay vì lệnh SSH gốc.

**Các bước:**
- Tải xuống và cài đặt PuTTY
- Làm theo hướng dẫn cấu hình PuTTY
- Nếu vấn đề vẫn tiếp diễn, hãy sử dụng EC2 Instance Connect như được mô tả trong bài giảng tiếp theo

## 4) Lỗi Connection Refused (Kết Nối Bị Từ Chối)

**Vấn đề:** Xuất hiện lỗi "Connection refused".

**Giải pháp:** Điều này có nghĩa là instance có thể truy cập được, nhưng không có dịch vụ SSH nào đang chạy trên instance.

**Các bước giải quyết:**
1. Thử khởi động lại instance
2. Nếu khởi động lại không hiệu quả, hãy terminate instance và tạo instance mới
3. Đảm bảo bạn đang sử dụng Amazon Linux 2

## 5) Lỗi Permission Denied (Quyền Truy Cập Bị Từ Chối)

**Vấn đề:** Thông báo lỗi "Permission denied (publickey,gssapi-keyex,gssapi-with-mic)"

**Các nguyên nhân có thể:**

### Security Key Sai
- Bạn đang sử dụng security key sai hoặc không sử dụng security key
- Kiểm tra cấu hình EC2 instance để đảm bảo bạn đã gán đúng key pair

### Tên Người Dùng Sai
- Bạn đang sử dụng tên người dùng sai
- Đảm bảo bạn đã khởi động Amazon Linux 2 EC2 instance
- Sử dụng đúng user: `ec2-user`
- Định dạng: `ec2-user@<public-ip>` (ví dụ: `ec2-user@35.180.242.162`)
- Áp dụng cho cả lệnh SSH và cấu hình PuTTY

## 6) Không Có Gì Hoạt Động

**Vấn đề:** Tất cả các bước khắc phục sự cố đều thất bại.

**Giải pháp:** Đừng hoảng sợ! Sử dụng EC2 Instance Connect như một giải pháp thay thế.

**Yêu cầu:**
- Đảm bảo bạn đã khởi động Amazon Linux 2 instance
- Truy cập thông qua EC2 Instance Connect từ AWS Console
- Bạn sẽ có thể làm theo hướng dẫn

## 7) Kết Nối Hoạt Động Hôm Qua Nhưng Hôm Nay Không

**Vấn đề:** Kết nối SSH hoạt động trước đó nhưng thất bại sau khi dừng và khởi động lại instance.

**Nguyên nhân gốc:** Khi bạn dừng và khởi động lại EC2 instance, địa chỉ public IP sẽ thay đổi.

**Giải pháp:**
- Lấy địa chỉ public IP mới từ EC2 console
- Cập nhật lệnh SSH hoặc cấu hình PuTTY với public IP mới
- Lưu cấu hình đã cập nhật

**Ví dụ:**
- Cũ: `ec2-user@35.180.242.162`
- Mới: `ec2-user@<new-public-ip>`

---

## Bảng Tham Khảo Nhanh

| Loại Lỗi | Nguyên Nhân Chính | Cách Khắc Phục Nhanh |
|-----------|-------------------|----------------------|
| Connection Timeout | Security Group / Firewall | Kiểm tra quy tắc security group |
| SSH Not Found (Windows) | Thiếu SSH client | Sử dụng PuTTY |
| Connection Refused | Dịch vụ SSH không chạy | Khởi động lại instance |
| Permission Denied | Key hoặc username sai | Xác minh key pair và dùng `ec2-user` |
| IP Thay Đổi | Instance bị dừng/khởi động | Cập nhật public IP trong cấu hình |

## Các Phương Pháp Hay Nhất

1. **Luôn sử dụng Amazon Linux 2** để đảm bảo tính nhất quán
2. **Giữ security groups được cấu hình đúng** với quyền truy cập tối thiểu cần thiết
3. **Sử dụng EC2 Instance Connect** như phương pháp dự phòng
4. **Lưu ý public IP thay đổi** khi dừng/khởi động instances
5. **Giữ private key an toàn** và ở đúng vị trí
6. **Sử dụng đúng username** (`ec2-user` cho Amazon Linux 2)



================================================================================
FILE: 35-ec2-instance-connect-tutorial.md
================================================================================

# Hướng Dẫn EC2 Instance Connect

## Tổng Quan

EC2 Instance Connect cung cấp một phương thức thay thế SSH dựa trên trình duyệt để kết nối với các EC2 instance của bạn. Phương pháp này dễ dàng hơn SSH truyền thống vì nó loại bỏ nhu cầu quản lý SSH keys thủ công.

## EC2 Instance Connect Là Gì?

EC2 Instance Connect là một tính năng cho phép bạn thiết lập phiên SSH dựa trên trình duyệt trực tiếp đến EC2 instance thông qua AWS Console. Khi bạn kết nối, AWS tự động tải lên một SSH key tạm thời để thiết lập kết nối, loại bỏ sự phức tạp trong việc quản lý SSH key.

## Cách Sử Dụng EC2 Instance Connect

### Bước 1: Điều Hướng Đến Instance Của Bạn

1. Click vào EC2 instance của bạn (ví dụ: "My First Instance")
2. Click nút **Connect** ở phía trên cùng của trang

### Bước 2: Chọn EC2 Instance Connect

Bạn sẽ thấy nhiều tùy chọn kết nối:
- SSH client (phương pháp truyền thống)
- **EC2 Instance Connect** (khuyến nghị vì dễ sử dụng)

### Bước 3: Cấu Hình Cài Đặt Kết Nối

- **Public IP Address**: Tự động được xác minh
- **Username**: Được điền sẵn là `ec2-user` (AWS tự động phát hiện Amazon Linux 2 AMI)
  - Bạn có thể ghi đè điều này nếu cần, nhưng nó phải khớp với username thực tế
- **SSH Key**: Không bắt buộc - AWS tự động xử lý với temporary key

### Bước 4: Kết Nối

Click nút **Connect**. Một tab trình duyệt mới sẽ mở với phiên terminal được kết nối đến Amazon Linux 2 AMI instance của bạn.

## Sử Dụng Instance

Sau khi kết nối, bạn có thể chạy bất kỳ lệnh Linux nào:

```bash
whoami
ping google.com
```

Phiên của bạn chạy hoàn toàn trong trình duyệt mà không cần ứng dụng terminal riêng biệt.

## So Sánh Các Phương Thức Kết Nối

Trong suốt khóa học này, khi SSH được đề cập, bạn có thể chọn bất kỳ phương pháp nào sau:

- **Terminal của bạn** với lệnh SSH
- **PuTTY** (Windows)
- **Lệnh SSH** (Windows, Linux, hoặc Mac)
- **EC2 Instance Connect** (Tất cả nền tảng, dựa trên trình duyệt)

## Quan Trọng: Cấu Hình Security Group

EC2 Instance Connect dựa vào SSH (port 22) ở phía sau. Security group của bạn **phải** cho phép lưu lượng SSH inbound.

### Khắc Phục Sự Cố Kết Nối

Nếu bạn gặp vấn đề kết nối:

#### Vấn Đề: "Problem connecting to your instance"

**Giải Pháp**: Đảm bảo port 22 được mở trong security group của bạn

1. Điều hướng đến security group của instance
2. Click **Edit inbound rules**
3. Thêm SSH rule:
   - **Type**: SSH
   - **Port**: 22
   - **Source**: Anywhere IPv4 (0.0.0.0/0)
4. Lưu các rules

#### Vấn Đề: Kết nối vẫn thất bại

Một số thiết lập yêu cầu cấu hình IPv6:

1. Chỉnh sửa inbound rules lại
2. Thêm một SSH rule khác:
   - **Type**: SSH
   - **Port**: 22
   - **Source**: Anywhere IPv6 (::/0)
3. Lưu các rules

### Security Group Rules Bắt Buộc

Để EC2 Instance Connect hoạt động ổn định:

| Type | Protocol | Port | Source |
|------|----------|------|--------|
| SSH  | TCP      | 22   | 0.0.0.0/0 (IPv4) |
| SSH  | TCP      | 22   | ::/0 (IPv6) |

**Lưu ý**: Các rules cụ thể cần thiết có thể khác nhau tùy thuộc vào thiết lập mạng của bạn.

## Kiểm Tra Kết Nối

Sau khi cấu hình security groups:

1. Đóng bất kỳ nỗ lực kết nối hiện tại nào
2. Quay lại EC2 instance của bạn
3. Click **Connect** lại
4. Chọn **EC2 Instance Connect**
5. Click **Connect**

Bây giờ bạn sẽ kết nối thành công đến instance của mình.

## Lợi Ích Của EC2 Instance Connect

- ✅ Không cần quản lý SSH key
- ✅ Truy cập dựa trên trình duyệt
- ✅ Hoạt động trên tất cả các nền tảng (Windows, Linux, Mac)
- ✅ Nhanh chóng và dễ sử dụng
- ✅ Temporary keys để tăng cường bảo mật

## Tóm Tắt

EC2 Instance Connect là một giải pháp thay thế thuận tiện cho SSH truyền thống và sẽ được sử dụng thường xuyên trong suốt khóa học này. Nó đơn giản hóa quy trình kết nối trong khi vẫn duy trì bảo mật thông qua các SSH key tạm thời được quản lý bởi AWS.

---

*Phương pháp này sẽ được sử dụng rộng rãi trong các bài giảng sắp tới cho các demo thực hành.*



================================================================================
FILE: 36-using-iam-roles-with-ec2-instances.md
================================================================================

# Sử Dụng IAM Roles với EC2 Instances - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách đúng đắn để cung cấp AWS credentials cho các EC2 instances bằng cách sử dụng IAM roles, thay vì hardcode access keys trực tiếp trên instance.

## Yêu Cầu Trước

- Tài khoản AWS với EC2 instance đang chạy
- Kiến thức cơ bản về IAM roles và policies
- Quyền truy cập EC2 Instance Connect hoặc SSH

## Kết Nối Đến EC2 Instance

Có nhiều cách để kết nối đến EC2 instance:

- **SSH** - Sử dụng terminal hoặc command line
- **EC2 Instance Connect** - Kết nối qua trình duyệt
- **PuTTY** - Dành cho người dùng Windows

Trong hướng dẫn này, chúng ta sẽ sử dụng **EC2 Instance Connect** vì nó đơn giản hơn và hoạt động trực tiếp trên trình duyệt web.

Sau khi kết nối, bạn sẽ thấy dấu nhắc tương tự như:
```
ec2-user@<private-ip>
```

## Kiểm Tra Các Lệnh Linux Cơ Bản

Bạn có thể xác minh kết nối bằng cách chạy các lệnh Linux cơ bản:

```bash
ping google.com
```

Nhấn `Ctrl + C` để dừng lệnh ping.

Để xóa màn hình:
```bash
clear
```

## AWS CLI trên Amazon Linux

Amazon Linux AMI đi kèm với AWS CLI được cài đặt sẵn, vì vậy bạn có thể ngay lập tức bắt đầu sử dụng các lệnh AWS.

## ❌ Cách Làm Sai: Sử Dụng AWS Configure

Bạn có thể bị cám dỗ để chạy:

```bash
aws iam list-users
```

Lệnh này sẽ trả về lỗi về việc không thể xác định credentials, và gợi ý bạn chạy `aws configure`.

### **KHÔNG BAO GIỜ LÀM ĐIỀU NÀY!**

Chạy `aws configure` và nhập Access Key ID và Secret Access Key cá nhân của bạn trực tiếp trên EC2 instance là một **thực hành bảo mật rất tệ**.

### Tại Sao Điều Này Nguy Hiểm:

- Bất kỳ ai có quyền truy cập vào tài khoản AWS của bạn đều có thể kết nối đến EC2 instance
- Họ có thể lấy được credentials đã lưu trữ của bạn
- IAM credentials cá nhân của bạn có thể bị xâm phạm

> **Nguyên Tắc Vàng**: Không bao giờ, không bao giờ, không bao giờ nhập IAM API keys (Access Key ID và Secret Access Key) vào EC2 instance.

## ✅ Cách Làm Đúng: Sử Dụng IAM Roles

### Bước 1: Tạo IAM Role

1. Vào IAM console
2. Điều hướng đến **Roles**
3. Tạo một role (ví dụ: `DemoRoleForEC2`)
4. Gắn policy cần thiết (ví dụ: `IAMReadOnlyAccess`)

### Bước 2: Gắn IAM Role vào EC2 Instance

1. Vào EC2 instance của bạn
2. Điều hướng đến tab **Security**
3. Bạn sẽ thấy hiện tại chưa có IAM role nào được gắn
4. Nhấp vào **Actions** → **Security** → **Modify IAM role**
5. Chọn IAM role của bạn (ví dụ: `DemoRoleForEC2`)
6. Nhấp **Save**

### Bước 3: Xác Minh Role Đang Hoạt Động

Quay lại tab **Security** và xác nhận IAM role đã được gắn.

Bây giờ, trong terminal EC2 instance của bạn, chạy:

```bash
aws iam list-users
```

**Thành công!** Bạn sẽ thấy phản hồi với danh sách IAM users, mặc dù bạn chưa bao giờ chạy `aws configure`.

## Kiểm Tra Quyền Của Role

### Gỡ Bỏ Quyền

1. Vào IAM role trong console
2. Tách policy `IAMReadOnlyAccess`
3. Chạy lại lệnh trong EC2 instance:

```bash
aws iam list-users
```

Bạn sẽ nhận được lỗi **Access Denied**, chứng minh role được liên kết trực tiếp với EC2 instance.

### Gắn Lại Quyền

1. Quay lại IAM và gắn lại policy `IAMReadOnlyAccess`
2. Chạy lại lệnh

**Lưu ý**: Bạn có thể nhận được lỗi access denied ban đầu. Các thay đổi IAM có thể mất một chút thời gian để lan truyền. Thử chạy lại lệnh sau vài giây, và bạn sẽ thấy kết quả mong đợi.

## Điểm Quan Trọng Cần Nhớ

- ✅ **Luôn sử dụng IAM roles** để cung cấp credentials cho EC2 instances
- ❌ **Không bao giờ sử dụng `aws configure`** để lưu trữ credentials cá nhân trên EC2 instances
- 🔒 IAM roles cung cấp quản lý credentials tạm thời và tự động
- ⏱️ Các thay đổi IAM policy có thể mất vài phút để lan truyền

## Thực Hành Tốt Nhất

1. Tạo các IAM roles cụ thể cho các mục đích EC2 instance khác nhau
2. Tuân theo nguyên tắc đặc quyền tối thiểu - chỉ cấp quyền cần thiết
3. Thường xuyên kiểm tra quyền của IAM role
4. Sử dụng IAM roles cho tất cả xác thực giữa các AWS resources

## Kết Luận

Sử dụng IAM roles cho EC2 instances là cách an toàn và được khuyến nghị để cung cấp AWS credentials. Phương pháp này đảm bảo credentials là tạm thời, tự động xoay vòng, và không bao giờ bị lộ trên chính instance.

---

*Hướng dẫn thực hành này trình bày các thực hành bảo mật AWS thiết yếu để quản lý credentials trong EC2 instances.*



================================================================================
FILE: 37-ec2-instances-purchasing-options.md
================================================================================

# Các Tùy Chọn Mua EC2 Instances

## Tổng Quan

AWS EC2 cung cấp nhiều tùy chọn mua khác nhau để tối ưu hóa chi phí dựa trên yêu cầu khối lượng công việc của bạn. Trong khi các instance on-demand cung cấp tính linh hoạt, các tùy chọn khác có thể giảm đáng kể chi phí cho các trường hợp sử dụng khác nhau.

## Tóm Tắt Các Tùy Chọn Mua

### 1. **On-Demand Instances (Instance Theo Yêu Cầu)**
- **Trường Hợp Sử Dụng**: Khối lượng công việc ngắn hạn với giá cả có thể dự đoán
- **Tính Phí**: Thanh toán theo giây (Linux/Windows sau phút đầu tiên) hoặc theo giờ (các HĐH khác)
- **Lợi Ích**: 
  - Không cần thanh toán trước
  - Không có cam kết dài hạn
  - Tính linh hoạt cao nhất
- **Phù Hợp Nhất Cho**: Khối lượng công việc ngắn hạn, không bị gián đoạn khi hành vi ứng dụng không thể dự đoán

### 2. **Reserved Instances (Instance Dự Trữ - RI)**
- **Thời Hạn**: 1 hoặc 3 năm
- **Giảm Giá**: Lên đến 72% so với on-demand
- **Trường Hợp Sử Dụng**: Khối lượng công việc dài hạn (ví dụ: cơ sở dữ liệu)
- **Thuộc Tính Đặt Trước**:
  - Loại instance
  - Khu vực (Region)
  - Tenancy
  - Hệ điều hành
- **Tùy Chọn Thanh Toán**:
  - Tất cả trả trước (giảm giá tối đa)
  - Một phần trả trước
  - Không trả trước
- **Tùy Chọn Phạm Vi**:
  - Khu vực (Regional)
  - Vùng cụ thể (Zonal - dự trữ dung lượng trong AZ cụ thể)
- **Tính Năng Bổ Sung**: Có thể mua/bán trên RI Marketplace
- **Phù Hợp Nhất Cho**: Các ứng dụng sử dụng ổn định

#### Convertible Reserved Instances (Instance Dự Trữ Có Thể Chuyển Đổi)
- **Giảm Giá**: Lên đến 66%
- **Tính Linh Hoạt**: Có thể thay đổi:
  - Loại instance
  - Họ instance
  - Hệ điều hành
  - Phạm vi
  - Tenancy

### 3. **EC2 Savings Plans (Kế Hoạch Tiết Kiệm EC2)**
- **Thời Hạn**: 1 hoặc 3 năm
- **Giảm Giá**: Lên đến 72%
- **Cam Kết**: Số tiền cụ thể mỗi giờ (ví dụ: $10/giờ)
- **Bị Khóa**: Họ instance và khu vực (ví dụ: M5 trong us-east-1)
- **Linh Hoạt**:
  - Kích thước instance (m5.xlarge, m5.2xlarge, v.v.)
  - Hệ điều hành
  - Tenancy (host, dedicated, default)
- **Vượt Mức**: Sử dụng vượt kế hoạch được tính theo giá on-demand
- **Phù Hợp Nhất Cho**: Khối lượng công việc dài hạn với tính linh hoạt hiện đại hơn

### 4. **Spot Instances (Instance Giá Thầu)**
- **Giảm Giá**: Lên đến 90% so với on-demand
- **Rủi Ro**: Có thể mất instance bất cứ lúc nào nếu giá spot vượt quá giá tối đa của bạn
- **Trường Hợp Sử Dụng**: Khối lượng công việc có khả năng chịu lỗi
- **Phù Hợp Cho**:
  - Công việc xử lý theo lô (Batch jobs)
  - Phân tích dữ liệu
  - Xử lý hình ảnh
  - Khối lượng công việc phân tán
  - Khối lượng công việc có thời gian bắt đầu/kết thúc linh hoạt
- **Không Phù Hợp Cho**: Công việc quan trọng hoặc cơ sở dữ liệu
- **Lưu Ý**: Tùy chọn tiết kiệm chi phí nhất trong AWS

### 5. **Dedicated Hosts (Máy Chủ Chuyên Dụng)**
- **Mô Tả**: Máy chủ vật lý với dung lượng EC2 hoàn toàn dành riêng cho bạn
- **Trường Hợp Sử Dụng**:
  - Yêu cầu tuân thủ (compliance)
  - Giấy phép phần mềm gắn với máy chủ (per-socket, per-core, per-VM)
  - Mang Giấy Phép Của Riêng Bạn (BYOL - Bring Your Own License)
  - Nhu cầu tuân thủ/quy định nghiêm ngặt
- **Thanh Toán**: On-demand (theo giây) hoặc Reserved (1-3 năm)
- **Chi Phí**: Tùy chọn đắt nhất
- **Truy Cập**: Có thể nhìn thấy phần cứng cấp thấp hơn

### 6. **Dedicated Instances (Instance Chuyên Dụng)**
- **Mô Tả**: Các instance chạy trên phần cứng dành riêng cho bạn
- **Khác Biệt với Dedicated Hosts**: 
  - Có thể chia sẻ phần cứng với các instance khác trong cùng tài khoản
  - Không kiểm soát vị trí đặt instance
  - Không thấy được máy chủ vật lý
- **Trường Hợp Sử Dụng**: Cách ly phần cứng mà không cần truy cập máy chủ vật lý

### 7. **Capacity Reservations (Đặt Trước Dung Lượng)**
- **Mô Tả**: Đặt trước các instance on-demand trong AZ cụ thể
- **Thời Hạn**: Bất kỳ thời hạn nào (không có cam kết thời gian)
- **Cam Kết**: Có thể đặt trước hoặc hủy bất cứ lúc nào
- **Tính Phí**: Giá on-demand (được tính phí cho dù bạn có chạy instance hay không)
- **Giảm Giá**: Không có (kết hợp với Regional RI hoặc Savings Plans để được giảm giá)
- **Phù Hợp Nhất Cho**: Khối lượng công việc ngắn hạn, không bị gián đoạn trong AZ cụ thể

## Ví Dụ Tương Tự Resort

Để hiểu rõ hơn các tùy chọn này, hãy nghĩ về một khu nghỉ dưỡng:

- **On-Demand**: Đến và ở bất cứ khi nào bạn thích, trả giá đầy đủ
- **Reserved**: Lên kế hoạch trước cho thời gian ở dài (1-3 năm), được giảm giá cho cam kết
- **Savings Plan**: Cam kết chi $300/tháng trong 12 tháng, có thể đổi loại phòng
- **Spot**: Giảm giá phút chót cho phòng trống, nhưng có thể bị đuổi ra nếu ai đó trả nhiều hơn
- **Dedicated Host**: Đặt toàn bộ tòa nhà của khu nghỉ dưỡng
- **Capacity Reservation**: Đặt phòng bạn có thể không sử dụng, trả giá đầy đủ để đảm bảo có sẵn

## Ví Dụ So Sánh Giá

Dựa trên m4.large trong us-east-1 (giá chỉ mang tính minh họa):

| Tùy Chọn | Giá | Giảm Giá |
|----------|-----|----------|
| On-Demand | $0.10/giờ | Cơ sở |
| Spot | ~$0.04/giờ | Lên đến 61% |
| Reserved (1 năm, không trả trước) | Khác nhau | ~40% |
| Reserved (3 năm, tất cả trả trước) | Khác nhau | ~72% |
| Convertible RI | Khác nhau | ~66% |
| Savings Plan | Giống RI | ~72% |
| Dedicated Host | $0.10/giờ | 0% |
| Dedicated Host Reserved | Khác nhau | ~70% |
| Capacity Reservation | $0.10/giờ | 0% |

## Điểm Chính Cần Nhớ

1. **Tối Ưu Hóa Chi Phí**: Chọn dựa trên đặc điểm khối lượng công việc
2. **Cam Kết vs Linh Hoạt**: Cam kết dài hơn = giảm giá cao hơn
3. **Phù Hợp Khối Lượng Công Việc**: Khớp loại instance với yêu cầu khối lượng công việc
4. **Nhu Cầu Tuân Thủ**: Sử dụng Dedicated Hosts/Instances khi cần thiết
5. **Lập Kế Hoạch Dung Lượng**: Sử dụng Capacity Reservations cho khối lượng công việc quan trọng trong AZ cụ thể

## Mẹo Cho Kỳ Thi

- Hiểu tùy chọn nào phù hợp với từng loại khối lượng công việc cụ thể
- Nhớ rằng Spot Instances KHÔNG phù hợp cho công việc quan trọng/cơ sở dữ liệu
- Biết sự khác biệt giữa Dedicated Hosts và Dedicated Instances
- Hiểu thời gian cam kết và mức giảm giá
- Nhận biết các trường hợp sử dụng cho từng tùy chọn mua



================================================================================
FILE: 38-aws-ebs-volumes-overview.md
================================================================================

# Tổng Quan về AWS EBS Volumes

## Giới Thiệu

Trong phần này, chúng ta sẽ khám phá các tùy chọn lưu trữ khác nhau có sẵn cho các EC2 instances, với trọng tâm chính là EBS (Elastic Block Store) volumes.

## EBS là gì?

**EBS (Elastic Block Store)** là một ổ đĩa mạng có thể được gắn vào các EC2 instances trong khi chúng đang chạy. EBS volumes đã được sử dụng trong các cấu hình trước đó, thường là không có nhận thức rõ ràng.

### Lợi Ích Chính

- **Lưu Trữ Dữ Liệu Bền Vững**: EBS volumes cho phép dữ liệu tồn tại ngay cả sau khi instance bị terminated
- **Khôi Phục Dữ Liệu**: Bạn có thể tạo lại một instance và mount lại EBS volume cũ để lấy lại dữ liệu
- **Linh Hoạt**: Volumes có thể được tháo rời và gắn lại vào các instances khác nhau

## Các Đặc Điểm Quan Trọng

### Ràng Buộc Availability Zone

Ở cấp độ Certified Cloud Practitioner (CCP):
- Một EBS volume chỉ có thể được mount vào **một instance tại một thời điểm**
- Khi được tạo, EBS volume được **ràng buộc với một availability zone cụ thể**
- Ví dụ: Một EBS volume được tạo trong US-East-1a không thể gắn vào instance trong US-East-1b

### Khái Niệm Ổ Đĩa Mạng

Hãy nghĩ về EBS volumes như **"USB sticks qua mạng"** - chúng có thể được chuyển giữa các máy tính mà không cần kết nối vật lý, hoạt động hoàn toàn qua mạng.

## Chi Tiết Kỹ Thuật

### Giao Tiếp Qua Mạng

- **Dựa trên mạng**: EBS không phải là ổ đĩa vật lý
- **Độ trễ**: Có thể có một chút độ trễ do giao tiếp mạng giữa instance và EBS volume
- **Tháo rời nhanh**: Volumes có thể được tháo rời nhanh chóng từ một EC2 instance và gắn vào instance khác
- **Trường hợp sử dụng**: Lý tưởng cho các tình huống failover

### Cung Cấp Dung Lượng

Bạn phải cung cấp dung lượng trước:
- **Kích thước**: Chỉ định số gigabytes (GB) cần thiết
- **IOPS**: Xác định I/O Operations Per Second (số thao tác I/O mỗi giây) cho yêu cầu hiệu năng
- **Thanh toán**: Tính phí dựa trên dung lượng được cung cấp
- **Khả năng mở rộng**: Dung lượng có thể được tăng lên theo thời gian để có hiệu năng tốt hơn hoặc dung lượng lưu trữ bổ sung

## Giải Thích Sơ Đồ Kiến Trúc

### Ví Dụ Trong Một Availability Zone (US-East-1a)

- **EC2 Instance 1**: Có thể có một hoặc nhiều EBS volumes được gắn vào
- **EC2 Instance 2**: Yêu cầu EBS volume(s) riêng của nó
- **Nhiều Volumes**: Một EC2 instance có thể có nhiều EBS volumes được gắn vào (giống như nhiều USB sticks qua mạng)
- **Hạn chế**: Ở cấp độ CCP, một EBS volume không thể được gắn vào hai instances cùng một lúc

### Xem Xét Giữa Các Availability Zones

- EBS volumes được liên kết với availability zone của chúng
- Tương tự như EC2 instances, EBS volumes bị ràng buộc với một AZ cụ thể
- Để sử dụng volumes trong các AZs khác nhau, bạn phải tạo chúng riêng biệt trong mỗi zone
- **Lưu ý**: Snapshots cho phép bạn di chuyển volumes giữa các availability zones

### Volumes Không Được Gắn Kết

- EBS volumes có thể tồn tại mà không được gắn vào bất kỳ EC2 instance nào
- Chúng có thể được gắn theo yêu cầu khi cần thiết
- Điều này cung cấp tính linh hoạt trong quản lý lưu trữ

## Thuộc Tính Delete on Termination

Đây là một chủ đề quan trọng trong các kỳ thi chứng chỉ AWS.

### Hành Vi Mặc Định

Khi tạo EC2 instance thông qua console:

1. **Root Volume**: 
   - Delete on Termination được **bật theo mặc định**
   - Root EBS volume bị xóa khi instance bị terminate

2. **EBS Volumes Bổ Sung**:
   - Delete on Termination được **tắt theo mặc định**
   - Các volumes bổ sung được giữ lại khi instance bị terminate

### Tùy Chọn Cấu Hình

Thuộc tính Delete on Termination có thể được kiểm soát qua giao diện console:
- Bạn có thể bật hoặc tắt nó cho bất kỳ volume nào
- Hữu ích cho việc bảo toàn dữ liệu khi instances bị terminate

### Ví Dụ Trường Hợp Sử Dụng

**Tình huống**: Bảo toàn dữ liệu root volume khi một instance bị terminate
- **Giải pháp**: Tắt "Delete on Termination" cho root volume
- **Kết quả**: Dữ liệu được lưu ngay cả sau khi instance bị terminate

> **Mẹo Thi**: Tình huống này thường xuất hiện trong các kỳ thi chứng chỉ AWS.

## Tóm Tắt

EBS volumes cung cấp lưu trữ linh hoạt, bền vững cho EC2 instances với các điểm chính sau:
- Lưu trữ khối dựa trên mạng
- Ràng buộc với các availability zones cụ thể
- Dung lượng và hiệu năng có thể cấu hình
- Hành vi xóa có thể quản lý được
- Thiết yếu cho tính bền vững dữ liệu và các tình huống failover

---

*Tài liệu này bao gồm các khái niệm cơ bản về AWS EBS volumes liên quan đến EC2 instances.*



================================================================================
FILE: 39-aws-ebs-volumes-hands-on-tutorial.md
================================================================================

# AWS EBS Volumes - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách quản lý các ổ đĩa Amazon Elastic Block Store (EBS) với các EC2 instance, bao gồm tạo, gắn kết và xóa các volume.

## Xem Các EBS Volume Gắn Với Instance

Hãy bắt đầu bằng cách kiểm tra các EBS volume đã gắn với EC2 instance của chúng ta:

1. Click vào **EC2 instance** của bạn
2. Chuyển đến tab **Storage**
3. Bạn sẽ thấy một root device với một block device được gắn kết

Trong ví dụ này, chúng ta có một volume **8 gigabytes** hiện đang được gắn vào EC2 instance.

### Truy Cập Giao Diện Volumes

- Click vào volume ID để truy cập giao diện volumes của AWS
- Volume sẽ hiển thị trạng thái "in use" (đang sử dụng) và được gắn với instance của bạn
- Hoặc truy cập từ menu bên trái bằng cách click vào **Volumes**

## Tạo EBS Volume Mới

Bây giờ chúng ta có một EBS volume 8 gigabytes. Hãy tạo volume thứ hai:

### Bước 1: Tạo Volume

1. Click **Create Volume**
2. Chọn loại volume: GP2, GP3, v.v. (chúng ta sẽ dùng **GP2**)
3. Đặt kích thước **2 gigabytes**

### Bước 2: Chọn Availability Zone

**Quan trọng:** Các EBS volume được ràng buộc với các availability zone cụ thể.

1. Vào chi tiết EC2 instance của bạn
2. Cuộn xuống phần **Networking**
3. Ghi chú availability zone (ví dụ: `eu-west-1b`)
4. Tạo volume của bạn trong **cùng availability zone** (`eu-west-1b`)

Điều này đảm bảo volume có thể được gắn vào instance của bạn.

## Gắn Volume Vào Instance

Sau khi tạo volume:

1. Trạng thái volume sẽ là **Available** (chưa gắn kết)
2. Chọn volume và click **Actions** → **Attach Volume**
3. Chọn EC2 instance đang chạy của bạn
4. Click **Attach Volume**

Instance của bạn giờ có hai EBS volume được gắn kết!

### Xác Minh Việc Gắn Kết

1. Làm mới trang EC2 instance
2. Vào tab **Storage**
3. Cuộn xuống **Block Devices**
4. Bạn sẽ thấy cả hai volume:
   - 8 gigabytes (root volume)
   - 2 gigabytes (volume mới gắn)

**Lưu ý:** Để thực sự sử dụng block device mới, bạn cần format nó. Để biết hướng dẫn, tìm kiếm "make an Amazon EBS volume available to use on Linux" - quá trình này nằm ngoài phạm vi của hướng dẫn này.

## Hiểu Về Giới Hạn Availability Zone

Hãy chứng minh rằng EBS volume được ràng buộc với các availability zone cụ thể:

### Tạo Volume Ở AZ Khác

1. Tạo một volume khác 2 gigabytes GP2
2. Lần này, chọn **eu-west-1a** (khác với `eu-west-1b` của instance)
3. Sau khi tạo xong, thử gắn nó vào EC2 instance của bạn

**Kết quả:** Bạn không thể gắn nó! Điều này chứng minh rằng EBS volume thực sự bị ràng buộc bởi các availability zone cụ thể.

### Dọn Dẹp

- Chọn volume ở AZ sai
- Click **Actions** → **Delete Volume**
- Volume được xóa ngay lập tức

Điều này thể hiện sức mạnh của cloud: bạn có thể yêu cầu và xóa volume trong vài giây.

## Thuộc Tính Delete on Termination

Hãy khám phá điều gì xảy ra khi bạn terminate một EC2 instance.

### Kiểm Tra Thuộc Tính

1. Vào tab **Storage** của EC2 instance
2. Xem bảng **Block Devices**
3. Cuộn sang phải để thấy cột **Delete on Termination**:
   - Root volume (8 GB): **Yes**
   - Volume bổ sung (2 GB): **No**

### Tại Sao Root Volume Được Đặt Thành "Yes"?

Khi khởi chạy EC2 instance:

1. Trong wizard khởi chạy instance, cuộn đến **Storage**
2. Click vào **Advanced**
3. Root volume có **Delete on Termination** được đặt thành **Yes** theo mặc định
4. Bạn có thể thay đổi thành **No** nếu muốn giữ root volume sau khi terminate

## Terminate Instance và Hành Vi Của Volume

Hãy terminate instance để xem điều gì xảy ra:

1. Terminate EC2 instance của bạn
2. Quay lại trang **EBS Volumes**
3. Làm mới danh sách volume

### Điều Gì Xảy Ra:

- Volume 2 GB trở thành **Available** (tách ra nhưng không bị xóa)
- Root volume 8 GB bị **xóa** (vì Delete on Termination = Yes)
- Chỉ còn volume 2 GB trong danh sách volume của bạn

### Xác Minh

Kiểm tra EC2 console của bạn - instance hiển thị trạng thái **Terminated**.

## Những Điểm Chính Cần Nhớ

1. **EBS volume được ràng buộc với các availability zone cụ thể** - chúng chỉ có thể gắn vào instance trong cùng AZ
2. **Nhiều volume có thể được gắn** vào một EC2 instance duy nhất
3. **Thuộc tính Delete on Termination** kiểm soát việc volume có bị xóa khi instance terminate không
4. **Root volume** thường có Delete on Termination được bật theo mặc định
5. **Volume bổ sung** có Delete on Termination bị tắt theo mặc định
6. **Tính linh hoạt của cloud** cho phép bạn tạo và xóa volume trong vài giây

## Kết Luận

Hướng dẫn thực hành này đã trình bày các thao tác cơ bản để quản lý EBS volume trong AWS, bao gồm tạo, gắn kết và hiểu về vòng đời của volume với EC2 instance.

---

*Bài Giảng Tiếp Theo: Tiếp tục khám phá các dịch vụ lưu trữ AWS và tính năng EC2.*



================================================================================
FILE: 4-aws-iam-introduction.md
================================================================================

# AWS IAM - Giới thiệu về Quản lý Danh tính và Truy cập

## Tổng quan

Chào mừng bạn đến với phần tìm hiểu sâu đầu tiên về dịch vụ AWS - **IAM (Identity and Access Management - Quản lý Danh tính và Truy cập)**.

IAM là một **dịch vụ toàn cầu** cho phép bạn tạo người dùng và tổ chức họ thành các nhóm để quản lý quyền truy cập vào tài khoản AWS của bạn.

## Tài khoản Root

Khi bạn tạo một tài khoản AWS, một **tài khoản root** sẽ tự động được tạo ra. Đây là người dùng root của tài khoản với quyền truy cập đầy đủ vào tất cả các dịch vụ và tài nguyên AWS.

### Nguyên tắc quan trọng cho Tài khoản Root:
- ⚠️ Chỉ sử dụng tài khoản root cho việc thiết lập tài khoản ban đầu
- ⚠️ Không sử dụng cho các hoạt động hàng ngày
- ⚠️ Không bao giờ chia sẻ thông tin đăng nhập tài khoản root

## Người dùng và Nhóm

### Người dùng (Users)
- **Người dùng** đại diện cho từng cá nhân trong tổ chức của bạn
- Mỗi người nên có tài khoản IAM user riêng
- Nên tạo người dùng thay vì chia sẻ tài khoản root

### Nhóm (Groups)
Nhóm giúp tổ chức người dùng có vai trò hoặc trách nhiệm tương tự.

**Ví dụ về Cấu trúc Tổ chức:**

Giả sử bạn có 6 người trong tổ chức: Alice, Bob, Charles, David, Edward và Fred.

- **Nhóm Developers**: Alice, Bob, Charles
- **Nhóm Operations**: David, Edward
- **Nhóm Audit**: Charles, David (người dùng có thể thuộc nhiều nhóm)
- **Không có Nhóm**: Fred (không được khuyến nghị, nhưng có thể)

### Quy tắc quan trọng:
- ✅ Nhóm chỉ có thể chứa người dùng, không chứa nhóm khác
- ✅ Người dùng có thể thuộc nhiều nhóm
- ⚠️ Người dùng không nhất thiết phải thuộc nhóm nào (không phải best practice)

## Chính sách IAM (IAM Policies)

Để cho phép người dùng truy cập các dịch vụ AWS, bạn phải cấp quyền cho họ thông qua **Chính sách IAM**.

### Chính sách IAM là gì?
- Một tài liệu JSON định nghĩa các quyền
- Chỉ định người dùng có thể thực hiện hành động gì trên dịch vụ AWS nào
- Có thể được gắn vào người dùng hoặc nhóm

### Ví dụ về Chính sách:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "elasticloadbalancing:Describe*",
        "cloudwatch:*"
      ],
      "Resource": "*"
    }
  ]
}
```

Chính sách này cho phép người dùng:
- Sử dụng dịch vụ EC2 (các thao tác mô tả)
- Sử dụng dịch vụ Elastic Load Balancing (các thao tác mô tả)
- Sử dụng dịch vụ CloudWatch (tất cả các thao tác)

## Nguyên tắc Đặc quyền Tối thiểu

AWS tuân theo **nguyên tắc đặc quyền tối thiểu** (principle of least privilege):

- 🔒 Không cấp cho người dùng nhiều quyền hơn mức họ cần
- 🔒 Chỉ cấp quyền truy cập vào các dịch vụ cụ thể mà người dùng yêu cầu
- 🔒 Ngăn chặn rủi ro bảo mật và chi phí không mong muốn

### Tại sao điều này quan trọng:
- Ngăn người dùng vô tình khởi chạy các dịch vụ tốn kém
- Giảm lỗ hổng bảo mật
- Duy trì kiểm soát tốt hơn đối với môi trường AWS của bạn

## Tóm tắt

IAM rất cần thiết cho:
- ✅ Tạo tài khoản người dùng cá nhân
- ✅ Tổ chức người dùng thành các nhóm
- ✅ Quản lý quyền thông qua các chính sách
- ✅ Tuân theo các thực tiễn bảo mật tốt nhất
- ✅ Tránh sử dụng tài khoản root cho hoạt động hàng ngày

## Bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ thực hành:
- Tạo người dùng IAM
- Tạo nhóm IAM
- Gán người dùng vào nhóm
- Gắn chính sách để kiểm soát quyền truy cập



================================================================================
FILE: 40-aws-ebs-snapshots-guide.md
================================================================================

# Hướng Dẫn AWS EBS Snapshots

## Giới Thiệu

EBS Snapshots là một tính năng quan trọng để sao lưu và quản lý các EBS volumes của bạn trong AWS. Hướng dẫn này bao gồm các khái niệm và tính năng chính của EBS Snapshots.

## EBS Snapshots là gì?

**EBS Snapshot** là bản sao lưu của EBS volume tại bất kỳ thời điểm nào. Mặc dù không bắt buộc phải tách EBS volume khỏi EC2 instance để tạo snapshot, nhưng điều này được khuyến nghị để đảm bảo tính nhất quán của dữ liệu.

## Lợi Ích Chính

### Chuyển Đổi Giữa Các Region và AZ

EBS Snapshots có thể được sao chép qua:
- Các Availability Zones (AZs) khác nhau
- Các AWS Regions khác nhau

### Ví Dụ Chuyển Đổi

Xem xét kịch bản sau:
- **EC2 Instance A** với EBS volume trong **US-EAST-1A**
- **EC2 Instance B** trong **US-EAST-1B**

Bạn có thể:
1. Tạo snapshot của EBS volume từ US-EAST-1A
2. Khôi phục snapshot đó trong US-EAST-1B

Đây là phương pháp chính để chuyển EBS volume từ AZ này sang AZ khác.

## Các Tính Năng của EBS Snapshot

### 1. EBS Snapshot Archive (Lưu Trữ Snapshot)

**EBS Snapshot Archive** cho phép bạn chuyển snapshots sang "archive tier" để tiết kiệm chi phí.

**Lợi ích:**
- Tiết kiệm đến **75%** chi phí lưu trữ

**Lưu ý:**
- Thời gian khôi phục mất từ **24 đến 72 giờ**
- Không phù hợp cho các yêu cầu truy cập ngay lập tức

### 2. Recycle Bin cho EBS Snapshots (Thùng Rác)

Tính năng **Recycle Bin** bảo vệ chống lại việc xóa snapshots một cách vô tình.

**Cách hoạt động:**
- Các snapshots bị xóa được chuyển vào Recycle Bin thay vì bị xóa vĩnh viễn
- Cho phép khôi phục từ các lần xóa nhầm
- Thời gian lưu trữ có thể cấu hình: **1 ngày đến 1 năm**

### 3. Fast Snapshot Restore (FSR - Khôi Phục Snapshot Nhanh)

**Fast Snapshot Restore** buộc khởi tạo đầy đủ snapshot của bạn để loại bỏ độ trễ khi sử dụng lần đầu.

**Trường hợp sử dụng:**
- Các snapshots lớn cần khởi tạo nhanh
- Khi bạn cần tạo EBS volumes hoặc instances ngay lập tức
- Các workloads quan trọng về thời gian

**Lưu ý quan trọng:**
⚠️ Tính năng này **rất tốn kém** - hãy sử dụng cẩn thận và chỉ khi cần thiết.

## Thực Hành Tốt Nhất

1. **Sao Lưu Định Kỳ**: Tạo snapshots thường xuyên để đảm bảo bảo vệ dữ liệu
2. **Lưu Trữ Snapshots Cũ**: Chuyển các snapshots ít truy cập sang archive tier để tiết kiệm chi phí
3. **Bật Recycle Bin**: Bảo vệ chống lại việc xóa nhầm
4. **Lên Kế Hoạch Sử Dụng FSR**: Chỉ bật Fast Snapshot Restore cho các workloads quan trọng do chi phí cao

## Tóm Tắt

EBS Snapshots cung cấp khả năng sao lưu và chuyển đổi dữ liệu linh hoạt trên hạ tầng AWS. Hiểu rõ các tính năng khác nhau—Archive, Recycle Bin và Fast Snapshot Restore—cho phép bạn tối ưu hóa cả chi phí và hiệu suất dựa trên yêu cầu cụ thể của mình.



================================================================================
FILE: 41-aws-ebs-snapshots-hands-on-tutorial.md
================================================================================

# Hướng Dẫn Thực Hành AWS EBS Snapshots

## Tổng Quan

Hướng dẫn này trình bày cách làm việc với Amazon EBS Snapshots, bao gồm tạo snapshot, sao chép qua các vùng, khôi phục volume, sử dụng Thùng Rác để bảo vệ và quản lý các tầng lưu trữ.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS có quyền truy cập vào EC2
- Một EBS volume hiện có (ví dụ: volume GP2 dung lượng 2 GB)
- Hiểu biết cơ bản về các vùng và availability zones của AWS

## Tạo EBS Snapshot

### Bước 1: Tạo Snapshot

1. Điều hướng đến EBS Volumes trong bảng điều khiển EC2
2. Chọn volume mà bạn muốn tạo snapshot (ví dụ: EBS Volume GP2 dung lượng 2 GB)
3. Nhấp **Actions** → **Create snapshot**
4. Thêm mô tả (ví dụ: "DemoSnapshots")
5. Nhấp **Create snapshots**

### Bước 2: Xem Các Snapshot

1. Trong menu bên trái, nhấp vào **Snapshots**
2. Bạn sẽ thấy danh sách tất cả các snapshot
3. Kiểm tra trạng thái - nó sẽ hiển thị:
   - Trạng thái: **Completed**
   - Khả dụng: **100%**

## Sao Chép Snapshot Qua Các Vùng

### Trường Hợp Sử Dụng: Khôi Phục Thảm Họa

Sao chép snapshot sang vùng khác là cần thiết cho chiến lược khôi phục thảm họa và đảm bảo dữ liệu của bạn được sao lưu ở nhiều vùng AWS.

### Các Bước:

1. Nhấp chuột phải vào snapshot của bạn
2. Chọn **Copy Snapshots**
3. Chọn bất kỳ vùng đích nào từ danh sách thả xuống
4. Nhấp **Copy**

**Lưu ý:** Tính năng này cho phép bạn sao chép dữ liệu qua các vùng AWS để đảm bảo dự phòng.

## Tạo Volume Từ Snapshot

### Khôi Phục Qua Các Availability Zone

Một trong những tính năng mạnh mẽ của EBS Snapshots là khả năng khôi phục volume ở các availability zone khác nhau.

### Các Bước:

1. Chọn snapshot của bạn
2. Nhấp **Actions** → **Create volume from snapshot**
3. Cấu hình volume:
   - Loại volume: GP2
   - Dung lượng: 2 GB
   - Target AZ: Chọn một zone khác (ví dụ: thay đổi từ eu-west-1a sang eu-west-1b)
   - Tùy chọn: Bật mã hóa
   - Tùy chọn: Thêm tags
4. Nhấp **Create volume**

### Kết Quả:

- Quay lại **Volumes**
- Bây giờ bạn sẽ thấy hai volume:
  - Volume gốc ở availability zone đầu tiên
  - Volume được khôi phục ở availability zone mới

**Lợi Ích Chính:** Snapshot cho phép bạn sao chép hiệu quả các EBS volume qua các availability zone khác nhau.

## Sử Dụng Thùng Rác (Recycle Bin)

### Mục Đích

Thùng Rác bảo vệ các EBS Snapshot và Amazon Machine Images (AMI) của bạn khỏi bị xóa vô tình bằng cách giữ lại các tài nguyên đã xóa trong một khoảng thời gian xác định.

### Tạo Quy Tắc Lưu Giữ

1. Điều hướng đến **Recycle Bin** trong bảng điều khiển EC2
2. Nhấp **Create Retention Rule**
3. Cấu hình quy tắc:
   - Tên quy tắc: "DemoRetentionRule"
   - Loại tài nguyên: **EBS Snapshots**
   - Áp dụng cho: **All resources** (Tất cả tài nguyên)
   - Thời gian lưu giữ: **1 ngày**
   - Cài đặt khóa quy tắc: Để **unlocked** (cho phép xóa quy tắc)
4. Nhấp **Create Retention Rule**

### Kiểm Tra Thùng Rác

1. Quay lại **Snapshots** trong bảng điều khiển EC2
2. Chọn một snapshot và xóa nó
3. Snapshot sẽ biến mất khỏi danh sách chính
4. Điều hướng đến **Recycle Bin** → **Resources**
5. Làm mới trang - snapshot đã xóa sẽ xuất hiện ở đây

### Khôi Phục Snapshot

1. Trong Thùng Rác, nhấp vào snapshot đã xóa
2. Nhấp **Recover**
3. Xác nhận bằng cách nhấp **Recover Resources**
4. Snapshot sẽ được khôi phục về bảng điều khiển EC2 Snapshots

**Lưu ý:** Trước khi có tính năng Thùng Rác, các snapshot đã xóa bị loại bỏ vĩnh viễn và không thể khôi phục.

## Các Tầng Lưu Trữ (Storage Tiers)

### Tổng Quan

EBS Snapshots hỗ trợ các tầng lưu trữ khác nhau để tối ưu hóa chi phí:

- **Standard Storage Tier**: Tầng mặc định với quyền truy cập ngay lập tức
- **Archive Tier**: Lưu trữ chi phí thấp hơn cho các snapshot ít được truy cập

### Lưu Trữ Snapshot

1. Chọn một snapshot (hiện đang ở Standard Storage Tier)
2. Nhấp **Actions** → **Archive snapshot**
3. Snapshot chuyển sang mức giá khác

**Quan Trọng:** Khôi phục snapshot đã lưu trữ yêu cầu từ 24 đến 72 giờ.

## Tóm Tắt

Trong hướng dẫn này, bạn đã học cách:

- ✅ Tạo EBS Snapshots từ volume
- ✅ Sao chép snapshot qua các vùng AWS để khôi phục thảm họa
- ✅ Khôi phục volume từ snapshot ở các availability zone khác nhau
- ✅ Thiết lập quy tắc lưu giữ Thùng Rác để bảo vệ chống xóa nhầm
- ✅ Khôi phục snapshot đã xóa từ Thùng Rác
- ✅ Hiểu về các tầng lưu trữ để tối ưu hóa chi phí

## Các Bước Tiếp Theo

- Khám phá việc tạo snapshot tự động bằng AWS Backup
- Triển khai chính sách vòng đời snapshot
- Thực hành các kịch bản khôi phục thảm họa qua vùng
- Tìm hiểu về chia sẻ snapshot qua các tài khoản AWS

---

**Tài Nguyên Bổ Sung:**
- [Tài Liệu AWS EBS Snapshots](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)
- [Tài Liệu AWS Recycle Bin](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recycle-bin.html)



================================================================================
FILE: 42-aws-ami-amazon-machine-image-guide.md
================================================================================

# Hướng Dẫn AWS AMI (Amazon Machine Image)

## Giới Thiệu về AMI

AMI là viết tắt của **Amazon Machine Image** (Ảnh Máy Amazon), và nó đại diện cho việc tùy chỉnh một EC2 instance. AMI là thành phần cơ bản cung cấp sức mạnh cho các EC2 instance trong AWS.

## AMI là gì?

Một AMI bao gồm:
- **Cấu hình phần mềm** - Các gói phần mềm và ứng dụng được tùy chỉnh
- **Thiết lập hệ điều hành** - Cài đặt hệ điều hành được cấu hình sẵn
- **Công cụ giám sát** - Các công cụ giám sát và quản lý được cài đặt sẵn

## Lợi Ích của Việc Sử Dụng AMI

### Thời Gian Khởi Động Nhanh Hơn
Khi bạn tạo AMI của riêng mình, bạn sẽ có thời gian khởi động và cấu hình nhanh hơn vì tất cả phần mềm bạn muốn cài đặt lên EC2 instance đã được đóng gói sẵn thông qua AMI.

### Triển Khai Theo Vùng
- AMI được xây dựng cho một AWS region cụ thể
- Chúng có thể được sao chép qua các region khác để tận dụng hạ tầng toàn cầu của AWS
- Điều này cho phép triển khai nhất quán trên toàn thế giới

## Các Loại AMI

### 1. Public AMI (AMI Công Khai)
- Do AWS cung cấp
- Ví dụ: **Amazon Linux 2 AMI** - một trong những AMI phổ biến nhất
- Được bảo trì và cập nhật bởi AWS

### 2. Custom AMI (AMI Tùy Chỉnh)
- Do bạn tạo và bảo trì
- Được điều chỉnh theo yêu cầu cụ thể của bạn
- Có sẵn các công cụ tự động hóa cho việc tạo và bảo trì AMI

### 3. AWS Marketplace AMI
- Do các nhà cung cấp bên thứ ba tạo ra
- Có thể miễn phí hoặc được bán thương mại
- Thường bao gồm phần mềm chuyên dụng với cấu hình được tối ưu hóa
- Bạn thậm chí có thể tạo một doanh nghiệp bán AMI trên AWS Marketplace

## Quy Trình Tạo AMI

Thực hiện các bước sau để tạo AMI từ một EC2 instance:

### Bước 1: Khởi Động và Tùy Chỉnh
Khởi chạy một EC2 instance và tùy chỉnh nó theo nhu cầu của bạn.

### Bước 2: Dừng Instance
Dừng instance để đảm bảo tính toàn vẹn dữ liệu là chính xác trước khi tạo AMI.

### Bước 3: Xây Dựng AMI
Tạo AMI từ instance đã dừng. Quá trình này sẽ tự động tạo các EBS snapshot ở phía sau.

### Bước 4: Khởi Chạy Instance Mới
Khởi chạy các instance mới từ custom AMI của bạn trong cùng hoặc khác vùng khả dụng (availability zone).

## Ví Dụ Thực Tế: Triển Khai Qua Các Availability Zone

Đây là một kịch bản điển hình để sử dụng AMI:

1. **Khởi chạy** một EC2 instance trong `us-east-1a`
2. **Tùy chỉnh** instance với các ứng dụng và cấu hình của bạn
3. **Tạo** một custom AMI từ instance đã tùy chỉnh
4. **Khởi chạy** các instance mới trong `us-east-1b` sử dụng custom AMI

Điều này tạo ra một bản sao của EC2 instance trong một availability zone khác, đảm bảo tính khả dụng cao và khôi phục thảm họa.

## Những Điểm Chính Cần Nhớ

- AMI cho phép triển khai nhanh chóng các EC2 instance được cấu hình sẵn
- Custom AMI giảm thời gian triển khai và đảm bảo tính nhất quán
- AMI có thể được chia sẻ qua các region và availability zone
- Cả AMI miễn phí và thương mại đều có sẵn thông qua AWS Marketplace

## Các Bước Tiếp Theo

Trong các hướng dẫn tiếp theo, bạn sẽ học cách:
- Tạo custom AMI đầu tiên của bạn
- Sao chép AMI qua các region
- Khởi chạy instance từ custom AMI
- Quản lý và bảo trì thư viện AMI của bạn



================================================================================
FILE: 43-aws-ami-hands-on-tutorial.md
================================================================================

# AWS AMI - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách tạo và sử dụng Amazon Machine Images (AMIs) để lưu và tái sử dụng cấu hình EC2 instance, giảm thời gian khởi động và chuẩn hóa việc triển khai.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS có quyền truy cập EC2
- Security group đã tồn tại (ví dụ: launch-wizard-1)
- Hiểu biết cơ bản về EC2 instances

## Phần 1: Tạo EC2 Instance với User Data

### Bước 1: Khởi Chạy EC2 Instance

1. Truy cập vào EC2 console và khởi chạy instance mới
2. Chọn **Amazon Linux 2** làm AMI
3. Chọn loại instance **t2.micro**
4. Chọn key pair của bạn (hoặc bỏ qua nếu không cần cho demo này)

### Bước 2: Cấu Hình Network Settings

1. Cuộn xuống phần network settings
2. Nhấp **Edit**
3. Chọn security group đã tồn tại (ví dụ: launch-wizard-1)

### Bước 3: Thêm User Data Script

1. Cuộn đến **Advanced Details**
2. Trong phần **User Data**, thêm script sau (không bao gồm dòng cuối):

```bash
#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd
# Lưu ý: Chúng ta KHÔNG tạo file index.html ở đây
```

**Quan trọng:** Sao chép mọi thứ ngoại trừ dòng cuối cùng. Chúng ta đang cài đặt Apache web server (HTTPD) nhưng chưa tạo file index. Điều này cho phép chúng ta tạo một AMI sạch với web server đã được cài đặt sẵn.

### Bước 4: Khởi Chạy và Chờ Đợi

1. Nhấp **Launch Instance**
2. Đợi instance đạt trạng thái "running"
3. **Hãy kiên nhẫn** - ngay cả khi trạng thái hiển thị "running", user data script cần 1-2 phút để hoàn thành

### Bước 5: Xác Minh Cài Đặt

1. Sao chép địa chỉ **Public IPv4**
2. Mở trình duyệt và truy cập `http://[địa-chỉ-ip-công-khai-của-bạn]`
3. Bạn sẽ thấy trang test Apache sau 2 phút
4. Nếu bạn thấy lỗi kết nối, hãy đợi thêm một chút để user data script hoàn tất

## Phần 2: Tạo AMI

### Bước 1: Tạo AMI

1. Nhấp chuột phải vào instance đang chạy
2. Chọn **Image and templates** > **Create image**
3. Đặt tên là `demo-image`
4. Giữ nguyên các thiết lập mặc định
5. Nhấp **Create image**

### Bước 2: Theo Dõi Quá Trình Tạo AMI

1. Điều hướng đến **AMIs** trong menu bên trái
2. Bạn sẽ thấy AMI của mình với trạng thái "pending"
3. Đợi trạng thái chuyển sang "available"

## Phần 3: Khởi Chạy Instance từ AMI Của Bạn

### Bước 1: Khởi Chạy từ AMI

1. Nhấp vào AMI của bạn và chọn **Launch instance from AMI**
2. Hoặc vào **Launch Instance** và chọn tab **My AMIs**
3. Chọn AMI `demo-image` của bạn

### Bước 2: Cấu Hình Instance Mới

1. Chọn key pair của bạn (tùy chọn)
2. Chỉnh sửa network settings và chọn security group đã có
3. Cuộn đến **Advanced Details** > **User Data**

### Bước 3: Thêm User Data Tối Thiểu

Vì HTTPD đã được cài đặt trong AMI, chúng ta chỉ cần tạo file index:

```bash
#!/bin/bash
echo "<h1>Hello World from $(hostname -f)</h1>" > /var/www/html/index.html
```

**Điểm Quan Trọng:** Chúng ta không cần cài đặt lại HTTPD vì nó đã có sẵn trong AMI. Điều này giảm đáng kể thời gian khởi động.

### Bước 4: Khởi Chạy và Xác Minh

1. Khởi chạy instance
2. Đợi nó đạt trạng thái "running"
3. Sao chép địa chỉ IP công khai
4. Truy cập `http://[địa-chỉ-ip-công-khai-của-bạn]`
5. Bạn sẽ thấy "Hello World" nhanh hơn nhiều so với trước

## Lợi Ích Của Việc Sử Dụng AMIs

### Tốc Độ
- **Thời gian khởi động nhanh hơn** - Phần mềm đã cài đặt sẵn không cần cài lại
- Trong demo này, instance thứ hai nhanh hơn nhiều vì HTTPD đã được cài đặt sẵn

### Chuẩn Hóa
- Đóng gói phần mềm bảo mật, dependencies và cấu hình
- Tạo golden image cho việc triển khai nhất quán
- Giảm sự khác biệt cấu hình giữa các instances

### Trường Hợp Sử Dụng
- Cài đặt phần mềm tiên quyết mất 2-3 phút
- Đóng gói thành AMI
- Khởi chạy instances mới từ AMI
- Thêm tùy chỉnh tối thiểu ở cuối
- Đạt được thời gian triển khai nhanh hơn nhiều

## Dọn Dẹp

1. Điều hướng đến EC2 instances của bạn
2. Chọn cả hai instances (instance gốc và instance từ AMI)
3. Nhấp **Instance State** > **Terminate**
4. Xác nhận terminate

## Những Điểm Chính Cần Nhớ

- AMIs lưu trạng thái hoàn chỉnh của một EC2 instance
- User data scripts chạy khi khởi động lần đầu để tùy chỉnh instances
- AMIs giảm đáng kể thời gian khởi động bằng cách cài đặt sẵn phần mềm
- AMIs lý tưởng để tạo các triển khai chuẩn hóa, có thể lặp lại
- Luôn đợi user data scripts hoàn thành trước khi kiểm tra

## Các Bước Tiếp Theo

- Khám phá việc tạo AMIs với các software stacks phức tạp hơn
- Tìm hiểu về chia sẻ AMI và quyền hạn
- Nghiên cứu tự động tạo AMI với AWS Systems Manager
- Thực hành với các bản phân phối Linux và cấu hình khác nhau



================================================================================
FILE: 44-ec2-instance-store-overview.md
================================================================================

# Tổng Quan về EC2 Instance Store

## Giới Thiệu

Mặc dù các EBS volume cung cấp lưu trữ gắn qua mạng cho các EC2 instance với hiệu suất tốt, nhưng có những tình huống yêu cầu hiệu suất cao hơn nữa. Đây là lúc **EC2 Instance Store** xuất hiện - một ổ đĩa cứng được gắn vật lý trực tiếp vào máy chủ lưu trữ EC2 instance của bạn.

## EC2 Instance Store là gì?

EC2 Instance Store là một tùy chọn lưu trữ hiệu suất cao sử dụng các ổ đĩa cứng vật lý được gắn trực tiếp vào máy chủ vật lý lưu trữ EC2 instance của bạn. Không giống như các EBS volume được gắn qua mạng, Instance Store cung cấp kết nối phần cứng trực tiếp để đạt hiệu suất I/O tối đa.

## Đặc Điểm Chính

### Hiệu Suất
- **Hiệu suất I/O tốt hơn** so với các EBS volume
- Khả năng **thông lượng cao**
- Hiệu suất ổ đĩa cực kỳ cao cho các khối lượng công việc đòi hỏi khắt khe

**Ví dụ về Hiệu Suất:**
- Các loại instance như dòng `i3` với Instance Store có thể đạt:
  - Random Read IOPS: lên đến **3.3 triệu**
  - Random Write IOPS: lên đến **1.4 triệu**
- So sánh, các EBS gp2 volume có thể đạt: **32,000 IOPS**

### Lưu Trữ Tạm Thời (Ephemeral Storage)
- **Dữ liệu bị mất** khi EC2 instance bị dừng hoặc kết thúc
- Dữ liệu **không bền vững** - có tính chất tạm thời
- Không thể sử dụng cho lưu trữ lâu dài, bền vững

### Yếu Tố Rủi Ro
- Nếu máy chủ vật lý bị lỗi, bạn có nguy cơ **mất dữ liệu**
- Phần cứng gắn kèm sẽ bị lỗi cùng với máy chủ
- **Trách nhiệm của bạn** để triển khai các chiến lược sao lưu và sao chép

## Trường Hợp Sử Dụng

### Trường Hợp Sử Dụng Tốt ✓
- **Lưu trữ bộ đệm (Buffer)**
- **Dữ liệu cache**
- **Dữ liệu tạm (Scratch data)**
- **Nội dung tạm thời**
- Các khối lượng công việc tính toán hiệu suất cao
- Các ứng dụng yêu cầu IOPS cực kỳ cao

### Trường Hợp Sử Dụng Không Tốt ✗
- Lưu trữ dữ liệu lâu dài
- Dữ liệu quan trọng không có chiến lược sao lưu
- Dữ liệu cần tồn tại qua các lần dừng/khởi động instance

## Thực Hành Tốt Nhất

1. **Chiến Lược Sao Lưu**: Luôn triển khai cơ chế sao lưu mạnh mẽ
2. **Sao Chép Dữ Liệu**: Sao chép dữ liệu quan trọng vào lưu trữ bền vững (như EBS hoặc S3)
3. **Sử Dụng cho Dữ Liệu Tạm**: Chỉ lưu trữ dữ liệu có thể tái tạo hoặc là tạm thời
4. **Giám Sát Sức Khỏe**: Theo dõi tình trạng instance và phần cứng

## So Sánh với EBS

| Tính Năng | EC2 Instance Store | EBS Volume |
|-----------|-------------------|------------|
| **Hiệu Suất** | Cực kỳ cao (hàng triệu IOPS) | Cao (lên đến 32k IOPS cho gp2) |
| **Độ Bền** | Tạm thời - mất khi dừng/kết thúc | Bền vững - tồn tại qua vòng đời instance |
| **Trường Hợp Sử Dụng** | Khối lượng công việc tạm thời, hiệu suất cao | Lưu trữ lâu dài |
| **Kết Nối** | Gắn phần cứng vật lý | Gắn qua mạng |
| **Sao Lưu** | Thủ công, trách nhiệm của bạn | Có snapshot |

## Mẹo Cho Kỳ Thi

- Khi bạn thấy yêu cầu về **các volume gắn phần cứng hiệu suất rất cao**, hãy nghĩ đến **EC2 Instance Store**
- Nhớ **tính chất tạm thời** - dữ liệu bị mất khi dừng/kết thúc
- Hiểu **sự đánh đổi**: hiệu suất so với độ bền vững

## Kết Luận

EC2 Instance Store là một tùy chọn mạnh mẽ cho các khối lượng công việc yêu cầu hiệu suất I/O cực cao. Tuy nhiên, tính chất tạm thời của nó có nghĩa là nó chỉ nên được sử dụng cho dữ liệu tạm thời hoặc kết hợp với chiến lược sao lưu và sao chép vững chắc. Đối với nhu cầu lưu trữ lâu dài, các EBS volume vẫn là lựa chọn tốt hơn.



================================================================================
FILE: 45-aws-ebs-volume-types-overview.md
================================================================================

# Tổng Quan Các Loại Ổ Đĩa EBS Trên AWS

## Giới Thiệu

Các ổ đĩa Amazon EBS (Elastic Block Store) có sáu loại khác nhau, có thể được nhóm thành nhiều danh mục dựa trên đặc điểm hiệu suất và trường hợp sử dụng.

## Các Danh Mục Ổ Đĩa EBS

### SSD Đa Năng (gp2/gp3)
Ổ đĩa SSD đa năng cân bằng giữa giá cả và hiệu suất cho nhiều loại khối lượng công việc khác nhau.

#### GP3 (Thế Hệ Mới Hơn)
- **Hiệu Suất Cơ Bản**: 3,000 IOPS và thông lượng 125 MB/s
- **Hiệu Suất Tối Đa**: Lên đến 16,000 IOPS và thông lượng 1,000 MB/s
- **Tính Năng Chính**: IOPS và thông lượng có thể tăng **độc lập** với nhau
- **Phạm Vi Kích Thước**: 1 GB đến 16 TB

#### GP2 (Thế Hệ Cũ Hơn)
- **Hiệu Suất**: Các ổ đĩa gp2 nhỏ có thể tăng đột biến lên đến 3,000 IOPS
- **Tính Năng Chính**: Kích thước ổ đĩa và IOPS **liên kết với nhau**
- **Tính Toán IOPS**: 3 IOPS mỗi GB
- **IOPS Tối Đa**: 16,000 IOPS (đạt được ở mức 5,334 GB)
- **Phạm Vi Kích Thước**: 1 GB đến 16 TB

**Trường Hợp Sử Dụng**:
- Ổ đĩa khởi động hệ thống
- Máy tính để bàn ảo
- Môi trường phát triển và thử nghiệm
- Lưu trữ tiết kiệm chi phí với độ trễ thấp

### SSD IOPS Được Cung Cấp (io1/io2)
Ổ đĩa SSD hiệu suất cao nhất được thiết kế cho các khối lượng công việc quan trọng, độ trễ thấp và thông lượng cao.

#### IO1
- **Phạm Vi Kích Thước**: 4 GB đến 16 TB
- **IOPS Tối Đa**: 
  - 64,000 IOPS cho các instance EC2 Nitro
  - 32,000 IOPS cho các instance khác
- **Tính Năng Chính**: IOPS được cung cấp có thể tăng độc lập với kích thước lưu trữ

#### IO2 Block Express
- **Phạm Vi Kích Thước**: Lên đến 64 TB
- **Độ Trễ**: Độ trễ dưới mili giây
- **IOPS Tối Đa**: 256,000 IOPS
- **Tỷ Lệ IOPS/GB**: 1,000:1
- **Tính Năng Đặc Biệt**: Hỗ trợ EBS multi-attach

**Trường Hợp Sử Dụng**:
- Ứng dụng kinh doanh quan trọng yêu cầu hiệu suất IOPS bền vững
- Ứng dụng cần hơn 16,000 IOPS
- Khối lượng công việc cơ sở dữ liệu nhạy cảm với hiệu suất và tính nhất quán của lưu trữ

### HDD Tối Ưu Hóa Thông Lượng (st1)
Ổ đĩa HDD chi phí thấp được thiết kế cho các khối lượng công việc tập trung vào thông lượng, được truy cập thường xuyên.

- **Phạm Vi Kích Thước**: Lên đến 16 TB
- **Thông Lượng Tối Đa**: 500 MB/s
- **IOPS Tối Đa**: 500
- **Không thể sử dụng làm ổ đĩa khởi động**

**Trường Hợp Sử Dụng**:
- Dữ liệu lớn (Big data)
- Kho dữ liệu
- Xử lý nhật ký

### HDD Lạnh (sc1)
Ổ đĩa HDD chi phí thấp nhất được thiết kế cho các khối lượng công việc ít được truy cập.

- **Phạm Vi Kích Thước**: Lên đến 16 TB
- **Thông Lượng Tối Đa**: 250 MB/s
- **IOPS Tối Đa**: 250
- **Không thể sử dụng làm ổ đĩa khởi động**

**Trường Hợp Sử Dụng**:
- Dữ liệu lưu trữ
- Dữ liệu ít được truy cập
- Các tình huống yêu cầu chi phí thấp nhất có thể

## Các Yếu Tố Chính Để Xác Định Ổ Đĩa EBS

1. **Kích Thước**: Dung lượng lưu trữ (GB đến TB)
2. **Thông Lượng**: Tốc độ truyền dữ liệu (MB/s)
3. **IOPS**: Số Thao Tác Đầu Vào/Đầu Ra Mỗi Giây

## Yêu Cầu Ổ Đĩa Khởi Động

Chỉ các loại ổ đĩa sau có thể được sử dụng làm ổ đĩa khởi động (nơi hệ điều hành gốc chạy):
- GP2
- GP3
- IO1
- IO2

## Lưu Ý Quan Trọng Cho Kỳ Thi

- **SSD Đa Năng (gp2/gp3)**: Lưu trữ tiết kiệm chi phí với độ trễ thấp
  - GP3 cho phép cài đặt IOPS và thông lượng độc lập
  - GP2 liên kết IOPS với kích thước ổ đĩa

- **SSD IOPS Được Cung Cấp (io1/io2)**: Cho các ứng dụng kinh doanh quan trọng
  - Sử dụng khi bạn cần hơn 16,000 IOPS
  - Lý tưởng cho khối lượng công việc cơ sở dữ liệu yêu cầu hiệu suất nhất quán

- **Ổ Đĩa HDD (st1/sc1)**: Cho các tình huống thông lượng cao hoặc chi phí thấp nhất
  - Không thể sử dụng làm ổ đĩa khởi động

- **Yêu Cầu IOPS Cao**: Để có được hơn 32,000 IOPS, bạn cần các instance EC2 Nitro với io1 hoặc io2

## Tổng Kết

Hiểu sự khác biệt giữa các loại ổ đĩa EBS là rất quan trọng:
- **SSD Đa Năng** vs **SSD IOPS Được Cung Cấp** (cho cơ sở dữ liệu)
- **HDD Tối Ưu Hóa Thông Lượng** vs **HDD Lạnh** (cho thông lượng cao vs chi phí thấp nhất)

Luôn tham khảo tài liệu AWS khi có nghi ngờ về các yêu cầu và cấu hình cụ thể.



================================================================================
FILE: 46-aws-ebs-multi-attach-feature.md
================================================================================

# Tính năng Multi-Attach của AWS EBS

## Tổng quan

Tính năng Multi-Attach của Amazon EBS volumes cho phép bạn gắn kết cùng một EBS volume với nhiều EC2 instances trong cùng một Availability Zone. Khả năng này mang lại sự linh hoạt cao hơn cho các ứng dụng cluster yêu cầu truy cập lưu trữ chia sẻ.

## Cách thức hoạt động

Tính năng Multi-Attach cho phép:
- Một EBS volume duy nhất có thể được gắn kết đồng thời với nhiều EC2 instances
- Tất cả các instances được gắn kết chia sẻ cùng một volume hiệu suất cao
- Chỉ khả dụng cho họ EBS volume **io1** và **io2**

### Kiến trúc

```
┌─────────────┐
│  EC2 Instance 1  │───┐
└─────────────┘   │
                  │    ┌──────────────┐
┌─────────────┐   ├────│  io2 Volume  │
│  EC2 Instance 2  │───┤    (Multi-   │
└─────────────┘   │    │   Attach)    │
                  │    └──────────────┘
┌─────────────┐   │
│  EC2 Instance 3  │───┘
└─────────────┘
```

## Các tính năng chính

### Quyền Đọc và Ghi
- Mỗi instance được gắn kết có **quyền đọc và ghi đầy đủ** đối với volume
- Tất cả các instances có thể đọc và ghi đồng thời vào volume hiệu suất cao

### Các trường hợp sử dụng

1. **Tính khả dụng ứng dụng cao hơn**
   - Lý tưởng cho các ứng dụng Linux cluster
   - Ví dụ: Teradata clusters

2. **Thao tác ghi đồng thời**
   - Các ứng dụng phải quản lý các thao tác ghi đồng thời
   - Lưu trữ chia sẻ cho khối lượng công việc đa instance

## Giới hạn và Yêu cầu

### Giới hạn Availability Zone
- Multi-Attach chỉ khả dụng **trong cùng một Availability Zone**
- Không thể gắn kết EBS volume từ một AZ này sang các instances ở AZ khác

### Giới hạn số lượng Instance
- **Tối đa 16 EC2 instances** có thể gắn kết đồng thời với cùng một volume
- Đây là giới hạn quan trọng cần nhớ cho các kỳ thi chứng chỉ AWS

### Yêu cầu về File System
- Phải sử dụng **file system có khả năng nhận biết cluster**
- Khác với các file system tiêu chuẩn như XFS hoặc EXT4
- File system phải có khả năng quản lý truy cập đồng thời từ nhiều instances

## Hỗ trợ loại Volume

| Loại Volume | Hỗ trợ Multi-Attach |
|-------------|---------------------|
| io1         | ✅ Có               |
| io2         | ✅ Có               |
| gp2         | ❌ Không            |
| gp3         | ❌ Không            |
| st1         | ❌ Không            |
| sc1         | ❌ Không            |

## Điểm quan trọng cho kỳ thi

- Multi-Attach chỉ khả dụng cho loại volume **io1** và **io2**
- Tối đa **16 instances** cho mỗi volume
- Phải nằm trong **cùng một Availability Zone**
- Yêu cầu **file system có khả năng nhận biết cluster**

## Tóm tắt

Tính năng EBS Multi-Attach là một khả năng mạnh mẽ cho các trường hợp sử dụng cụ thể yêu cầu lưu trữ chia sẻ giữa nhiều EC2 instances. Mặc dù có một số giới hạn nhất định, nó cung cấp chức năng thiết yếu cho các ứng dụng cluster và kiến trúc có tính khả dụng cao trong AWS.



================================================================================
FILE: 47-amazon-efs-elastic-file-system.md
================================================================================

# Amazon EFS - Hệ Thống Tệp Đàn Hồi

## Tổng Quan

Amazon EFS (Elastic File System) là một hệ thống NFS (Network File System) được quản lý, cung cấp lưu trữ tệp có khả năng mở rộng và tính sẵn sàng cao cho các EC2 instance trên nhiều vùng sẵn sàng.

### Đặc Điểm Chính

- **Tính Sẵn Sàng Cao**: Có thể truy cập qua nhiều vùng sẵn sàng
- **Khả Năng Mở Rộng**: Tự động mở rộng mà không cần lập kế hoạch dung lượng
- **Chi Phí Cao**: Khoảng gấp 3 lần chi phí của EBS volume GP2
- **Trả Theo Sử Dụng**: Không cần cấp phát dung lượng trước

## Kiến Trúc

Hệ thống tệp EFS được bảo vệ bởi security groups và có thể được mount đồng thời bởi nhiều EC2 instance trên các vùng sẵn sàng khác nhau:

- EC2 instances trong US-EAST-1A
- EC2 instances trong US-EAST-1B
- EC2 instances trong US-EAST-1C

Tất cả các instance có thể kết nối đồng thời với cùng một hệ thống tệp mạng thông qua EFS.

## Trường Hợp Sử Dụng

- Quản lý nội dung
- Web serving
- Chia sẻ dữ liệu
- Hosting WordPress

## Yêu Cầu Kỹ Thuật

### Giao Thức và Tương Thích

- **Giao Thức**: NFS (Network File System)
- **Kiểm Soát Truy Cập**: Security groups
- **Tương Thích HĐH**: Chỉ hỗ trợ Linux-based AMI (không tương thích với Windows)
- **Mã Hóa**: Hỗ trợ mã hóa dữ liệu nghỉ bằng KMS
- **Hệ Thống Tệp**: Tuân thủ POSIX với API tệp chuẩn

### Tự Động Mở Rộng

- Không cần lập kế hoạch dung lượng
- Hệ thống tệp tự động mở rộng
- Thanh toán theo mức sử dụng mỗi gigabyte

## Hiệu Năng và Quy Mô

### Khả Năng Mở Rộng

- **Client Đồng Thời**: Hàng nghìn NFS client
- **Throughput**: 10+ GB/s
- **Kích Thước Tối Đa**: Quy mô petabyte (tăng trưởng tự động)

### Chế Độ Hiệu Năng

Được thiết lập khi tạo EFS:

#### 1. General Purpose (Mặc Định)
- Tối ưu cho các trường hợp nhạy cảm về độ trễ
- Lý tưởng cho: Web server, ứng dụng CMS

#### 2. Max I/O
- Độ trễ cao nhưng throughput cao hơn
- Xử lý song song cao
- Lý tưởng cho: Ứng dụng big data, xử lý media

### Chế Độ Throughput

#### 1. Bursting (Bùng Nổ)
- Baseline: 50 MB/s cho mỗi TB lưu trữ
- Burst: Lên đến 100 MB/s
- Throughput tăng theo dung lượng lưu trữ

#### 2. Provisioned (Cấp Phát)
- Thiết lập throughput độc lập với dung lượng lưu trữ
- Ví dụ: 1 GB/s cho 1 TB lưu trữ
- Tách biệt throughput khỏi dung lượng lưu trữ

#### 3. Elastic (Khuyến nghị cho workload không dự đoán được)
- Tự động điều chỉnh throughput dựa trên workload
- Lên đến 3 GB/s cho đọc
- Lên đến 1 GB/s cho ghi
- Hoàn hảo cho workload không dự đoán được

## Lớp Lưu Trữ

### Các Tầng Lưu Trữ

EFS cung cấp quản lý vòng đời để tự động di chuyển tệp giữa các tầng lưu trữ:

#### 1. Standard Tier (Tầng Chuẩn)
- Dành cho các tệp được truy cập thường xuyên
- Chi phí cao hơn nhưng truy cập ngay lập tức

#### 2. EFS-IA (Infrequent Access - Truy Cập Không Thường Xuyên)
- Chi phí lưu trữ thấp hơn
- Chi phí theo lượt truy xuất
- Dành cho tệp được truy cập ít thường xuyên

#### 3. Archive Storage Tier (Tầng Lưu Trữ)
- Dành cho dữ liệu hiếm khi truy cập (vài lần mỗi năm)
- Chi phí lưu trữ thấp nhất
- Lý tưởng cho lưu trữ dài hạn

### Chính Sách Vòng Đời

Tự động di chuyển tệp giữa các tầng lưu trữ dựa trên mẫu truy cập:

**Ví dụ**: Các tệp trong EFS Standard không được truy cập trong 60 ngày có thể tự động chuyển sang tầng EFS-IA.

## Tính Sẵn Sàng và Độ Bền

### Standard (Multi-AZ - Đa Vùng)
- EFS trên nhiều vùng sẵn sàng
- Khuyến nghị cho workload production
- Kiến trúc chống thảm họa

### One Zone (Một Vùng)
- Chỉ một vùng sẵn sàng
- Tùy chọn chi phí thấp hơn
- Phù hợp cho môi trường phát triển
- Vẫn bao gồm chức năng backup
- Tương thích với tầng lưu trữ IA (EFS One Zone-IA)

## Tiết Kiệm Chi Phí

Bằng cách triển khai đúng sự kết hợp giữa các lớp lưu trữ và chính sách vòng đời, bạn có thể đạt được:

**Tiết kiệm lên đến 90% chi phí**

## Tóm Tắt

Amazon EFS cung cấp một hệ thống tệp mạng được quản lý, có khả năng mở rộng cao và có thể được chia sẻ trên nhiều EC2 instance trong các vùng sẵn sàng khác nhau. Mặc dù đắt hơn EBS, khả năng tự động mở rộng, mô hình trả theo sử dụng và các tùy chọn hiệu năng linh hoạt khiến nó trở nên lý tưởng cho các ứng dụng yêu cầu lưu trữ tệp được chia sẻ với tính sẵn sàng cao và độ bền tốt.



================================================================================
FILE: 48-aws-efs-hands-on-tutorial.md
================================================================================

# Hướng Dẫn Thực Hành AWS EFS (Elastic File System)

## Tổng Quan

Hướng dẫn này trình bày cách tạo và cấu hình Amazon Elastic File System (EFS) và gắn kết nó vào các EC2 instance trên nhiều vùng khả dụng (availability zones).

## Tạo EFS File System

### Bước 1: Cấu Hình Ban Đầu

1. Truy cập dịch vụ Amazon Elastic File System
2. Nhấp vào **Create File System** (Tạo hệ thống tệp)
3. Tùy chọn đặt tên (có thể để trống)
4. Chọn VPC nơi bạn muốn kết nối file system (sử dụng VPC mặc định)
5. Nhấp vào **Customize** (Tùy chỉnh) để xem các tùy chọn nâng cao

### Bước 2: Cài Đặt File System

#### Loại File System

- **Regional** (Khu vực): Cung cấp file system trên nhiều vùng khả dụng
  - Tính khả dụng và độ bền cao
  - Được khuyến nghị cho môi trường production
  
- **One Zone** (Một vùng): Triển khai trên một vùng khả dụng duy nhất
  - Tùy chọn tiết kiệm chi phí
  - Chỉ phù hợp cho môi trường phát triển
  - Dữ liệu sẽ không thể truy cập nếu AZ gặp sự cố

**Khuyến nghị**: Sử dụng **Regional** cho môi trường production.

#### Sao Lưu Tự Động

- Giữ tính năng sao lưu tự động **được bật** (khuyến nghị)

#### Quản Lý Vòng Đời (Lifecycle Management)

Cấu hình chuyển đổi dữ liệu tự động để tiết kiệm chi phí:

- **Chuyển sang Infrequent Access (IA)**: Di chuyển các tệp không được truy cập trong 30 ngày
- **Chuyển sang Archive**: Di chuyển các tệp không được truy cập trong 90 ngày
- **Chuyển lại Standard**: Khi được truy cập lần đầu sau khi lưu trữ

Quản lý vòng đời này giúp giảm chi phí lưu trữ cho các tệp hiếm khi được truy cập.

#### Mã Hóa

- Giữ tính năng mã hóa **được bật**

### Bước 3: Cài Đặt Hiệu Suất

#### Chế Độ Throughput

1. **Elastic** (Linh hoạt - Khuyến nghị)
   - Tự động mở rộng dựa trên nhu cầu workload
   - Tốt nhất cho workload I/O không thể dự đoán
   - Chỉ trả tiền cho những gì bạn sử dụng
   - Có thể mở rộng từ 0 MB/s lên 100+ MB/s ngay lập tức
   - Không cần lập kế hoạch trước

2. **Bursting** (Đột phá)
   - Throughput tăng theo kích thước lưu trữ
   - Phù hợp khi nhu cầu throughput tỷ lệ với kích thước dữ liệu

3. **Provisioned** (Được cấp phát)
   - Chỉ định yêu cầu throughput trước
   - Trả tiền cho dung lượng được cấp phát trước
   - Sử dụng khi bạn biết chính xác nhu cầu throughput

#### Chế Độ Hiệu Suất

- **General Purpose** (Mục đích chung): Độ trễ thấp, hiệu suất cao (khuyến nghị)
- **Max I/O**: Độ trễ cao hơn nhưng hỗ trợ workload song song cao (cho các tình huống big data)

**Cấu Hình Khuyến Nghị**: Chế độ Enhanced với Elastic throughput và General Purpose performance.

## Cấu Hình Mạng

### Bước 1: Tạo Security Group

1. Vào EC2 Console → Security Groups
2. Nhấp **Create Security Group** (Tạo nhóm bảo mật)
3. Tên: `sg-efs-demo` hoặc `EFS Demo SG`
4. Tạo security group (ban đầu không có inbound rules)

### Bước 2: Cài Đặt Network Access

1. Chọn VPC của bạn (VPC mặc định)
2. Cấu hình mount targets:
   - Đối với Regional EFS, mount targets được tạo trong nhiều AZ
   - Mỗi AZ được gán cho một subnet (sử dụng subnet mặc định)
   - Địa chỉ IP được gán tự động
3. Gán security group đã tạo trước đó cho tất cả mount targets
4. Nhấp **Next** (Tiếp theo)

### Bước 3: File System Policy

- Để cài đặt file system policy ở mặc định (tính năng nâng cao tùy chọn)
- Nhấp **Next**

### Bước 4: Xem Xét và Tạo

- Xem xét tất cả các cài đặt
- Nhấp **Create** (Tạo)
- Đợi file system sẵn sàng

## Gắn Kết EFS vào EC2 Instances

### Khởi Chạy EC2 Instance A (trong AZ-A)

1. **Launch Instance** với tên: `Instance A`
2. **AMI**: Amazon Linux 2
3. **Instance Type**: t2.micro (free tier)
4. **Key Pair**: Tắt (sử dụng EC2 Instance Connect)
5. **Network Settings** (Cài đặt mạng):
   - Chọn subnet trong `eu-west-1a` (hoặc AZ-A ưa thích của bạn)
   - Cho phép truy cập SSH từ mọi nơi
6. **Storage** (Lưu trữ): 8 GB GP2
7. **File Systems** (Hệ thống tệp):
   - Chỉnh sửa và thêm EFS file system
   - Chọn EFS đã tạo của bạn
   - Mount point: `/mnt/efs/fs1`
   - Bật tự động mount với user data scripts
   - Security groups sẽ được tự động tạo và gắn kết
8. **Launch Instance** (Khởi chạy instance)

### Khởi Chạy EC2 Instance B (trong AZ-B)

1. **Launch Instance** với tên: `Instance B`
2. **AMI**: Amazon Linux 2
3. **Instance Type**: t2.micro
4. **Key Pair**: Tắt (sử dụng EC2 Instance Connect)
5. **Network Settings**:
   - Chọn subnet trong `eu-west-1b` (hoặc AZ-B ưa thích của bạn)
   - Chọn security group từ Instance A (ví dụ: `launch-wizard-2`)
6. **File Systems**:
   - Thêm cùng EFS file system
   - Cùng mount point: `/mnt/efs/fs1`
   - Bật tự động mount
7. **Launch Instance**

## Cấu Hình Security Group

Khi bạn thêm EFS vào EC2 instances thông qua console:

- AWS tự động tạo security groups (ví dụ: `efs-sg-1`, `efs-sg-2`)
- Các security groups này được gắn vào EFS mount targets của bạn
- Inbound rules cho phép giao thức NFS trên cổng 2049
- Source được đặt thành security group của EC2 instance
- Điều này cho phép EC2 instances truy cập EFS file system

## Kiểm Tra Chia Sẻ Tệp EFS

### Trên Instance A:

```bash
# Kết nối qua EC2 Instance Connect

# Liệt kê mount point EFS
ls /mnt/efs/fs1/

# Nâng quyền
sudo su

# Tạo tệp kiểm tra
echo "hello world" > /mnt/efs/fs1/hello.txt

# Xác minh tệp đã tạo
cat /mnt/efs/fs1/hello.txt
```

### Trên Instance B:

```bash
# Kết nối qua EC2 Instance Connect

# Liệt kê mount point EFS
ls /mnt/efs/fs1/

# Đọc tệp được tạo từ Instance A
cat /mnt/efs/fs1/hello.txt
```

**Kết Quả**: Tệp `hello.txt` được tạo trên Instance A có thể nhìn thấy và truy cập được trên Instance B, chứng minh rằng EFS đã được gắn kết thành công như một ổ đĩa mạng chia sẻ trên cả hai instances ở các vùng khả dụng khác nhau.

## Dọn Dẹp

### Xóa EC2 Instances

1. Vào EC2 Console → Instances
2. Chọn cả hai instances
3. Nhấp **Terminate** (Chấm dứt)

### Xóa EFS File System

1. Vào EFS Console
2. Chọn file system của bạn
3. Nhấp **Delete** (Xóa)
4. Nhập file system ID để xác nhận
5. Nhấp **Delete**

### Xóa Security Groups

1. Vào EC2 Console → Security Groups
2. Xóa các security groups bổ sung được tạo trong demo:
   - `efs-sg-1`
   - `efs-sg-2`
   - `sg-efs-demo`

## Những Điểm Chính

- **EFS cung cấp lưu trữ mạng chia sẻ** có thể được gắn kết đồng thời trên nhiều EC2 instances
- **Khả dụng cross-AZ** đảm bảo tính khả dụng cao và độ bền
- **Trả tiền theo sử dụng** - chi phí dựa trên dung lượng lưu trữ thực tế
- **Quản lý vòng đời** giúp tối ưu hóa chi phí bằng cách di chuyển dữ liệu ít được truy cập sang các tầng lưu trữ rẻ hơn
- **Chế độ Elastic throughput** được khuyến nghị cho hầu hết các workload
- **Tự động mount** thông qua EC2 console đơn giản hóa thiết lập với user data scripts
- **Security groups** được tự động cấu hình để cho phép truy cập NFS

## Thực Hành Tốt Nhất

- Sử dụng **Regional** EFS cho workload production
- Bật **sao lưu tự động**
- Sử dụng **chế độ Elastic throughput** cho workload không thể dự đoán
- Cấu hình **quản lý vòng đời** để tối ưu hóa chi phí
- Giữ **mã hóa được bật**
- Sử dụng cấu hình **security group** phù hợp để kiểm soát truy cập



================================================================================
FILE: 49-ebs-vs-efs-vs-instance-store-comparison.md
================================================================================

# So Sánh EBS vs EFS vs Instance Store: Các Tùy Chọn Lưu Trữ AWS

## Tổng Quan

Tài liệu này giải thích các điểm khác biệt chính giữa các tùy chọn lưu trữ AWS: EBS volumes, EFS file systems và EC2 Instance Store.

## EBS (Elastic Block Store) Volumes

### Đặc Điểm Chính

- **Gắn Kết**: EBS volumes được gắn vào **một instance tại một thời điểm**
  - Ngoại lệ: Tính năng multi-attach cho các loại volume io1 và io2 (chỉ dành cho các trường hợp sử dụng cụ thể)

- **Khóa Theo Availability Zone**: EBS volumes bị khóa ở cấp độ AZ (Availability Zone)
  - Ví dụ: Một EBS volume ở AZ 1 không thể gắn trực tiếp vào EC2 instance ở AZ 2

### Các Loại Volume và Hiệu Suất

#### gp2 (General Purpose SSD)
- IO tăng tỷ lệ thuận với dung lượng ổ đĩa

#### gp3 và io1 (Provisioned IOPS SSD)
- IO có thể tăng độc lập với dung lượng ổ đĩa
- Cấu hình hiệu suất linh hoạt hơn

### Di Chuyển Giữa Các Availability Zones

Để di chuyển EBS volume giữa các AZ:
1. Tạo **snapshot** của EBS volume
2. Lưu trữ snapshot vào EBS Snapshots
3. Khôi phục snapshot tại AZ đích

### Lưu Ý Về Sao Lưu

- Sao lưu EBS volume sử dụng tài nguyên IO
- **Thực Hành Tốt**: Tránh chạy sao lưu trong thời gian lưu lượng truy cập cao để tránh ảnh hưởng đến hiệu suất

### Hành Vi Khi Xóa Instance

- Root EBS volumes **bị xóa theo mặc định** khi EC2 instance bị xóa
- Hành vi này có thể được tắt nếu cần

## EFS (Elastic File System)

### Đặc Điểm Chính

- **Network File System**: Được thiết kế cho truy cập chia sẻ trên nhiều instances
- **Hỗ Trợ Multi-AZ**: Có thể gắn vào hàng trăm instances trên các availability zones khác nhau đồng thời

### Kiến Trúc

- Một EFS file system có thể có nhiều mount targets ở các AZ khác nhau
- Nhiều instances có thể chia sẻ cùng một file system
- Cho phép các workloads cộng tác và truy cập dữ liệu chia sẻ

### Các Trường Hợp Sử Dụng

- **Triển khai WordPress**: Nhiều web servers chia sẻ cùng nội dung
- Các ứng dụng yêu cầu truy cập file chia sẻ giữa các instances

### Yêu Cầu Nền Tảng

- **Chỉ dành cho Linux instances** (sử dụng hệ thống file POSIX)

### Cân Nhắc Về Chi Phí

- Giá cao hơn so với EBS
- **Tối Ưu Chi Phí**: Tận dụng các storage tiers của EFS để tiết kiệm chi phí

## EC2 Instance Store

### Đặc Điểm Chính

- **Gắn vật lý** vào EC2 instance
- Cung cấp lưu trữ local với hiệu suất cao

### Hạn Chế Quan Trọng

- **Lưu trữ tạm thời (Ephemeral)**: Nếu bạn mất EC2 instance, bạn cũng mất dữ liệu lưu trữ
- Dữ liệu không tồn tại khi instance dừng hoặc bị xóa

## Bảng So Sánh Tổng Hợp

| Tính Năng | EBS | EFS | Instance Store |
|-----------|-----|-----|----------------|
| Gắn Kết | Một instance (trừ io1/io2 multi-attach) | Hàng trăm instances | Gắn vật lý vào một instance |
| Khả Dụng | Khóa theo AZ | Multi-AZ | Theo instance |
| Tính Bền Vững | Bền vững (tồn tại sau khi xóa instance nếu được cấu hình) | Bền vững | Tạm thời |
| Trường Hợp Sử Dụng | Block storage cho một instance | Hệ thống file chia sẻ | Lưu trữ tạm thời hiệu suất cao |
| Nền Tảng | Tất cả hệ điều hành | Chỉ Linux (POSIX) | Tất cả hệ điều hành |
| Giá | Trung bình | Cao hơn (có tùy chọn tier) | Bao gồm trong instance |

## Thực Hành Tốt Nhất

1. **EBS**: Sử dụng cho nhu cầu lưu trữ block bền vững, cấu hình bảo vệ xóa cho dữ liệu quan trọng
2. **EFS**: Sử dụng khi nhiều instances cần chia sẻ files, tận dụng storage tiers để tối ưu chi phí
3. **Instance Store**: Chỉ sử dụng cho dữ liệu tạm thời, cache hoặc buffers có thể mất

---

*Hiểu rõ những điểm khác biệt này là rất quan trọng để thiết kế kiến trúc AWS có khả năng phục hồi và hiệu quả về chi phí.*



================================================================================
FILE: 5-creating-iam-users-in-aws.md
================================================================================

# Tạo IAM Users trong AWS

## Giới thiệu

Trong hướng dẫn này, chúng ta sẽ thực hành sử dụng dịch vụ IAM (Identity and Access Management) để tạo người dùng trong AWS. Đây là kỹ năng cơ bản để quản lý tài khoản AWS một cách an toàn.

## Truy cập IAM Console

Để bắt đầu:
1. Gõ "IAM" vào thanh tìm kiếm của AWS
2. Điều hướng đến IAM console

Khi đến IAM Dashboard, bạn sẽ thấy một số khuyến nghị về bảo mật mà chúng ta có thể bỏ qua tạm thời.

## Hiểu về IAM như một Global Service

Một điều quan trọng cần chú ý: nếu bạn nhìn vào góc trên bên phải và nhấp vào "Global", bạn sẽ thấy rằng tùy chọn chọn region không hoạt động. Điều này có nghĩa là **IAM là một dịch vụ toàn cầu (global service)** - không có region nào được chọn.

Khi bạn tạo một user trong IAM, nó sẽ có sẵn ở mọi nơi. Tuy nhiên, một số console AWS khác được đề cập trong khóa học này sẽ dành riêng cho từng region cụ thể.

## Tại sao phải tạo IAM Users?

Hiện tại, khi bạn lần đầu đăng nhập vào AWS, bạn đang sử dụng cái gọi là **root user**. Bạn có thể xác định điều này bằng cách nhấp vào góc trên bên phải - bạn sẽ chỉ thấy account ID.

**Quan trọng:** Việc sử dụng root account cho các hoạt động hàng ngày không phải là best practice. Do đó, chúng ta muốn tạo các user như admin users để có thể sử dụng tài khoản của mình một cách an toàn hơn.

## Tạo IAM User đầu tiên

### Bước 1: Bắt đầu tạo User

1. Điều hướng đến "Users" ở thanh bên trái
2. Nhấp "Create user"
3. Cung cấp username (ví dụ: "Stephane")

### Bước 2: Cấu hình truy cập Console

Khi thiết lập quyền truy cập console, bạn có hai tùy chọn:
- **Identity Center** (được AWS khuyến nghị)
- **Create an IAM user** (đơn giản hơn và là điều bạn cần biết cho kỳ thi)

Trong hướng dẫn này, chúng ta sẽ chọn tùy chọn thứ hai: tạo IAM user.

### Bước 3: Cấu hình Password

Bạn có hai tùy chọn về mật khẩu:

**Đối với người dùng khác:**
- Để là auto-generated password
- Yêu cầu thay đổi mật khẩu khi đăng nhập lần đầu

**Đối với chính bạn:**
- Nhập custom password
- Có thể bỏ chọn "User must create a new password at next sign-in"

### Bước 4: Thêm Permissions

Thay vì thêm permissions trực tiếp, hãy sử dụng groups (best practice):

1. Nhấp "Create a group"
2. Đặt tên group là "admin"
3. Gắn policy "AdministratorAccess"
4. Thêm user vào admin group

### Bước 5: Thêm Tags (Tùy chọn)

Tags là metadata tùy chọn có thể được thêm vào các tài nguyên AWS. Ví dụ:
- Key: `department`
- Value: `engineering`

Mặc dù chúng ta sẽ không thêm tags ở mọi nơi trong khóa học này, nhưng biết cách chúng hoạt động là điều tốt.

### Bước 6: Review và Create

Xem lại tất cả các cài đặt:
- Username
- Permissions (thông qua group membership)
- Tags

Sau đó nhấp "Create user" để hoàn tất quá trình.

## Hiểu về IAM Groups và Permissions

Sau khi tạo user, hãy xem cách permissions hoạt động:

### User Groups
1. Điều hướng đến "User groups" ở thanh bên trái
2. Bạn sẽ thấy group "admin" mà chúng ta đã tạo
3. Group hiển thị:
   - Một user (Stephane)
   - Policy AdministratorAccess được gắn vào group

### User Permissions
Khi bạn xem permission policies của user, bạn sẽ thấy:
- AdministratorAccess có mặt
- Nhưng nó **không được gắn trực tiếp**
- Nó được gắn **thông qua group "admin"**

Điều này có nghĩa là user kế thừa permissions từ admin group mà họ thuộc về. **Đây là lý do tại sao chúng ta đặt users vào groups** - việc quản lý permissions theo cách này đơn giản hơn nhiều.

## Tùy chỉnh Sign-in URL

Để việc đăng nhập dễ dàng hơn:

1. Quay lại IAM Dashboard
2. Nhìn vào phần AWS account của bạn
3. Bạn sẽ thấy Account ID và Sign-in URL
4. Nhấp "Create alias" để tùy chỉnh URL
5. Nhập một alias (ví dụ: "aws-stephane-v5") - nó phải là duy nhất
6. Điều này đơn giản hóa sign-in URL của bạn

## Đăng nhập với IAM User

### Sử dụng hai cửa sổ trình duyệt (Khuyến nghị)

Để quản lý đồng thời cả root và IAM user accounts:

1. Giữ cửa sổ trình duyệt hiện tại với root user
2. Mở một **cửa sổ private/incognito** trong trình duyệt của bạn
   - Chrome, Firefox và Safari đều có tính năng này
3. Dán sign-in URL vào cửa sổ private

**Lợi ích của cách tiếp cận này:**
- Bạn có thể có hai cửa sổ đặt cạnh nhau
- Root account ở bên trái (cửa sổ thông thường)
- IAM user ở bên phải (cửa sổ private)
- Cả hai đều duy trì trạng thái đăng nhập đồng thời

### Quy trình đăng nhập

1. Đến trang đăng nhập AWS
2. Chọn "IAM user" (không phải root user)
3. Nhập một trong hai:
   - Account ID, hoặc
   - Account alias (cái bạn đã tạo)
4. Nhập IAM username của bạn (ví dụ: "Stephane")
5. Nhập password của bạn
6. Nhấp "Sign in"

### Xác minh đăng nhập

Sau khi đăng nhập, nhìn vào góc trên bên phải:
- **Cửa sổ IAM user:** Hiển thị account ID và IAM username
- **Cửa sổ Root user:** Chỉ hiển thị account ID

## Lời nhắc quan trọng về bảo mật

⚠️ **Quan trọng:** Hãy chắc chắn không làm mất thông tin đăng nhập root account và admin login của bạn. Nếu không, bạn sẽ gặp rắc rối lớn với tài khoản của mình và sẽ phải liên hệ với bộ phận hỗ trợ của AWS.

### Best Practices cho khóa học này

- **Khuyến nghị:** Sử dụng IAM user cho các hoạt động hàng ngày (không phải root user)
- Đôi khi trong khóa học, bạn có thể thấy cả root và IAM user đều được sử dụng
- Khi bạn cần sử dụng cụ thể root hoặc IAM user, nó sẽ được chỉ ra rõ ràng
- Đừng lo lắng - bạn sẽ được hướng dẫn trong suốt khóa học

## Các bước tiếp theo

Trong phần còn lại của section này, vui lòng giữ hai cửa sổ này mở (root và IAM user) vì chúng ta sẽ sử dụng chúng trong các bài giảng sắp tới.

---

**Tóm tắt:** Bây giờ bạn đã học được cách:
- Truy cập IAM console
- Hiểu IAM như một global service
- Tạo IAM users với permissions phù hợp
- Sử dụng groups để quản lý permissions hiệu quả
- Tùy chỉnh sign-in URL của bạn
- Đăng nhập với IAM user trong khi vẫn duy trì quyền truy cập root



================================================================================
FILE: 50-aws-cleanup-guide-after-section.md
================================================================================

# Hướng Dẫn Dọn Dẹp Tài Nguyên AWS Sau Mỗi Phần

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thực hiện quy trình dọn dẹp tài nguyên AWS sau khi hoàn thành một phần học để tránh các khoản phí không cần thiết. Nội dung bao gồm việc xóa hệ thống file EFS, EC2 instances, EBS volumes, snapshots và security groups.

## Yêu Cầu Trước Khi Bắt Đầu

- Quyền truy cập AWS Console
- Các tài nguyên đã tạo trong phần trước (EFS, EC2, EBS, v.v.)

## Quy Trình Dọn Dẹp Từng Bước

### 1. Xóa Hệ Thống File EFS

Đầu tiên, chúng ta sẽ dọn dẹp Elastic File System (EFS):

1. Điều hướng đến dịch vụ EFS trong AWS Console
2. Chọn **Actions** trên file system của bạn
3. Chọn **Delete**
4. Nhập **File System ID** khi được yêu cầu
5. Xác nhận việc xóa

Hệ thống file sẽ được xóa khỏi tài khoản của bạn.

### 2. Terminate EC2 Instances

Đảm bảo terminate tất cả EC2 instances đang chạy:

1. Vào EC2 Dashboard
2. Điều hướng đến **Instances**
3. Chọn tất cả instances đang chạy
4. Click **Instance State** → **Terminate**
5. Xác nhận việc terminate

### 3. Xóa EBS Volumes

Dọn dẹp tất cả EBS volumes ở trạng thái available:

1. Trong EC2 Dashboard, điều hướng đến **Volumes**
2. Lọc các volumes có trạng thái **Available**
3. Nhấp chuột phải vào từng volume
4. Chọn **Delete Volume**
5. Xác nhận việc xóa cho tất cả volumes available

> **Lưu ý:** Chỉ những volumes không được gắn vào instances mới có thể xóa được.

### 4. Xóa EBS Snapshots

Xóa các snapshots để tránh phí lưu trữ:

1. Điều hướng đến **Snapshots** trong EC2 Dashboard
2. Chọn tất cả snapshots bạn đã tạo trong phần học
3. Click **Actions** → **Delete**
4. Xác nhận việc xóa cho từng snapshot

Điều này đảm bảo bạn sẽ không phải trả phí cho việc lưu trữ snapshots.

### 5. Dọn Dẹp Security Groups

Cuối cùng, xóa các security groups không cần thiết:

1. Điều hướng đến **Security Groups** trong EC2 Dashboard
2. Chọn các security groups bạn muốn xóa
3. Click **Actions** → **Delete security group**

**Những điểm quan trọng cần lưu ý:**

- **Không bao giờ xóa default security group** - nó được AWS yêu cầu
- Security groups chỉ có thể xóa sau khi tất cả EC2 instances liên quan đã được terminate
- Một số security groups có thể không bị xóa ngay lập tức - hãy đợi instances terminate hoàn toàn
- Tiếp tục thử cho đến khi thành công

#### Ví Dụ Thứ Tự Xóa:

1. Xóa các custom security groups (ví dụ: load balancer security group)
2. Đợi EC2 instances terminate hoàn toàn
3. Xóa các security groups liên quan đến EC2 (ví dụ: EC2 for EFS)

> **Mẹo:** Nếu security group vẫn đang được sử dụng, bạn sẽ nhận được thông báo lỗi. Đợi vài phút để instances tắt hoàn toàn, sau đó thử lại.

## Xác Minh

Sau khi hoàn thành tất cả các bước:

- ✅ EFS file systems đã xóa
- ✅ EC2 instances đã terminate
- ✅ EBS volumes đã xóa
- ✅ Snapshots đã xóa
- ✅ Custom security groups đã xóa

Bạn đã sẵn sàng để tiếp tục phần tiếp theo mà không phải lo lắng về các khoản phí bất ngờ!

## Xử Lý Sự Cố

### Security Group Không Thể Xóa

**Vấn đề:** Security group vẫn được liên kết với instances đang chạy

**Giải pháp:** 
- Đợi tất cả EC2 instances terminate hoàn toàn (có thể mất vài phút)
- Kiểm tra xem có network interfaces nào vẫn đang sử dụng security group không
- Thử xóa lại sau vài phút

### Volume Không Thể Xóa

**Vấn đề:** Volume vẫn được gắn vào một instance

**Giải pháp:**
- Đảm bảo EC2 instance đã được terminate
- Đợi instance terminate hoàn toàn
- Volume sẽ có sẵn để xóa

## Cân Nhắc Về Chi Phí

Dọn dẹp tài nguyên kịp thời giúp bạn:

- Tránh các khoản phí cho EC2 instances đã dừng (nhưng chưa terminate)
- Ngăn chặn phí lưu trữ EBS volume
- Loại bỏ chi phí lưu trữ snapshot
- Dừng phí lưu trữ EFS

Ghi nhớ: AWS tính phí cho các tài nguyên ngay cả khi chúng không được sử dụng tích cực, vì vậy việc dọn dẹp thường xuyên là rất quan trọng!



================================================================================
FILE: 51-aws-scalability-and-high-availability.md
================================================================================

# Khả Năng Mở Rộng và Tính Sẵn Sàng Cao trên AWS

## Giới Thiệu

Bài học này trình bày các khái niệm cơ bản về khả năng mở rộng (scalability) và tính sẵn sàng cao (high availability) trên AWS. Những khái niệm này rất quan trọng để hiểu cách xây dựng các ứng dụng đám mây mạnh mẽ và linh hoạt.

## Khả Năng Mở Rộng là gì?

Khả năng mở rộng có nghĩa là ứng dụng hoặc hệ thống của bạn có thể xử lý tải lớn hơn bằng cách thích ứng. Có hai loại khả năng mở rộng chính:

1. **Mở Rộng Theo Chiều Dọc** (Vertical Scalability)
2. **Mở Rộng Theo Chiều Ngang** (Horizontal Scalability) - còn gọi là Elasticity

> **Lưu ý:** Khả năng mở rộng khác với tính sẵn sàng cao - chúng có liên quan nhưng là các khái niệm khác biệt.

## Mở Rộng Theo Chiều Dọc (Vertical Scalability)

### Định Nghĩa

Mở rộng theo chiều dọc có nghĩa là tăng kích thước của instance.

### Ví Dụ Trung Tâm Cuộc Gọi

Hãy nghĩ về một nhân viên điện thoại trong trung tâm cuộc gọi:
- **Nhân viên cấp Junior**: Có thể xử lý 5 cuộc gọi mỗi phút
- **Nhân viên cấp Senior**: Có thể xử lý 10 cuộc gọi mỗi phút

Khi bạn thăng cấp nhân viên junior lên senior, bạn đã mở rộng năng lực của họ. Đây là mở rộng theo chiều dọc - đi lên phía trên!

### Ví Dụ EC2

- Ứng dụng của bạn chạy trên instance `t2.micro`
- Để nâng cấp, bạn chuyển sang instance `t2.large`

### Khi Nào Sử Dụng Mở Rộng Theo Chiều Dọc

Mở rộng theo chiều dọc rất phổ biến cho **các hệ thống không phân tán**, chẳng hạn như:
- Cơ sở dữ liệu (Database)
- Amazon RDS
- Amazon ElastiCache

Bạn có thể mở rộng các dịch vụ này theo chiều dọc bằng cách nâng cấp loại instance cơ bản.

### Giới Hạn

Thường có giới hạn về mức độ mở rộng theo chiều dọc do ràng buộc phần cứng. Tuy nhiên, mở rộng theo chiều dọc phù hợp với nhiều trường hợp sử dụng.

## Mở Rộng Theo Chiều Ngang (Horizontal Scalability)

### Định Nghĩa

Mở rộng theo chiều ngang có nghĩa là tăng số lượng instance hoặc hệ thống cho ứng dụng của bạn.

### Ví Dụ Trung Tâm Cuộc Gọi

Bắt đầu với một nhân viên bị quá tải:
1. Thuê nhân viên thứ hai → tăng gấp đôi năng lực
2. Thuê nhân viên thứ ba → tăng gấp ba năng lực
3. Thuê sáu nhân viên → năng lực tăng 6 lần

Đây là mở rộng theo chiều ngang - mở rộng ra bên ngoài!

### Đặc Điểm Chính

- Ngụ ý **hệ thống phân tán** (distributed systems)
- Phổ biến cho các ứng dụng web và ứng dụng hiện đại
- **Lưu ý:** Không phải mọi ứng dụng đều có thể là hệ thống phân tán

### Lợi Thế Đám Mây

Mở rộng theo chiều ngang rất dễ dàng với các dịch vụ đám mây như Amazon EC2. Bạn chỉ cần khởi chạy instance mới bằng vài cú nhấp chuột, và ứng dụng của bạn đã được mở rộng theo chiều ngang.

## Tính Sẵn Sàng Cao (High Availability)

### Định Nghĩa

Tính sẵn sàng cao có nghĩa là chạy ứng dụng hoặc hệ thống của bạn trong ít nhất hai trung tâm dữ liệu hoặc vùng khả dụng (availability zones - AZs) trên AWS.

### Mục Tiêu

Mục tiêu của tính sẵn sàng cao là có thể tồn tại khi mất một trung tâm dữ liệu. Nếu một trung tâm ngừng hoạt động, hệ thống vẫn tiếp tục chạy.

### Ví Dụ Trung Tâm Cuộc Gọi

- **Tòa nhà 1 (New York)**: 3 nhân viên điện thoại
- **Tòa nhà 2 (San Francisco)**: 3 nhân viên điện thoại

Nếu tòa nhà New York mất kết nối internet hoặc kết nối cuộc gọi, tòa nhà San Francisco vẫn có thể nhận cuộc gọi. Trung tâm cuộc gọi vẫn sẵn sàng cao.

### Các Loại Tính Sẵn Sàng Cao

1. **Tính Sẵn Sàng Cao Thụ Động** (Passive High Availability)
   - Ví dụ: RDS Multi-AZ
   - Các hệ thống dự phòng sẵn sàng tiếp quản

2. **Tính Sẵn Sàng Cao Chủ Động** (Active High Availability)
   - Xảy ra với mở rộng theo chiều ngang
   - Tất cả các hệ thống đều xử lý yêu cầu đồng thời
   - Ví dụ: Nhiều tòa nhà cùng nhận cuộc gọi cùng một lúc

## Khả Năng Mở Rộng và Tính Sẵn Sàng Cao trên EC2

### Mở Rộng Theo Chiều Dọc

- **Scale Up/Down**: Tăng hoặc giảm kích thước instance
- **Phạm Vi**: 
  - Nhỏ nhất: `t2.nano` (0.5 GB RAM, 1 vCPU)
  - Lớn nhất: `u-12tb1.metal` (12.3 TB RAM, 450 vCPU)
- Bạn có thể mở rộng từ instance rất nhỏ đến cực kỳ lớn

### Mở Rộng Theo Chiều Ngang

- **Scale Out**: Tăng số lượng instance
- **Scale In**: Giảm số lượng instance
- **Trường Hợp Sử Dụng**:
  - Auto Scaling Groups (Nhóm Tự Động Mở Rộng)
  - Load Balancers (Bộ Cân Bằng Tải)

### Tính Sẵn Sàng Cao

- Chạy cùng một instance ứng dụng trên nhiều AZ
- **Triển Khai**:
  - Auto Scaling Group với multi-AZ được bật
  - Load Balancer với multi-AZ được bật

## Tóm Tắt

Hiểu về khả năng mở rộng và tính sẵn sàng cao là rất quan trọng cho các chứng chỉ AWS và ứng dụng thực tế:

- **Mở Rộng Theo Chiều Dọc**: Tăng kích thước instance (scale up/down)
- **Mở Rộng Theo Chiều Ngang**: Tăng số lượng instance (scale out/in)
- **Tính Sẵn Sàng Cao**: Chạy trên nhiều trung tâm dữ liệu/AZ

### Điểm Chính Cần Nhớ

Hãy nhớ **ví dụ về trung tâm cuộc gọi** khi suy nghĩ về các khái niệm này:
- Mở rộng theo chiều dọc = Đào tạo nhân viên xử lý nhiều cuộc gọi hơn
- Mở rộng theo chiều ngang = Thuê thêm nhiều nhân viên
- Tính sẵn sàng cao = Có nhân viên ở nhiều tòa nhà

Những khái niệm này là nền tảng và có thể xuất hiện trong các câu hỏi thi, vì vậy hãy đảm bảo bạn hiểu rõ chúng!



================================================================================
FILE: 52-aws-elastic-load-balancer-introduction.md
================================================================================

# AWS Elastic Load Balancer - Giới Thiệu

## Load Balancing Là Gì?

Load balancer (bộ cân bằng tải) là một máy chủ hoặc một tập hợp các máy chủ có nhiệm vụ chuyển tiếp lưu lượng truy cập đến nhiều EC2 instance hoặc máy chủ backend/downstream.

### Cách Hoạt Động Của Load Balancing

Xét một kịch bản với ba EC2 instance được đặt phía sau một Elastic Load Balancer (ELB):

- Khi người dùng đầu tiên kết nối đến ELB, lưu lượng của họ được gửi đến một EC2 instance
- Khi người dùng thứ hai kết nối, họ được định tuyến đến một EC2 instance khác
- Người dùng thứ ba được cân bằng đến EC2 instance thứ ba

Nguyên tắc chính là khi có nhiều người dùng kết nối, tải sẽ được phân phối đều trên nhiều EC2 instance. Người dùng không biết họ đang kết nối đến instance backend nào - họ chỉ kết nối đến load balancer, cung cấp một điểm kết nối duy nhất.

## Tại Sao Nên Sử Dụng Load Balancer?

### Lợi Ích Chính

1. **Phân Tán Tải**: Phân phối lưu lượng truy cập trên nhiều instance downstream
2. **Điểm Truy Cập Duy Nhất**: Cung cấp một endpoint duy nhất cho ứng dụng của bạn
3. **Xử Lý Lỗi**: Xử lý liền mạch các lỗi của instance downstream thông qua cơ chế health check
4. **Kiểm Tra Sức Khỏe**: Giám sát tình trạng instance liên tục
5. **SSL Termination**: Xử lý lưu lượng HTTPS được mã hóa cho website của bạn
6. **Stickiness**: Duy trì phiên làm việc với cookies
7. **High Availability**: Duy trì tính khả dụng cao trên nhiều zone
8. **Phân Tách Lưu Lượng**: Tách biệt lưu lượng công khai khỏi lưu lượng riêng tư trong cloud

## Elastic Load Balancer (ELB)

### Managed Load Balancer (Dịch Vụ Được Quản Lý)

Elastic Load Balancer là một dịch vụ được quản lý, nghĩa là:

- **Quản Lý Bởi AWS**: AWS quản lý load balancer và đảm bảo nó sẽ hoạt động
- **Bảo Trì**: AWS xử lý việc nâng cấp, bảo trì và high availability
- **Cấu Hình**: Cung cấp các tùy chọn cấu hình để điều chỉnh hành vi của load balancer
- **Tiết Kiệm Chi Phí**: Rẻ hơn so với việc tự thiết lập load balancer của riêng bạn
- **Khả Năng Mở Rộng**: Loại bỏ khó khăn trong việc quản lý load balancer riêng từ góc độ khả năng mở rộng

### Tích Hợp Với AWS

Load balancer tích hợp liền mạch với nhiều dịch vụ AWS:

- EC2 instances
- Auto Scaling Groups
- Amazon ECS
- AWS Certificate Manager
- Amazon CloudWatch
- Amazon Route 53
- AWS WAF
- AWS Global Accelerator
- Và nhiều dịch vụ khác theo thời gian

## Health Checks (Kiểm Tra Sức Khỏe)

Health check là cơ chế quan trọng để load balancer xác minh xem EC2 instance có hoạt động đúng hay không. Nếu một instance không hoạt động, lưu lượng sẽ không được gửi đến instance đó.

### Cấu Hình Health Check

Health check được thực hiện bằng cách sử dụng:
- **Port**: Cổng để kiểm tra (ví dụ: 4567)
- **Route**: Endpoint để xác minh (ví dụ: `/health`)
- **Protocol**: Thường là HTTP

**Ví Dụ Cấu Hình:**
- Protocol: HTTP
- Port: 4567
- Endpoint: `/health`

Nếu EC2 instance không phản hồi với response OK (thường là mã trạng thái HTTP 200), instance sẽ được đánh dấu là không khỏe mạnh (unhealthy), và load balancer sẽ ngừng gửi lưu lượng đến instance đó.

## Các Loại AWS Load Balancer

### 1. Classic Load Balancer (CLB)
- **Thế Hệ**: V1 (thế hệ cũ)
- **Năm**: 2009
- **Giao Thức**: HTTP, HTTPS, TCP, SSL (Secure TCP)
- **Trạng Thái**: Đã lỗi thời - AWS không khuyến nghị sử dụng nữa
- **Khả Dụng**: Vẫn có sẵn nhưng hiển thị là deprecated trong console

### 2. Application Load Balancer (ALB)
- **Thế Hệ**: V2 (thế hệ mới)
- **Năm**: 2016
- **Giao Thức**: HTTP, HTTPS, WebSocket
- **Khuyến Nghị**: Được khuyến nghị cho các ứng dụng hiện đại

### 3. Network Load Balancer (NLB)
- **Thế Hệ**: V2 (thế hệ mới)
- **Năm**: 2017
- **Giao Thức**: TCP, TLS (Secure TCP), UDP
- **Trường Hợp Sử Dụng**: Ứng dụng hiệu suất cao, độ trễ thấp

### 4. Gateway Load Balancer (GWLB)
- **Thế Hệ**: Mới nhất
- **Năm**: 2020
- **Lớp**: Network Layer (Layer 3)
- **Giao Thức**: IP Protocol
- **Trường Hợp Sử Dụng**: Triển khai, mở rộng và quản lý các thiết bị ảo của bên thứ ba

### Khuyến Nghị

Rất khuyến nghị sử dụng các load balancer thế hệ mới (ALB, NLB, GWLB) vì chúng cung cấp nhiều tính năng hơn.

### Các Loại Load Balancer Theo Quyền Truy Cập

- **Internal (Private)**: Truy cập mạng riêng tư
- **External (Public)**: Load balancer công khai cho website và ứng dụng

## Cấu Hình Bảo Mật

### Security Group Của Load Balancer

Người dùng có thể truy cập load balancer từ bất kỳ đâu bằng HTTP hoặc HTTPS.

**Quy Tắc Security Group:**
- **Port Range**: 80 (HTTP) hoặc 443 (HTTPS)
- **Source**: `0.0.0.0/0` (bất kỳ đâu)

Điều này cho phép tất cả người dùng kết nối đến load balancer.

### Security Group Của EC2 Instance

EC2 instance chỉ nên cho phép lưu lượng đến trực tiếp từ load balancer.

**Quy Tắc Security Group:**
- **Protocol**: HTTP
- **Port**: 80
- **Source**: Security Group của Load Balancer (không phải IP range)

Bằng cách liên kết security group của EC2 instance với security group của load balancer, bạn đảm bảo rằng EC2 instance chỉ chấp nhận lưu lượng có nguồn gốc từ load balancer. Đây là một cơ chế bảo mật nâng cao.

## Tóm Tắt

Load balancer là một lựa chọn hiển nhiên khi nói đến cân bằng tải trên AWS. Chúng cung cấp:
- Phân phối lưu lượng tự động
- High availability và khả năng chịu lỗi
- Tích hợp liền mạch với các dịch vụ AWS
- Cơ chế bảo mật nâng cao
- Giải pháp tiết kiệm chi phí và có khả năng mở rộng

Trong các phần tiếp theo, chúng ta sẽ thảo luận chi tiết hơn về Classic Load Balancer, Application Load Balancer và Network Load Balancer.



================================================================================
FILE: 53-aws-application-load-balancer-overview.md
================================================================================

# Tổng Quan về AWS Application Load Balancer (ALB)

## Lưu Ý: Về Classic Load Balancer (CLB)

Classic Load Balancer đã bị ngừng hỗ trợ tại AWS và sẽ sớm không còn khả dụng trong AWS Console. Kỳ thi cũng đã loại bỏ mọi tham chiếu đến nó, do đó nó sẽ không được đề cập sâu trong khóa học này hay các bài thực hành.

## Giới Thiệu về Application Load Balancer

Application Load Balancer (ALB) là loại load balancer thứ hai có sẵn trong AWS. Đây là một **load balancer chỉ hoạt động ở Layer 7 (HTTP)**, được thiết kế đặc biệt cho lưu lượng HTTP.

### Các Tính Năng Chính

- **Định Tuyến Đa Ứng Dụng**: Định tuyến lưu lượng đến nhiều ứng dụng HTTP trên nhiều máy
- **Target Groups (Nhóm Đích)**: Tổ chức các máy thành các nhóm logic gọi là target groups
- **Hỗ Trợ Container**: Cân bằng tải cho nhiều ứng dụng trên cùng một EC2 instance sử dụng container và ECS
- **Hỗ Trợ HTTP/2 và WebSocket**: Hỗ trợ đầy đủ các giao thức HTTP hiện đại
- **Chuyển Hướng Tự Động**: Có thể chuyển hướng lưu lượng từ HTTP sang HTTPS tại tầng load balancer

## Khả Năng Định Tuyến

ALB hỗ trợ định tuyến thông minh dựa trên nhiều tiêu chí khác nhau:

### 1. Định Tuyến Theo Đường Dẫn (Path-Based)
Định tuyến dựa trên đường dẫn URL:
- `example.com/users` → Target Group 1
- `example.com/posts` → Target Group 2

### 2. Định Tuyến Theo Hostname
Định tuyến dựa trên tên miền:
- `one.example.com` → Target Group 1
- `other.example.com` → Target Group 2

### 3. Định Tuyến Theo Query String và Header
Định tuyến dựa trên tham số truy vấn:
- `example.com/reserves?id=123&order=false` → Target Group cụ thể

## Trường Hợp Sử Dụng

ALB lý tưởng cho:
- **Kiến trúc microservices**
- **Ứng dụng dựa trên container** (Docker, ECS)
- **Tính năng ánh xạ cổng** để chuyển hướng cổng động trên các EC2 instance chạy ECS

### So Sánh với Classic Load Balancer

- **Classic Load Balancer**: Cần một load balancer cho mỗi ứng dụng
- **Application Load Balancer**: Một ALB có thể xử lý nhiều ứng dụng cùng lúc

## Ví Dụ Kiến Trúc: Microservices

```
External Application Load Balancer (Công khai)
    ↓
    ├── Target Group 1: route /user
    │   └── EC2 Instances (Ứng dụng User)
    │
    └── Target Group 2: route /search
        └── EC2 Instances (Ứng dụng Search)
```

Cả hai microservices hoạt động độc lập nhưng đều có thể truy cập thông qua cùng một ALB, ALB sẽ định tuyến các yêu cầu một cách thông minh dựa trên đường dẫn URL.

## Target Groups (Nhóm Đích)

Target groups có thể bao gồm:

1. **EC2 Instances** - Được quản lý bởi Auto Scaling Groups
2. **ECS Tasks** - Cho các ứng dụng container hóa
3. **Lambda Functions** - Nền tảng của serverless trong AWS
4. **Địa Chỉ IP** - Phải là địa chỉ IP private

ALB có thể định tuyến đến nhiều target groups, và các health check được thực hiện ở cấp độ target group.

## Ví Dụ Định Tuyến Nâng Cao: Kiến Trúc Hybrid

```
Application Load Balancer
    ↓
    ├── Target Group 1: ?Platform=Mobile
    │   └── EC2 Instances (AWS Cloud)
    │
    └── Target Group 2: ?Platform=Desktop
        └── Private Servers (On-Premises)
```

Trong ví dụ này:
- Lưu lượng mobile được định tuyến sử dụng query string `?Platform=Mobile` đến các EC2 instance trên cloud
- Lưu lượng desktop được định tuyến sử dụng query string `?Platform=Desktop` đến các máy chủ tại chỗ (được đăng ký bằng IP private)

## Những Điều Cần Lưu Ý

### Fixed Hostname (Tên Miền Cố Định)
- ALB cung cấp một hostname cố định (tương tự Classic Load Balancer)

### Bảo Toàn IP Của Client
Các application server không nhìn thấy trực tiếp IP của client. Thay vào đó, ALB sử dụng các header đặc biệt:

- **X-Forwarded-For**: Chứa địa chỉ IP thực của client
- **X-Forwarded-Port**: Chứa cổng của client
- **X-Forwarded-Proto**: Chứa giao thức được sử dụng (HTTP/HTTPS)

### Quy Trình Connection Termination

```
Client (12.34.56.78)
    ↓ [Connection Termination]
Load Balancer (Private IP)
    ↓
EC2 Instance
```

1. Client kết nối đến load balancer với IP công khai của họ (ví dụ: 12.34.56.78)
2. Load balancer ngắt kết nối (terminate connection)
3. Load balancer tạo kết nối mới đến EC2 instance sử dụng IP private của nó
4. EC2 instance đọc IP gốc của client từ header `X-Forwarded-For`

## Tóm Tắt

Application Load Balancer là một load balancer Layer 7 mạnh mẽ, xuất sắc trong việc định tuyến lưu lượng HTTP trong các kiến trúc phân tán hiện đại. Khả năng định tuyến nâng cao, hỗ trợ nhiều loại target khác nhau, và tích hợp liền mạch với các dịch vụ container và serverless khiến nó trở thành lựa chọn ưu tiên cho các ứng dụng microservices và cloud-native.



================================================================================
FILE: 54-aws-application-load-balancer-hands-on-tutorial.md
================================================================================

# AWS Application Load Balancer - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn thực hành này trình bày cách tạo và cấu hình AWS Application Load Balancer (ALB) để phân phối lưu lượng truy cập giữa nhiều EC2 instance. Bạn sẽ học cách thiết lập target group, cấu hình security group và kiểm tra chức năng cân bằng tải.

## Điều Kiện Tiên Quyết

- Tài khoản AWS với quyền phù hợp
- Hiểu biết cơ bản về EC2 instance
- Quen thuộc với security group

## Phần 1: Khởi Chạy EC2 Instance

### Bước 1: Tạo Hai EC2 Instance

1. Truy cập bảng điều khiển EC2 và nhấp **Launch Instances**
2. Cấu hình các thiết lập sau:
   - **Số lượng instance**: 2
   - **Tên**: My First Instance (đổi tên instance thứ hai thành "My Second Instance")
   - **AMI**: Amazon Linux 2
   - **Loại instance**: t2.micro
   - **Key pair**: Tiếp tục mà không cần key pair (chúng ta sẽ dùng EC2 Instance Connect nếu cần)

### Bước 2: Cấu Hình Network Settings

1. Chọn **existing security group**
2. Chọn security group **Launch Wizard 1**
   - Cho phép lưu lượng HTTP và SSH đến EC2 instance

### Bước 3: Thêm User Data Script

1. Cuộn xuống **Advanced details**
2. Thêm EC2 user data script để tự động cấu hình các instance
3. Khởi chạy cả hai instance

### Bước 4: Xác Minh Thiết Lập Instance

1. Đợi cả hai instance đạt trạng thái "running"
2. Sao chép địa chỉ IPv4 của instance đầu tiên và truy cập trong trình duyệt
3. Bạn sẽ thấy "Hello World" từ instance đầu tiên
4. Lặp lại với instance thứ hai
5. Cả hai instance đều hiển thị "Hello World" với các mã định danh khác nhau

## Phần 2: Hiểu Về Các Loại Load Balancer

### Application Load Balancer (ALB)
- **Giao thức**: HTTP và HTTPS
- **Trường hợp sử dụng**: Ứng dụng web và microservices
- **Tầng**: Tầng 7 (Tầng ứng dụng)

### Network Load Balancer (NLB)
- **Giao thức**: TCP, UDP, hoặc TLS qua TCP
- **Trường hợp sử dụng**: Ứng dụng hiệu suất cực cao
- **Hiệu suất**: Hàng triệu yêu cầu mỗi giây với độ trễ cực thấp

### Gateway Load Balancer (GLB)
- **Trường hợp sử dụng**: Bảo mật, phát hiện xâm nhập, tường lửa
- **Mục đích**: Phân tích lưu lượng mạng

### Classic Load Balancer
- **Trạng thái**: Đang bị ngừng hỗ trợ (có thể không còn khả dụng)
- **Lưu ý**: Không khuyến nghị cho các triển khai mới

## Phần 3: Tạo Application Load Balancer

### Bước 1: Cấu Hình Cài Đặt Cơ Bản

1. Điều hướng đến **Load Balancers** trong bảng điều khiển EC2
2. Nhấp **Create Load Balancer**
3. Chọn **Application Load Balancer**
4. Cấu hình:
   - **Tên**: DemoALB
   - **Scheme**: Internet-facing
   - **Loại địa chỉ IP**: IPv4

### Bước 2: Network Mapping

1. Chọn tất cả các availability zone để đảm bảo tính khả dụng cao
2. Điều này đảm bảo load balancer được triển khai trên nhiều AZ

### Bước 3: Cấu Hình Security Group

1. Tạo security group mới:
   - **Tên**: demo-sg-load-balancer
   - **Mô tả**: Allow HTTP into load balancer, into ALB
   - **Inbound rules**: Cho phép HTTP từ mọi nơi (0.0.0.0/0)
   - **Outbound rules**: Giữ cài đặt mặc định

2. Sau khi tạo, làm mới và chọn security group mới
3. Xóa security group mặc định

## Phần 4: Tạo Target Group

### Bước 1: Cấu Hình Cơ Bản

1. Nhấp **Create target group**
2. Cấu hình:
   - **Loại target**: Instances
   - **Tên**: demo-tg-alb
   - **Giao thức**: HTTP
   - **Cổng**: 80
   - **Phiên bản HTTP**: HTTP/1

### Bước 2: Health Check

- Giữ cài đặt health check mặc định
- Điều này cho phép ALB giám sát tình trạng sức khỏe của instance

### Bước 3: Đăng Ký Target

1. Nhấp **Next**
2. Chọn cả hai EC2 instance
3. Chỉ định **cổng 80** cho cả hai instance
4. Nhấp **Include as pending below**
5. Tạo target group

## Phần 5: Hoàn Thành Thiết Lập Load Balancer

### Bước 1: Liên Kết Target Group Với Listener

1. Quay lại trang tạo load balancer
2. Làm mới danh sách target group
3. Chọn **demo-tg-alb** làm target group
4. Listener sẽ định tuyến lưu lượng HTTP trên cổng 80 đến target group này

### Bước 2: Tạo Load Balancer

1. Nhấp **Create load balancer**
2. Đợi load balancer được cung cấp (trạng thái: Active)

## Phần 6: Kiểm Tra Load Balancer

### Kiểm Tra 1: Xác Minh Load Balancing

1. Sao chép DNS name của load balancer
2. Dán vào trình duyệt
3. Bạn sẽ thấy "Hello World" từ một trong các instance
4. Làm mới trang nhiều lần
5. **Kết quả**: Instance đích thay đổi mỗi lần làm mới, chứng minh load balancing đang hoạt động

### Kiểm Tra 2: Kiểm Tra Target Health

1. Điều hướng đến phần **Target Groups**
2. Chọn **demo-tg-alb**
3. Xem tab **Targets**
4. Cả hai instance đều hiển thị trạng thái **healthy**

### Kiểm Tra 3: Tình Huống Instance Lỗi

1. Dừng một trong các EC2 instance
2. Đợi khoảng 30 giây
3. Làm mới chế độ xem target group
4. **Kết quả**: Instance đã dừng hiển thị "unused" hoặc "unhealthy"
5. Truy cập URL load balancer lần nữa
6. **Kết quả**: Lưu lượng chỉ được chuyển đến instance còn healthy

### Kiểm Tra 4: Khôi Phục Instance

1. Khởi động lại instance đã dừng
2. Đợi nó khởi động
3. Instance sẽ hiển thị trạng thái "initial health"
4. Sau khi vượt qua health check, nó trở thành "healthy"
5. Làm mới URL load balancer
6. **Kết quả**: Lưu lượng giờ được cân bằng giữa cả hai instance

## Những Điều Quan Trọng Cần Nhớ

### Lợi Ích Của Load Balancer

1. **Điểm truy cập duy nhất**: Một URL để truy cập nhiều instance
2. **Chuyển đổi dự phòng tự động**: Instance không healthy tự động bị loại khỏi rotation
3. **Tính khả dụng cao**: Lưu lượng tiếp tục chảy ngay cả khi instance lỗi
4. **Giám sát sức khỏe**: Target group liên tục giám sát tình trạng instance
5. **Khôi phục tự động**: Instance tự động được thêm lại khi healthy

### Các Thực Hành Tốt Nhất

- Triển khai load balancer trên nhiều availability zone
- Cấu hình health check phù hợp
- Sử dụng security group riêng cho load balancer
- Giám sát target health thường xuyên
- Lập kế hoạch bảo trì và khôi phục instance

## Kết Luận

Bạn đã thành công:
- Tạo và cấu hình Application Load Balancer
- Thiết lập target group với hai EC2 instance
- Kiểm tra chức năng load balancing
- Xác minh cơ chế chuyển đổi dự phòng và khôi phục tự động

Application Load Balancer cung cấp một giải pháp mạnh mẽ để phân phối lưu lượng giữa nhiều target trong khi đảm bảo tính khả dụng cao và quản lý sức khỏe tự động.



================================================================================
FILE: 55-aws-alb-advanced-concepts-security-and-rules.md
================================================================================

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



================================================================================
FILE: 56-aws-network-load-balancer-overview.md
================================================================================

# Tổng Quan về AWS Network Load Balancer (NLB)

## Giới Thiệu

Network Load Balancer (NLB) là giải pháp cân bằng tải mạnh mẽ của AWS hoạt động ở tầng 4 của mô hình OSI, xử lý lưu lượng TCP và UDP với hiệu năng vượt trội.

## Tính Năng Chính

### Cân Bằng Tải Tầng 4

- **Hỗ trợ Giao thức**: Xử lý lưu lượng TCP và UDP
- **Mức thấp hơn**: Hoạt động ở Layer 4 (Tầng Giao vận), khác với Application Load Balancer hoạt động ở Layer 7 (HTTP/HTTPS)
- **Trường hợp sử dụng**: Khi bạn thấy yêu cầu về UDP hoặc TCP trong bài thi, hãy nghĩ đến Network Load Balancer

### Hiệu Năng Cao

- **Hiệu năng cực cao**: Có khả năng xử lý hàng triệu yêu cầu mỗi giây
- **Độ trễ cực thấp**: Độ trễ tối thiểu trong xử lý yêu cầu
- **Tốt nhất cho**: Ứng dụng yêu cầu hiệu năng cao với giao thức TCP hoặc UDP

### Địa Chỉ IP Tĩnh

- **Một IP tĩnh cho mỗi Availability Zone**: Mỗi AZ có một địa chỉ IP tĩnh riêng
- **Gán Elastic IP**: Bạn có thể gán Elastic IP cho mỗi AZ
- **Trường hợp sử dụng**: Hoàn hảo khi ứng dụng của bạn cần được truy cập thông qua một tập hợp địa chỉ IP cố định (1, 2 hoặc 3 IP cụ thể)

## Kiến Trúc và Target Groups

### Cách Hoạt Động

Network Load Balancer hoạt động tương tự như Application Load Balancer:
1. Tạo các target groups
2. NLB chuyển hướng lưu lượng đến các target groups này
3. Hỗ trợ lưu lượng TCP trên cả frontend và backend
4. Có thể sử dụng các giao thức khác nhau (ví dụ: TCP ở frontend, GTP ở backend)

### Các Tùy Chọn Target Group

Network Load Balancer hỗ trợ hai loại targets:

#### 1. EC2 Instances
- Định tuyến trực tiếp đến các EC2 instances
- Gửi lưu lượng TCP hoặc UDP đến các instances đã đăng ký

#### 2. Địa Chỉ IP (Chỉ Private IPs)
- **Địa chỉ IP riêng được mã hóa cứng**
- Có thể bao gồm:
  - Private IPs của các EC2 instances của bạn
  - Private IPs của các server trong data center của bạn
- Cho phép kiến trúc hybrid cloud với tích hợp on-premises

### Cấu Hình Nâng Cao: Kết Hợp NLB + ALB

Bạn có thể đặt Network Load Balancer phía trước Application Load Balancer:

**Lợi ích:**
- **Từ NLB**: Địa chỉ IP cố định cho client truy cập
- **Từ ALB**: Các quy tắc xử lý và định tuyến lưu lượng HTTP nâng cao
- **Kết quả**: Một sự kết hợp hợp lệ và mạnh mẽ cho các kiến trúc phức tạp

## Health Checks

Target groups của Network Load Balancer hỗ trợ health checks sử dụng ba giao thức:

1. **Giao thức TCP**
2. **Giao thức HTTP**
3. **Giao thức HTTPS**

Nếu ứng dụng backend của bạn hỗ trợ HTTP hoặc HTTPS, bạn có thể cấu hình health checks sử dụng các giao thức này.

## Khi Nào Sử Dụng Network Load Balancer

Chọn Network Load Balancer khi bạn cần:

- ✅ **Hiệu năng cực cao**: Hàng triệu yêu cầu mỗi giây
- ✅ **Giao thức TCP/UDP**: Xử lý lưu lượng mạng mức thấp
- ✅ **Yêu cầu IP tĩnh**: Địa chỉ IP cố định (bao gồm Elastic IPs)
- ✅ **Độ trễ cực thấp**: Yêu cầu độ trễ tối thiểu
- ✅ **Kiến trúc Hybrid**: Tích hợp với data center on-premises

## Mẹo Thi

- **Lưu lượng UDP** → Nghĩ đến Network Load Balancer
- **Lưu lượng TCP** → Cân nhắc Network Load Balancer
- **Yêu cầu Static/Elastic IP** → Network Load Balancer
- **Nhu cầu hiệu năng cao** → Network Load Balancer
- **HTTP/HTTPS với IP cố định** → Kết hợp NLB + ALB

## Tóm Tắt

Network Load Balancer là giải pháp cân bằng tải Layer 4 hiệu năng cao của AWS, được thiết kế cho các kịch bản hiệu năng cực cao yêu cầu xử lý lưu lượng TCP/UDP và địa chỉ IP tĩnh. Khả năng xử lý hàng triệu yêu cầu mỗi giây với độ trễ cực thấp làm cho nó trở nên lý tưởng cho các ứng dụng quan trọng về hiệu năng.



================================================================================
FILE: 57-aws-network-load-balancer-hands-on-tutorial.md
================================================================================

# AWS Network Load Balancer (NLB) - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn thực hành này sẽ giúp bạn tạo và cấu hình AWS Network Load Balancer (NLB), bao gồm thiết lập security groups, target groups và khắc phục các sự cố thường gặp.

## Tạo Network Load Balancer

### Bước 1: Cấu Hình Cơ Bản

1. Điều hướng đến trang tạo Load Balancer
2. Chọn **Network Load Balancer**
3. Cấu hình các thiết lập sau:
   - **Tên**: `DemoNLB`
   - **Scheme**: Internet-facing (Hướng ra Internet)
   - **Loại địa chỉ IP**: IPv4

### Bước 2: Ánh Xạ Mạng (Network Mapping)

1. Chọn VPC của bạn
2. Kích hoạt tất cả các availability zone (trong ví dụ này là ba AZ)
3. Với mỗi availability zone:
   - Một subnet sẽ được tự động liên kết
   - Một địa chỉ IPv4 sẽ được AWS gán
   - **Lưu ý**: Bạn sẽ nhận được một địa chỉ IPv4 cố định cho mỗi AZ được kích hoạt
   - **Tùy chọn**: Bạn có thể sử dụng Elastic IP thay vì địa chỉ IP do AWS gán

### Bước 3: Security Groups

Việc gắn security group vào Network Load Balancer được khuyến nghị và là một tính năng mới hơn.

1. Nhấp **Create security group** (Tạo nhóm bảo mật)
2. Cấu hình security group:
   - **Tên**: `demo-sg-nlb`
   - **Inbound rules**: Cho phép HTTP (cổng 80) từ bất kỳ đâu (0.0.0.0/0)
   - **Outbound rules**: Mặc định (cho phép tất cả)
3. Tạo security group
4. Làm mới và chọn `demo-sg-nlb`
5. Xóa security group mặc định

**Điểm Quan Trọng**: Tương tự như Application Load Balancers (ALB), Network Load Balancers cũng sử dụng security groups để kiểm soát lưu lượng truy cập.

### Bước 4: Listeners và Routing

1. Cấu hình giao thức listener:
   - **Các tùy chọn có sẵn**: TCP, TCP_UDP, TLS, hoặc UDP
   - **Đã chọn**: TCP trên cổng 80
2. Tạo target group (xem phần tiếp theo)

## Tạo Target Group

### Cấu Hình Target Group

1. Nhấp **Create target group** (Tạo nhóm mục tiêu)
2. Chọn **Instances** làm loại target
3. Cấu hình các thiết lập:
   - **Tên**: `demo-tg-nlb`
   - **Giao thức**: TCP
   - **Cổng**: 80
   - **VPC**: Chọn VPC của bạn

### Cài Đặt Health Check (Kiểm Tra Sức Khỏe)

1. **Giao thức**: HTTP (vì chúng ta có ứng dụng HTTP trên các EC2 instances)
   - Các tùy chọn khác bao gồm: TCP, HTTPS
2. **Cài đặt nâng cao**:
   - **Ngưỡng khỏe mạnh (Healthy threshold)**: 2
   - **Thời gian chờ (Timeout)**: 2 giây
   - **Khoảng thời gian (Interval)**: 5 giây

### Đăng Ký Targets

1. Nhấp **Next** (Tiếp theo)
2. Chọn hai EC2 instances có sẵn của bạn
3. Nhấp **Include as pending below** (Bao gồm dưới dạng đang chờ)
4. Tạo target group

### Hoàn Tất Tạo Load Balancer

1. Quay lại cấu hình Network Load Balancer
2. Làm mới danh sách target group
3. Chọn `demo-tg-nlb`
4. Xem lại cấu hình
5. Tạo Network Load Balancer

## Khắc Phục Sự Cố

### Vấn Đề: Instances Không Khỏe Mạnh (Unhealthy)

Khi lần đầu truy cập URL của NLB, ứng dụng có thể không hoạt động.

**Nguyên Nhân Gốc Rễ**: Các target instances không khỏe mạnh vì health checks đang thất bại.

**Giải Pháp**: Cập nhật security groups của EC2 instances

1. Điều hướng đến các EC2 instances trong target group
2. Nhấp vào **Security** → **Security groups**
3. Kiểm tra các inbound rules hiện tại:
   - SSH từ bất kỳ đâu ✓
   - HTTP từ ALB security group ✓
   - HTTP từ NLB security group ✗ (thiếu)

4. Thêm một inbound rule mới:
   - **Loại**: HTTP
   - **Nguồn**: `demo-sg-nlb` (NLB security group)
   - **Mô tả**: "Allow traffic from NLB" (Cho phép lưu lượng từ NLB)

**Kết Quả**: Sau khi thêm quy tắc này, NLB có thể giao tiếp với các EC2 instances trong target group, và health checks sẽ vượt qua.

## Xác Minh

1. Đợi các instances trở nên khỏe mạnh trong target group
2. Truy cập URL của Network Load Balancer trong trình duyệt
3. Bạn sẽ thấy: "Hello World from [IP của instance]"
4. Làm mới nhiều lần để thấy IP thay đổi, xác nhận việc cân bằng tải giữa các instances

## Những Điểm Chính

- Network Load Balancers hoạt động tương tự như Application Load Balancers về mặt security groups
- Security groups của EC2 instances phải cho phép lưu lượng từ **cả** ALB và NLB security groups
- Cấu hình security group là rất quan trọng để NLB hoạt động đúng cách

## Dọn Dẹp (Phòng Tránh Chi Phí)

Để tránh phát sinh chi phí:

1. **Xóa Network Load Balancer**:
   - Chọn `DemoNLB`
   - Xóa

2. **Tùy chọn**: Xóa target group:
   - Chọn `demo-tg-nlb`
   - Xóa

3. **Tùy chọn**: Xóa security group:
   - Chọn `demo-sg-nlb`
   - Xóa
   - Lưu ý: Điều này không thực sự cần thiết nhưng là thực hành tốt

## Kết Luận

Bạn đã thành công tạo và cấu hình AWS Network Load Balancer, thiết lập security groups, khắc phục các vấn đề về health check, và học được các phương pháp tốt nhất để quản lý tài nguyên NLB.



================================================================================
FILE: 58-aws-gateway-load-balancer-overview.md
================================================================================

# Tổng quan về AWS Gateway Load Balancer

## Giới thiệu

**Gateway Load Balancer (GWLB)** là loại load balancer mới nhất trong AWS, được thiết kế để triển khai, mở rộng và quản lý các thiết bị mạng ảo của bên thứ ba trong AWS.

## Các trường hợp sử dụng

Bạn nên sử dụng Gateway Load Balancer khi cần:

- **Bảo vệ Tường lửa**: Định tuyến toàn bộ lưu lượng mạng qua các thiết bị tường lửa của bạn
- **Hệ thống Phát hiện và Ngăn chặn Xâm nhập (IDPS)**: Kiểm tra lưu lượng để phát hiện các mối đe dọa bảo mật
- **Kiểm tra Gói tin Sâu**: Phân tích nội dung gói tin ở cấp độ mạng
- **Sửa đổi Payload**: Điều chỉnh payload mạng ở tầng mạng

## Cách hoạt động

### Kiến trúc Truyền thống
Trước đây, người dùng có thể truy cập ứng dụng trực tiếp thông qua load balancer (như Application Load Balancer), với luồng lưu lượng: Người dùng → ALB → Ứng dụng.

### Kiến trúc Gateway Load Balancer

Với Gateway Load Balancer, luồng lưu lượng trở thành:

1. **Lưu lượng Người dùng** → Gateway Load Balancer
2. **GWLB** → Thiết bị Ảo Bên thứ ba (Target Group)
3. **Thiết bị Ảo** phân tích lưu lượng:
   - Nếu được phê duyệt → Lưu lượng quay lại GWLB
   - Nếu bị từ chối → Lưu lượng bị loại bỏ
4. **GWLB** → Ứng dụng (nếu lưu lượng được phê duyệt)

### Chi tiết Triển khai Chính

- **Sửa đổi Route Table**: GWLB cập nhật các route table của VPC ở hậu trường
- **Trong suốt với Ứng dụng**: Ứng dụng không biết lưu lượng đã được kiểm tra
- **Điểm Vào/Ra Duy nhất**: Toàn bộ lưu lượng VPC đi qua GWLB

## Thông số Kỹ thuật

### Tầng Mạng
- **Hoạt động ở Layer 3**: Tầng mạng (IP packets)
- **Giao thức**: Sử dụng giao thức GENEVE trên cổng 6081

### Hai Chức năng Chính
1. **Cổng Mạng Trong suốt**: Điểm vào và ra duy nhất cho toàn bộ lưu lượng VPC
2. **Load Balancer**: Phân phối lưu lượng trên các thiết bị ảo trong target group

## Target Groups (Nhóm Đích)

Gateway Load Balancer hỗ trợ các loại target sau:

### EC2 Instances
- Đăng ký theo Instance ID
- Thiết bị ảo chạy trên AWS EC2

### Địa chỉ IP
- Phải là địa chỉ IP private
- Hữu ích cho các thiết bị ảo chạy trên:
  - Mạng riêng của bạn
  - Data center tại chỗ (on-premises)
  - Yêu cầu đăng ký IP thủ công

## Điểm Chính Cần Nhớ

- **Hoạt động Layer 3**: Làm việc ở tầng mạng với các gói tin IP
- **Thiết bị Bên thứ ba**: Được thiết kế cho các thiết bị kiểm tra và bảo mật mạng
- **Giao thức GENEVE**: Sử dụng cổng 6081 (mẹo thi)
- **Tích hợp Trong suốt**: Ứng dụng không nhận biết việc kiểm tra lưu lượng
- **Đăng ký Target Linh hoạt**: Hỗ trợ EC2 instances và địa chỉ IP private

## Kết luận

Gateway Load Balancer đơn giản hóa quy trình phức tạp trước đây của việc định tuyến lưu lượng qua các thiết bị mạng bên thứ ba. Nó cung cấp một giải pháp tập trung, có khả năng mở rộng cho bảo mật mạng và kiểm tra lưu lượng trong môi trường AWS.

---

*Lưu ý: Việc triển khai thực hành Gateway Load Balancer khá phức tạp và thường yêu cầu kiến thức mạng nâng cao cùng với cấu hình thiết bị bên thứ ba phù hợp.*



================================================================================
FILE: 59-aws-elb-sticky-sessions-guide.md
================================================================================

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



================================================================================
FILE: 6-aws-multi-session-support.md
================================================================================

# Hỗ Trợ Đa Phiên AWS Console

## Tổng Quan

Hướng dẫn này giới thiệu tính năng hỗ trợ đa phiên trong AWS Console, cho phép bạn quản lý nhiều tài khoản AWS đồng thời trên cùng một trình duyệt.

## Hỗ Trợ Đa Phiên Là Gì?

Hỗ trợ đa phiên là một tính năng cho phép bạn:
- Đăng nhập vào nhiều tài khoản AWS sử dụng cùng một trình duyệt
- Chuyển đổi giữa các danh tính AWS khác nhau mà không cần đăng xuất
- Quản lý tài nguyên trên nhiều tài khoản khác nhau trong các cửa sổ trình duyệt riêng biệt

## Cách Hoạt Động

### Kích Hoạt Hỗ Trợ Đa Phiên

1. Nhấp vào tùy chọn hỗ trợ đa phiên để bật tính năng
2. Sau khi được kích hoạt, bạn có thể có một vai trò hoặc tài khoản cụ thể trong trình duyệt của mình
3. Nhấp vào "Add a session" (Thêm phiên) để đăng nhập vào các danh tính AWS bổ sung

### Sử Dụng Nhiều Phiên

Sau khi kích hoạt tính năng:
- Bạn có thể đăng nhập lại bằng bất kỳ account ID hoặc tài khoản root nào
- Mỗi phiên duy trì ngữ cảnh riêng biệt của nó
- Các cửa sổ trình duyệt khác nhau sẽ hiển thị thông tin tài khoản khác nhau

## Ví Dụ Thực Tế: EC2 và EBS

Để minh họa cách hoạt động của hỗ trợ đa phiên, đây là một ví dụ thực tế:

### Phiên 1
1. Điều hướng đến EC2 console
2. Vào mục **Volumes** trong EBS
3. Tạo một EBS volume (ví dụ: 1 GB)
4. Volume được tạo và hiển thị trong tài khoản này

### Phiên 2
1. Mở cùng trình duyệt với một phiên khác
2. Điều hướng đến EC2 → EBS
3. Lưu ý rằng các volume từ Phiên 1 **không hiển thị**
4. Điều này là do bạn đang sử dụng cửa sổ tài khoản khác

## Lợi Ích Chính

- **Cô Lập Tài Khoản**: Mỗi phiên duy trì sự tách biệt hoàn toàn giữa các tài khoản
- **Cải Thiện Quy Trình**: Không cần đăng xuất và đăng nhập lại để chuyển đổi tài khoản
- **Quản Lý Quy Mô**: Thiết yếu cho việc quản lý AWS ở quy mô lớn
- **Hiệu Quả Trình Duyệt**: Sử dụng một trình duyệt duy nhất cho nhiều tài khoản

## Lưu Ý Quan Trọng

- Tính năng này trước đây không khả dụng và đại diện cho một cải tiến đáng kể
- Bạn có thể có hai (hoặc nhiều hơn) tài khoản khác nhau trong các cửa sổ trình duyệt khác nhau
- Mỗi cửa sổ duy trì phiên và tài nguyên độc lập của riêng nó
- Đối với người dùng quản lý AWS trong nhiều năm, đây là một tính năng mang tính cách mạng

## Kết Luận

Hỗ trợ đa phiên là một bổ sung đáng hoan nghênh cho AWS Console, giúp việc quản lý nhiều tài khoản đồng thời dễ dàng hơn nhiều. Tính năng này đặc biệt có giá trị cho những người dùng cần làm việc với AWS ở quy mô lớn.

---

*Tính năng này loại bỏ nhu cầu sử dụng nhiều trình duyệt hoặc cửa sổ duyệt web ẩn danh để quản lý các tài khoản AWS khác nhau.*



================================================================================
FILE: 60-aws-cross-zone-load-balancing-guide.md
================================================================================

# Hướng Dẫn Cross-Zone Load Balancing trên AWS

## Tổng Quan

Cross-zone load balancing là một tính năng quan trọng trong AWS Elastic Load Balancing, quyết định cách thức phân phối traffic đến các EC2 instances trên nhiều Availability Zones (AZs).

## Cross-Zone Load Balancing là gì?

Cross-zone load balancing cho phép mỗi load balancer instance phân phối traffic đều đặn đến tất cả các instances đã đăng ký trong tất cả các availability zones, bất kể load balancer node nằm ở AZ nào.

### Ví Dụ Minh Họa

Xét một thiết lập với hai availability zones:
- **AZ1**: Load balancer với 2 EC2 instances
- **AZ2**: Load balancer với 8 EC2 instances
- Tổng cộng: 10 EC2 instances

## Khi Bật Cross-Zone Load Balancing

Khi cross-zone load balancing được kích hoạt:

1. Client gửi 50% traffic đến ALB instance thứ nhất và 50% đến ALB instance thứ hai
2. **Mỗi ALB phân phối traffic đến TẤT CẢ 10 EC2 instances** (bất kể AZ nào)
3. Mỗi EC2 instance nhận được 10% tổng traffic
4. Traffic được phân phối đồng đều trên tất cả các instances

### Lợi Ích
- Phân phối traffic đồng đều trên tất cả instances
- Không có instance nào bị quá tải do mất cân bằng AZ
- Tận dụng tài nguyên tốt hơn

## Khi Tắt Cross-Zone Load Balancing

Khi cross-zone load balancing bị vô hiệu hóa:

1. Client gửi 50% traffic đến AZ1 và 50% đến AZ2
2. **Mỗi ALB chỉ phân phối traffic đến các EC2 instances trong cùng AZ của nó**
3. Ở AZ1: Mỗi instance trong số 2 instances nhận 25% tổng traffic (50% ÷ 2)
4. Ở AZ2: Mỗi instance trong số 8 instances nhận 6.25% tổng traffic (50% ÷ 8)
5. Traffic được giữ trong phạm vi mỗi AZ

### Hệ Quả
- Phân phối traffic có thể không đồng đều nếu các AZ có số lượng instances khác nhau
- Một số instances có thể nhận nhiều traffic hơn các instances khác
- Traffic ở lại trong cùng AZ (không có data transfer giữa các AZ)

## Các Loại Load Balancer và Cài Đặt Mặc Định

### Application Load Balancer (ALB)
- **Mặc định**: Cross-zone load balancing **ĐƯỢC BẬT**
- Có thể tắt ở cấp độ target group
- **Chi phí**: Không tính phí cho data transfer giữa các AZ
- Cross-zone load balancing luôn bật mặc định cho ALB
- Có thể ghi đè cài đặt ở cấp độ target group với ba tùy chọn:
  - Kế thừa từ thuộc tính load balancer (bật mặc định)
  - Bắt buộc bật
  - Bắt buộc tắt

### Network Load Balancer (NLB)
- **Mặc định**: Cross-zone load balancing **BỊ TẮT**
- Có thể bật trong phần attributes settings
- **Chi phí**: Áp dụng phí data transfer khu vực khi được bật

### Gateway Load Balancer (GWLB)
- **Mặc định**: Cross-zone load balancing **BỊ TẮT**
- Có thể bật trong phần attributes settings
- **Chi phí**: Áp dụng phí data transfer khu vực khi được bật

### Classic Load Balancer (CLB) - Phiên Bản Cũ
- **Mặc định**: Cross-zone load balancing **BỊ TẮT**
- Có thể bật
- **Chi phí**: Không tính phí cho data transfer giữa các AZ khi được bật
- **Lưu ý**: Classic Load Balancer là thế hệ cũ và sẽ sớm bị ngừng hỗ trợ

## Cân Nhắc Chi Phí

### Lưu Ý Quan Trọng Về Phí Data Transfer

| Loại Load Balancer | Cài Đặt Mặc Định | Phí Cross-AZ Khi Bật |
|-------------------|-----------------|----------------------|
| Application (ALB) | Bật | **Không tính phí** |
| Network (NLB) | Tắt | **Có tính phí** |
| Gateway (GWLB) | Tắt | **Có tính phí** |
| Classic (CLB) | Tắt | **Không tính phí** |

Trong AWS, data transfer giữa các Availability Zones thường phát sinh chi phí. Tuy nhiên:
- **ALB**: Không tính phí cho cross-zone data transfer (mặc dù được bật mặc định)
- **NLB và GWLB**: Phải trả phí khu vực nếu cross-zone được bật
- **CLB**: Không tính phí cho cross-zone data transfer khi được bật

## Hướng Dẫn Thực Hành

### Cấu Hình Network Load Balancer

1. Điều hướng đến NLB của bạn trong AWS Console
2. Kéo xuống và nhấp vào **Attributes**
3. Cross-zone load balancing sẽ hiển thị là **OFF** mặc định
4. Nhấp **Edit**
5. Bật cross-zone load balancing
6. Lưu ý: Điều này có thể bao gồm phí khu vực cho NLB của bạn

### Cấu Hình Gateway Load Balancer

1. Điều hướng đến GWLB của bạn trong AWS Console
2. Vào **Attributes**
3. Cross-zone load balancing sẽ hiển thị là **OFF** mặc định
4. Nhấp **Edit**
5. Bật cross-zone load balancing
6. Lưu ý: Điều này sẽ phát sinh phí data transfer

### Cấu Hình Application Load Balancer

1. Điều hướng đến ALB của bạn trong AWS Console
2. Vào **Attributes**
3. Cross-zone load balancing **BẬT** mặc định
4. Để điều khiển chi tiết hơn, điều hướng đến **Target Group** của bạn
5. Vào phần **Attributes** của target group
6. Nhấp **Edit**
7. Cấu hình cross-zone load balancing với các tùy chọn:
   - Kế thừa cài đặt từ thuộc tính load balancer (bật mặc định)
   - Bắt buộc bật
   - Bắt buộc tắt cho target group cụ thể

## Các Trường Hợp Sử Dụng

### Khi Nào Nên Bật Cross-Zone Load Balancing
- Bạn có số lượng instances không đồng đều giữa các AZ
- Bạn muốn phân phối traffic đều bất kể AZ nào
- Bạn ưu tiên cân bằng tải hơn chi phí data transfer (cho NLB/GWLB)

### Khi Nào Nên Tắt Cross-Zone Load Balancing
- Bạn muốn giảm thiểu chi phí data transfer giữa các AZ
- Bạn có instances phân phối đều trên các AZ
- Kiến trúc của bạn yêu cầu traffic ở lại trong cùng AZ
- Bạn muốn kiểm tra tính độc lập của AZ

## Những Điểm Chính

1. **Cross-zone load balancing phân phối traffic đến tất cả instances trong tất cả các AZ**
2. **Không có nó, traffic chỉ đi đến instances trong cùng AZ với load balancer node**
3. **Các loại load balancer khác nhau có cài đặt mặc định và chi phí khác nhau**
4. **ALB có tính năng này bật mặc định và không tính phí thêm**
5. **NLB và GWLB có nó tắt mặc định và tính phí data transfer khi bật**
6. **Không có câu trả lời đúng hay sai - tùy thuộc vào trường hợp sử dụng của bạn**

## Dọn Dẹp

Sau khi hoàn thành thực hành, nhớ xóa các load balancers để tránh phí không cần thiết.

## Kết Luận

Cross-zone load balancing là một tính năng linh hoạt cho phép bạn kiểm soát cách traffic được phân phối trên cơ sở hạ tầng của bạn. Hiểu rõ hành vi, chi phí và các tùy chọn cấu hình cho từng loại load balancer sẽ giúp bạn đưa ra lựa chọn đúng đắn cho trường hợp sử dụng cụ thể của mình.



================================================================================
FILE: 61-aws-ssl-tls-certificates-and-sni.md
================================================================================

# Chứng Chỉ SSL/TLS và Server Name Indication (SNI) trên AWS

## Giới Thiệu

Hướng dẫn này cung cấp tổng quan về chứng chỉ SSL/TLS và cách tích hợp chúng với AWS Load Balancers, bao gồm khái niệm quan trọng về Server Name Indication (SNI).

## Tổng Quan về Chứng Chỉ SSL/TLS

### Chứng Chỉ SSL/TLS là gì?

Chứng chỉ SSL cho phép lưu lượng giữa khách hàng và load balancer của bạn được mã hóa trong khi truyền tải. Đây được gọi là **mã hóa trong quá trình truyền tải** (in-flight encryption), nghĩa là dữ liệu khi đi qua mạng sẽ được mã hóa và chỉ có thể được giải mã bởi người gửi và người nhận.

### SSL và TLS

- **SSL** (Secure Sockets Layer): Giao thức ban đầu được sử dụng để mã hóa kết nối truyền tải
- **TLS** (Transport Layer Security): Phiên bản mới hơn của SSL

**Lưu ý:** Mặc dù chứng chỉ TLS là loại chứng chỉ chủ yếu được sử dụng ngày nay, mọi người thường vẫn gọi chúng là "chứng chỉ SSL" để đơn giản hóa và vì lý do lịch sử.

### Certificate Authorities (CAs) - Tổ Chức Cấp Chứng Chỉ

Chứng chỉ SSL công khai được cấp bởi các Certificate Authorities, bao gồm:
- Comodo
- Symantec
- GoDaddy
- GlobalSign
- Digicert
- Let's Encrypt

### Thuộc Tính của Chứng Chỉ

- Chứng chỉ SSL có ngày hết hạn và phải được gia hạn thường xuyên để đảm bảo tính xác thực
- Khi bạn truy cập một trang web có mã hóa SSL/TLS đúng cách, bạn sẽ thấy biểu tượng khóa trên trình duyệt
- Nếu không có mã hóa, trình duyệt sẽ hiển thị cảnh báo khuyên bạn không nên nhập thông tin nhạy cảm

## SSL/TLS với AWS Load Balancers

### Cách Hoạt Động

1. **Kết Nối từ Client**: Người dùng kết nối qua HTTPS (được mã hóa bằng chứng chỉ SSL) thông qua internet công cộng đến load balancer của bạn
2. **SSL Certificate Termination**: Load balancer xử lý việc kết thúc chứng chỉ SSL
3. **Giao Tiếp Backend**: Load balancer có thể giao tiếp với các EC2 instances sử dụng HTTP (không mã hóa) qua VPC, đây là mạng lưu lượng riêng tư

### Chứng Chỉ X.509

Load balancer tải chứng chỉ X.509 (chứng chỉ server SSL/TLS). Bạn có thể:
- Quản lý chứng chỉ SSL trong AWS bằng **ACM** (AWS Certificate Manager)
- Tải lên chứng chỉ của riêng bạn vào ACM

### Cấu Hình HTTPS Listener

Khi thiết lập HTTPS listener:
- Bạn phải chỉ định một **chứng chỉ mặc định**
- Bạn có thể thêm danh sách chứng chỉ tùy chọn để hỗ trợ nhiều tên miền
- Các client có thể sử dụng **SNI** (Server Name Indication) để chỉ định hostname mà họ muốn truy cập
- Bạn có thể đặt các chính sách bảo mật cụ thể để hỗ trợ các phiên bản SSL/TLS cũ hơn (legacy clients)

## Server Name Indication (SNI)

### SNI Giải Quyết Vấn Đề Gì?

SNI giải quyết vấn đề tải nhiều chứng chỉ SSL lên một web server để phục vụ nhiều trang web.

### SNI Hoạt Động Như Thế Nào?

1. SNI là một giao thức mới hơn yêu cầu client chỉ định hostname của server đích trong quá trình bắt tay SSL ban đầu
2. Client nói rằng, "Tôi muốn kết nối đến trang web này"
3. Server biết chứng chỉ nào cần tải dựa trên thông tin này

### Khả Năng Tương Thích của SNI

**Được Hỗ Trợ:**
- Application Load Balancer (ALB)
- Network Load Balancer (NLB)
- CloudFront

**Không Được Hỗ Trợ:**
- Classic Load Balancer (thế hệ cũ)

**Điểm Chính:** Khi bạn thấy nhiều chứng chỉ SSL trên load balancer, hãy nghĩ đến ALB hoặc NLB.

### Ví Dụ Sơ Đồ SNI

Xem xét một ALB với hai target groups:
- **www.mycorp.com**
- **Domain1.example.com**

Quy trình:
1. ALB có hai chứng chỉ SSL (một cho mỗi tên miền)
2. Client kết nối đến ALB và yêu cầu "www.mycorp.com" (sử dụng SNI)
3. ALB xác định hostname được yêu cầu và sử dụng chứng chỉ SSL đúng
4. ALB mã hóa lưu lượng và định tuyến đến target group chính xác (mycorp.com)
5. Nếu một client khác yêu cầu "Domain1.example.com", ALB sử dụng chứng chỉ thích hợp và định tuyến đến target group đó

Sử dụng SNI, bạn có thể có nhiều target groups cho các trang web khác nhau sử dụng các chứng chỉ SSL khác nhau.

## Hỗ Trợ Chứng Chỉ SSL theo Loại Load Balancer

### Classic Load Balancer (CLB)
- **Hỗ trợ:** Chỉ một chứng chỉ SSL
- **Nhiều Hostnames:** Sử dụng nhiều Classic Load Balancers

### Application Load Balancer (ALB v2)
- **Hỗ trợ:** Nhiều listeners với nhiều chứng chỉ SSL
- **Công nghệ:** Sử dụng SNI để hoạt động

### Network Load Balancer (NLB)
- **Hỗ trợ:** Nhiều listeners với nhiều chứng chỉ SSL
- **Công nghệ:** Sử dụng SNI để hoạt động

## Tóm Tắt

- Chứng chỉ SSL/TLS mã hóa lưu lượng giữa clients và load balancers
- Các load balancers AWS hiện đại (ALB và NLB) hỗ trợ nhiều chứng chỉ SSL thông qua SNI
- SNI cho phép một load balancer phục vụ nhiều trang web với các chứng chỉ SSL khác nhau
- Luôn quản lý và gia hạn chứng chỉ của bạn thường xuyên để đảm bảo bảo mật
- Sử dụng AWS Certificate Manager (ACM) để đơn giản hóa việc quản lý chứng chỉ



================================================================================
FILE: 62-aws-ssl-tls-certificates-on-load-balancers.md
================================================================================

# AWS SSL/TLS Certificates trên Load Balancers

## Tổng quan

Hướng dẫn này giải thích cách kích hoạt chứng chỉ SSL/TLS trên AWS Application Load Balancer (ALB) và Network Load Balancer (NLB) để bảo mật ứng dụng của bạn với giao thức HTTPS/TLS.

## Kích hoạt Chứng chỉ SSL trên Application Load Balancer (ALB)

### Thêm HTTPS Listener

Để kích hoạt chứng chỉ SSL trên ALB, bạn cần thêm một listener với cấu hình sau:

1. **Thêm listener mới**
   - Giao thức: `HTTPS`
   - Cổng: `443` (cổng HTTPS mặc định)

2. **Cấu hình định tuyến**
   - Khi client sử dụng cổng 443 với giao thức HTTPS
   - Chuyển tiếp lưu lượng đến target group cụ thể

### Cài đặt Secure Listener

#### Chính sách Bảo mật SSL
- Thiết lập chính sách bảo mật SSL để xác định cách thương lượng chứng chỉ
- Cấu hình dựa trên yêu cầu tương thích với các phiên bản SSL/TLS cũ hơn
- Cài đặt mặc định phù hợp với hầu hết các trường hợp sử dụng

#### Các tùy chọn vị trí Chứng chỉ

Bạn có ba tùy chọn để cung cấp chứng chỉ SSL/TLS:

1. **AWS Certificate Manager (ACM)** - Được khuyến nghị
   - Quản lý chứng chỉ tập trung
   - Gia hạn tự động
   - Chứng chỉ SSL/TLS miễn phí cho tài nguyên AWS

2. **IAM Certificate Store**
   - Không được khuyến nghị làm phương pháp chính
   - Tùy chọn cũ để lưu trữ chứng chỉ

3. **Import Chứng chỉ Thủ công**
   - Dán private key
   - Dán certificate body
   - Dán certificate chain (nếu cần)
   - Chứng chỉ sẽ được import trực tiếp vào ACM

## Kích hoạt Chứng chỉ TLS trên Network Load Balancer (NLB)

### Thêm TLS Listener

Quy trình cho NLB tương tự như ALB:

1. **Điều hướng đến NLB listeners**
   - Thêm listener mới
   - Giao thức: `TLS`

2. **Cấu hình định tuyến**
   - Chuyển tiếp đến target group

3. **Chính sách Bảo mật**
   - Chọn chính sách bảo mật phù hợp
   - Các tùy chọn tương tự như ALB

4. **Cấu hình Chứng chỉ**
   - Chọn nguồn chứng chỉ: ACM, IAM, hoặc Import
   - Cấu hình Application Layer Protocol Negotiation (ALPN)
   - ALPN là cài đặt TLS nâng cao cho thương lượng giao thức

## Sự khác biệt chính

| Tính năng | ALB | NLB |
|-----------|-----|-----|
| Giao thức | HTTPS | TLS |
| Cổng mặc định | 443 | 443 |
| Hỗ trợ ALPN | Không | Có |
| Lớp | Layer 7 | Layer 4 |

## Best Practices (Thực hành tốt nhất)

1. **Sử dụng AWS Certificate Manager (ACM)**
   - Đơn giản hóa quản lý chứng chỉ
   - Gia hạn tự động
   - Không tốn thêm chi phí

2. **Chọn chính sách bảo mật phù hợp**
   - Cân bằng giữa bảo mật và khả năng tương thích
   - Thường xuyên cập nhật lên các phiên bản TLS mới hơn

3. **Lên kế hoạch cho việc xoay vòng chứng chỉ**
   - Thiết lập cảnh báo trước khi hết hạn
   - Sử dụng ACM để gia hạn tự động

## Tóm tắt

Chứng chỉ SSL/TLS trên AWS load balancers cung cấp kết nối mã hóa giữa client và ứng dụng của bạn. Cả ALB và NLB đều hỗ trợ cấu hình chứng chỉ thông qua ACM, IAM, hoặc import thủ công, với ACM là phương pháp được khuyến nghị cho việc quản lý dễ dàng và gia hạn tự động.



================================================================================
FILE: 63-aws-elb-connection-draining-deregistration-delay.md
================================================================================

# AWS ELB Connection Draining / Deregistration Delay

## Tổng quan

Connection Draining là một tính năng quan trọng của AWS Elastic Load Balancers mà bạn cần hiểu cho kỳ thi và ứng dụng thực tế. Tính năng này có tên gọi khác nhau tùy theo loại load balancer:

- **Classic Load Balancer (CLB)**: Được gọi là **Connection Draining**
- **Application Load Balancer (ALB) / Network Load Balancer (NLB)**: Được gọi là **Deregistration Delay**

## Connection Draining là gì?

Connection Draining cho phép các EC2 instance có thời gian để hoàn thành các request đang xử lý hoặc các request đang hoạt động trong khi instance đang được hủy đăng ký hoặc được đánh dấu là không khỏe mạnh. Điều này đảm bảo việc tắt máy một cách êm ái mà không đột ngột ngắt kết nối người dùng đang hoạt động.

### Hành vi chính

- Khi một instance vào chế độ draining, ELB **ngừng gửi request mới** đến instance đó
- Các kết nối hiện có được cho thời gian để hoàn thành dựa trên thời gian draining
- Instance vẫn hoạt động chỉ để hoàn thành các request hiện có

## Cách hoạt động

### Luồng kiến trúc

1. **Ba EC2 Instance** được đăng ký với ELB
2. **Một instance** được đặt vào chế độ draining (đang hủy đăng ký hoặc được đánh dấu không khỏe mạnh)
3. **Người dùng hiện có** đang kết nối với instance đang draining được cho thời gian (thời gian draining) để hoàn thành request
4. **Người dùng mới** kết nối đến ELB được tự động chuyển hướng chỉ đến các instance khỏe mạnh
5. Khi tất cả kết nối hoàn thành, instance draining được hủy đăng ký hoàn toàn

### Sơ đồ minh họa

```
┌─────────────────────────────────────────────┐
│         Elastic Load Balancer (ELB)         │
└─────────────────────────────────────────────┘
              │
              ├───────────────┬───────────────┐
              ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │   EC2    │    │   EC2    │    │   EC2    │
        │ Instance │    │ Instance │    │ Instance │
        │    #1    │    │    #2    │    │    #3    │
        │          │    │          │    │          │
        │ DRAINING │    │  ACTIVE  │    │  ACTIVE  │
        └──────────┘    └──────────┘    └──────────┘
             ▲
             │
    Kết nối hiện có
    hoàn thành êm ái
    
    Kết nối mới → Chuyển hướng đến Instance #2 hoặc #3
```

## Tham số cấu hình

### Cài đặt thời gian Draining

- **Phạm vi**: 1 đến 3,600 giây (1 giây đến 1 giờ)
- **Mặc định**: 300 giây (5 phút)
- **Vô hiệu hóa**: Đặt thành 0 để vô hiệu hóa hoàn toàn connection draining

### Chọn giá trị phù hợp

#### Request ngắn hạn
- **Trường hợp sử dụng**: Request hoàn thành trong vòng chưa đến 1 giây
- **Cài đặt khuyến nghị**: 30 giây
- **Lợi ích**: Instance có thể được drain và đưa offline nhanh chóng
- **Ví dụ**: API call đơn giản, health check, nội dung tĩnh

#### Request dài hạn
- **Trường hợp sử dụng**: Upload, xử lý file, các thao tác chạy lâu
- **Cài đặt khuyến nghị**: Giá trị cao (ví dụ: 1,800-3,600 giây)
- **Đánh đổi**: Instance mất nhiều thời gian hơn để hủy đăng ký hoàn toàn
- **Ví dụ**: Upload file, xử lý video, các thao tác batch

## Thực hành tốt nhất

1. **Khớp với thời gian Request**: Đặt thời gian draining dựa trên thời gian hoàn thành request điển hình của bạn
2. **Cân bằng tính khả dụng**: Xem xét sự đánh đổi giữa tắt máy êm ái và tốc độ thay thế instance
3. **Giám sát Metrics**: Theo dõi số lượng kết nối và thời gian hoàn thành request
4. **Kiểm tra kịch bản**: Xác thực hành vi draining trong các sự kiện triển khai và mở rộng

## Những điểm quan trọng cần lưu ý

- Đặt giá trị thành **zero sẽ vô hiệu hóa draining**, gây ra việc ngắt kết nối ngay lập tức
- **Giá trị thấp** cho phép thay thế instance nhanh hơn nhưng có thể ngắt một số request
- **Giá trị cao** đảm bảo tất cả request hoàn thành nhưng trì hoãn việc loại bỏ instance
- Instance đang draining sẽ **không nhận request mới** từ load balancer

## Các trường hợp sử dụng

- **Sự kiện Auto Scaling**: Chấm dứt instance một cách êm ái trong các thao tác scale-in
- **Thay thế Instance**: Thay thế an toàn các instance không khỏe mạnh mà không làm mất kết nối
- **Cập nhật triển khai**: Đảm bảo triển khai không downtime bằng cách drain trước khi cập nhật
- **Cửa sổ bảo trì**: Chuẩn bị instance cho bảo trì mà không ảnh hưởng đến người dùng

## Tóm tắt

Connection Draining (hoặc Deregistration Delay) là một tính năng quan trọng để duy trì tính khả dụng cao và trải nghiệm người dùng trong các sự kiện vòng đời instance. Bằng cách cấu hình đúng thời gian draining dựa trên mẫu request của ứng dụng, bạn có thể đảm bảo việc tắt máy êm ái và giảm thiểu gián đoạn dịch vụ.

---

**Những điểm chính cần nhớ:**
- Tên gọi khác nhau cho CLB so với ALB/NLB
- Cho phép các request đang xử lý hoàn thành
- Có thể cấu hình từ 1-3,600 giây (mặc định: 300 giây)
- Chọn giá trị dựa trên thời lượng request
- Cần thiết cho triển khai không downtime



================================================================================
FILE: 64-aws-auto-scaling-groups-overview.md
================================================================================

# Tổng Quan về AWS Auto Scaling Groups (ASG)

## Giới Thiệu

Khi triển khai một website hoặc ứng dụng, tải có thể thay đổi theo thời gian khi có nhiều người dùng truy cập website của bạn hơn. Trong AWS, chúng ta có thể tạo và xóa server rất nhanh chóng bằng cách sử dụng API call tạo EC2 instance. Để tự động hóa quy trình này, chúng ta có thể sử dụng Auto Scaling Groups (ASG).

## Auto Scaling Group là gì?

Auto Scaling Group là một dịch vụ AWS tự động điều chỉnh số lượng EC2 instances trong ứng dụng của bạn dựa trên nhu cầu.

### Mục Tiêu Chính của ASG

- **Scale Out (Mở rộng)**: Thêm EC2 instances để đáp ứng tải tăng cao
- **Scale In (Thu hẹp)**: Xóa bớt EC2 instances khi tải giảm
- Kích thước ASG của bạn thay đổi theo thời gian dựa trên nhu cầu

## Các Tính Năng Chính

### 1. Quản Lý Dung Lượng

Bạn có thể định nghĩa các tham số để đảm bảo có:
- Số lượng **tối thiểu** EC2 instances chạy mọi lúc
- Số lượng **tối đa** EC2 instances có thể chạy
- **Dung lượng mong muốn** để đạt hiệu suất tối ưu

### 2. Tích Hợp với Load Balancer

ASG có khả năng tích hợp mạnh mẽ với load balancer:
- Bất kỳ EC2 instances nào trong ASG đều tự động được liên kết với load balancer
- Traffic được phân phối đều trên tất cả các instances
- Cung cấp trải nghiệm người dùng liền mạch

### 3. Giám Sát Sức Khỏe và Tự Động Phục Hồi

- Nếu một instance được coi là không khỏe mạnh, nó sẽ tự động bị chấm dứt
- Một EC2 instance mới được tạo để thay thế instance không khỏe mạnh
- Đảm bảo tính sẵn sàng cao cho ứng dụng của bạn

### 4. Tiết Kiệm Chi Phí

- Bản thân Auto Scaling Groups là **miễn phí**
- Bạn chỉ trả tiền cho các tài nguyên được tạo bên dưới (EC2 instances)

## Cách Hoạt Động của ASG

### Cấu Hình Dung Lượng

1. **Dung Lượng Tối Thiểu**: Số lượng instances tối thiểu bạn muốn trong ASG (ví dụ: 2)
2. **Dung Lượng Mong Muốn**: Số lượng instances bạn muốn chạy (ví dụ: 4)
3. **Dung Lượng Tối Đa**: Số lượng instances tối đa được phép (ví dụ: 7)

Khi bạn điều chỉnh dung lượng mong muốn lên cao hơn (nhưng vẫn nhỏ hơn dung lượng tối đa), ASG của bạn có thể mở rộng bằng cách thêm nhiều EC2 instances hơn.

### Tích Hợp với Load Balancers

Khi bạn có các instances được đăng ký trong ASG:
- Elastic Load Balancer (ELB) phân phối traffic đến tất cả các instances
- Người dùng có thể truy cập website được cân bằng tải
- ELB thực hiện kiểm tra sức khỏe trên các EC2 instances
- Kết quả kiểm tra sức khỏe được chuyển đến ASG
- Các instances không khỏe mạnh tự động bị chấm dứt và thay thế

Sự kết hợp giữa load balancer và auto scaling group này cực kỳ mạnh mẽ để duy trì tính khả dụng và hiệu suất của ứng dụng.

## Tạo Auto Scaling Group

### Launch Template (Mẫu Khởi Chạy)

Để tạo một ASG, bạn cần một **launch template** (lưu ý: launch configurations đã lỗi thời nhưng hoạt động tương tự).

Launch template chứa thông tin về cách khởi chạy EC2 instances trong ASG của bạn:

- **AMI** (Amazon Machine Image)
- **Loại Instance**
- **EC2 User Data**
- **EBS Volumes**
- **Security Groups**
- **SSH Key Pair**
- **IAM Roles** cho EC2 instances
- **Thông Tin Network và Subnet**
- **Thông Tin Load Balancer**

Các tham số này tương tự như những tham số được chỉ định khi tạo một EC2 instance độc lập.

### Các Tham Số ASG Bổ Sung

- Kích thước tối thiểu
- Kích thước tối đa
- Dung lượng ban đầu
- Chính sách mở rộng (scaling policies)

## Auto Scaling với CloudWatch

### Tích Hợp CloudWatch Alarm

Auto Scaling Groups có thể thu hẹp và mở rộng dựa trên CloudWatch alarms. Điều này cho phép thực sự tự động hóa việc mở rộng cơ sở hạ tầng của bạn.

### Cách Hoạt Động

1. Bạn thiết lập CloudWatch alarms dựa trên các metrics (ví dụ: mức sử dụng CPU trung bình)
2. Khi ngưỡng metric bị vượt qua, alarm được kích hoạt
3. Alarm kích hoạt một hoạt động mở rộng trong ASG của bạn
4. Instances được thêm hoặc xóa tự động

### Ví Dụ Tình Huống

- ASG của bạn có 3 EC2 instances đang chạy
- Mức sử dụng CPU trung bình trên ASG tăng vượt ngưỡng
- CloudWatch alarm được kích hoạt
- Chính sách scale-out được kích hoạt
- Các EC2 instances bổ sung được khởi chạy tự động

### Chính Sách Mở Rộng

- **Chính Sách Scale Out**: Tăng số lượng instances khi nhu cầu cao
- **Chính Sách Scale In**: Giảm số lượng instances khi nhu cầu thấp

Việc tự động mở rộng kết hợp với alarms này chính là lý do tại sao nó được gọi là "Auto" Scaling Group.

## Tóm Tắt

Auto Scaling Groups cung cấp:
- Tự động điều chỉnh dung lượng dựa trên nhu cầu
- Tối ưu hóa chi phí bằng cách chỉ chạy các instances cần thiết
- Tính sẵn sàng cao thông qua giám sát sức khỏe và tự động phục hồi
- Tích hợp liền mạch với load balancers
- Tự động hóa thông qua CloudWatch alarms và chính sách mở rộng

Tất cả các tính năng này cùng nhau tạo thành một giải pháp mạnh mẽ để chạy các ứng dụng có khả năng mở rộng và sẵn sàng cao trong AWS.

---

*Hướng dẫn này cung cấp tổng quan về AWS Auto Scaling Groups và sự tích hợp của chúng với các dịch vụ AWS khác như EC2, ELB và CloudWatch.*



================================================================================
FILE: 65-aws-auto-scaling-groups-hands-on-tutorial.md
================================================================================

# AWS Auto Scaling Groups - Hướng Dẫn Thực Hành

## Giới Thiệu

Hướng dẫn thực hành này sẽ giúp bạn tạo và quản lý AWS Auto Scaling Groups (ASG). Bạn sẽ học cách tạo launch templates, cấu hình các thiết lập ASG, tích hợp với Application Load Balancers, và trải nghiệm tính năng auto scaling trong thực tế.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu hướng dẫn này:
- Terminate (chấm dứt) tất cả EC2 instances đang chạy để bắt đầu từ đầu
- Đảm bảo bạn có không có instance nào đang chạy trong EC2

## Bước 1: Tạo Auto Scaling Group

1. Điều hướng đến **Auto Scaling Groups** ở menu bên trái
2. Nhấp **Create Auto Scaling Group**
3. Đặt tên cho ASG của bạn: `Demo ASG`

## Bước 2: Tạo Launch Template

Vì chúng ta cần tham chiếu đến một launch template, hãy tạo một cái:

### Cấu Hình Cơ Bản

1. Nhấp **Create a launch template**
2. **Tên template**: `my demo template`
3. **Mô tả**: `templates`

### Cấu Hình Instance

1. **Amazon Machine Image (AMI)**:
   - Vào Quick Start
   - Chọn **Amazon Linux**
   - Chọn **Amazon Linux 2** (phiên bản X86)
   - Sử dụng AMI đủ điều kiện free tier

2. **Instance Type**:
   - Chọn **t2.micro** (đủ điều kiện free tier)

3. **Key Pair**:
   - Bao gồm key pair **EC2 tutorial**

4. **Security Group**:
   - Chọn một security group đã tồn tại (ví dụ: `launch-wizard-1`)
   - Lưu ý: Subnets không được bao gồm trong launch templates

5. **Storage (Lưu trữ)**:
   - Mặc định: 8 GB gp2 volume

### Chi Tiết Nâng Cao - User Data

1. Cuộn xuống **Advanced Details**
2. Tìm phần **User Data**
3. Nhập script user data của bạn (script này sẽ tạo web server trên mỗi EC2 instance)

```bash
#!/bin/bash
# Script user data của bạn ở đây
# Script này sẽ bootstrap một web server trên mỗi instance
```

4. Nhấp **Create launch template**

## Bước 3: Cấu Hình Auto Scaling Group

### Chọn Launch Template

1. Làm mới danh sách template
2. Chọn `my demo template` (version 1)
3. Xem lại tóm tắt
4. Nhấp **Next**

### Tùy Chọn Khởi Chạy Instance

1. **Instance Type Requirements**:
   - Giữ nguyên t2.micro mặc định từ launch template
   - Reset về launch template nếu cần

2. **Cấu Hình Network**:
   - Chọn VPC của bạn
   - Chọn nhiều Availability Zones
   - **AZ Distribution**: Balanced best effort (đảm bảo instances được phân bổ đều trên 3 AZs)

### Tích Hợp Load Balancer

1. **Gắn vào Load Balancer**:
   - Chọn "Attach to an existing load balancer target group"
   - Chọn `demo tg alb` (target group đã tạo trước đó)
   - Điều này gắn tất cả instances của ASG vào load balancer

2. Bỏ qua VPC Lattice integration và zonal shift settings

### Health Checks (Kiểm Tra Sức Khỏe)

Bật cả hai:
- **EC2 health checks**
- **Load balancer health checks**

Điều này cho phép ALB kiểm tra sức khỏe của instance, và ASG có thể tự động terminate các instances không khỏe mạnh.

## Bước 4: Cấu Hình Kích Thước Group và Scaling

1. **Desired capacity** (Dung lượng mong muốn): 1
2. **Minimum capacity** (Dung lượng tối thiểu): 1
3. **Maximum capacity** (Dung lượng tối đa): 1

Tạm thời, chúng ta sẽ để automatic scaling ở chế độ tắt để khám phá nó sau.

## Bước 5: Cài Đặt Bổ Sung

1. **Instance maintenance policy**: No policy
2. **Additional capacity settings**: Sử dụng mặc định
3. Bỏ qua notifications và tags
4. Xem lại tất cả các tùy chọn
5. Nhấp **Create Auto Scaling Group**

## Bước 6: Giám Sát Hoạt Động ASG

### Lịch Sử Hoạt Động (Activity History)

1. Nhấp vào Auto Scaling Group của bạn
2. Vào tab **Activity**
3. Làm mới để xem lịch sử hoạt động
4. Bạn sẽ thấy: "Launching a new instance" vì dung lượng là 0 và desired là 1

### Quản Lý Instance

1. Vào tab **Instance Management**
2. Xác minh rằng một EC2 instance đã được tạo bởi ASG
3. Điều hướng đến **EC2 Instances** để xem instance đang chạy

### Đăng Ký Target Group

1. Vào **Target Groups** (menu bên trái)
2. Tìm target group của bạn
3. Vào tab **Targets**
4. Ban đầu hiển thị **unhealthy** (instance vẫn đang bootstrapping)
5. Sau khi bootstrapping hoàn tất, trạng thái chuyển sang **healthy**

### Kiểm Tra Load Balancer

1. Điều hướng đến Application Load Balancer của bạn
2. Sao chép DNS name và mở trong trình duyệt
3. Bạn nên thấy phản hồi "Hello World"
4. Điều này xác nhận toàn bộ cài đặt đang hoạt động:
   - Instance được tạo bởi ASG ✓
   - Đã đăng ký trong target group ✓
   - Load balancer đang định tuyến traffic ✓

## Khắc Phục Sự Cố Instance Không Khỏe Mạnh

Nếu instance của bạn không bao giờ trở nên healthy:

**Vấn Đề Thường Gặp**:
1. **Security Group cấu hình sai**: Kiểm tra inbound/outbound rules
2. **Vấn đề EC2 User Data script**: Xác minh cú pháp và logic của script

ASG sẽ tự động terminate các instances không khỏe mạnh và tạo instances mới. Kiểm tra Activity History để xem các sự kiện này.

## Bước 7: Trải Nghiệm Scale Out (Mở Rộng)

### Tăng Dung Lượng

1. **Edit Auto Scaling Group size**
2. Đặt **Desired capacity**: 2
3. Đặt **Maximum capacity**: 2
4. Nhấp **Update**

### Giám Sát Hoạt Động Scaling

1. Vào **Activity History**
2. Làm mới để xem hoạt động mới
3. Bạn sẽ thấy: "Launching a new EC2 instance" vì desired capacity thay đổi từ 1 lên 2
4. Instance thứ hai sẽ được tạo và đăng ký vào target group

### Xác Minh Phân Phối Tải

1. Đợi instance mới trở nên healthy
2. Điều hướng đến DNS name của ALB
3. Làm mới nhiều lần
4. Bạn sẽ thấy hai địa chỉ IP khác nhau luân phiên
5. Điều này xác nhận load balancing trên cả hai instances

## Bước 8: Trải Nghiệm Scale In (Thu Hẹp)

### Giảm Dung Lượng

1. **Edit Auto Scaling Group size**
2. Đặt **Desired capacity**: 1
3. Nhấp **Update**

### Giám Sát Việc Terminate

1. Vào **Activity History**
2. Bạn sẽ thấy thông báo: "Terminating instance"
3. ASG sẽ:
   - Chọn một trong hai instances
   - Terminate nó
   - Hủy đăng ký khỏi target group
4. Bạn quay lại với một EC2 instance

## Tóm Tắt

Trong hướng dẫn thực hành này, bạn đã học:

- ✓ Cách tạo và cấu hình Launch Templates
- ✓ Cách tạo Auto Scaling Groups
- ✓ Cách tích hợp ASG với Application Load Balancers
- ✓ Cách cấu hình health checks
- ✓ Cách scale out thủ công (tăng dung lượng)
- ✓ Cách scale in thủ công (giảm dung lượng)
- ✓ Cách ASG tự động quản lý vòng đời của instance

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá **automatic scaling** - nơi ASG tự động điều chỉnh dung lượng dựa trên nhu cầu mà không cần can thiệp thủ công.

---

**Những Điểm Chính Cần Nhớ**:
- Auto Scaling Groups cung cấp tính khả dụng cao và khả năng chịu lỗi
- Launch Templates định nghĩa cách instances nên được cấu hình
- Tích hợp với ALB cho phép phân phối traffic một cách liền mạch
- ASG tự động thay thế các instances không khỏe mạnh
- Manual scaling thể hiện sức mạnh của ASG trước khi tự động hóa nó



================================================================================
FILE: 66-aws-auto-scaling-policies-and-metrics.md
================================================================================

# Chính Sách và Chỉ Số Auto Scaling trong AWS

## Tổng Quan

Tài liệu này trình bày các chính sách mở rộng khác nhau có sẵn cho AWS Auto Scaling Groups (ASG), cùng với các chỉ số được khuyến nghị và các phương pháp hay nhất.

## Các Chính Sách Scaling

AWS Auto Scaling Groups hỗ trợ nhiều loại chính sách scaling để giúp quản lý cơ sở hạ tầng của bạn một cách tự động.

### 1. Dynamic Scaling (Mở Rộng Động)

Dynamic scaling điều chỉnh dung lượng dựa trên các chỉ số và điều kiện thời gian thực.

#### Target Tracking Scaling (Theo Dõi Mục Tiêu)

- **Mô tả**: Chính sách scaling đơn giản nhất để thiết lập
- **Cách hoạt động**: 
  - Định nghĩa một chỉ số cho ASG của bạn (ví dụ: mức sử dụng CPU)
  - Đặt giá trị mục tiêu (ví dụ: 40%)
  - ASG tự động mở rộng hoặc thu hẹp để duy trì chỉ số xung quanh giá trị mục tiêu

#### Simple or Step Scaling (Mở Rộng Đơn Giản hoặc Theo Bước)

- **Mô tả**: Mở rộng dựa trên các cảnh báo CloudWatch
- **Cách hoạt động**:
  - Định nghĩa các cảnh báo CloudWatch kích hoạt khi cần thay đổi dung lượng
  - Cảnh báo có thể kích hoạt để thêm hoặc xóa các đơn vị dung lượng khỏi ASG
  - Cung cấp kiểm soát chi tiết hơn đối với các hành động mở rộng

### 2. Scheduled Scaling (Mở Rộng Theo Lịch)

- **Mô tả**: Dự đoán mở rộng dựa trên các mẫu sử dụng đã biết
- **Trường hợp sử dụng**: Khi bạn có các mẫu lưu lượng có thể dự đoán
- **Ví dụ**: Tăng dung lượng tối thiểu lên 10 vào mỗi thứ Sáu lúc 5:00 chiều khi người dùng mới thường xuất hiện

### 3. Predictive Scaling (Mở Rộng Dự Đoán)

- **Mô tả**: Sử dụng machine learning để dự báo tải và lên lịch các hành động mở rộng
- **Cách hoạt động**:
  - Liên tục phân tích dữ liệu tải lịch sử
  - Tạo dự báo dựa trên các mẫu
  - Lên lịch các hành động mở rộng trước
- **Tốt nhất cho**: Các ứng dụng có mẫu tuần hoàn hoặc lặp lại

## Các Chỉ Số Scaling Được Khuyến Nghị

Chọn đúng chỉ số là rất quan trọng cho việc auto scaling hiệu quả. Dưới đây là các chỉ số thường được sử dụng nhất:

### 1. CPU Utilization (Mức Sử Dụng CPU)

- **Tại sao hiệu quả**: Hầu hết các yêu cầu đều liên quan đến tính toán sử dụng CPU
- **Chỉ báo**: Mức sử dụng CPU trung bình cao hơn trên các instance có nghĩa là chúng đang được sử dụng nhiều hơn
- **Tốt nhất cho**: Các ứng dụng tính toán cao

### 2. RequestCountPerTarget (Số Lượng Yêu Cầu Trên Mỗi Target)

- **Mô tả**: Chỉ số dành riêng cho ứng dụng dựa trên các yêu cầu load balancer
- **Cách sử dụng**: 
  - Xác định số lượng yêu cầu tối ưu cho mỗi EC2 instance thông qua kiểm thử
  - Ví dụ: Đặt mục tiêu là 1.000 yêu cầu cho mỗi instance
- **Trường hợp sử dụng**: 
  - Auto Scaling Group với 3 EC2 instances
  - ALB phân phối yêu cầu trên tất cả các instances
  - Nếu mỗi instance trung bình có 3 yêu cầu đang chờ xử lý, giá trị chỉ số là 3

### 3. Network In/Out (Mạng Vào/Ra)

- **Tốt nhất cho**: Các ứng dụng bị giới hạn bởi mạng
- **Trường hợp sử dụng**: Các ứng dụng có nhiều tải lên/tải xuống
- **Cách hoạt động**: Mở rộng dựa trên các chỉ số mạng vào hoặc ra trung bình
- **Lợi ích**: Ngăn mạng trở thành điểm nghẽn cổ chai

### 4. Custom Metrics (Chỉ Số Tùy Chỉnh)

- **Mô tả**: Các chỉ số dành riêng cho ứng dụng được đẩy lên CloudWatch
- **Tính linh hoạt**: Định nghĩa bất kỳ chỉ số nào liên quan đến ứng dụng của bạn
- **Tốt nhất cho**: Các ứng dụng chuyên biệt có yêu cầu mở rộng độc đáo

## Thời Gian Cooldown của Scaling

### Cooldown là gì?

Sau một hoạt động mở rộng (thêm hoặc xóa instances), ASG sẽ vào thời gian cooldown.

### Chi Tiết Chính

- **Thời lượng mặc định**: 5 phút (300 giây)
- **Mục đích**: 
  - Cho phép các chỉ số ổn định
  - Để các instance mới có hiệu lực
  - Quan sát các giá trị chỉ số mới
- **Hành vi**: Trong thời gian cooldown, ASG sẽ không khởi chạy hoặc chấm dứt các instances bổ sung

### Quy Trình Quyết Định

Khi một hành động mở rộng được kích hoạt:
1. Có cooldown mặc định đang có hiệu lực không?
   - **Có**: Bỏ qua hành động
   - **Không**: Tiến hành hành động mở rộng (khởi chạy hoặc chấm dứt instances)

## Các Phương Pháp Hay Nhất

### 1. Sử Dụng AMI Sẵn Sàng

- **Lợi ích**: Giảm thời gian cấu hình cho các EC2 instances
- **Kết quả**: Instances có thể phục vụ yêu cầu nhanh hơn
- **Tác động**: Cho phép thời gian cooldown ngắn hơn và mở rộng linh hoạt hơn

### 2. Bật Detailed Monitoring (Giám Sát Chi Tiết)

- **Tần suất**: Nhận chỉ số mỗi 1 phút thay vì 5 phút
- **Lợi ích**: Phản ứng nhanh hơn với các thay đổi về nhu cầu
- **Kết quả**: Các quyết định mở rộng chính xác và kịp thời hơn

### 3. Tối Ưu Hóa Thời Gian Cooldown

- Bằng cách giảm thời gian khởi động instance với các AMI được cấu hình sẵn
- Bạn có thể giảm thời gian cooldown
- Điều này cho phép mở rộng phản ứng nhanh hơn

## Tóm Tắt

AWS Auto Scaling Groups cung cấp các tùy chọn mở rộng linh hoạt thông qua các chính sách động, theo lịch trình và dự đoán. Chọn đúng chỉ số và tối ưu hóa thời gian cooldown của bạn là chìa khóa để duy trì hiệu suất tối ưu và hiệu quả chi phí.



================================================================================
FILE: 67-aws-auto-scaling-dynamic-scaling-policies-hands-on.md
================================================================================

# AWS Auto Scaling - Hướng Dẫn Thực Hành Chính Sách Mở Rộng Động

## Tổng Quan

Hướng dẫn này trình bày cách triển khai và kiểm tra các chính sách mở rộng tự động cho AWS Auto Scaling Groups (ASG), tập trung vào mở rộng động, mở rộng dự đoán và hành động theo lịch.

## Các Loại Chính Sách Mở Rộng

### 1. Hành Động Theo Lịch (Scheduled Actions)

Hành động theo lịch cho phép bạn lập kế hoạch các hoạt động mở rộng trước dựa trên các sự kiện có thể dự đoán.

**Tính Năng Chính:**
- Đặt công suất mong muốn, giá trị tối thiểu hoặc tối đa
- Cấu hình lịch trình định kỳ (hàng giờ, hàng tuần, v.v.)
- Xác định thời gian bắt đầu và kết thúc
- Hoàn hảo cho các sự kiện dự kiến trước (ví dụ: các chiến dịch khuyến mãi)

### 2. Chính Sách Mở Rộng Dự Đoán (Predictive Scaling)

Mở rộng dựa trên machine learning với dữ liệu lịch sử và dự báo.

**Tùy Chọn Cấu Hình:**
- Chọn các chỉ số để giám sát:
  - Sử dụng CPU
  - Mạng vào/ra
  - Số lượng yêu cầu Application Load Balancer
  - Chỉ số tùy chỉnh
- Đặt mức sử dụng mục tiêu (ví dụ: 50% CPU)
- Yêu cầu dữ liệu lịch sử (thường tối thiểu một tuần)

**Lưu ý:** Mở rộng dự đoán cần thời gian giám sát kéo dài để tạo ra dự báo chính xác.

### 3. Chính Sách Mở Rộng Động (Dynamic Scaling)

Mở rộng theo thời gian thực dựa trên cảnh báo CloudWatch và chỉ số hiện tại.

#### Các Loại Mở Rộng Động:

**Mở Rộng Đơn Giản (Simple Scaling):**
- Kích hoạt dựa trên cảnh báo CloudWatch đơn lẻ
- Thêm/xóa số lượng instance cố định hoặc theo phần trăm
- Ví dụ: Thêm 2 instance hoặc 10% kích thước nhóm

**Mở Rộng Theo Bước (Step Scaling):**
- Nhiều bước mở rộng dựa trên mức độ nghiêm trọng của cảnh báo
- Các hành động khác nhau cho các mức ngưỡng khác nhau
- Ví dụ: Thêm 10 instance cho tải trọng nghiêm trọng, 1 instance cho tải trọng vừa phải

**Mở Rộng Theo Dõi Mục Tiêu (Target Tracking):**
- Tự động duy trì chỉ số cụ thể ở giá trị mục tiêu
- Tạo cảnh báo CloudWatch tự động
- Đơn giản nhất để cấu hình và quản lý

## Thực Hành: Triển Khai Chính Sách Theo Dõi Mục Tiêu

### Yêu Cầu Trước
- Auto Scaling Group đang hoạt động
- Các EC2 instance đang chạy
- Quyền IAM phù hợp

### Bước 1: Cấu Hình Công Suất ASG

1. Đặt công suất tối thiểu: 1
2. Đặt công suất tối đa: 3
3. Đặt công suất mong muốn: 1

Điều này cho phép ASG mở rộng từ 1 đến 3 instance.

### Bước 2: Tạo Chính Sách Theo Dõi Mục Tiêu

1. Điều hướng đến Auto Scaling Group của bạn
2. Vào tab "Automatic scaling"
3. Tạo chính sách mở rộng động
4. Chọn "Target tracking scaling"
5. Cấu hình:
   - **Tên Chính Sách:** target tracking policy
   - **Chỉ Số:** Sử dụng CPU trung bình
   - **Giá Trị Mục Tiêu:** 40%
6. Tạo chính sách

### Bước 3: Hiểu Về Cảnh Báo CloudWatch

Chính sách theo dõi mục tiêu tự động tạo hai cảnh báo CloudWatch:

**AlarmHigh (Mở Rộng Ra):**
- Kích hoạt khi CPU > 40% trong 3 điểm dữ liệu (3 phút)
- Hành động: Thêm instance

**AlarmLow (Thu Hẹp Lại):**
- Kích hoạt khi CPU < 28% trong 15 điểm dữ liệu (15 phút)
- Hành động: Xóa instance

### Bước 4: Kiểm Tra Chính Sách Mở Rộng

#### Mô Phỏng Tải CPU Cao

1. Kết nối đến EC2 instance bằng EC2 Instance Connect
2. Cài đặt công cụ stress:
   ```bash
   sudo amazon-linux-extras install epel -y
   sudo yum install stress -y
   ```
3. Tạo tải CPU:
   ```bash
   stress -c 4
   ```
   Lệnh này sử dụng 4 vCPU ở công suất 100%.

#### Quan Sát Hành Vi Mở Rộng

1. **Giám Sát Hoạt Động:**
   - Vào ASG → tab Activity
   - Theo dõi các hoạt động mở rộng

2. **Kiểm Tra Số Lượng Instance:**
   - Vào Instance Management
   - Quan sát các instance mới được khởi chạy

3. **Xem Chỉ Số:**
   - Kiểm tra tab Monitoring
   - Sử dụng CPU nên tăng vọt lên ~100%
   - Theo dõi điểm kích hoạt mở rộng

4. **Xác Minh Cảnh Báo CloudWatch:**
   - Điều hướng đến dịch vụ CloudWatch
   - Kiểm tra phần Alarms
   - AlarmHigh nên ở trạng thái "In alarm"

### Bước 5: Kiểm Tra Hành Động Thu Hẹp

1. Dừng lệnh stress (Ctrl+C) hoặc khởi động lại instance
2. Sử dụng CPU giảm xuống ~0%
3. Đợi 15 phút cho thời gian cooldown thu hẹp
4. AlarmLow kích hoạt
5. ASG chấm dứt các instance thừa
6. Công suất trở về mức tối thiểu (1 instance)

## Kết Quả Mong Đợi

### Chuỗi Mở Rộng Ra:
1. CPU đạt 40% → AlarmHigh kích hoạt
2. Công suất mong muốn: 1 → 2 instance
3. Nếu CPU vẫn cao: 2 → 3 instance

### Chuỗi Thu Hẹp Lại:
1. CPU giảm dưới 28% trong 15 phút → AlarmLow kích hoạt
2. Công suất mong muốn: 3 → 2 instance
3. Sau cooldown: 2 → 1 instance

## Thực Hành Tốt Nhất

1. **Đặt Ngưỡng Phù Hợp:**
   - Xem xét yêu cầu của ứng dụng
   - Cân bằng giữa chi phí và hiệu suất

2. **Cấu Hình Thời Gian Cooldown:**
   - Ngăn chặn dao động mở rộng nhanh
   - Mặc định thu hẹp lại thận trọng hơn (15 phút)

3. **Giám Sát Hoạt Động Mở Rộng:**
   - Xem xét Activity History thường xuyên
   - Điều chỉnh chính sách dựa trên các mẫu

4. **Quản Lý Chi Phí:**
   - Đặt giới hạn công suất tối đa
   - Xóa các chính sách mở rộng không sử dụng
   - Giám sát chi phí cảnh báo CloudWatch

## Dọn Dẹp

Để dọn dẹp tài nguyên:

1. Xóa chính sách mở rộng theo dõi mục tiêu
2. Cảnh báo CloudWatch sẽ được tự động xóa
3. Chấm dứt bất kỳ EC2 instance thừa nếu cần
4. Cân nhắc xóa ASG nếu không còn cần thiết

## Tóm Tắt

Chính sách theo dõi mục tiêu cung cấp:
- ✅ Tự động tạo cảnh báo CloudWatch
- ✅ Cấu hình đơn giản
- ✅ Mở rộng hai chiều (ra và vào)
- ✅ Tự động hóa dựa trên chỉ số
- ✅ Sử dụng tài nguyên tiết kiệm chi phí

Điều này khiến chúng trở nên lý tưởng cho hầu hết các trường hợp sử dụng auto-scaling khi bạn muốn duy trì một chỉ số hiệu suất cụ thể ở giá trị mục tiêu.



================================================================================
FILE: 68-aws-auto-scaling-instance-refresh.md
================================================================================

# AWS Auto Scaling Group - Instance Refresh

## Tổng Quan

Instance Refresh là một tính năng gốc của AWS Auto Scaling groups cho phép bạn cập nhật toàn bộ Auto Scaling group với một launch template mới bằng cách thay thế có hệ thống tất cả các EC2 instances.

## Instance Refresh Là Gì?

Instance Refresh là một tính năng tiện lợi giúp bạn cập nhật Auto Scaling group khi bạn đã tạo một launch template mới. Thay vì phải thủ công terminate từng instance một và chờ đợi chúng khởi động lại, bạn có thể sử dụng tính năng tự động có sẵn này.

## Cách Hoạt Động

### Thiết Lập Ban Đầu

Xem xét kịch bản sau:
- Bạn có một Auto Scaling group với các EC2 instances được khởi chạy bằng launch template cũ
- Bạn tạo một launch template mới (ví dụ: với AMI đã được cập nhật)
- Bạn muốn thay thế tất cả các instances hiện tại bằng các instances mới sử dụng template đã cập nhật

### Quy Trình

1. **Khởi Động Refresh**: Gọi API `Start Instance Refresh`
2. **Đặt Minimum Healthy Percentage**: Xác định bao nhiêu instances phải duy trì trạng thái khỏe mạnh trong quá trình refresh (ví dụ: 60%)
3. **Thay Thế Dần Dần**: 
   - Các instances được terminate dần dần
   - Các instances mới được khởi chạy với launch template mới
   - Quá trình tiếp tục cho đến khi tất cả instances cũ được thay thế

### Các Tham Số Chính

#### Minimum Healthy Percentage (Phần Trăm Khỏe Mạnh Tối Thiểu)
- Xác định có bao nhiêu instances có thể bị xóa theo thời gian
- Ví dụ: Đặt 60% có nghĩa là ít nhất 60% công suất của bạn phải duy trì trạng thái khỏe mạnh trong quá trình refresh
- Điều này kiểm soát tốc độ thay thế instances

#### Warm-up Time (Thời Gian Khởi Động)
- Chỉ định thời gian chờ đợi cho đến khi một EC2 instance mới được coi là sẵn sàng sử dụng
- Đảm bảo các instances có đủ thời gian để được khởi tạo đầy đủ và sẵn sàng phục vụ traffic
- Giúp ngăn chặn việc gán instance quá sớm

## Lợi Ích

- **Quy Trình Tự Động**: Không cần can thiệp thủ công để thay thế instances
- **Không Downtime**: Duy trì phần trăm khỏe mạnh tối thiểu trong suốt quá trình refresh
- **Cập Nhật An Toàn**: Triển khai dần dần đảm bảo tính khả dụng của dịch vụ
- **Kiểm Soát Linh Hoạt**: Cấu hình tốc độ và thời gian thay thế instances

## Các Trường Hợp Sử Dụng

- Cập nhật AMI (Amazon Machine Image) cho các instances của bạn
- Áp dụng cấu hình launch template mới
- Triển khai các phiên bản ứng dụng đã cập nhật
- Triển khai các bản vá bảo mật trên tất cả instances

## Tóm Tắt

Instance Refresh là một cách hiệu quả để cập nhật toàn bộ Auto Scaling group của bạn mà không cần quản lý instances thủ công. Bằng cách đặt phần trăm khỏe mạnh tối thiểu và thời gian warm-up phù hợp, bạn có thể đảm bảo quá trình chuyển đổi suôn sẻ từ instances cũ sang instances mới trong khi vẫn duy trì tính khả dụng của dịch vụ.



================================================================================
FILE: 7-iam-policies-in-depth.md
================================================================================

# Tìm Hiểu Sâu Về IAM Policies (Chính Sách IAM)

## Tổng Quan

Trong bài giảng này, chúng ta sẽ khám phá chi tiết về IAM policies và hiểu cách chúng hoạt động với users, groups cũng như cấu trúc kế thừa của chúng.

## Cấu Trúc IAM Policy và Groups

### Gán Policy Dựa Trên Group

Hãy xem xét một ví dụ thực tế với một nhóm các developers:
- **Users**: Alice, Bob, và Charles
- Khi chúng ta gán một policy ở cấp độ group, nó sẽ áp dụng cho tất cả các thành viên
- Cả ba users (Alice, Bob, và Charles) đều sẽ kế thừa và có quyền truy cập thông qua policy này

### Ví Dụ Về Nhiều Groups

Nếu chúng ta có một nhóm thứ hai gọi là "Operations" với một policy khác:
- Users David và Edward sẽ có policy khác với nhóm developers
- Mỗi nhóm duy trì bộ quyền riêng biệt của mình

### Inline Policies

Đối với các users riêng lẻ như Fred:
- Users không nhất thiết phải thuộc về một group
- Chúng ta có thể tạo **inline policies** - các policies được gán trực tiếp cho một user cụ thể
- Inline policies có thể được áp dụng cho bất kỳ user nào, dù họ có thuộc group hay không

### Thành Viên Của Nhiều Groups

Users có thể thuộc nhiều groups cùng một lúc:
- Nếu Charles và David đều thuộc về "Audit Team" với policy riêng
- **Charles** kế thừa policies từ cả hai:
  - Policy của nhóm Developers
  - Policy của nhóm Audit team
- **David** kế thừa policies từ cả hai:
  - Policy của nhóm Operations team
  - Policy của nhóm Audit team

Mô hình kế thừa này sẽ trở nên rõ ràng hơn khi bạn thực hành trực tiếp.

## Cấu Trúc IAM Policy

### Định Dạng JSON Document

IAM policies được viết dưới dạng JSON documents. Hiểu cấu trúc này rất quan trọng vì bạn sẽ gặp nó thường xuyên trong AWS.

### Các Thành Phần Chính

Cấu trúc IAM policy bao gồm:

#### 1. Version (Phiên bản)
- Thường là `2012-10-17`
- Đại diện cho phiên bản ngôn ngữ policy

#### 2. ID (Tùy chọn)
- Định danh cho policy
- Không bắt buộc nhưng hữu ích cho việc tổ chức

#### 3. Statement(s) (Câu lệnh)
- Có thể là một hoặc nhiều statements
- Mỗi statement chứa nhiều phần quan trọng

### Các Thành Phần Của Statement

Mỗi statement bao gồm:

#### Sid (Statement ID)
- Định danh cho statement
- Trường tùy chọn
- Ví dụ: Có thể được đánh số như "1", "2", v.v.

#### Effect (Bắt buộc)
- Xác định statement **cho phép** hay **từ chối** quyền truy cập
- Chỉ có hai giá trị: `Allow` hoặc `Deny`

#### Principal (Bắt buộc)
- Chỉ định accounts, users, hoặc roles mà policy áp dụng
- Ví dụ: Có thể là root account của AWS account của bạn

#### Action (Bắt buộc)
- Danh sách các API calls sẽ được cho phép hoặc từ chối dựa trên Effect
- Định nghĩa những operations nào có thể được thực hiện

#### Resource (Bắt buộc)
- Danh sách các resources mà actions sẽ được áp dụng
- Ví dụ: Một S3 bucket hoặc các AWS resources khác

#### Condition (Tùy chọn)
- Chỉ định khi nào statement nên được áp dụng
- Không phải lúc nào cũng có vì nó là tùy chọn

## Chuẩn Bị Cho Kỳ Thi

Đối với kỳ thi AWS, hãy đảm bảo bạn hiểu các thành phần chính sau:
- **Effect**: Allow hoặc Deny
- **Principal**: Policy áp dụng cho ai
- **Action**: Những API calls nào bị ảnh hưởng
- **Resource**: Những resources nào được nhắm đến

Đừng lo lắng nếu điều này có vẻ phức tạp bây giờ - bạn sẽ gặp những khái niệm này xuyên suốt khóa học và sẽ tự tin hơn với chúng vào cuối khóa.

## Tóm Tắt

- IAM policies kiểm soát quyền truy cập vào các AWS resources
- Policies có thể được gán cho groups, users, hoặc roles
- Users kế thừa policies từ tất cả các groups họ thuộc về
- Inline policies cung cấp quyền cụ thể cho từng user
- Cấu trúc policy tuân theo định dạng JSON chuẩn
- Hiểu về Effect, Principal, Action, và Resource là cần thiết

Đó là tất cả cho bài giảng này! Hẹn gặp bạn ở bài tiếp theo.



================================================================================
FILE: 8-iam-policies-hands-on-tutorial.md
================================================================================

# Hướng Dẫn Thực Hành IAM Policies

## Tổng Quan

Hướng dẫn thực hành này sẽ minh họa cách hoạt động của IAM policies bằng cách quản lý quyền hạn cho người dùng tên Stephane. Chúng ta sẽ khám phá cách thêm và xóa quyền, hiểu về kế thừa policy, và tạo các policy tùy chỉnh.

## Thiết Lập Người Dùng Ban Đầu

### Kiểm Tra Quyền Của Người Dùng

Hãy bắt đầu bằng cách xem xét IAM policies chi tiết. Trước tiên, điều hướng đến phần IAM users.

**Trạng thái hiện tại:**
- Người dùng "Stephane" thuộc nhóm admin
- Có quyền administrator access đối với AWS
- Có thể thực hiện bất kỳ hành động nào trong AWS console

**Xác minh:**
1. Đăng nhập bằng user Stephane
2. Truy cập IAM console
3. Nhấp vào "Users" ở menu bên trái
4. Bạn có thể thấy user Stephane hiển thị

Vì Stephane có quyền administrator thông qua nhóm admin, nó có thể xem và quản lý tất cả người dùng.

## Xóa Quyền Của Người Dùng

### Xóa Khỏi Nhóm Admin

Để minh họa cách hoạt động của quyền, hãy xóa Stephane khỏi nhóm admin:

**Các bước:**
1. Điều hướng đến nhóm admin
2. Xóa user Stephane khỏi nhóm này
3. Hành động này sẽ thu hồi ngay lập tức tất cả các quyền liên quan

### Xác Minh Mất Quyền

Sau khi xóa user, làm mới trang IAM users:

**Kết quả:**
- Hiển thị zero users (không có user nào)
- Xuất hiện lỗi "Access Denied" (Truy cập bị từ chối)
- Thông báo lỗi: "You don't have permission to do iamListUsers"

**Điều gì đã xảy ra:**
Bằng cách xóa Stephane khỏi nhóm admin, chúng ta đã mất quyền xem users. Điều này chứng minh rằng việc tham gia nhóm trực tiếp kiểm soát quyền truy cập.

## Khôi Phục Quyền Hạn Chế

### Thêm Quyền Read-Only

Hãy khắc phục điều này bằng cách thêm quyền hạn chế:

**Các bước:**
1. Điều hướng đến IAM
2. Vào "Users" và tìm Stephane
3. Lưu ý: Hiện tại có zero permission policies (không có policy nào)
4. Nhấp "Add permissions"
5. Chọn "Attach policies directly" (không thêm vào nhóm)
6. Chọn policy `IAMReadOnlyAccess`
7. Thêm permission này

### Kiểm Tra Quyền Read-Only

Sau khi thêm IAMReadOnlyAccess policy:

**Những gì bạn có thể làm:**
- Làm mới trang users - bây giờ nó hoạt động!
- Xem user Stephane
- Xem các user groups (như "admin")

**Những gì bạn không thể làm:**
- Thử tạo một nhóm mới có tên "developers"
- Bạn sẽ nhận được lỗi: không thể tạo groups
- Lý do: IAMReadOnlyAccess chỉ cung cấp quyền đọc

**Nguyên tắc quan trọng:**
Người dùng chỉ nên có quyền cho những gì họ cần làm (nguyên tắc đặc quyền tối thiểu - principle of least privilege).

## Tạo Nhiều Nguồn Quyền

### Tạo Nhóm Developer

Hãy tạo một nhóm mới để minh họa nhiều nguồn permission:

**Các bước:**
1. Vào "User Groups" ở menu bên trái
2. Tạo nhóm có tên "developers"
3. Thêm user Stephane vào nhóm này
4. Đính kèm bất kỳ policy nào (ví dụ: "AlexaForBusiness" - policy cụ thể không quan trọng cho demo này)
5. Tạo nhóm

### Thêm Lại Vào Nhóm Admin

Bây giờ hãy thêm Stephane trở lại nhóm admin:

**Các bước:**
1. Điều hướng đến nhóm admin
2. Nhấp "Add users"
3. Thêm lại Stephane vào nhóm này

### Kiểm Tra Nhiều Quyền

Điều hướng trở lại user Stephane để xem tất cả quyền:

**Các Permission Policies hiện tại (tổng cộng 3):**

1. **AdministratorAccess**
   - Nguồn: Kế thừa từ nhóm "admin"
   - Mức độ truy cập: Quyền administrator đầy đủ

2. **AlexaForBusiness** (managed policy)
   - Nguồn: Kế thừa từ nhóm "developers"
   - Mức độ truy cập: Đặc thù cho Alexa for Business

3. **IAMReadOnlyAccess**
   - Nguồn: Đính kèm trực tiếp vào user
   - Mức độ truy cập: Quyền read-only đối với IAM

**Bài học quan trọng:**
Người dùng kế thừa các quyền khác nhau dựa trên cách chúng được đính kèm:
- Thông qua tư cách thành viên nhóm
- Thông qua đính kèm policy trực tiếp

## Hiểu Cấu Trúc Policy

### Kiểm Tra AdministratorAccess Policy

Điều hướng đến "Policies" ở menu bên trái và chọn `AdministratorAccess`:

**Xem tóm tắt:**
- Cho phép tất cả các dịch vụ trong AWS (số lượng có thể thay đổi theo thời gian)
- Các dịch vụ bao gồm: App Mesh, Alexa for Business, Amplify, v.v.
- Tất cả các dịch vụ đều có "Full access"

**Cấu trúc JSON:**

Nhấp vào tab "JSON" để xem policy thô:

```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```

**Giải thích:**
- `*` (dấu sao) trong AWS có nghĩa là "bất cứ thứ gì"
- `Action: "*"` = Cho phép mọi hành động
- `Resource: "*"` = Trên mọi tài nguyên
- Kết quả: Quyền truy cập administrator đầy đủ

### Kiểm Tra IAMReadOnlyAccess Policy

Hãy xem một ví dụ policy khác:

**Xem tóm tắt:**
- IAM được ủy quyền với "Full: List" và "Limited: Read"
- Bạn có thể mở rộng để xem tất cả các API calls được cho phép

**Cấu trúc JSON:**

```json
{
  "Effect": "Allow",
  "Action": [
    "iam:GenerateCredentialReport",
    "iam:GenerateServiceLastAccessedDetails",
    "iam:Get*",
    "iam:List*"
  ],
  "Resource": "*"
}
```

**Hiểu về Wildcards:**
- `Get*` có nghĩa là bất cứ thứ gì bắt đầu với "Get" theo sau bởi bất kỳ ký tự nào
  - Ví dụ: GetUsers, GetGroups
- `List*` có nghĩa là bất cứ thứ gì bắt đầu với "List" theo sau bởi bất kỳ ký tự nào
  - Ví dụ: ListUsers, ListGroups
- Sử dụng wildcards (`*`) nhóm nhiều API calls liên quan lại với nhau

Policy được cho phép trên `Resource: "*"`, có nghĩa là tất cả các tài nguyên.

## Tạo Policy Tùy Chỉnh

### Sử Dụng Visual Editor

AWS cung cấp hai phương pháp để tạo policies:

1. **Visual Editor** - Giao diện thân thiện với người dùng
2. **JSON Editor** - Chỉnh sửa JSON trực tiếp

**Tạo Policy với Visual Editor:**

**Các bước:**
1. Nhấp "Create policy"
2. Chọn giữa Visual Editor hoặc JSON
3. Chọn Visual Editor
4. Chọn service: IAM
5. Chọn actions:
   - Chọn "ListUsers" (1 trong 38 list actions)
   - Chọn "GetUser" (1 trong 32 read actions)
6. Xác định resources:
   - Tất cả resources, hoặc
   - Resources cụ thể
7. Nhấp "Next"
8. Đặt tên policy: "MyIAMPermissions"
9. Tạo policy

**Xem JSON Được Tạo:**

Sau khi tạo, xem policy để thấy JSON được tạo ra:

```json
{
  "Effect": "Allow",
  "Action": [
    "iam:ListUsers",
    "iam:GetUser"
  ],
  "Resource": "*"
}
```

Visual editor tự động tạo JSON dựa trên các lựa chọn của bạn.

**Sử dụng Policy:**
Policy này bây giờ có thể được đính kèm vào các groups hoặc users khi cần.

## Quản Lý Permissions trong AWS

Quy trình được minh họa cho thấy cách quản lý permissions trong AWS:

1. Tạo policies (có sẵn hoặc tùy chỉnh)
2. Đính kèm policies vào groups
3. Thêm users vào groups
4. Đính kèm policies trực tiếp vào users
5. Users kế thừa permissions từ tất cả các nguồn

## Dọn Dẹp và Xác Minh Cuối Cùng

### Xóa Các Tài Nguyên Không Cần Thiết

Để dọn dẹp môi trường demo:

**Các bước:**
1. Điều hướng đến "User Groups"
2. Xóa nhóm "developers" (không còn cần thiết)
3. Vào user Stephane
4. Xóa policy `IAMReadOnlyAccess` được đính kèm trực tiếp

**Trạng thái cuối cùng:**
- Stephane chỉ thuộc nhóm "admin"
- Có quyền administrator thông qua tư cách thành viên nhóm

### Xác Minh Chức Năng

Quay lại IAM console:

1. Điều hướng đến "Users"
2. Xác nhận tất cả users đều hiển thị
3. Mọi thứ hiển thị chính xác

**Kết luận:**
Hệ thống đang hoạt động chính xác với permissions được đơn giản hóa.

## Những Điểm Chính Cần Nhớ

### Các Khái Niệm Quan Trọng

1. **Permissions Dựa Trên Nhóm**: Đính kèm policies vào groups ảnh hưởng đến tất cả thành viên nhóm
2. **Đính Kèm Policy Trực Tiếp**: Policies có thể được đính kèm trực tiếp vào users
3. **Kế Thừa Permission**: Users có thể có permissions từ nhiều nguồn
4. **Read-Only vs. Full Access**: Các policies khác nhau cung cấp các mức độ truy cập khác nhau
5. **Cấu Trúc Policy**: Định dạng JSON với Effect, Action, và Resource
6. **Wildcards**: Sử dụng `*` để đại diện cho "bất kỳ" trong AWS policies
7. **Visual vs. JSON Editing**: Nhiều cách để tạo policies
8. **Least Privilege**: Chỉ cấp quyền cần thiết

### Thực Hành Tốt Nhất

- Sử dụng groups để quản lý permissions của nhiều users
- Áp dụng nguyên tắc đặc quyền tối thiểu
- Hiểu về kế thừa policy từ nhiều nguồn
- Sử dụng read-only policies khi không cần quyền ghi
- Tận dụng visual editor để tạo policy dễ dàng hơn
- Xem xét và dọn dẹp các policies và groups không cần thiết thường xuyên

## Kết Luận

Bản minh họa thực hành này đã cho thấy cách IAM policies hoạt động trong thực tế. Bạn đã học cách:
- Thêm và xóa quyền của người dùng
- Hiểu về kế thừa policy
- Kiểm tra các policies có sẵn
- Tạo policies tùy chỉnh
- Quản lý permissions thông qua groups và đính kèm trực tiếp

Hiểu các khái niệm này là điều cần thiết để quản lý đúng cách quyền truy cập và bảo mật trong AWS.

---

**Vậy là xong cho bài giảng này. Tôi hy vọng bạn thích nó, và tôi sẽ gặp bạn trong bài giảng tiếp theo!**



================================================================================
FILE: 9-aws-iam-password-policy-and-mfa.md
================================================================================

# Chính Sách Mật Khẩu và Xác Thực Đa Yếu Tố (MFA) trong AWS IAM

## Giới Thiệu

Sau khi tạo người dùng và nhóm trong AWS IAM, việc bảo vệ họ khỏi bị xâm nhập là điều cần thiết. AWS cung cấp hai cơ chế phòng thủ chính để bảo mật tài khoản và người dùng IAM của bạn.

## Cơ Chế Phòng Thủ

### 1. Chính Sách Mật Khẩu

Chính sách mật khẩu mạnh là tuyến phòng thủ đầu tiên của bạn. Mật khẩu càng mạnh, tài khoản của bạn càng an toàn.

#### Các Tùy Chọn Chính Sách Mật Khẩu

AWS cho phép bạn cấu hình chính sách mật khẩu với các tùy chọn sau:

- **Độ Dài Mật Khẩu Tối Thiểu**: Đặt số ký tự tối thiểu cho mật khẩu
- **Yêu Cầu Loại Ký Tự**: Yêu cầu các loại ký tự cụ thể bao gồm:
  - Chữ cái viết hoa
  - Chữ cái viết thường
  - Số
  - Ký tự không phải chữ và số (ví dụ: ?, !, @)
- **Thay Đổi Mật Khẩu Tự Phục Vụ**: Cho phép hoặc ngăn người dùng IAM thay đổi mật khẩu của chính họ
- **Hết Hạn Mật Khẩu**: Yêu cầu người dùng thay đổi mật khẩu sau một khoảng thời gian nhất định (ví dụ: mỗi 90 ngày)
- **Ngăn Chặn Tái Sử Dụng Mật Khẩu**: Ngăn người dùng sử dụng lại các mật khẩu trước đó

#### Lợi Ích

Chính sách mật khẩu rất hiệu quả trong việc chống lại các cuộc tấn công brute force vào tài khoản của bạn.

### 2. Xác Thực Đa Yếu Tố (MFA)

MFA là một biện pháp bảo mật quan trọng được khuyến nghị mạnh mẽ cho các tài khoản AWS, đặc biệt là cho các quản trị viên có quyền truy cập rộng rãi để thay đổi cấu hình và xóa tài nguyên.

#### MFA Là Gì?

MFA kết hợp hai yếu tố để xác thực:
1. **Thứ bạn biết**: Mật khẩu của bạn
2. **Thứ bạn sở hữu**: Một thiết bị bảo mật (mã token MFA)

Sự kết hợp này cung cấp bảo mật cao hơn đáng kể so với chỉ sử dụng mật khẩu.

#### MFA Hoạt Động Như Thế Nào

Khi người dùng (ví dụ: Alice) đăng nhập với MFA được bật:
1. Cô ấy nhập mật khẩu
2. Cô ấy cung cấp mã token MFA từ thiết bị của mình
3. Chỉ với cả hai yếu tố thì việc đăng nhập mới thành công

#### Lợi Ích Của MFA

Ngay cả khi mật khẩu bị đánh cắp hoặc bị hack, tài khoản vẫn được bảo vệ vì kẻ tấn công cũng cần có quyền truy cập vật lý vào thiết bị MFA của người dùng (chẳng hạn như điện thoại của họ). Điều này làm cho việc truy cập trái phép trở nên khó khăn hơn nhiều.

## Các Tùy Chọn Thiết Bị MFA trong AWS

AWS hỗ trợ nhiều loại thiết bị MFA:

### 1. Thiết Bị MFA Ảo

**Các Tùy Chọn Phổ Biến:**
- **Google Authenticator**: Hoạt động trên một điện thoại tại một thời điểm
- **Authy**: Hỗ trợ nhiều token trên một thiết bị duy nhất

**Tính Năng:**
- Có thể quản lý nhiều tài khoản và người dùng IAM trên một thiết bị duy nhất
- Dễ dàng thiết lập và sử dụng
- Được khuyến nghị cho thực hành thực tế

### 2. Khóa Bảo Mật Universal 2nd Factor (U2F)

**Ví Dụ:**
- **YubiKey của Yubico** (nhà cung cấp bên thứ ba)

**Tính Năng:**
- Khóa bảo mật vật lý
- Hỗ trợ nhiều tài khoản root và người dùng IAM với một khóa duy nhất
- Tiện lợi để mang theo trên móc chìa khóa

### 3. Thiết Bị MFA Key Fob Phần Cứng

**Ví Dụ:**
- **Gemalto** (nhà cung cấp bên thứ ba)

**Tính Năng:**
- Thiết bị phần cứng chuyên dụng
- Trình tạo token vật lý

### 4. Key Fob Phần Cứng cho AWS GovCloud

**Nhà Cung Cấp:**
- **SurePassID** (nhà cung cấp bên thứ ba)

**Trường Hợp Sử Dụng:**
- Được thiết kế đặc biệt cho người dùng Government Cloud của Hoa Kỳ (AWS GovCloud)

## Thực Hành Tốt Nhất

- **Luôn bảo vệ tài khoản root của bạn** bằng MFA
- **Bật MFA cho tất cả người dùng IAM**, đặc biệt là quản trị viên
- **Chọn phương thức MFA** phù hợp với yêu cầu bảo mật và sự tiện lợi của bạn
- **Triển khai chính sách mật khẩu mạnh** để bổ sung cho bảo vệ MFA

## Tóm Tắt

Bảo vệ tài khoản AWS của bạn yêu cầu một cách tiếp cận nhiều lớp:
1. Triển khai chính sách mật khẩu toàn diện để thực thi mật khẩu mạnh
2. Bật MFA để có thêm bảo mật bằng cách sử dụng yếu tố xác thực thứ hai
3. Chọn loại thiết bị MFA phù hợp với nhu cầu của bạn

Bằng cách kết hợp các cơ chế phòng thủ này, bạn giảm đáng kể nguy cơ truy cập trái phép vào tài nguyên AWS của mình.

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ thực hành triển khai các biện pháp bảo mật này để xem chúng hoạt động như thế nào trong thực tế..


