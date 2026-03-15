# AWS DynamoDB - Optimistic Locking (Khóa Lạc Quan)

## Tổng quan

DynamoDB có một tính năng gọi là **Optimistic Locking** (Khóa Lạc Quan) cho phép bạn thực hiện Conditional Writes (Ghi Có Điều Kiện). Tính năng này đảm bảo rằng một mục không thay đổi trước khi bạn cập nhật hoặc xóa nó.

## Optimistic Locking là gì?

Optimistic Locking là một cơ chế cho phép bạn ghi vào DynamoDB chỉ khi các điều kiện nhất định được đáp ứng. Về cơ bản bạn đang nói: "Tôi muốn ghi dữ liệu này chỉ khi điều kiện này được thỏa mãn."

## Cách Hoạt Động

Việc triển khai sử dụng một thuộc tính số phiên bản trên các mục:
- Một thuộc tính đóng vai trò như số phiên bản
- Điều kiện bằng nhau được kiểm tra trên số phiên bản này trước khi ghi
- Điều này ngăn chặn xung đột cập nhật đồng thời

## Ví dụ Kịch bản

### Trạng thái Ban đầu
```
Mục trong Bảng DynamoDB:
- User ID: [id_nào_đó]
- First Name: [tên_nào_đó]
- Version: 1
```

### Thử Cập Nhật Đồng Thời

Hai client đồng thời cố gắng cập nhật cùng một mục:

**Client 1:** 
- Cập nhật: `name = John`
- Điều kiện: `chỉ khi version = 1`

**Client 2:**
- Cập nhật: `name = Lisa`
- Điều kiện: `chỉ khi version = 1`

### Điều Gì Xảy Ra

1. Một yêu cầu đến DynamoDB trước (giả sử là Client 2)
2. DynamoDB cập nhật:
   - First Name → `Lisa`
   - Version → `2`
3. Cập nhật của Client 1 thất bại vì:
   - Client 1 chỉ định điều kiện: `version = 1`
   - Phiên bản hiện tại bây giờ là: `2`
4. Client 1 nhận được thông báo lỗi cho biết dữ liệu đã thay đổi
5. Client 1 phải thực hiện thao tác GET để lấy dữ liệu mới nhất trước khi thử cập nhật lại

## Điểm Chính Cần Nhớ

- **Conditional Writes** ngăn chặn việc ghi đè các thay đổi được thực hiện bởi các client khác
- **Số phiên bản** hoạt động như một cơ chế kiểm soát đồng thời
- Cập nhật thất bại yêu cầu lấy dữ liệu mới nhất trước khi thử lại
- Đây là một chủ đề quan trọng trong các kỳ thi chứng chỉ AWS

## Trường Hợp Sử Dụng

- Ngăn chặn các điều kiện race trong môi trường đồng thời
- Đảm bảo tính nhất quán của dữ liệu mà không cần khóa
- Quản lý cập nhật các tài nguyên được chia sẻ

---

*Lưu ý: Tính năng này thường được kiểm tra trong các kỳ thi chứng chỉ AWS.*
