# AWS EBS Volumes - Hướng Dẫn Thực Hành

## Tổng Quan

Hướng dẫn này trình bày cách quản lý các ổ đĩa Amazon Elastic Block Store (EBS) với các EC2 instance, bao gồm tạo, gắn kết và xóa các volume.

## Xem Các EBS Volume Gắn Với Instance

Hãy bắt đầu bằng cách kiểm tra các EBS volume đã gắn với EC2 instance của chúng ta:

1. Click vào **EC2 instance** của bạn
2. Chuyển đến tab **Storage**
3. Bạn sẽ thấy một root device với một block device được gắn kết

Trong ví dụ này, chúng ta có một volume **8 gigabytes** hiện đang được gắn vào EC2 instance.

### Truy Cập Giao Diện Volumes

- Click vào volume ID để truy cập giao diện volumes của AWS
- Volume sẽ hiển thị trạng thái "in use" (đang sử dụng) và được gắn với instance của bạn
- Hoặc truy cập từ menu bên trái bằng cách click vào **Volumes**

## Tạo EBS Volume Mới

Bây giờ chúng ta có một EBS volume 8 gigabytes. Hãy tạo volume thứ hai:

### Bước 1: Tạo Volume

1. Click **Create Volume**
2. Chọn loại volume: GP2, GP3, v.v. (chúng ta sẽ dùng **GP2**)
3. Đặt kích thước **2 gigabytes**

### Bước 2: Chọn Availability Zone

**Quan trọng:** Các EBS volume được ràng buộc với các availability zone cụ thể.

1. Vào chi tiết EC2 instance của bạn
2. Cuộn xuống phần **Networking**
3. Ghi chú availability zone (ví dụ: `eu-west-1b`)
4. Tạo volume của bạn trong **cùng availability zone** (`eu-west-1b`)

Điều này đảm bảo volume có thể được gắn vào instance của bạn.

## Gắn Volume Vào Instance

Sau khi tạo volume:

1. Trạng thái volume sẽ là **Available** (chưa gắn kết)
2. Chọn volume và click **Actions** → **Attach Volume**
3. Chọn EC2 instance đang chạy của bạn
4. Click **Attach Volume**

Instance của bạn giờ có hai EBS volume được gắn kết!

### Xác Minh Việc Gắn Kết

1. Làm mới trang EC2 instance
2. Vào tab **Storage**
3. Cuộn xuống **Block Devices**
4. Bạn sẽ thấy cả hai volume:
   - 8 gigabytes (root volume)
   - 2 gigabytes (volume mới gắn)

**Lưu ý:** Để thực sự sử dụng block device mới, bạn cần format nó. Để biết hướng dẫn, tìm kiếm "make an Amazon EBS volume available to use on Linux" - quá trình này nằm ngoài phạm vi của hướng dẫn này.

## Hiểu Về Giới Hạn Availability Zone

Hãy chứng minh rằng EBS volume được ràng buộc với các availability zone cụ thể:

### Tạo Volume Ở AZ Khác

1. Tạo một volume khác 2 gigabytes GP2
2. Lần này, chọn **eu-west-1a** (khác với `eu-west-1b` của instance)
3. Sau khi tạo xong, thử gắn nó vào EC2 instance của bạn

**Kết quả:** Bạn không thể gắn nó! Điều này chứng minh rằng EBS volume thực sự bị ràng buộc bởi các availability zone cụ thể.

### Dọn Dẹp

- Chọn volume ở AZ sai
- Click **Actions** → **Delete Volume**
- Volume được xóa ngay lập tức

Điều này thể hiện sức mạnh của cloud: bạn có thể yêu cầu và xóa volume trong vài giây.

## Thuộc Tính Delete on Termination

Hãy khám phá điều gì xảy ra khi bạn terminate một EC2 instance.

### Kiểm Tra Thuộc Tính

1. Vào tab **Storage** của EC2 instance
2. Xem bảng **Block Devices**
3. Cuộn sang phải để thấy cột **Delete on Termination**:
   - Root volume (8 GB): **Yes**
   - Volume bổ sung (2 GB): **No**

### Tại Sao Root Volume Được Đặt Thành "Yes"?

Khi khởi chạy EC2 instance:

1. Trong wizard khởi chạy instance, cuộn đến **Storage**
2. Click vào **Advanced**
3. Root volume có **Delete on Termination** được đặt thành **Yes** theo mặc định
4. Bạn có thể thay đổi thành **No** nếu muốn giữ root volume sau khi terminate

## Terminate Instance và Hành Vi Của Volume

Hãy terminate instance để xem điều gì xảy ra:

1. Terminate EC2 instance của bạn
2. Quay lại trang **EBS Volumes**
3. Làm mới danh sách volume

### Điều Gì Xảy Ra:

- Volume 2 GB trở thành **Available** (tách ra nhưng không bị xóa)
- Root volume 8 GB bị **xóa** (vì Delete on Termination = Yes)
- Chỉ còn volume 2 GB trong danh sách volume của bạn

### Xác Minh

Kiểm tra EC2 console của bạn - instance hiển thị trạng thái **Terminated**.

## Những Điểm Chính Cần Nhớ

1. **EBS volume được ràng buộc với các availability zone cụ thể** - chúng chỉ có thể gắn vào instance trong cùng AZ
2. **Nhiều volume có thể được gắn** vào một EC2 instance duy nhất
3. **Thuộc tính Delete on Termination** kiểm soát việc volume có bị xóa khi instance terminate không
4. **Root volume** thường có Delete on Termination được bật theo mặc định
5. **Volume bổ sung** có Delete on Termination bị tắt theo mặc định
6. **Tính linh hoạt của cloud** cho phép bạn tạo và xóa volume trong vài giây

## Kết Luận

Hướng dẫn thực hành này đã trình bày các thao tác cơ bản để quản lý EBS volume trong AWS, bao gồm tạo, gắn kết và hiểu về vòng đời của volume với EC2 instance.

---

*Bài Giảng Tiếp Theo: Tiếp tục khám phá các dịch vụ lưu trữ AWS và tính năng EC2.*