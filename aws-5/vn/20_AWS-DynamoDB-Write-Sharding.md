# AWS DynamoDB Write Sharding

## Tổng quan
DynamoDB Write Sharding là chiến lược phân tán dữ liệu đều hơn qua các partition để tránh vấn đề hot partition.

## Vấn đề: Hot Partitions (Phân vùng nóng)

### Ví dụ Use Case
Xét một ứng dụng bầu cử với hai ứng viên:
- Ứng viên A
- Ứng viên B

### Vấn đề
Nếu sử dụng **ID Ứng viên** làm partition key:
- Tất cả phiếu bầu chỉ đi vào **2 partitions** (mỗi ứng viên một partition)
- Tạo ra **vấn đề hot partition** cho cả việc ghi và đọc
- Hiệu suất kém do phân phối không đều

## Giải pháp: Thêm Suffix hoặc Prefix vào Partition Key

### Chiến lược
Phân phối ID ứng viên tốt hơn qua các partition bằng cách thêm suffix hoặc prefix vào giá trị partition key.

### Ví dụ Triển khai
Thay vì:
- `candidate_A`
- `candidate_B`

Sử dụng:
- `candidate_A_11`
- `candidate_A_20`
- `candidate_B_17`
- `candidate_B_18`

### Kết quả
- Partition key nhận **nhiều giá trị unique hơn**
- Dữ liệu được **phân phối đầy đủ** trên bảng DynamoDB
- Hiệu suất **ghi và đọc tốt hơn**

## Phương pháp tạo Suffix/Prefix

### 1. Random Suffix (Hậu tố ngẫu nhiên)
- Tạo số ngẫu nhiên để thêm vào
- Triển khai đơn giản
- Đảm bảo phân phối

### 2. Calculated Suffix (Hậu tố được tính toán - Thuật toán Hash)
- Sử dụng thuật toán hash để tính suffix
- Phương pháp xác định
- Phân phối nhất quán

## Điểm chính cần nhớ
Mục tiêu là tạo ra một **partition key được phân phối cao** để tránh hot partition và đảm bảo hiệu suất tối ưu trong DynamoDB.

---

**Chủ đề**: AWS DynamoDB
**Khái niệm**: Chiến lược Write Sharding
**Cấp độ**: Trung cấp
