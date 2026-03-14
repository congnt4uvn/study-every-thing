# Biến Môi Trường AWS Lambda

## Tổng Quan
Hướng dẫn này trình bày cách sử dụng biến môi trường trong các hàm AWS Lambda để quản lý cài đặt cấu hình.

## Mục Tiêu
Học cách truyền và truy xuất biến môi trường trong các hàm Lambda mà không mã hóa (phần mã hóa sẽ được đề cập trong phần bảo mật).

## Hướng Dẫn Từng Bước

### 1. Tạo Hàm Lambda
- Tên hàm: `lambda-config-demo`
- Runtime: Python 3.8
- Mục đích: Thực hành sử dụng biến môi trường

### 2. Chỉnh Sửa Code Lambda

Import module cần thiết:
```python
import os
```

Cập nhật câu lệnh return để lấy biến môi trường:
```python
return os.getenv("ENVIRONMENT_NAME")
```

**Điểm Chính:**
- `os.getenv()` truy xuất các biến môi trường
- `ENVIRONMENT_NAME` là biến chúng ta sẽ tạo
- Hàm sẽ truy xuất và trả về giá trị của biến

### 3. Deploy Các Thay Đổi
Lưu và deploy hàm để áp dụng các thay đổi code.

### 4. Cấu Hình Biến Môi Trường

1. Điều hướng đến phần **Configuration** của hàm Lambda
2. Chọn **Environment variables** từ menu bên trái
3. Nhấp **Edit** và thêm biến môi trường mới:
   - **Key** (Khóa): `ENVIRONMENT_NAME`
   - **Value** (Giá trị): `dev` (hoặc giá trị bất kỳ bạn muốn)

**Lưu Ý:**
- Bạn có thể thêm nhiều biến môi trường nếu cần
- Cấu hình mã hóa có sẵn nhưng sẽ được đề cập trong phần bảo mật
- Hiện tại, biến môi trường vẫn chưa được mã hóa

## Khái Niệm Chính

### Biến Môi Trường Là Gì?
Các giá trị cấu hình có thể được truyền đến các hàm Lambda mà không cần hardcode chúng trong source code.

### Lợi Ích
- Tách biệt cấu hình khỏi code
- Dễ dàng chỉnh sửa mà không cần redeploy code
- Hỗ trợ các môi trường khác nhau (dev, staging, prod)

### Cân Nhắc Về Bảo Mật
Biến môi trường có thể được mã hóa bằng các dịch vụ mã hóa của AWS (được đề cập trong các phần bảo mật nâng cao).

## Tóm Tắt
Hướng dẫn này trình bày cách thiết lập và sử dụng cơ bản biến môi trường trong các hàm AWS Lambda sử dụng Python 3.8 runtime.
