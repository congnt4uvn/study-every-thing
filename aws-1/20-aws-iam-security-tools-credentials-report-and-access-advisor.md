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