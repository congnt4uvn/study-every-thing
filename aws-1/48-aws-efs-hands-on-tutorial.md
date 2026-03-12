# Hướng Dẫn Thực Hành AWS EFS (Elastic File System)

## Tổng Quan

Hướng dẫn này trình bày cách tạo và cấu hình Amazon Elastic File System (EFS) và gắn kết nó vào các EC2 instance trên nhiều vùng khả dụng (availability zones).

## Tạo EFS File System

### Bước 1: Cấu Hình Ban Đầu

1. Truy cập dịch vụ Amazon Elastic File System
2. Nhấp vào **Create File System** (Tạo hệ thống tệp)
3. Tùy chọn đặt tên (có thể để trống)
4. Chọn VPC nơi bạn muốn kết nối file system (sử dụng VPC mặc định)
5. Nhấp vào **Customize** (Tùy chỉnh) để xem các tùy chọn nâng cao

### Bước 2: Cài Đặt File System

#### Loại File System

- **Regional** (Khu vực): Cung cấp file system trên nhiều vùng khả dụng
  - Tính khả dụng và độ bền cao
  - Được khuyến nghị cho môi trường production
  
- **One Zone** (Một vùng): Triển khai trên một vùng khả dụng duy nhất
  - Tùy chọn tiết kiệm chi phí
  - Chỉ phù hợp cho môi trường phát triển
  - Dữ liệu sẽ không thể truy cập nếu AZ gặp sự cố

**Khuyến nghị**: Sử dụng **Regional** cho môi trường production.

#### Sao Lưu Tự Động

- Giữ tính năng sao lưu tự động **được bật** (khuyến nghị)

#### Quản Lý Vòng Đời (Lifecycle Management)

Cấu hình chuyển đổi dữ liệu tự động để tiết kiệm chi phí:

- **Chuyển sang Infrequent Access (IA)**: Di chuyển các tệp không được truy cập trong 30 ngày
- **Chuyển sang Archive**: Di chuyển các tệp không được truy cập trong 90 ngày
- **Chuyển lại Standard**: Khi được truy cập lần đầu sau khi lưu trữ

Quản lý vòng đời này giúp giảm chi phí lưu trữ cho các tệp hiếm khi được truy cập.

#### Mã Hóa

- Giữ tính năng mã hóa **được bật**

### Bước 3: Cài Đặt Hiệu Suất

#### Chế Độ Throughput

1. **Elastic** (Linh hoạt - Khuyến nghị)
   - Tự động mở rộng dựa trên nhu cầu workload
   - Tốt nhất cho workload I/O không thể dự đoán
   - Chỉ trả tiền cho những gì bạn sử dụng
   - Có thể mở rộng từ 0 MB/s lên 100+ MB/s ngay lập tức
   - Không cần lập kế hoạch trước

2. **Bursting** (Đột phá)
   - Throughput tăng theo kích thước lưu trữ
   - Phù hợp khi nhu cầu throughput tỷ lệ với kích thước dữ liệu

3. **Provisioned** (Được cấp phát)
   - Chỉ định yêu cầu throughput trước
   - Trả tiền cho dung lượng được cấp phát trước
   - Sử dụng khi bạn biết chính xác nhu cầu throughput

#### Chế Độ Hiệu Suất

- **General Purpose** (Mục đích chung): Độ trễ thấp, hiệu suất cao (khuyến nghị)
- **Max I/O**: Độ trễ cao hơn nhưng hỗ trợ workload song song cao (cho các tình huống big data)

**Cấu Hình Khuyến Nghị**: Chế độ Enhanced với Elastic throughput và General Purpose performance.

## Cấu Hình Mạng

### Bước 1: Tạo Security Group

1. Vào EC2 Console → Security Groups
2. Nhấp **Create Security Group** (Tạo nhóm bảo mật)
3. Tên: `sg-efs-demo` hoặc `EFS Demo SG`
4. Tạo security group (ban đầu không có inbound rules)

### Bước 2: Cài Đặt Network Access

1. Chọn VPC của bạn (VPC mặc định)
2. Cấu hình mount targets:
   - Đối với Regional EFS, mount targets được tạo trong nhiều AZ
   - Mỗi AZ được gán cho một subnet (sử dụng subnet mặc định)
   - Địa chỉ IP được gán tự động
3. Gán security group đã tạo trước đó cho tất cả mount targets
4. Nhấp **Next** (Tiếp theo)

### Bước 3: File System Policy

- Để cài đặt file system policy ở mặc định (tính năng nâng cao tùy chọn)
- Nhấp **Next**

### Bước 4: Xem Xét và Tạo

- Xem xét tất cả các cài đặt
- Nhấp **Create** (Tạo)
- Đợi file system sẵn sàng

## Gắn Kết EFS vào EC2 Instances

### Khởi Chạy EC2 Instance A (trong AZ-A)

1. **Launch Instance** với tên: `Instance A`
2. **AMI**: Amazon Linux 2
3. **Instance Type**: t2.micro (free tier)
4. **Key Pair**: Tắt (sử dụng EC2 Instance Connect)
5. **Network Settings** (Cài đặt mạng):
   - Chọn subnet trong `eu-west-1a` (hoặc AZ-A ưa thích của bạn)
   - Cho phép truy cập SSH từ mọi nơi
6. **Storage** (Lưu trữ): 8 GB GP2
7. **File Systems** (Hệ thống tệp):
   - Chỉnh sửa và thêm EFS file system
   - Chọn EFS đã tạo của bạn
   - Mount point: `/mnt/efs/fs1`
   - Bật tự động mount với user data scripts
   - Security groups sẽ được tự động tạo và gắn kết
8. **Launch Instance** (Khởi chạy instance)

### Khởi Chạy EC2 Instance B (trong AZ-B)

1. **Launch Instance** với tên: `Instance B`
2. **AMI**: Amazon Linux 2
3. **Instance Type**: t2.micro
4. **Key Pair**: Tắt (sử dụng EC2 Instance Connect)
5. **Network Settings**:
   - Chọn subnet trong `eu-west-1b` (hoặc AZ-B ưa thích của bạn)
   - Chọn security group từ Instance A (ví dụ: `launch-wizard-2`)
6. **File Systems**:
   - Thêm cùng EFS file system
   - Cùng mount point: `/mnt/efs/fs1`
   - Bật tự động mount
7. **Launch Instance**

## Cấu Hình Security Group

Khi bạn thêm EFS vào EC2 instances thông qua console:

- AWS tự động tạo security groups (ví dụ: `efs-sg-1`, `efs-sg-2`)
- Các security groups này được gắn vào EFS mount targets của bạn
- Inbound rules cho phép giao thức NFS trên cổng 2049
- Source được đặt thành security group của EC2 instance
- Điều này cho phép EC2 instances truy cập EFS file system

## Kiểm Tra Chia Sẻ Tệp EFS

### Trên Instance A:

```bash
# Kết nối qua EC2 Instance Connect

# Liệt kê mount point EFS
ls /mnt/efs/fs1/

# Nâng quyền
sudo su

# Tạo tệp kiểm tra
echo "hello world" > /mnt/efs/fs1/hello.txt

# Xác minh tệp đã tạo
cat /mnt/efs/fs1/hello.txt
```

### Trên Instance B:

```bash
# Kết nối qua EC2 Instance Connect

# Liệt kê mount point EFS
ls /mnt/efs/fs1/

# Đọc tệp được tạo từ Instance A
cat /mnt/efs/fs1/hello.txt
```

**Kết Quả**: Tệp `hello.txt` được tạo trên Instance A có thể nhìn thấy và truy cập được trên Instance B, chứng minh rằng EFS đã được gắn kết thành công như một ổ đĩa mạng chia sẻ trên cả hai instances ở các vùng khả dụng khác nhau.

## Dọn Dẹp

### Xóa EC2 Instances

1. Vào EC2 Console → Instances
2. Chọn cả hai instances
3. Nhấp **Terminate** (Chấm dứt)

### Xóa EFS File System

1. Vào EFS Console
2. Chọn file system của bạn
3. Nhấp **Delete** (Xóa)
4. Nhập file system ID để xác nhận
5. Nhấp **Delete**

### Xóa Security Groups

1. Vào EC2 Console → Security Groups
2. Xóa các security groups bổ sung được tạo trong demo:
   - `efs-sg-1`
   - `efs-sg-2`
   - `sg-efs-demo`

## Những Điểm Chính

- **EFS cung cấp lưu trữ mạng chia sẻ** có thể được gắn kết đồng thời trên nhiều EC2 instances
- **Khả dụng cross-AZ** đảm bảo tính khả dụng cao và độ bền
- **Trả tiền theo sử dụng** - chi phí dựa trên dung lượng lưu trữ thực tế
- **Quản lý vòng đời** giúp tối ưu hóa chi phí bằng cách di chuyển dữ liệu ít được truy cập sang các tầng lưu trữ rẻ hơn
- **Chế độ Elastic throughput** được khuyến nghị cho hầu hết các workload
- **Tự động mount** thông qua EC2 console đơn giản hóa thiết lập với user data scripts
- **Security groups** được tự động cấu hình để cho phép truy cập NFS

## Thực Hành Tốt Nhất

- Sử dụng **Regional** EFS cho workload production
- Bật **sao lưu tự động**
- Sử dụng **chế độ Elastic throughput** cho workload không thể dự đoán
- Cấu hình **quản lý vòng đời** để tối ưu hóa chi phí
- Giữ **mã hóa được bật**
- Sử dụng cấu hình **security group** phù hợp để kiểm soát truy cập