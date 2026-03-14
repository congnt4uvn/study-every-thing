# Giới Hạn AWS Lambda - Tài Liệu Học Tập

## Tổng Quan
AWS Lambda có các giới hạn cụ thể khác nhau theo từng vùng (region). Các giới hạn này rất quan trọng để hiểu cho kỳ thi chứng chỉ AWS, vì chúng giúp xác định liệu Lambda có phù hợp với một workload cụ thể hay không.

## Giới Hạn Thực Thi (Execution Limits)

### Phân Bổ Bộ Nhớ
- **Phạm vi**: 128 MB đến 10 GB
- **Bước tăng**: 64 MB
- **Lưu ý**: Tăng bộ nhớ cũng đồng thời tăng phân bổ vCPU

### Thời Gian Thực Thi Tối Đa
- **Giới hạn**: 900 giây (15 phút)
- **Ý nghĩa**: Các workload cần thời gian thực thi lâu hơn không phù hợp với Lambda

### Biến Môi Trường (Environment Variables)
- **Giới hạn dung lượng**: 4 KB
- **Trường hợp sử dụng**: Lưu trữ dữ liệu cấu hình và tham số

### Lưu Trữ Tạm Thời (/tmp)
- **Dung lượng**: Lên đến 10 GB
- **Trường hợp sử dụng**: Tải các file lớn trong quá trình thực thi function
- **Lưu ý**: Sử dụng cho các file vượt quá giới hạn kích thước triển khai

### Thực Thi Đồng Thời (Concurrent Executions)
- **Giới hạn mặc định**: 1,000 lần thực thi đồng thời trên tất cả các Lambda function
- **Khả năng mở rộng**: Có thể tăng thông qua yêu cầu hỗ trợ AWS
- **Best Practice**: Sử dụng reserved concurrency sớm để quản lý capacity

## Giới Hạn Triển Khai (Deployment Limits)

### Kích Thước Gói Function
- **Nén (.zip)**: Tối đa 50 MB
- **Không nén**: Tối đa 250 MB
- **Giải pháp thay thế**: Đối với các file lớn hơn, sử dụng thư mục /tmp

### Biến Môi Trường
- **Giới hạn dung lượng**: 4 KB (giống với giới hạn thực thi)

## Mẹo Cho Kỳ Thi

Khi bạn thấy các câu hỏi thi với các yêu cầu sau, Lambda **KHÔNG PHẢI** là giải pháp đúng:

❌ Yêu cầu 30 GB RAM (vượt quá giới hạn 10 GB)
❌ Cần 30 phút thời gian thực thi (vượt quá giới hạn 15 phút)
❌ Yêu cầu file triển khai 3 GB (vượt quá giới hạn 250 MB khi không nén)

## Điểm Cần Nhớ

1. Tất cả giới hạn là **theo từng region**
2. Biết sự khác biệt giữa giới hạn **thực thi** và **triển khai**
3. Nhớ thư mục /tmp (10 GB) để xử lý các file lớn trong quá trình thực thi
4. Hiểu khi nào Lambda KHÔNG phù hợp cho một workload
5. Bộ nhớ và vCPU được liên kết - nhiều bộ nhớ hơn = nhiều vCPU hơn

---
*Ngày Học: 14 tháng 3, 2026*
