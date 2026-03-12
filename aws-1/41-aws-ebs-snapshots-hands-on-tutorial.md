# Hướng Dẫn Thực Hành AWS EBS Snapshots

## Tổng Quan

Hướng dẫn này trình bày cách làm việc với Amazon EBS Snapshots, bao gồm tạo snapshot, sao chép qua các vùng, khôi phục volume, sử dụng Thùng Rác để bảo vệ và quản lý các tầng lưu trữ.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản AWS có quyền truy cập vào EC2
- Một EBS volume hiện có (ví dụ: volume GP2 dung lượng 2 GB)
- Hiểu biết cơ bản về các vùng và availability zones của AWS

## Tạo EBS Snapshot

### Bước 1: Tạo Snapshot

1. Điều hướng đến EBS Volumes trong bảng điều khiển EC2
2. Chọn volume mà bạn muốn tạo snapshot (ví dụ: EBS Volume GP2 dung lượng 2 GB)
3. Nhấp **Actions** → **Create snapshot**
4. Thêm mô tả (ví dụ: "DemoSnapshots")
5. Nhấp **Create snapshots**

### Bước 2: Xem Các Snapshot

1. Trong menu bên trái, nhấp vào **Snapshots**
2. Bạn sẽ thấy danh sách tất cả các snapshot
3. Kiểm tra trạng thái - nó sẽ hiển thị:
   - Trạng thái: **Completed**
   - Khả dụng: **100%**

## Sao Chép Snapshot Qua Các Vùng

### Trường Hợp Sử Dụng: Khôi Phục Thảm Họa

Sao chép snapshot sang vùng khác là cần thiết cho chiến lược khôi phục thảm họa và đảm bảo dữ liệu của bạn được sao lưu ở nhiều vùng AWS.

### Các Bước:

1. Nhấp chuột phải vào snapshot của bạn
2. Chọn **Copy Snapshots**
3. Chọn bất kỳ vùng đích nào từ danh sách thả xuống
4. Nhấp **Copy**

**Lưu ý:** Tính năng này cho phép bạn sao chép dữ liệu qua các vùng AWS để đảm bảo dự phòng.

## Tạo Volume Từ Snapshot

### Khôi Phục Qua Các Availability Zone

Một trong những tính năng mạnh mẽ của EBS Snapshots là khả năng khôi phục volume ở các availability zone khác nhau.

### Các Bước:

1. Chọn snapshot của bạn
2. Nhấp **Actions** → **Create volume from snapshot**
3. Cấu hình volume:
   - Loại volume: GP2
   - Dung lượng: 2 GB
   - Target AZ: Chọn một zone khác (ví dụ: thay đổi từ eu-west-1a sang eu-west-1b)
   - Tùy chọn: Bật mã hóa
   - Tùy chọn: Thêm tags
4. Nhấp **Create volume**

### Kết Quả:

- Quay lại **Volumes**
- Bây giờ bạn sẽ thấy hai volume:
  - Volume gốc ở availability zone đầu tiên
  - Volume được khôi phục ở availability zone mới

**Lợi Ích Chính:** Snapshot cho phép bạn sao chép hiệu quả các EBS volume qua các availability zone khác nhau.

## Sử Dụng Thùng Rác (Recycle Bin)

### Mục Đích

Thùng Rác bảo vệ các EBS Snapshot và Amazon Machine Images (AMI) của bạn khỏi bị xóa vô tình bằng cách giữ lại các tài nguyên đã xóa trong một khoảng thời gian xác định.

### Tạo Quy Tắc Lưu Giữ

1. Điều hướng đến **Recycle Bin** trong bảng điều khiển EC2
2. Nhấp **Create Retention Rule**
3. Cấu hình quy tắc:
   - Tên quy tắc: "DemoRetentionRule"
   - Loại tài nguyên: **EBS Snapshots**
   - Áp dụng cho: **All resources** (Tất cả tài nguyên)
   - Thời gian lưu giữ: **1 ngày**
   - Cài đặt khóa quy tắc: Để **unlocked** (cho phép xóa quy tắc)
4. Nhấp **Create Retention Rule**

### Kiểm Tra Thùng Rác

1. Quay lại **Snapshots** trong bảng điều khiển EC2
2. Chọn một snapshot và xóa nó
3. Snapshot sẽ biến mất khỏi danh sách chính
4. Điều hướng đến **Recycle Bin** → **Resources**
5. Làm mới trang - snapshot đã xóa sẽ xuất hiện ở đây

### Khôi Phục Snapshot

1. Trong Thùng Rác, nhấp vào snapshot đã xóa
2. Nhấp **Recover**
3. Xác nhận bằng cách nhấp **Recover Resources**
4. Snapshot sẽ được khôi phục về bảng điều khiển EC2 Snapshots

**Lưu ý:** Trước khi có tính năng Thùng Rác, các snapshot đã xóa bị loại bỏ vĩnh viễn và không thể khôi phục.

## Các Tầng Lưu Trữ (Storage Tiers)

### Tổng Quan

EBS Snapshots hỗ trợ các tầng lưu trữ khác nhau để tối ưu hóa chi phí:

- **Standard Storage Tier**: Tầng mặc định với quyền truy cập ngay lập tức
- **Archive Tier**: Lưu trữ chi phí thấp hơn cho các snapshot ít được truy cập

### Lưu Trữ Snapshot

1. Chọn một snapshot (hiện đang ở Standard Storage Tier)
2. Nhấp **Actions** → **Archive snapshot**
3. Snapshot chuyển sang mức giá khác

**Quan Trọng:** Khôi phục snapshot đã lưu trữ yêu cầu từ 24 đến 72 giờ.

## Tóm Tắt

Trong hướng dẫn này, bạn đã học cách:

- ✅ Tạo EBS Snapshots từ volume
- ✅ Sao chép snapshot qua các vùng AWS để khôi phục thảm họa
- ✅ Khôi phục volume từ snapshot ở các availability zone khác nhau
- ✅ Thiết lập quy tắc lưu giữ Thùng Rác để bảo vệ chống xóa nhầm
- ✅ Khôi phục snapshot đã xóa từ Thùng Rác
- ✅ Hiểu về các tầng lưu trữ để tối ưu hóa chi phí

## Các Bước Tiếp Theo

- Khám phá việc tạo snapshot tự động bằng AWS Backup
- Triển khai chính sách vòng đời snapshot
- Thực hành các kịch bản khôi phục thảm họa qua vùng
- Tìm hiểu về chia sẻ snapshot qua các tài khoản AWS

---

**Tài Nguyên Bổ Sung:**
- [Tài Liệu AWS EBS Snapshots](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)
- [Tài Liệu AWS Recycle Bin](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/recycle-bin.html)