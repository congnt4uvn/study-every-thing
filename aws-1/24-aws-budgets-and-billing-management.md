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