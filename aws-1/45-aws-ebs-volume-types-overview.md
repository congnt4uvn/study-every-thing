# Tổng Quan Các Loại Ổ Đĩa EBS Trên AWS

## Giới Thiệu

Các ổ đĩa Amazon EBS (Elastic Block Store) có sáu loại khác nhau, có thể được nhóm thành nhiều danh mục dựa trên đặc điểm hiệu suất và trường hợp sử dụng.

## Các Danh Mục Ổ Đĩa EBS

### SSD Đa Năng (gp2/gp3)
Ổ đĩa SSD đa năng cân bằng giữa giá cả và hiệu suất cho nhiều loại khối lượng công việc khác nhau.

#### GP3 (Thế Hệ Mới Hơn)
- **Hiệu Suất Cơ Bản**: 3,000 IOPS và thông lượng 125 MB/s
- **Hiệu Suất Tối Đa**: Lên đến 16,000 IOPS và thông lượng 1,000 MB/s
- **Tính Năng Chính**: IOPS và thông lượng có thể tăng **độc lập** với nhau
- **Phạm Vi Kích Thước**: 1 GB đến 16 TB

#### GP2 (Thế Hệ Cũ Hơn)
- **Hiệu Suất**: Các ổ đĩa gp2 nhỏ có thể tăng đột biến lên đến 3,000 IOPS
- **Tính Năng Chính**: Kích thước ổ đĩa và IOPS **liên kết với nhau**
- **Tính Toán IOPS**: 3 IOPS mỗi GB
- **IOPS Tối Đa**: 16,000 IOPS (đạt được ở mức 5,334 GB)
- **Phạm Vi Kích Thước**: 1 GB đến 16 TB

**Trường Hợp Sử Dụng**:
- Ổ đĩa khởi động hệ thống
- Máy tính để bàn ảo
- Môi trường phát triển và thử nghiệm
- Lưu trữ tiết kiệm chi phí với độ trễ thấp

### SSD IOPS Được Cung Cấp (io1/io2)
Ổ đĩa SSD hiệu suất cao nhất được thiết kế cho các khối lượng công việc quan trọng, độ trễ thấp và thông lượng cao.

#### IO1
- **Phạm Vi Kích Thước**: 4 GB đến 16 TB
- **IOPS Tối Đa**: 
  - 64,000 IOPS cho các instance EC2 Nitro
  - 32,000 IOPS cho các instance khác
- **Tính Năng Chính**: IOPS được cung cấp có thể tăng độc lập với kích thước lưu trữ

#### IO2 Block Express
- **Phạm Vi Kích Thước**: Lên đến 64 TB
- **Độ Trễ**: Độ trễ dưới mili giây
- **IOPS Tối Đa**: 256,000 IOPS
- **Tỷ Lệ IOPS/GB**: 1,000:1
- **Tính Năng Đặc Biệt**: Hỗ trợ EBS multi-attach

**Trường Hợp Sử Dụng**:
- Ứng dụng kinh doanh quan trọng yêu cầu hiệu suất IOPS bền vững
- Ứng dụng cần hơn 16,000 IOPS
- Khối lượng công việc cơ sở dữ liệu nhạy cảm với hiệu suất và tính nhất quán của lưu trữ

### HDD Tối Ưu Hóa Thông Lượng (st1)
Ổ đĩa HDD chi phí thấp được thiết kế cho các khối lượng công việc tập trung vào thông lượng, được truy cập thường xuyên.

- **Phạm Vi Kích Thước**: Lên đến 16 TB
- **Thông Lượng Tối Đa**: 500 MB/s
- **IOPS Tối Đa**: 500
- **Không thể sử dụng làm ổ đĩa khởi động**

**Trường Hợp Sử Dụng**:
- Dữ liệu lớn (Big data)
- Kho dữ liệu
- Xử lý nhật ký

### HDD Lạnh (sc1)
Ổ đĩa HDD chi phí thấp nhất được thiết kế cho các khối lượng công việc ít được truy cập.

- **Phạm Vi Kích Thước**: Lên đến 16 TB
- **Thông Lượng Tối Đa**: 250 MB/s
- **IOPS Tối Đa**: 250
- **Không thể sử dụng làm ổ đĩa khởi động**

**Trường Hợp Sử Dụng**:
- Dữ liệu lưu trữ
- Dữ liệu ít được truy cập
- Các tình huống yêu cầu chi phí thấp nhất có thể

## Các Yếu Tố Chính Để Xác Định Ổ Đĩa EBS

1. **Kích Thước**: Dung lượng lưu trữ (GB đến TB)
2. **Thông Lượng**: Tốc độ truyền dữ liệu (MB/s)
3. **IOPS**: Số Thao Tác Đầu Vào/Đầu Ra Mỗi Giây

## Yêu Cầu Ổ Đĩa Khởi Động

Chỉ các loại ổ đĩa sau có thể được sử dụng làm ổ đĩa khởi động (nơi hệ điều hành gốc chạy):
- GP2
- GP3
- IO1
- IO2

## Lưu Ý Quan Trọng Cho Kỳ Thi

- **SSD Đa Năng (gp2/gp3)**: Lưu trữ tiết kiệm chi phí với độ trễ thấp
  - GP3 cho phép cài đặt IOPS và thông lượng độc lập
  - GP2 liên kết IOPS với kích thước ổ đĩa

- **SSD IOPS Được Cung Cấp (io1/io2)**: Cho các ứng dụng kinh doanh quan trọng
  - Sử dụng khi bạn cần hơn 16,000 IOPS
  - Lý tưởng cho khối lượng công việc cơ sở dữ liệu yêu cầu hiệu suất nhất quán

- **Ổ Đĩa HDD (st1/sc1)**: Cho các tình huống thông lượng cao hoặc chi phí thấp nhất
  - Không thể sử dụng làm ổ đĩa khởi động

- **Yêu Cầu IOPS Cao**: Để có được hơn 32,000 IOPS, bạn cần các instance EC2 Nitro với io1 hoặc io2

## Tổng Kết

Hiểu sự khác biệt giữa các loại ổ đĩa EBS là rất quan trọng:
- **SSD Đa Năng** vs **SSD IOPS Được Cung Cấp** (cho cơ sở dữ liệu)
- **HDD Tối Ưu Hóa Thông Lượng** vs **HDD Lạnh** (cho thông lượng cao vs chi phí thấp nhất)

Luôn tham khảo tài liệu AWS khi có nghi ngờ về các yêu cầu và cấu hình cụ thể.