# Tích Hợp AWS Lambda và CodeGuru

## Tổng Quan
Tài liệu này trình bày cách AWS Lambda và CodeGuru làm việc cùng nhau để cung cấp thông tin chi tiết về hiệu suất runtime của các hàm Lambda.

## Các Khái Niệm Chính

### CodeGuru Profiler cho Lambda
CodeGuru Profiler cung cấp thông tin chi tiết về hiệu suất runtime của các hàm Lambda, giúp bạn tối ưu hóa hiệu quả code và giảm chi phí.

### Các Runtime Được Hỗ Trợ
- **Java**
- **Python**

## Cách Hoạt Động

### Profiler Group (Nhóm Profiler)
Khi bạn bật tích hợp CodeGuru, CodeGuru sẽ tạo một profiler group riêng cho hàm Lambda của bạn.

### Quy Trình Kích Hoạt
1. Truy cập Lambda console
2. Điều hướng đến hàm Lambda của bạn
3. Bật tích hợp CodeGuru từ phần monitoring

### Những Gì Xảy Ra Khi Bạn Kích Hoạt Tích Hợp

#### 1. Thêm Lambda Layer
Một CodeGuru Profiler layer sẽ được tự động thêm vào hàm Lambda của bạn dưới dạng Lambda layer.

#### 2. Biến Môi Trường
Các biến môi trường liên quan đến CodeGuru được thêm vào cấu hình hàm để cho phép giao tiếp với dịch vụ profiler.

#### 3. Quyền IAM
Policy `AmazonCodeGuruProfilerAgentAccess` được tự động thêm vào IAM role của hàm, cấp các quyền cần thiết cho các hoạt động profiling.

## Lợi Ích

- **Thông Tin Chi Tiết Về Hiệu Suất Runtime**: Nhận các số liệu chi tiết về hiệu suất của hàm Lambda
- **Tối Ưu Hóa Code**: Xác định các điểm nghẽn về hiệu suất và các mẫu code không hiệu quả
- **Giảm Chi Phí**: Tối ưu hóa code để giảm thời gian thực thi và chi phí liên quan
- **Thiết Lập Tự Động**: Tích hợp được hợp lý hóa với cấu hình tự động

## Yêu Cầu

✅ Hàm Lambda sử dụng Java hoặc Python runtime  
✅ Quyền truy cập vào Lambda console  
✅ Quyền IAM phù hợp để sửa đổi cấu hình Lambda  
✅ CodeGuru Profiler được bật trong tài khoản AWS của bạn

## Thực Hành Tốt Nhất

1. Bật profiling cho các hàm production có tỷ lệ gọi cao
2. Xem xét dữ liệu profiling thường xuyên để xác định cơ hội tối ưu hóa
3. Giám sát tác động của profiler layer đối với hiệu suất hàm
4. Sử dụng insights để tinh chỉnh code trước khi triển khai lớn

## Tóm Tắt

Tích hợp CodeGuru Profiler với Lambda cung cấp một cách dễ dàng để có được khả năng hiển thị hiệu suất hàm. Chỉ cần bật tích hợp từ Lambda console, bạn sẽ có thiết lập tự động với các layer cần thiết, biến môi trường và quyền IAM được cấu hình tự động.
