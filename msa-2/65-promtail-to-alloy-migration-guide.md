# Lưu Ý Quan Trọng Về Việc Di Chuyển Từ Promtail

## Promtail Đã Được Thay Thế Bởi Alloy

### Tổng Quan

Từ **Grafana Loki phiên bản 3.0** trở đi, Promtail - công cụ chịu trách nhiệm thu thập các dòng log, đã được thay thế bằng một sản phẩm mới có tên là **Alloy**.

### Những Điều Bạn Cần Biết

Mặc dù các bài giảng sắp tới sẽ thảo luận về Promtail, nhưng **Alloy sẽ hoạt động tương tự**. Vì đây là các thành phần nội bộ của Grafana Loki, nên thay đổi này sẽ không có tác động đáng kể đến việc triển khai của bạn.

### Các Thay Đổi Chính

- **Promtail** (Cũ) → **Alloy** (Hiện tại)
- Alloy phục vụ cùng mục đích: thu thập các dòng log
- Tác động tối thiểu đến kiến trúc microservices của bạn
- Các file cấu hình cần được cập nhật để sử dụng Alloy thay vì Promtail

### Các File Docker Compose Đã Được Cập Nhật

Tất cả các file Docker Compose đã được cập nhật với các thay đổi liên quan đến Alloy bên trong kho lưu trữ GitHub.

### Tài Liệu

Bạn có thể tìm tài liệu đầy đủ về Alloy cùng với Loki tại liên kết sau:

🔗 [Hướng Dẫn Bắt Đầu Nhanh Grafana Loki](https://grafana.com/docs/loki/latest/get-started/quick-start/)

### Làm Việc Với Các Phiên Bản Cũ

Nếu vì lý do nào đó các dự án thực tế của bạn sử dụng **phiên bản cũ của Grafana Loki** (trước phiên bản 3.0), thì bạn sẽ cần sử dụng **Promtail**.

Các thay đổi liên quan đến Promtail có sẵn trong các **nhánh cũ hơn** của kho lưu trữ GitHub của khóa học.

---

## Tóm Tắt

- ✅ Sử dụng **Alloy** cho Grafana Loki 3.0 trở lên
- ✅ Cập nhật các file cấu hình để sử dụng cấu hình Alloy thay vì Promtail
- ✅ Tham khảo kho lưu trữ GitHub cho các file Docker Compose đã được cập nhật
- ⚠️ Chỉ sử dụng Promtail cho các phiên bản Grafana Loki cũ hơn (< 3.0)

---

*Hướng dẫn này là một phần của tài liệu khóa học Microservices với Spring Boot.*