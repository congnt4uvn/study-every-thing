# AWS CloudWatch Agent (Logs Agent và Unified Agent)

## 1) Ý chính
- Mặc định, EC2 **không tự gửi** log hệ điều hành/ứng dụng lên CloudWatch.
- Để gửi log, bạn cần cài và chạy **CloudWatch Agent** (một chương trình nhỏ) trên máy để **đẩy các file log bạn chọn** lên **CloudWatch Logs**.
- Cách làm này cũng áp dụng được cho **server on‑premises** (ví dụ máy ảo), không chỉ riêng EC2.

## 2) Điều kiện cần (quyền truy cập)
- EC2 instance cần có **IAM role** cho phép **gửi log lên CloudWatch Logs**.

## 3) Có 2 loại agent
### A) CloudWatch Logs Agent (bản cũ)
- Agent đời cũ.
- **Chỉ** gửi **log** lên **CloudWatch Logs**.

### B) CloudWatch Unified Agent (bản mới)
- Agent đời mới.
- Gửi **log** lên **CloudWatch Logs**.
- Đồng thời thu thập **metric ở mức hệ thống** (chi tiết hơn so với monitoring mặc định của EC2).
- Dễ cấu hình tập trung hơn nhờ **SSM Parameter Store**.

## 4) Unified Agent thu thêm được những metric nào?
> Không cần học thuộc từng tên metric con; điều quan trọng là **độ chi tiết** và các **nhóm metric bổ sung** (như memory/swap/processes).

- **CPU** (chi tiết hơn): active, guest, idle, system, user, steal
- **Disk**: free, used, total
- **Disk I/O**: writes, reads, bytes, IOPS
- **RAM**: free, inactive, used, total, cached
- **Netstats**: số kết nối TCP/UDP, packets, bytes
- **Processes**: số lượng / trạng thái như dead, blocked, idle, running, sleep
- **Swap space**: free, used, % used

## 5) Khi nào nên nghĩ tới “Unified Agent”?
- Khi bạn cần **metric chi tiết hơn** so với monitoring mặc định của EC2.
- Monitoring mặc định của EC2 có metric mức cao cho **CPU / disk / network**, nhưng **không có memory và swap**.

## 6) Tự kiểm tra nhanh (ôn tập)
- Vì sao EC2 không tự gửi log lên CloudWatch theo mặc định?
- Instance cần IAM role như thế nào để ship log?
- Điểm khác nhau chính giữa Logs Agent và Unified Agent là gì?
- Kể tên 3 nhóm metric mà Unified Agent bổ sung so với mặc định.
