# Giải Thích AWS Route 53 TTL (Time To Live)

## Giới Thiệu

Trong hướng dẫn này, chúng ta sẽ tìm hiểu về DNS TTL (Time To Live) và cách nó hoạt động với AWS Route 53. Chúng ta sẽ đề cập đến lý thuyết về TTL và thực hành với một ví dụ cụ thể.

## TTL Là Gì?

TTL của bản ghi DNS là giá trị **Time To Live** (Thời Gian Tồn Tại) xác định thời gian một phản hồi DNS được lưu cache bởi client.

### Cách TTL Hoạt Động

Hãy xem xét một ví dụ trong đó client truy cập web server thông qua DNS Route 53:

1. **Yêu Cầu DNS**: Client thực hiện yêu cầu DNS cho `myapp.example.com`
2. **Phản Hồi DNS**: Route 53 phản hồi với:
   - Một bản ghi A
   - Địa chỉ IP
   - Giá trị TTL (ví dụ: 300 giây)
3. **Client Cache**: Client lưu cache kết quả trong khoảng thời gian TTL
4. **Các Yêu Cầu Tiếp Theo**: Trong thời gian cache, client không truy vấn DNS nữa - nó sử dụng phản hồi đã được cache

### Tại Sao Sử Dụng TTL?

Mục đích của TTL là giảm các truy vấn DNS không cần thiết. Vì các bản ghi DNS không thay đổi thường xuyên, việc cache phản hồi giúp cải thiện hiệu suất và giảm lưu lượng đến hệ thống DNS.

## Đánh Đổi Khi Chọn Giá Trị TTL

Việc chọn giá trị TTL phù hợp liên quan đến việc cân bằng hai yếu tố:

### TTL Cao (ví dụ: 24 giờ)

**Ưu Điểm:**
- Ít lưu lượng đến Route 53
- Ít truy vấn DNS từ client
- Chi phí thấp hơn (Route 53 tính phí theo số truy vấn)

**Nhược Điểm:**
- Bản ghi có thể bị lỗi thời
- Thay đổi mất tới 24 giờ để lan truyền
- Khó thực hiện cập nhật nhanh

### TTL Thấp (ví dụ: 60 giây)

**Ưu Điểm:**
- Bản ghi luôn cập nhật
- Thay đổi lan truyền nhanh
- Dễ dàng cập nhật bản ghi

**Nhược Điểm:**
- Nhiều lưu lượng đến Route 53
- Chi phí cao hơn do nhiều truy vấn
- Tăng tải cho DNS server

## Chiến Lược Thay Đổi TTL

Khi lên kế hoạch thay đổi bản ghi DNS:

1. **Giảm TTL** 24 giờ trước khi thay đổi (ví dụ: từ 24 giờ xuống 60 giây)
2. **Chờ đợi** TTL thấp lan truyền đến tất cả client
3. **Cập nhật bản ghi** - thay đổi sẽ lan truyền nhanh chóng
4. **Tăng TTL** trở lại giá trị ban đầu sau khi hoàn thành thay đổi

## Lưu Ý Quan Trọng

- TTL là **bắt buộc** cho mọi bản ghi DNS
- **Ngoại lệ**: Bản ghi Alias (sẽ được đề cập trong bài giảng riêng) không yêu cầu TTL

## Thực Hành Demo

### Tạo Bản Ghi Thử Nghiệm

Hãy tạo một bản ghi demo để quan sát hành vi của TTL:

1. **Tên Bản Ghi**: `demo.stephanetheteacher.com`
2. **Loại Bản Ghi**: Bản ghi A
3. **Giá Trị**: Địa chỉ IP của EC2 instance trong `eu-central-1`
4. **TTL**: 120 giây (2 phút)

### Kiểm Tra Bản Ghi

#### Sử Dụng Trình Duyệt Web

Truy cập `demo.stephanetheteacher.com` trên Google Chrome - bạn sẽ thấy ứng dụng chạy trên instance eu-central-1.

#### Sử Dụng Công Cụ Dòng Lệnh

**Lệnh nslookup:**
```bash
nslookup demo.stephanetheteacher.com
```

**Lệnh dig:**
```bash
dig demo.stephanetheteacher.com
```

Lệnh `dig` hiển thị TTL còn lại trong phần answer. Ví dụ, nếu bạn thấy `115`, có nghĩa là bản ghi sẽ được cache thêm 115 giây nữa.

### Quan Sát TTL Hoạt Động

1. **Truy Vấn Đầu Tiên**: Chạy `dig` - bạn có thể thấy TTL là 115 giây
2. **Truy Vấn Lại**: Chạy `dig` ngay lập tức - TTL giảm xuống 98 giây (hoặc tương tự)
3. **Thay Đổi Bản Ghi**: Chỉnh sửa bản ghi để trỏ đến IP khác (ví dụ: ap-southeast-1)
4. **Truy Vấn Lại**: Mặc dù đã cập nhật, IP cũ vẫn được trả về vì nó được cache
5. **Chờ TTL Hết Hạn**: Sau khi cache hết hạn (120 giây), IP mới được trả về

### Kết Quả Sau Khi TTL Hết Hạn

Sau khi chờ TTL hết hạn:

- **Trình Duyệt Web**: Refresh hiển thị instance mới (ap-southeast-1b)
- **Lệnh dig**: Hiển thị TTL mới là 120 giây và địa chỉ IP mới
- **CloudShell**: Xác nhận bản ghi DNS hiện trỏ đến server mới

## Những Điểm Chính Cần Nhớ

1. **TTL kiểm soát cache**: Nó xác định thời gian client cache phản hồi DNS
2. **Cân bằng là quan trọng**: Chọn giá trị TTL dựa trên tần suất cập nhật và chi phí
3. **Thay đổi không tức thì**: Thay đổi DNS mất thời gian để lan truyền dựa trên TTL
4. **Lên kế hoạch trước**: Giảm TTL trước khi thực hiện thay đổi quan trọng
5. **Sử dụng dig/nslookup**: Các công cụ này giúp xác minh thay đổi DNS và giám sát TTL

## Kết Luận

Hiểu về TTL là rất quan trọng để quản lý bản ghi DNS hiệu quả trong AWS Route 53. Giá trị TTL phù hợp phụ thuộc vào trường hợp sử dụng cụ thể của bạn - tần suất cập nhật bản ghi so với chi phí lưu lượng DNS mà bạn sẵn sàng chi trả.

Trong bài giảng tiếp theo, chúng ta sẽ khám phá bản ghi Alias, một loại bản ghi DNS đặc biệt không yêu cầu cấu hình TTL.