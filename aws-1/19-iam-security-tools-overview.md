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