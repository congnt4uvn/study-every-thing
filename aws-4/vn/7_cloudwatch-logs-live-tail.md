# CloudWatch Logs — Live Tail (Ghi chú học)

## Live Tail là gì?
**Live Tail** là một tính năng của CloudWatch Logs cho phép bạn xem log **gần như theo thời gian thực** trong một giao diện riêng, có thể lọc theo **log group** và (tuỳ chọn) theo **log stream**. Tính năng này rất hữu ích khi **debug** vì bạn thấy log xuất hiện ngay khi hệ thống ghi nhận.

## Khi nào nên dùng
- Kiểm tra ứng dụng có đang ghi log đúng không
- Debug trong lúc tái hiện lỗi (xem log chạy trực tiếp)
- Theo dõi luồng log nhanh mà không cần refresh liên tục

## Thuật ngữ quan trọng
- **Log group**: Nhóm chứa nhiều log stream (thường theo ứng dụng/service).
- **Log stream**: Chuỗi log từ một nguồn cụ thể (VD: 1 instance/container).
- **Log event**: Một bản ghi log (message + timestamp).

## Thực hành: Tạo log và kiểm tra bằng Live Tail
### 1) Tạo log group
1. Mở **CloudWatch** → **Logs**.
2. Tạo **log group**.
   - Ví dụ: `demo log group`

### 2) Tạo log stream
1. Mở log group vừa tạo.
2. Tạo **log stream**.
   - Ví dụ: `DemoLogStream`

### 3) Bật Live Tail
1. Trong CloudWatch Logs, mở **Live Tail**.
2. Lọc theo:
   - **Log group**: chọn `demo log group`
   - **Log stream**: tuỳ chọn (chọn `DemoLogStream` để thu hẹp phạm vi)
3. Apply filter và **Start tailing**.
4. Giữ Live Tail mở, sau đó tạo log event ở tab khác.

### 4) Gửi một log event thử
1. Quay lại trang log stream.
2. Chọn **Actions** → **Create log event**.
3. Nhập nội dung (VD: `hello world`) rồi post.
4. Kiểm tra event có xuất hiện trong **Live Tail**.

## Quan sát trong Live Tail UI
- Các event khớp filter sẽ hiện lên khi CloudWatch nhận được
- Bạn có thể xem metadata (thời gian, group/stream)
- Có thể bấm để nhảy tới đúng log stream nơi event phát sinh

## Lưu ý chi phí / giới hạn miễn phí
Theo nội dung trong transcript, Live Tail có **một mức miễn phí giới hạn theo ngày** (VD: khoảng 1 giờ/ngày). Vì vậy:
- Hãy **Stop/đóng** phiên Live Tail khi debug xong để tránh phát sinh chi phí.

## Lỗi thường gặp
- Không thấy log:
  - Kiểm tra chọn đúng log group/stream chưa
  - Xác nhận log event thật sự được ghi vào stream đó
  - Thử bỏ lọc theo stream (chỉ lọc theo group) để dễ thấy hơn

## Tự kiểm tra nhanh
1. Phân biệt log group và log stream?
2. Khi nào nên lọc theo log stream?
3. Debug xong cần làm gì để kiểm soát chi phí?
