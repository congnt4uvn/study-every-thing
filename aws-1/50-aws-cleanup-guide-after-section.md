# Hướng Dẫn Dọn Dẹp Tài Nguyên AWS Sau Mỗi Phần

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thực hiện quy trình dọn dẹp tài nguyên AWS sau khi hoàn thành một phần học để tránh các khoản phí không cần thiết. Nội dung bao gồm việc xóa hệ thống file EFS, EC2 instances, EBS volumes, snapshots và security groups.

## Yêu Cầu Trước Khi Bắt Đầu

- Quyền truy cập AWS Console
- Các tài nguyên đã tạo trong phần trước (EFS, EC2, EBS, v.v.)

## Quy Trình Dọn Dẹp Từng Bước

### 1. Xóa Hệ Thống File EFS

Đầu tiên, chúng ta sẽ dọn dẹp Elastic File System (EFS):

1. Điều hướng đến dịch vụ EFS trong AWS Console
2. Chọn **Actions** trên file system của bạn
3. Chọn **Delete**
4. Nhập **File System ID** khi được yêu cầu
5. Xác nhận việc xóa

Hệ thống file sẽ được xóa khỏi tài khoản của bạn.

### 2. Terminate EC2 Instances

Đảm bảo terminate tất cả EC2 instances đang chạy:

1. Vào EC2 Dashboard
2. Điều hướng đến **Instances**
3. Chọn tất cả instances đang chạy
4. Click **Instance State** → **Terminate**
5. Xác nhận việc terminate

### 3. Xóa EBS Volumes

Dọn dẹp tất cả EBS volumes ở trạng thái available:

1. Trong EC2 Dashboard, điều hướng đến **Volumes**
2. Lọc các volumes có trạng thái **Available**
3. Nhấp chuột phải vào từng volume
4. Chọn **Delete Volume**
5. Xác nhận việc xóa cho tất cả volumes available

> **Lưu ý:** Chỉ những volumes không được gắn vào instances mới có thể xóa được.

### 4. Xóa EBS Snapshots

Xóa các snapshots để tránh phí lưu trữ:

1. Điều hướng đến **Snapshots** trong EC2 Dashboard
2. Chọn tất cả snapshots bạn đã tạo trong phần học
3. Click **Actions** → **Delete**
4. Xác nhận việc xóa cho từng snapshot

Điều này đảm bảo bạn sẽ không phải trả phí cho việc lưu trữ snapshots.

### 5. Dọn Dẹp Security Groups

Cuối cùng, xóa các security groups không cần thiết:

1. Điều hướng đến **Security Groups** trong EC2 Dashboard
2. Chọn các security groups bạn muốn xóa
3. Click **Actions** → **Delete security group**

**Những điểm quan trọng cần lưu ý:**

- **Không bao giờ xóa default security group** - nó được AWS yêu cầu
- Security groups chỉ có thể xóa sau khi tất cả EC2 instances liên quan đã được terminate
- Một số security groups có thể không bị xóa ngay lập tức - hãy đợi instances terminate hoàn toàn
- Tiếp tục thử cho đến khi thành công

#### Ví Dụ Thứ Tự Xóa:

1. Xóa các custom security groups (ví dụ: load balancer security group)
2. Đợi EC2 instances terminate hoàn toàn
3. Xóa các security groups liên quan đến EC2 (ví dụ: EC2 for EFS)

> **Mẹo:** Nếu security group vẫn đang được sử dụng, bạn sẽ nhận được thông báo lỗi. Đợi vài phút để instances tắt hoàn toàn, sau đó thử lại.

## Xác Minh

Sau khi hoàn thành tất cả các bước:

- ✅ EFS file systems đã xóa
- ✅ EC2 instances đã terminate
- ✅ EBS volumes đã xóa
- ✅ Snapshots đã xóa
- ✅ Custom security groups đã xóa

Bạn đã sẵn sàng để tiếp tục phần tiếp theo mà không phải lo lắng về các khoản phí bất ngờ!

## Xử Lý Sự Cố

### Security Group Không Thể Xóa

**Vấn đề:** Security group vẫn được liên kết với instances đang chạy

**Giải pháp:** 
- Đợi tất cả EC2 instances terminate hoàn toàn (có thể mất vài phút)
- Kiểm tra xem có network interfaces nào vẫn đang sử dụng security group không
- Thử xóa lại sau vài phút

### Volume Không Thể Xóa

**Vấn đề:** Volume vẫn được gắn vào một instance

**Giải pháp:**
- Đảm bảo EC2 instance đã được terminate
- Đợi instance terminate hoàn toàn
- Volume sẽ có sẵn để xóa

## Cân Nhắc Về Chi Phí

Dọn dẹp tài nguyên kịp thời giúp bạn:

- Tránh các khoản phí cho EC2 instances đã dừng (nhưng chưa terminate)
- Ngăn chặn phí lưu trữ EBS volume
- Loại bỏ chi phí lưu trữ snapshot
- Dừng phí lưu trữ EFS

Ghi nhớ: AWS tính phí cho các tài nguyên ngay cả khi chúng không được sử dụng tích cực, vì vậy việc dọn dẹp thường xuyên là rất quan trọng!