# AWS Route 53 - Chính Sách Định Tuyến Có Trọng Số (Weighted Routing Policy)

## Tổng Quan

**Chính sách định tuyến có trọng số (Weighted Routing Policy)** trong AWS Route 53 cho phép bạn kiểm soát phần trăm các yêu cầu được chuyển đến các tài nguyên cụ thể bằng cách sử dụng trọng số. Điều này cho phép phân phối lưu lượng chính xác trên nhiều điểm cuối.

## Cách Thức Hoạt Động

### Khái Niệm Cơ Bản

- Amazon Route 53 có thể phân phối lưu lượng truy cập trên nhiều EC2 instance (hoặc tài nguyên khác) dựa trên trọng số được gán
- Ví dụ: Ba EC2 instance với trọng số là 70, 20 và 10
- 70% phản hồi DNS chuyển hướng đến instance thứ nhất, 20% đến instance thứ hai và 10% đến instance thứ ba

### Tính Toán Trọng Số

Phần trăm lưu lượng gửi đến mỗi bản ghi được tính như sau:

```
Phần Trăm Lưu Lượng = (Trọng Số của Bản Ghi) / (Tổng Tất Cả Trọng Số)
```

**Lưu Ý Quan Trọng:**
- Trọng số không cần phải tổng bằng 100
- Trọng số là chỉ số tương đối của phân phối lưu lượng
- Các bản ghi DNS phải có cùng tên và loại
- Có thể được liên kết với health checks (kiểm tra sức khỏe)

## Các Trường Hợp Sử Dụng

1. **Cân Bằng Tải**: Phân phối lưu lượng trên các vùng khác nhau
2. **Kiểm Thử A/B**: Gửi một lượng nhỏ lưu lượng để kiểm tra phiên bản ứng dụng mới
3. **Di Chuyển Dần Dần**: Chuyển dịch lưu lượng theo thời gian bằng cách điều chỉnh trọng số
4. **Kiểm Soát Lưu Lượng**: Đặt trọng số về 0 để ngừng gửi lưu lượng đến tài nguyên cụ thể

**Trường Hợp Đặc Biệt**: Nếu tất cả các bản ghi tài nguyên có trọng số bằng 0, tất cả các bản ghi sẽ được trả về với trọng số bằng nhau.

## Hướng Dẫn Thực Hành

### Bước 1: Tạo Bản Ghi Có Trọng Số Đầu Tiên

1. Tạo bản ghi mới: `weighted.stephanetheteacher.com`
2. Loại bản ghi: **A record**
3. Chính sách định tuyến: **Weighted** (Có trọng số)
4. Giá trị: IP từ vùng `ap-southeast-1`
5. Trọng số: **10**
6. TTL: **3 giây** (chỉ để demo - không khuyến nghị cho môi trường production)
7. Record ID: **southeast**

### Bước 2: Tạo Bản Ghi Có Trọng Số Thứ Hai

1. Cùng tên miền: `weighted.stephanetheteacher.com`
2. Chính sách định tuyến: **Weighted**
3. Giá trị: IP từ vùng `us-east-1`
4. Trọng số: **70**
5. TTL: **3 giây**
6. Record ID: **US East**

### Bước 3: Tạo Bản Ghi Có Trọng Số Thứ Ba

1. Cùng tên miền: `weighted.stephanetheteacher.com`
2. Chính sách định tuyến: **Weighted**
3. Giá trị: IP từ vùng `eu-central-1`
4. Trọng số: **20**
5. TTL: **3 giây**
6. Record ID: **EU**

### Bước 4: Xác Minh Cấu Hình

Sau khi tạo các bản ghi, bạn sẽ thấy:
- **Ba bản ghi riêng biệt** trong bảng (khác với định tuyến đơn giản chỉ hiển thị một bản ghi với nhiều giá trị)
- Mỗi bản ghi có một giá trị với trọng số tương ứng (10, 20, 70)

## Kiểm Tra Định Tuyến Có Trọng Số

### Kiểm Tra Trên Trình Duyệt

1. Truy cập `weighted.stephanetheteacher.com`
2. Phản hồi đầu tiên có thể từ `us-east-1a` (trọng số 70%)
3. Làm mới trang mỗi 3 giây để thấy các phản hồi khác nhau
4. Đôi khi, bạn sẽ nhận được phản hồi từ các vùng khác dựa trên trọng số của chúng

### Kiểm Tra Bằng Dòng Lệnh

Sử dụng lệnh `dig` để xem phản hồi DNS:

```bash
dig weighted.stephanetheteacher.com
```

**Kết Quả Mong Đợi:**
- TTL là 3 giây
- Hầu hết phản hồi từ us-east-1 (xác suất 70%)
- Đôi khi có phản hồi từ eu-central-1 (xác suất 20%)
- Hiếm khi có phản hồi từ ap-southeast-1 (xác suất 10%)

## Những Điểm Chính Cần Nhớ

- Định tuyến có trọng số chuyển hướng hầu hết các truy vấn đến các bản ghi có trọng số cao hơn
- Các bản ghi khác vẫn nhận lưu lượng tỷ lệ thuận với trọng số của chúng
- Hệ thống hoạt động chính xác như thiết kế - cung cấp phân phối lưu lượng theo xác suất
- Hoàn hảo cho các kịch bản triển khai dần dần và cân bằng tải

## Những Lưu Ý Quan Trọng

- **Cài Đặt TTL**: TTL 3 giây được sử dụng trong demo này chỉ để minh họa. Hãy sử dụng giá trị TTL phù hợp trong môi trường production
- **Health Checks**: Có thể được liên kết với các bản ghi có trọng số để chuyển đổi dự phòng tự động
- **Trọng Số Bằng Không**: Đặt trọng số về 0 sẽ ngừng lưu lượng đến tài nguyên đó một cách hiệu quả

---

**Ghi Chú**: Chính sách định tuyến này thể hiện sức mạnh và tính linh hoạt của weighted records trong Route 53 cho các chiến lược quản lý lưu lượng phức tạp.