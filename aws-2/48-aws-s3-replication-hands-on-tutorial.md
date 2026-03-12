# Hướng Dẫn Thực Hành AWS S3 Replication

## Tổng Quan

Hướng dẫn này trình bày cách thiết lập và cấu hình tính năng sao chép (replication) của Amazon S3, bao gồm cả Cross-Region Replication (CRR) và Same-Region Replication (SRR). Bạn sẽ học cách sao chép các đối tượng giữa các S3 bucket và hiểu được cơ chế hoạt động của delete marker cũng như version replication.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS với quyền phù hợp
- Hiểu biết cơ bản về S3 versioning
- Hai S3 bucket (nguồn và đích)

## Bước 1: Tạo Bucket Nguồn (Origin)

1. Truy cập vào S3 console
2. Tạo bucket mới với các thiết lập sau:
   - **Tên bucket**: `s3-stephane-bucket-origin-v2`
   - **Region**: `eu-west-1` (hoặc region bạn muốn)
   - **Bật versioning**: ✓ Bắt buộc cho replication

> **Quan trọng**: Tính năng replication chỉ hoạt động khi versioning được bật trên cả bucket nguồn và bucket đích.

## Bước 2: Tạo Bucket Đích (Destination)

1. Tạo bucket thứ hai:
   - **Tên bucket**: `s3-stephane-bucket-replica-v2`
   - **Region**: `us-east-1` (cho Cross-Region Replication) hoặc cùng region (cho Same-Region Replication)
   - **Bật versioning**: ✓ Bắt buộc

## Bước 3: Upload File Thử Nghiệm Ban Đầu

1. Truy cập vào bucket nguồn
2. Upload một file thử nghiệm (ví dụ: `beach.jpg`)
3. Lưu ý: File này sẽ **không** được tự động sao chép vì quy tắc replication chưa được cấu hình

## Bước 4: Cấu Hình Quy Tắc Replication

1. Trong bucket nguồn, vào tab **Management**
2. Cuộn xuống phần **Replication rules**
3. Click **Create replication rule**
4. Cấu hình các thiết lập sau:

### Cấu Hình Replication Rule

- **Tên quy tắc**: `DemoReplicationRule`
- **Trạng thái**: Enabled (Đã bật)
- **Source bucket**: Áp dụng cho tất cả objects trong bucket
- **Destination** (Đích):
  - Chọn "Bucket in this account" (Bucket trong tài khoản này)
  - Nhập tên bucket đích: `s3-stephane-bucket-replica-v2`
  - Region sẽ được tự động nhận diện (ví dụ: `us-east-1`)
- **IAM Role**: Tạo role mới (tự động cấu hình)

### Xử Lý Các Object Đã Tồn Tại

Khi được hỏi về việc sao chép các object đã tồn tại:
- **Hành vi mặc định**: Replication chỉ áp dụng cho các object được upload **sau khi** quy tắc được tạo
- **Đối với object đã tồn tại**: Sử dụng S3 Batch Operations để sao chép các object đã upload trước đó
- **Trong hướng dẫn này**: Chọn "No, do not replicate existing objects" (Không sao chép object đã tồn tại)

## Bước 5: Kiểm Tra Replication

### Kiểm Tra 1: Upload Object Mới

1. Upload file mới vào bucket nguồn (ví dụ: `coffee.jpg`)
2. Đợi khoảng 5-10 giây
3. Kiểm tra bucket đích - file sẽ xuất hiện với:
   - Cùng tên file
   - Cùng version ID
   - Metadata giống hệt

### Kiểm Tra 2: Xác Minh Version Replication

1. Trong bucket nguồn, click "Show versions"
2. Ghi nhận version ID (ví dụ: `GBk`)
3. Trong bucket đích, click "Show versions"
4. Xác minh rằng version ID khớp chính xác

### Kiểm Tra 3: Upload Phiên Bản Mới Của File Đã Tồn Tại

1. Upload lại `beach.jpg` vào bucket nguồn
2. Một version mới sẽ được tạo (ví dụ: version ID: `DK2`)
3. Kiểm tra bucket đích để xác nhận version mới được sao chép

## Bước 6: Cấu Hình Delete Marker Replication

### Hiểu Về Delete Marker

Theo mặc định, delete marker **không được sao chép**. Để bật tính năng này:

1. Vào **Management** → **Replication rules**
2. Chỉnh sửa replication rule của bạn
3. Cuộn xuống **Delete marker replication**
4. Bật tùy chọn này
5. Lưu thay đổi

### Kiểm Tra Delete Marker Replication

1. Trong bucket nguồn, xóa một file (ví dụ: `coffee.jpg`)
2. Điều này tạo ra delete marker (không phải xóa vĩnh viễn)
3. Đợi vài giây
4. Kiểm tra bucket đích - delete marker sẽ được sao chép
5. Sử dụng "Show versions" để xác minh object vẫn tồn tại nhưng được đánh dấu là đã xóa

## Các Hành Vi Quan Trọng Của Replication

### Những Gì Được Sao Chép

✅ **Được sao chép**:
- Object mới được upload sau khi replication được bật
- Các version của object
- Metadata
- Delete marker (nếu được bật trong cài đặt replication)

### Những Gì KHÔNG Được Sao Chép

❌ **Không được sao chép**:
- Object đã tồn tại trước khi replication được bật (trừ khi dùng Batch Operations)
- Xóa vĩnh viễn các version cụ thể
- Lifecycle actions
- Object được mã hóa bằng SSE-C

### Hành Vi Xóa Vĩnh Viễn (Permanent Delete)

Khi bạn xóa một **version ID cụ thể** (xóa vĩnh viễn):
- Hành động này **KHÔNG được sao chép** đến bucket đích
- Chỉ có delete marker được sao chép
- Object vẫn tồn tại trong bucket đích

**Ví dụ**:
1. Xóa vĩnh viễn version của `beach.jpg` trong bucket nguồn
2. File vẫn còn trong bucket replica
3. Chỉ có delete marker được sao chép, không phải xóa vĩnh viễn

## Các Loại Replication

### Cross-Region Replication (CRR)
- Sao chép object qua các AWS region khác nhau
- Trường hợp sử dụng: Tuân thủ quy định, truy cập với độ trễ thấp hơn, khôi phục thảm họa

### Same-Region Replication (SRR)
- Sao chép object trong cùng một AWS region
- Trường hợp sử dụng: Tổng hợp log, sao chép trực tiếp giữa tài khoản production và test

## Những Điểm Chính Cần Nhớ

1. **Versioning là bắt buộc** trên cả bucket nguồn và bucket đích
2. **Replication là bất đồng bộ** - mong đợi độ trễ vài giây
3. **Chỉ object mới được sao chép** theo mặc định sau khi bật replication
4. **Delete marker có thể được sao chép** nếu được bật rõ ràng
5. **Xóa vĩnh viễn không bao giờ được sao chép** để duy trì tính toàn vẹn dữ liệu
6. **Version ID được giữ nguyên** trong quá trình replication
7. **IAM role được tự động tạo** để quản lý quyền replication

## Dọn Dẹp

Để tránh chi phí liên tục:

1. Làm trống cả hai bucket (xóa tất cả object và version)
2. Xóa replication rule
3. Xóa cả hai S3 bucket
4. Xóa IAM role được tạo cho replication

## Kết Luận

S3 replication là một tính năng mạnh mẽ cho dự phòng dữ liệu, tuân thủ quy định và khôi phục thảm họa. Hiểu rõ cách hoạt động của delete marker và version replication là rất quan trọng cho các kỳ thi chứng chỉ AWS và triển khai thực tế.

## Các Bước Tiếp Theo

- Khám phá S3 Batch Replication cho các object đã tồn tại
- Tìm hiểu về Replication Time Control (RTC) cho replication có thể dự đoán
- Nghiên cứu S3 lifecycle policies kết hợp với replication
- Xem xét các số liệu và giám sát S3 replication