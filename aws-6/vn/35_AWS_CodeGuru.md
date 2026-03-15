# Amazon CodeGuru

## Tổng quan

Amazon CodeGuru là dịch vụ được hỗ trợ bởi machine learning (học máy) cung cấp hai khả năng chính:

1. **Đánh giá code tự động (Automated code reviews)**
2. **Khuyến nghị về hiệu suất ứng dụng (Application performance recommendations)**

## Các thành phần

### CodeGuru Reviewer

**Mục đích:** Đánh giá code tự động với phân tích code tĩnh

**Tính năng chính:**
- Phân tích code trong các repository (CodeCommit, GitHub, Bitbucket)
- Cung cấp các khuyến nghị khả thi cho bugs và memory leaks
- Phát hiện vấn đề trước cả các reviewer con người nhờ machine learning
- Xác định các vấn đề nghiêm trọng, lỗ hổng bảo mật và bugs khó tìm

**Khả năng:**
- Triển khai các best practices trong coding
- Tìm resource leaks (rò rỉ tài nguyên)
- Phát hiện bảo mật và xác định lỗ hổng
- Xác thực đầu vào (input validation)

**Ngôn ngữ hỗ trợ:**
- Java
- Python

**Cách hoạt động:**
- Sử dụng machine learning và automated reasoning
- Được huấn luyện trên hàng nghìn repositories mã nguồn mở
- Được huấn luyện trên tất cả repositories của amazon.com

### CodeGuru Profiler

**Mục đích:** Giám sát và tối ưu hóa hiệu suất ứng dụng

**Khi nào sử dụng:**
- Trong giai đoạn build và test (pre-production)
- Trong môi trường production runtime

**Tính năng chính:**
- Cung cấp khả năng hiển thị hiệu suất ứng dụng trong runtime
- Phát hiện và tối ưu hóa các dòng code tốn kém ở pre-production
- Đo lường hiệu suất ứng dụng theo thời gian thực
- Xác định các cải thiện về hiệu suất và chi phí trong production

**Khả năng:**
- Hiểu hành vi runtime của ứng dụng
- Xác định code tiêu thụ quá nhiều CPU
- Loại bỏ các điểm kém hiệu quả trong code
- Cải thiện hiệu suất ứng dụng
- Giảm sử dụng CPU và giảm chi phí tính toán
- Cung cấp heap summaries để xác định các objects chiếm nhiều bộ nhớ
- Phát hiện bất thường khi ứng dụng hoạt động lạ

**Triển khai:**
- Hỗ trợ ứng dụng chạy trên AWS Cloud
- Hỗ trợ ứng dụng on-premises
- Chi phí overhead tối thiểu cho các ứng dụng được giám sát

## Tóm tắt

CodeGuru kết hợp đánh giá code tự động và profiling hiệu suất để giúp developers:
- Phát hiện bugs sớm trong quá trình phát triển
- Cải thiện chất lượng code
- Tối ưu hóa hiệu suất ứng dụng
- Giảm chi phí
- Tăng cường bảo mật
