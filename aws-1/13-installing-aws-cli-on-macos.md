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