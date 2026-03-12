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