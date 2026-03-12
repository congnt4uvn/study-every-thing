# Các Tùy Chọn Mua EC2 Instances

## Tổng Quan

AWS EC2 cung cấp nhiều tùy chọn mua khác nhau để tối ưu hóa chi phí dựa trên yêu cầu khối lượng công việc của bạn. Trong khi các instance on-demand cung cấp tính linh hoạt, các tùy chọn khác có thể giảm đáng kể chi phí cho các trường hợp sử dụng khác nhau.

## Tóm Tắt Các Tùy Chọn Mua

### 1. **On-Demand Instances (Instance Theo Yêu Cầu)**
- **Trường Hợp Sử Dụng**: Khối lượng công việc ngắn hạn với giá cả có thể dự đoán
- **Tính Phí**: Thanh toán theo giây (Linux/Windows sau phút đầu tiên) hoặc theo giờ (các HĐH khác)
- **Lợi Ích**: 
  - Không cần thanh toán trước
  - Không có cam kết dài hạn
  - Tính linh hoạt cao nhất
- **Phù Hợp Nhất Cho**: Khối lượng công việc ngắn hạn, không bị gián đoạn khi hành vi ứng dụng không thể dự đoán

### 2. **Reserved Instances (Instance Dự Trữ - RI)**
- **Thời Hạn**: 1 hoặc 3 năm
- **Giảm Giá**: Lên đến 72% so với on-demand
- **Trường Hợp Sử Dụng**: Khối lượng công việc dài hạn (ví dụ: cơ sở dữ liệu)
- **Thuộc Tính Đặt Trước**:
  - Loại instance
  - Khu vực (Region)
  - Tenancy
  - Hệ điều hành
- **Tùy Chọn Thanh Toán**:
  - Tất cả trả trước (giảm giá tối đa)
  - Một phần trả trước
  - Không trả trước
- **Tùy Chọn Phạm Vi**:
  - Khu vực (Regional)
  - Vùng cụ thể (Zonal - dự trữ dung lượng trong AZ cụ thể)
- **Tính Năng Bổ Sung**: Có thể mua/bán trên RI Marketplace
- **Phù Hợp Nhất Cho**: Các ứng dụng sử dụng ổn định

#### Convertible Reserved Instances (Instance Dự Trữ Có Thể Chuyển Đổi)
- **Giảm Giá**: Lên đến 66%
- **Tính Linh Hoạt**: Có thể thay đổi:
  - Loại instance
  - Họ instance
  - Hệ điều hành
  - Phạm vi
  - Tenancy

### 3. **EC2 Savings Plans (Kế Hoạch Tiết Kiệm EC2)**
- **Thời Hạn**: 1 hoặc 3 năm
- **Giảm Giá**: Lên đến 72%
- **Cam Kết**: Số tiền cụ thể mỗi giờ (ví dụ: $10/giờ)
- **Bị Khóa**: Họ instance và khu vực (ví dụ: M5 trong us-east-1)
- **Linh Hoạt**:
  - Kích thước instance (m5.xlarge, m5.2xlarge, v.v.)
  - Hệ điều hành
  - Tenancy (host, dedicated, default)
- **Vượt Mức**: Sử dụng vượt kế hoạch được tính theo giá on-demand
- **Phù Hợp Nhất Cho**: Khối lượng công việc dài hạn với tính linh hoạt hiện đại hơn

### 4. **Spot Instances (Instance Giá Thầu)**
- **Giảm Giá**: Lên đến 90% so với on-demand
- **Rủi Ro**: Có thể mất instance bất cứ lúc nào nếu giá spot vượt quá giá tối đa của bạn
- **Trường Hợp Sử Dụng**: Khối lượng công việc có khả năng chịu lỗi
- **Phù Hợp Cho**:
  - Công việc xử lý theo lô (Batch jobs)
  - Phân tích dữ liệu
  - Xử lý hình ảnh
  - Khối lượng công việc phân tán
  - Khối lượng công việc có thời gian bắt đầu/kết thúc linh hoạt
- **Không Phù Hợp Cho**: Công việc quan trọng hoặc cơ sở dữ liệu
- **Lưu Ý**: Tùy chọn tiết kiệm chi phí nhất trong AWS

### 5. **Dedicated Hosts (Máy Chủ Chuyên Dụng)**
- **Mô Tả**: Máy chủ vật lý với dung lượng EC2 hoàn toàn dành riêng cho bạn
- **Trường Hợp Sử Dụng**:
  - Yêu cầu tuân thủ (compliance)
  - Giấy phép phần mềm gắn với máy chủ (per-socket, per-core, per-VM)
  - Mang Giấy Phép Của Riêng Bạn (BYOL - Bring Your Own License)
  - Nhu cầu tuân thủ/quy định nghiêm ngặt
- **Thanh Toán**: On-demand (theo giây) hoặc Reserved (1-3 năm)
- **Chi Phí**: Tùy chọn đắt nhất
- **Truy Cập**: Có thể nhìn thấy phần cứng cấp thấp hơn

### 6. **Dedicated Instances (Instance Chuyên Dụng)**
- **Mô Tả**: Các instance chạy trên phần cứng dành riêng cho bạn
- **Khác Biệt với Dedicated Hosts**: 
  - Có thể chia sẻ phần cứng với các instance khác trong cùng tài khoản
  - Không kiểm soát vị trí đặt instance
  - Không thấy được máy chủ vật lý
- **Trường Hợp Sử Dụng**: Cách ly phần cứng mà không cần truy cập máy chủ vật lý

### 7. **Capacity Reservations (Đặt Trước Dung Lượng)**
- **Mô Tả**: Đặt trước các instance on-demand trong AZ cụ thể
- **Thời Hạn**: Bất kỳ thời hạn nào (không có cam kết thời gian)
- **Cam Kết**: Có thể đặt trước hoặc hủy bất cứ lúc nào
- **Tính Phí**: Giá on-demand (được tính phí cho dù bạn có chạy instance hay không)
- **Giảm Giá**: Không có (kết hợp với Regional RI hoặc Savings Plans để được giảm giá)
- **Phù Hợp Nhất Cho**: Khối lượng công việc ngắn hạn, không bị gián đoạn trong AZ cụ thể

## Ví Dụ Tương Tự Resort

Để hiểu rõ hơn các tùy chọn này, hãy nghĩ về một khu nghỉ dưỡng:

- **On-Demand**: Đến và ở bất cứ khi nào bạn thích, trả giá đầy đủ
- **Reserved**: Lên kế hoạch trước cho thời gian ở dài (1-3 năm), được giảm giá cho cam kết
- **Savings Plan**: Cam kết chi $300/tháng trong 12 tháng, có thể đổi loại phòng
- **Spot**: Giảm giá phút chót cho phòng trống, nhưng có thể bị đuổi ra nếu ai đó trả nhiều hơn
- **Dedicated Host**: Đặt toàn bộ tòa nhà của khu nghỉ dưỡng
- **Capacity Reservation**: Đặt phòng bạn có thể không sử dụng, trả giá đầy đủ để đảm bảo có sẵn

## Ví Dụ So Sánh Giá

Dựa trên m4.large trong us-east-1 (giá chỉ mang tính minh họa):

| Tùy Chọn | Giá | Giảm Giá |
|----------|-----|----------|
| On-Demand | $0.10/giờ | Cơ sở |
| Spot | ~$0.04/giờ | Lên đến 61% |
| Reserved (1 năm, không trả trước) | Khác nhau | ~40% |
| Reserved (3 năm, tất cả trả trước) | Khác nhau | ~72% |
| Convertible RI | Khác nhau | ~66% |
| Savings Plan | Giống RI | ~72% |
| Dedicated Host | $0.10/giờ | 0% |
| Dedicated Host Reserved | Khác nhau | ~70% |
| Capacity Reservation | $0.10/giờ | 0% |

## Điểm Chính Cần Nhớ

1. **Tối Ưu Hóa Chi Phí**: Chọn dựa trên đặc điểm khối lượng công việc
2. **Cam Kết vs Linh Hoạt**: Cam kết dài hơn = giảm giá cao hơn
3. **Phù Hợp Khối Lượng Công Việc**: Khớp loại instance với yêu cầu khối lượng công việc
4. **Nhu Cầu Tuân Thủ**: Sử dụng Dedicated Hosts/Instances khi cần thiết
5. **Lập Kế Hoạch Dung Lượng**: Sử dụng Capacity Reservations cho khối lượng công việc quan trọng trong AZ cụ thể

## Mẹo Cho Kỳ Thi

- Hiểu tùy chọn nào phù hợp với từng loại khối lượng công việc cụ thể
- Nhớ rằng Spot Instances KHÔNG phù hợp cho công việc quan trọng/cơ sở dữ liệu
- Biết sự khác biệt giữa Dedicated Hosts và Dedicated Instances
- Hiểu thời gian cam kết và mức giảm giá
- Nhận biết các trường hợp sử dụng cho từng tùy chọn mua