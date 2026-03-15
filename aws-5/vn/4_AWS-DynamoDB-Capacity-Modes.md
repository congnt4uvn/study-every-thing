# AWS DynamoDB - Chế Độ Dung Lượng Đọc và Ghi

## Tổng Quan

Chế độ dung lượng DynamoDB kiểm soát cách bảng của bạn xử lý thông lượng. Bạn có thể chọn giữa hai chế độ:

1. **Chế độ Provisioned (Đã Cung Cấp)** - Chỉ định thông lượng đọc và ghi trước
2. **Chế độ On-Demand (Theo Yêu Cầu)** - Tự động mở rộng dựa trên khối lượng công việc

> **Lưu ý:** Bạn có thể chuyển đổi giữa các chế độ mỗi 24 giờ một lần.

---

## Chế Độ Provisioned

### Khái Niệm Chính

- **RCU (Read Capacity Units - Đơn vị Dung lượng Đọc)** - Thông lượng cho đọc
- **WCU (Write Capacity Units - Đơn vị Dung lượng Ghi)** - Thông lượng cho ghi
- Bạn trả tiền cho những gì bạn cung cấp, bất kể mức sử dụng thực tế
- Có sẵn tính năng auto-scaling để đáp ứng nhu cầu
- **Burst Capacity (Dung lượng Đột biến)** - Dung lượng tạm thời có sẵn nếu vượt quá giới hạn đã cung cấp

### Khi Vượt Quá Dung Lượng

Nếu bạn cạn kiệt burst capacity, bạn sẽ nhận được:
- **`ProvisionedThroughputExceededException`**
- Giải pháp: Sử dụng **exponential backoff retry strategy (chiến lược thử lại với độ trễ tăng dần)**

---

## Write Capacity Units (WCU)

### Công Thức

**1 WCU = 1 lần ghi mỗi giây cho mục có kích thước tối đa 1 KB**

- Mục lớn hơn 1 KB sẽ tiêu thụ nhiều WCU hơn
- **Luôn làm tròn lên KB gần nhất**

### Ví Dụ

**Ví dụ 1:**
- Ghi 10 mục/giây
- Kích thước mục: 2 KB
- Tính toán: `10 × (2 KB / 1 KB) = 20 WCUs`

**Ví dụ 2:**
- Ghi 6 mục/giây
- Kích thước mục: 4.5 KB → làm tròn lên 5 KB
- Tính toán: `6 × (5 KB / 1 KB) = 30 WCUs`

**Ví dụ 3:**
- Ghi 120 mục/phút
- Kích thước mục: 2 KB
- Tính toán: `(120 / 60) × (2 KB / 1 KB) = 2 × 2 = 4 WCUs`

---

## Read Capacity Units (RCU)

### Các Loại Tính Nhất Quán Khi Đọc

#### Eventually Consistent Read (Đọc Nhất Quán Cuối Cùng) - Mặc định
- Có thể trả về dữ liệu cũ nếu đọc ngay sau khi ghi
- Dữ liệu thường nhất quán trong vòng ~100 mili giây
- **Tiết kiệm chi phí hơn**

#### Strongly Consistent Read (Đọc Nhất Quán Mạnh)
- Luôn trả về dữ liệu mới nhất
- Đặt tham số `ConsistentRead` thành `True` trong các lệnh gọi API
- Có sẵn cho: GetItem, BatchGetItem, Query, Scan
- **Tiêu thụ gấp đôi RCU**
- Có thể có độ trễ cao hơn một chút

### Công Thức

**1 RCU = Một trong những điều sau:**
- 1 lần đọc strongly consistent/giây cho mục tối đa 4 KB
- 2 lần đọc eventually consistent/giây cho mục tối đa 4 KB

- Mục lớn hơn 4 KB tiêu thụ nhiều RCU hơn
- **Luôn làm tròn lên 4 KB gần nhất**

### Ví Dụ

**Ví dụ 1: Đọc Strongly Consistent**
- 10 lần đọc strongly consistent/giây
- Kích thước mục: 4 KB
- Tính toán: `10 × (4 KB / 4 KB) = 10 RCUs`

**Ví dụ 2: Đọc Eventually Consistent**
- 16 lần đọc eventually consistent/giây
- Kích thước mục: 12 KB
- Tính toán: `(16 / 2) × (12 KB / 4 KB) = 8 × 3 = 24 RCUs`

**Ví dụ 3: Strongly Consistent với Làm Tròn**
- 10 lần đọc strongly consistent/giây
- Kích thước mục: 6 KB → làm tròn lên 8 KB
- Tính toán: `10 × (8 KB / 4 KB) = 10 × 2 = 20 RCUs`

---

## Partitions (Phân Vùng) trong DynamoDB

### Cách Hoạt Động của Partitions

- Bảng được chia thành các partition (phân phối trên nhiều server)
- **Partition key** đi qua hàm hash để xác định vị trí partition
- Dữ liệu được sao chép trên nhiều server

### Công Thức Phân Vùng (để tham khảo)

- Số partition theo dung lượng: `(RCU / 3000) + (WCU / 1000)`
- Số partition theo kích thước: `Tổng kích thước / 10 GB`
- Số partition cuối cùng = `max(theo-dung-lượng, theo-kích-thước)`

> **Quan trọng:** RCU và WCU được **phân bổ đều** trên các partition

### Ví Dụ
- 10 partition với 10 WCU và 10 RCU đã cung cấp
- Mỗi partition nhận được: 1 WCU và 1 RCU

---

## Throttling (Điều Tiết)

### Nguyên Nhân của `ProvisionedThroughputExceededException`

1. **Hot Key** - Một partition key được đọc/ghi quá thường xuyên
2. **Hot Partition** - Một partition nhận quá nhiều traffic
3. **Mục Rất Lớn** - Mục lớn tiêu thụ nhiều RCU/WCU hơn

### Giải Pháp

1. **Exponential Backoff** - Thử lại với độ trễ tăng dần (đã bao gồm trong SDK)
2. **Thiết Kế Partition Key Tốt Hơn** - Phân phối dữ liệu đều hơn
3. **DynamoDB Accelerator (DAX)** - Giải pháp caching cho khối lượng đọc lớn

---

## Chế Độ On-Demand

### Tính Năng Chính

- **Không cần lập kế hoạch dung lượng**
- Tự động mở rộng lên/xuống theo khối lượng công việc
- Không bị throttling (dung lượng không giới hạn)
- Trả tiền cho mỗi yêu cầu:
  - **RRU (Read Request Units - Đơn vị Yêu cầu Đọc)**
  - **WRU (Write Request Units - Đơn vị Yêu cầu Ghi)**

### Giá Cả

- Khoảng **đắt gấp 2.5 lần** so với chế độ provisioned

### Trường Hợp Sử Dụng Tốt Nhất

- Khối lượng công việc không xác định
- Traffic ứng dụng không thể dự đoán
- Ứng dụng mới không có lịch sử traffic
- Khối lượng công việc đột biến hoặc không thường xuyên

---

## Tóm Tắt

| Tính Năng | Chế Độ Provisioned | Chế Độ On-Demand |
|-----------|-------------------|------------------|
| **Lập Kế Hoạch Dung Lượng** | Bắt buộc (RCU/WCU) | Không bắt buộc |
| **Mở Rộng** | Auto-scaling có sẵn | Tự động |
| **Throttling** | Có (nếu vượt quá) | Không |
| **Giá Cả** | Trả cho dung lượng đã cung cấp | Trả mỗi yêu cầu (~đắt gấp 2.5 lần) |
| **Tốt Nhất Cho** | Khối lượng dự đoán được | Khối lượng không dự đoán/đột biến |

---

## Tham Khảo Nhanh

### Tính Toán WCU
```
WCU = (số mục mỗi giây) × (kích thước mục tính bằng KB làm tròn lên / 1 KB)
```

### Tính Toán RCU
```
Strongly Consistent:
RCU = (số mục mỗi giây) × (kích thước mục tính bằng KB làm tròn lên 4 KB / 4 KB)

Eventually Consistent:
RCU = (số mục mỗi giây / 2) × (kích thước mục tính bằng KB làm tròn lên 4 KB / 4 KB)
```
