# Tổng Quan về EC2 Instance Store

## Giới Thiệu

Mặc dù các EBS volume cung cấp lưu trữ gắn qua mạng cho các EC2 instance với hiệu suất tốt, nhưng có những tình huống yêu cầu hiệu suất cao hơn nữa. Đây là lúc **EC2 Instance Store** xuất hiện - một ổ đĩa cứng được gắn vật lý trực tiếp vào máy chủ lưu trữ EC2 instance của bạn.

## EC2 Instance Store là gì?

EC2 Instance Store là một tùy chọn lưu trữ hiệu suất cao sử dụng các ổ đĩa cứng vật lý được gắn trực tiếp vào máy chủ vật lý lưu trữ EC2 instance của bạn. Không giống như các EBS volume được gắn qua mạng, Instance Store cung cấp kết nối phần cứng trực tiếp để đạt hiệu suất I/O tối đa.

## Đặc Điểm Chính

### Hiệu Suất
- **Hiệu suất I/O tốt hơn** so với các EBS volume
- Khả năng **thông lượng cao**
- Hiệu suất ổ đĩa cực kỳ cao cho các khối lượng công việc đòi hỏi khắt khe

**Ví dụ về Hiệu Suất:**
- Các loại instance như dòng `i3` với Instance Store có thể đạt:
  - Random Read IOPS: lên đến **3.3 triệu**
  - Random Write IOPS: lên đến **1.4 triệu**
- So sánh, các EBS gp2 volume có thể đạt: **32,000 IOPS**

### Lưu Trữ Tạm Thời (Ephemeral Storage)
- **Dữ liệu bị mất** khi EC2 instance bị dừng hoặc kết thúc
- Dữ liệu **không bền vững** - có tính chất tạm thời
- Không thể sử dụng cho lưu trữ lâu dài, bền vững

### Yếu Tố Rủi Ro
- Nếu máy chủ vật lý bị lỗi, bạn có nguy cơ **mất dữ liệu**
- Phần cứng gắn kèm sẽ bị lỗi cùng với máy chủ
- **Trách nhiệm của bạn** để triển khai các chiến lược sao lưu và sao chép

## Trường Hợp Sử Dụng

### Trường Hợp Sử Dụng Tốt ✓
- **Lưu trữ bộ đệm (Buffer)**
- **Dữ liệu cache**
- **Dữ liệu tạm (Scratch data)**
- **Nội dung tạm thời**
- Các khối lượng công việc tính toán hiệu suất cao
- Các ứng dụng yêu cầu IOPS cực kỳ cao

### Trường Hợp Sử Dụng Không Tốt ✗
- Lưu trữ dữ liệu lâu dài
- Dữ liệu quan trọng không có chiến lược sao lưu
- Dữ liệu cần tồn tại qua các lần dừng/khởi động instance

## Thực Hành Tốt Nhất

1. **Chiến Lược Sao Lưu**: Luôn triển khai cơ chế sao lưu mạnh mẽ
2. **Sao Chép Dữ Liệu**: Sao chép dữ liệu quan trọng vào lưu trữ bền vững (như EBS hoặc S3)
3. **Sử Dụng cho Dữ Liệu Tạm**: Chỉ lưu trữ dữ liệu có thể tái tạo hoặc là tạm thời
4. **Giám Sát Sức Khỏe**: Theo dõi tình trạng instance và phần cứng

## So Sánh với EBS

| Tính Năng | EC2 Instance Store | EBS Volume |
|-----------|-------------------|------------|
| **Hiệu Suất** | Cực kỳ cao (hàng triệu IOPS) | Cao (lên đến 32k IOPS cho gp2) |
| **Độ Bền** | Tạm thời - mất khi dừng/kết thúc | Bền vững - tồn tại qua vòng đời instance |
| **Trường Hợp Sử Dụng** | Khối lượng công việc tạm thời, hiệu suất cao | Lưu trữ lâu dài |
| **Kết Nối** | Gắn phần cứng vật lý | Gắn qua mạng |
| **Sao Lưu** | Thủ công, trách nhiệm của bạn | Có snapshot |

## Mẹo Cho Kỳ Thi

- Khi bạn thấy yêu cầu về **các volume gắn phần cứng hiệu suất rất cao**, hãy nghĩ đến **EC2 Instance Store**
- Nhớ **tính chất tạm thời** - dữ liệu bị mất khi dừng/kết thúc
- Hiểu **sự đánh đổi**: hiệu suất so với độ bền vững

## Kết Luận

EC2 Instance Store là một tùy chọn mạnh mẽ cho các khối lượng công việc yêu cầu hiệu suất I/O cực cao. Tuy nhiên, tính chất tạm thời của nó có nghĩa là nó chỉ nên được sử dụng cho dữ liệu tạm thời hoặc kết hợp với chiến lược sao lưu và sao chép vững chắc. Đối với nhu cầu lưu trữ lâu dài, các EBS volume vẫn là lựa chọn tốt hơn.