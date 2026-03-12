# Các Tùy Chọn Nâng Cao của AWS CloudFront

## Tổng quan

Tài liệu này trình bày các tùy chọn cấu hình nâng cao của CloudFront bao gồm định giá, các lớp giá, nhiều nguồn gốc, nhóm nguồn gốc và mã hóa cấp trường.

---

## Định Giá và Lớp Giá của CloudFront

### Hiểu về Định Giá CloudFront

Các edge location của CloudFront được phân bố toàn cầu, và chi phí truyền dữ liệu thay đổi theo khu vực địa lý và vị trí edge location.

#### Ví dụ Định Giá theo Khu Vực

- **Hoa Kỳ, Canada và Mexico**: $0.085/GB cho 10 TB đầu tiên
- **Ấn Độ**: $0.170/GB cho 10 TB đầu tiên (khoảng gấp 2 lần chi phí ở Mỹ)
- **Giảm giá theo Khối lượng**: Giá giảm khi lượng truyền dữ liệu tăng
  - Trên 5 PB được truyền từ Mỹ: $0.020/GB

**Nguyên tắc Chính**: Chi phí truyền dữ liệu tăng từ trái sang phải trên bảng giá, với một số khu vực đắt hơn đáng kể so với các khu vực khác.

### Các Lớp Giá CloudFront

Bạn có thể giảm chi phí bằng cách giới hạn số lượng edge location được sử dụng cho phân phối CloudFront của mình. Ba lớp giá có sẵn:

#### Lớp Giá All (Tất cả)
- **Phủ sóng**: Tất cả các khu vực trên toàn thế giới
- **Hiệu suất**: Hiệu suất tốt nhất
- **Chi phí**: Chi phí cao nhất (bao gồm các khu vực đắt tiền)

#### Lớp Giá 200
- **Phủ sóng**: Hầu hết các khu vực
- **Loại trừ**: Loại trừ các khu vực đắt nhất
- **Chi phí**: Tùy chọn chi phí trung bình

#### Lớp Giá 100
- **Phủ sóng**: Chỉ các khu vực rẻ nhất
- **Khu vực**: Châu Mỹ, Bắc Mỹ và Châu Âu
- **Chi phí**: Tùy chọn chi phí thấp nhất

---

## Nhiều Nguồn Gốc trong CloudFront

### Trường hợp Sử dụng: Định tuyến Dựa trên Nội dung

CloudFront cho phép bạn định tuyến đến các nguồn gốc khác nhau dựa trên loại nội dung hoặc mẫu đường dẫn.

### Ví dụ Cấu hình

Bạn có thể thiết lập các hành vi bộ nhớ cache khác nhau với các mẫu đường dẫn cụ thể:

- **`/images/*`** → S3 bucket cho hình ảnh tĩnh
- **`/api/*`** → Application Load Balancer cho các yêu cầu API
- **`/*`** (mặc định) → S3 bucket cho tất cả nội dung tĩnh khác

Điều này cho phép định tuyến hiệu quả trong đó:
- Các yêu cầu API đi đến Application Load Balancer của bạn
- Nội dung tĩnh được phục vụ từ các S3 bucket

---

## Nhóm Nguồn Gốc (Origin Groups)

### Mục đích

Nhóm nguồn gốc cung cấp tính khả dụng cao và chuyển đổi dự phòng tự động khi nguồn gốc chính bị lỗi.

### Kiến trúc

Một nhóm nguồn gốc bao gồm:
- **Nguồn Gốc Chính**: Lựa chọn đầu tiên để phục vụ yêu cầu
- **Nguồn Gốc Phụ**: Tùy chọn sao lưu để chuyển đổi dự phòng

### Cách Hoạt động

1. CloudFront gửi yêu cầu đến nguồn gốc chính
2. Nếu nguồn gốc chính trả về lỗi, CloudFront tự động thử lại yêu cầu với nguồn gốc phụ
3. Nguồn gốc phụ phản hồi với mã trạng thái thành công

### Ví dụ 1: Các EC2 Instance với Chuyển đổi Dự phòng

- **Nguồn Gốc Chính**: EC2 Instance A
- **Nguồn Gốc Phụ**: EC2 Instance B
- **Lợi ích**: Tính khả dụng cao ở cấp ứng dụng

### Ví dụ 2: S3 Đa Khu vực với Khôi phục Thảm họa

Kiến trúc này cung cấp tính khả dụng cao ở cấp khu vực:

**Thiết lập**:
- **Nguồn Gốc Chính**: S3 bucket ở Khu vực A
- **Nguồn Gốc Phụ**: S3 bucket ở Khu vực B
- **Sao chép**: Sao chép S3 giữa các khu vực

**Quy trình Chuyển đổi Dự phòng**:
1. CloudFront yêu cầu từ S3 bucket chính (Khu vực A)
2. Nếu xảy ra sự cố ở cấp khu vực, yêu cầu thất bại
3. CloudFront tự động yêu cầu từ S3 bucket phụ (Khu vực B)
4. Bucket phụ có dữ liệu được sao chép và phản hồi thành công

**Lợi ích**: Khôi phục thảm họa ở cấp khu vực cho kiến trúc CloudFront và S3

---

## Mã Hóa Cấp Trường (Field-Level Encryption)

### Mục đích

Mã hóa cấp trường bảo vệ thông tin nhạy cảm trong toàn bộ ngăn xếp ứng dụng, thêm một lớp bảo mật bổ sung ngoài mã hóa HTTPS trong quá trình truyền.

### Cách Hoạt động

- Sử dụng **mã hóa bất đối xứng**
- Edge location mã hóa các trường cụ thể bằng **khóa công khai**
- Chỉ các thực thể có **khóa riêng tư** mới có thể giải mã dữ liệu

### Cấu hình

- Chỉ định tối đa **10 trường** để mã hóa (ví dụ: số thẻ tín dụng)
- Cung cấp khóa công khai để mã hóa
- Áp dụng cho các yêu cầu POST được gửi đến CloudFront

### Ví dụ: Bảo vệ Thẻ Tín dụng

**Luồng Kiến trúc**:
1. **Client** → HTTPS → **Edge Location**
2. **Edge Location** → HTTPS → **CloudFront**
3. **CloudFront** → HTTPS → **Application Load Balancer**
4. **Application Load Balancer** → HTTPS → **Web Server**

**Quy trình Mã hóa**:

1. Người dùng gửi thông tin thẻ tín dụng qua HTTPS
2. Edge location mã hóa trường thẻ tín dụng bằng khóa công khai
3. Trường được mã hóa đi qua:
   - CloudFront
   - Application Load Balancer
   - Web Server
4. **Chỉ web server** (có khóa riêng tư) mới có thể giải mã trường

### Lợi ích Bảo mật

- **Bảo vệ end-to-end**: Dữ liệu nhạy cảm được mã hóa tại edge
- **Truy cập giải mã hạn chế**: Chỉ web server mới có thể giải mã
- **Phòng thủ nhiều lớp**: CloudFront và ALB không thể truy cập dữ liệu đã mã hóa
- **Logic ứng dụng tùy chỉnh**: Web server xử lý giải mã với khóa riêng tư

---

## Tóm tắt

Các tùy chọn nâng cao của CloudFront cung cấp:
- **Tối ưu hóa chi phí** thông qua lựa chọn lớp giá
- **Định tuyến linh hoạt** với nhiều nguồn gốc
- **Tính khả dụng cao** sử dụng nhóm nguồn gốc
- **Bảo mật nâng cao** với mã hóa cấp trường

Các tính năng này cho phép bạn xây dựng kiến trúc phân phối nội dung mạnh mẽ, hiệu quả về chi phí và an toàn trên AWS.