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