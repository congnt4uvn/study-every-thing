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