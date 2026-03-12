# Tổng Quan Các Lớp Lưu Trữ Amazon S3

## Giới Thiệu

Amazon S3 cung cấp nhiều lớp lưu trữ được thiết kế cho các trường hợp sử dụng khác nhau, mỗi lớp có các đặc điểm về tính khả dụng, độ bền và giá cả khác nhau. Hiểu rõ các lớp lưu trữ này là điều cần thiết để tối ưu hóa chi phí và hiệu suất.

## Các Lớp Lưu Trữ Có Sẵn

Amazon S3 cung cấp các lớp lưu trữ sau:

1. **Amazon S3 Standard - Mục Đích Chung**
2. **Amazon S3 - Infrequent Access (IA) - Truy Cập Không Thường Xuyên**
3. **Amazon S3 One Zone - Infrequent Access - Một Vùng Truy Cập Không Thường Xuyên**
4. **Amazon S3 Glacier Instant Retrieval - Truy Xuất Tức Thời**
5. **Amazon S3 Glacier Flexible Retrieval - Truy Xuất Linh Hoạt**
6. **Amazon S3 Glacier Deep Archive - Lưu Trữ Sâu**
7. **Amazon S3 Intelligent-Tiering - Phân Tầng Thông Minh**

### Quản Lý Các Lớp Lưu Trữ

Khi tạo một đối tượng trong Amazon S3, bạn có thể:
- Chọn lớp lưu trữ khi tạo
- Thay đổi lớp lưu trữ thủ công sau khi tạo
- Sử dụng **cấu hình Amazon S3 Lifecycle** để tự động di chuyển đối tượng giữa các lớp lưu trữ

## Khái Niệm Cơ Bản: Độ Bền và Tính Khả Dụng

### Độ Bền (Durability)

**Độ bền** thể hiện tần suất một đối tượng bị mất bởi Amazon S3.

- Amazon S3 có độ bền rất cao: **11 số 9 (99.999999999%)**
- Điều này có nghĩa là trung bình, nếu bạn lưu trữ 10 triệu đối tượng trên Amazon S3, bạn có thể mất một đối tượng duy nhất mỗi 10,000 năm
- **Độ bền giống nhau cho tất cả các lớp lưu trữ** trong Amazon S3

### Tính Khả Dụng (Availability)

**Tính khả dụng** thể hiện mức độ sẵn sàng của dịch vụ.

- Tính khả dụng thay đổi tùy thuộc vào lớp lưu trữ
- Ví dụ, S3 Standard có **tính khả dụng 99.99%**
- Điều này có nghĩa là khoảng 53 phút mỗi năm dịch vụ có thể không khả dụng
- Ứng dụng nên được thiết kế để xử lý các lỗi dịch vụ thỉnh thoảng

## Chi Tiết Các Lớp Lưu Trữ

### 1. Amazon S3 Standard - Mục Đích Chung

**Đặc điểm:**
- **Tính khả dụng:** 99.99%
- **Trường hợp sử dụng:** Dữ liệu được truy cập thường xuyên
- **Hiệu suất:** Độ trễ thấp và thông lượng cao
- **Khả năng phục hồi:** Có thể chịu được hai lỗi cơ sở vật chất đồng thời

**Phù hợp cho:**
- Phân tích dữ liệu lớn (Big data analytics)
- Ứng dụng di động và game
- Phân phối nội dung

### 2. Amazon S3 Standard - Infrequent Access (Standard-IA)

**Đặc điểm:**
- **Tính khả dụng:** 99.9% (thấp hơn một chút so với Standard)
- **Trường hợp sử dụng:** Dữ liệu được truy cập ít thường xuyên nhưng cần truy cập nhanh khi cần
- **Chi phí:** Chi phí lưu trữ thấp hơn S3 Standard, nhưng có phí truy xuất

**Phù hợp cho:**
- Khắc phục thảm họa (Disaster recovery)
- Sao lưu dự phòng (Backups)

### 3. Amazon S3 One Zone - Infrequent Access (One Zone-IA)

**Đặc điểm:**
- **Tính khả dụng:** 99.5%
- **Độ bền:** Độ bền cao chỉ trong một Vùng Khả Dụng (AZ)
- **Rủi ro:** Dữ liệu sẽ bị mất nếu AZ bị phá hủy
- **Chi phí:** Thấp hơn Standard-IA

**Phù hợp cho:**
- Bản sao lưu thứ cấp
- Sao lưu dữ liệu on-premises
- Dữ liệu có thể tái tạo được

## Các Lớp Lưu Trữ Glacier

Amazon Glacier cung cấp lưu trữ đối tượng chi phí thấp dành cho lưu trữ và sao lưu. Tất cả các lớp Glacier có:
- Chi phí lưu trữ cộng với chi phí truy xuất
- Yêu cầu thời gian lưu trữ tối thiểu

### 4. Amazon S3 Glacier Instant Retrieval - Truy Xuất Tức Thời

**Đặc điểm:**
- **Thời gian truy xuất:** Mili giây
- **Thời gian lưu trữ tối thiểu:** 90 ngày
- **Trường hợp sử dụng:** Dữ liệu được truy cập một lần mỗi quý

**Phù hợp cho:**
- Sao lưu cần truy cập ngay lập tức
- Dữ liệu lưu trữ dài hạn với nhu cầu truy xuất tức thời

### 5. Amazon S3 Glacier Flexible Retrieval - Truy Xuất Linh Hoạt

Trước đây được gọi là "Amazon S3 Glacier"

**Các Tùy Chọn Truy Xuất:**
- **Expedited (Nhanh):** 1-5 phút
- **Standard (Tiêu chuẩn):** 3-5 giờ
- **Bulk (Hàng loạt):** 5-12 giờ (miễn phí)

**Đặc điểm:**
- **Thời gian lưu trữ tối thiểu:** 90 ngày
- Thời gian truy xuất linh hoạt dựa trên nhu cầu của bạn

### 6. Amazon S3 Glacier Deep Archive - Lưu Trữ Sâu

**Đặc điểm:**
- **Các Tùy Chọn Truy Xuất:**
  - Standard (Tiêu chuẩn): 12 giờ
  - Bulk (Hàng loạt): 48 giờ
- **Thời gian lưu trữ tối thiểu:** 180 ngày
- **Chi phí:** Tùy chọn lưu trữ có chi phí thấp nhất

**Phù hợp cho:**
- Lưu trữ dài hạn
- Dữ liệu hiếm khi cần truy cập
- Lưu trữ tuân thủ và quy định

## 7. Amazon S3 Intelligent-Tiering - Phân Tầng Thông Minh

Tự động di chuyển đối tượng giữa các tầng truy cập dựa trên mẫu sử dụng.

**Chi phí:**
- Phí giám sát hàng tháng nhỏ
- Phí tự động phân tầng nhỏ
- **Không có phí truy xuất**

**Các Tầng Tự Động:**
1. **Frequent Access Tier (Tầng Truy Cập Thường Xuyên)** - Tầng mặc định (tự động)
2. **Infrequent Access Tier (Tầng Truy Cập Không Thường Xuyên)** - Đối tượng không được truy cập trong 30 ngày (tự động)
3. **Archive Instant Access Tier (Tầng Lưu Trữ Truy Cập Tức Thời)** - Đối tượng không được truy cập trong 90 ngày (tự động)

**Các Tầng Tùy Chọn** (có thể cấu hình):
4. **Archive Access Tier (Tầng Truy Cập Lưu Trữ)** - Có thể cấu hình từ 90 đến 700+ ngày
5. **Deep Archive Access Tier (Tầng Truy Cập Lưu Trữ Sâu)** - Có thể cấu hình từ 180 đến 700+ ngày

**Phù hợp cho:**
- Mẫu truy cập không thể dự đoán
- Tối ưu hóa chi phí tự động mà không cần can thiệp thủ công

## Tổng Kết So Sánh

### Điểm Chính

- **Độ bền:** 11 số 9 (99.999999999%) trên tất cả các lớp lưu trữ
- **Tính khả dụng:** Thay đổi theo lớp lưu trữ - giảm khi có ít vùng hơn
- **Thời gian lưu trữ tối thiểu:** Thay đổi theo lớp (0, 90 hoặc 180 ngày)
- **Giá cả:** Thường giảm với thời gian truy xuất dài hơn và tính khả dụng thấp hơn

### Lưu Ý Quan Trọng

- Bạn không cần ghi nhớ các con số chính xác cho chứng chỉ
- Hiểu mục đích và trường hợp sử dụng của mỗi lớp quan trọng hơn
- Giá thay đổi theo khu vực (ví dụ: us-east-1)
- Xem tài liệu giá cho các yêu cầu cụ thể

## Thực Hành Tốt Nhất

1. **Chọn lớp lưu trữ phù hợp** dựa trên mẫu truy cập
2. **Sử dụng chính sách S3 Lifecycle** để tự động chuyển đổi đối tượng
3. **Xem xét chi phí truy xuất** khi chọn các lớp truy cập không thường xuyên
4. **Sử dụng Intelligent-Tiering** khi mẫu truy cập không thể dự đoán
5. **Lên kế hoạch cho yêu cầu về tính khả dụng** trong thiết kế ứng dụng của bạn

## Kết Luận

Các lớp lưu trữ Amazon S3 cung cấp các tùy chọn linh hoạt để tối ưu hóa chi phí trong khi đáp ứng các yêu cầu về hiệu suất và tính khả dụng. Bằng cách hiểu các đặc điểm của từng lớp lưu trữ, bạn có thể đưa ra quyết định sáng suốt về nơi lưu trữ dữ liệu của mình để tối ưu chi phí.

---

*Để biết giá cả và thông số kỹ thuật mới nhất, vui lòng tham khảo tài liệu chính thức của AWS S3.*