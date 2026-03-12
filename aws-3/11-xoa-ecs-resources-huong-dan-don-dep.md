# Xóa ECS Resources - Hướng Dẫn Dọn Dẹp

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thực hiện các bước đúng đắn để xóa và dọn dẹp các tài nguyên AWS ECS (Elastic Container Service) nhằm tránh các chi phí không cần thiết. Điều quan trọng là phải tuân theo đúng thứ tự khi xóa các tài nguyên để đảm bảo quá trình xóa diễn ra suôn sẻ.

## Yêu Cầu Trước Khi Bắt Đầu

Trước khi bắt đầu quá trình dọn dẹp, hãy đảm bảo bạn có:
- Quyền truy cập vào AWS Console
- Quyền IAM phù hợp để xóa các tài nguyên ECS
- Một ECS service đang chạy mà bạn muốn xóa

## Quy Trình Dọn Dẹp Từng Bước

### Bước 1: Dừng ECS Service

Đầu tiên, bạn cần dừng service đang chạy bằng cách giảm số lượng task xuống 0:

1. Điều hướng đến ECS service của bạn trong AWS Console
2. Kiểm tra số lượng task hiện đang chạy
3. Nhấp vào **Update Service** (Cập nhật Service)
4. Đặt số lượng **Desired Tasks** (Task Mong Muốn) thành `0`
5. Lưu các thay đổi và đợi tất cả các task dừng lại

### Bước 2: Xóa ECS Service

Sau khi tất cả các task đã dừng:

1. Nhấp vào **Delete Service** (Xóa Service)
2. Gõ `Delete` vào hộp thoại xác nhận
3. Xác nhận việc xóa

**Quan trọng:** Khi bạn xóa service, AWS CloudFormation sẽ tự động xử lý việc xóa các tài nguyên liên quan.

### Bước 3: Xóa CloudFormation Stack

Việc xóa service sẽ kích hoạt quá trình xóa CloudFormation stack, tự động xóa các thành phần sau:

- ECS Service
- Load Balancer Listener
- Load Balancer
- Security Groups (Nhóm Bảo Mật)
- Target Groups (Nhóm Mục Tiêu)

**Lưu ý:** Quá trình này có thể mất vài phút. Hãy đợi cho đến khi hoàn tất trước khi chuyển sang bước tiếp theo.

### Bước 4: Xóa ECS Cluster

Sau khi service đã được xóa hoàn toàn:

1. Điều hướng đến cluster (ví dụ: "demo cluster")
2. Nhấp vào **Delete Cluster** (Xóa Cluster)
3. Xác nhận việc xóa

Điều này sẽ kích hoạt một CloudFormation stack deletion khác để xóa:

- Capacity Provider (Nhà Cung Cấp Năng Lực)
- Auto Scaling Group (Nhóm Tự Động Mở Rộng)
- ECS Cluster
- Launch Templates (Mẫu Khởi Chạy)

### Bước 5: Task Definitions (Tùy Chọn)

Task definitions không phát sinh chi phí vì chúng chỉ là các mẫu cấu hình. Tuy nhiên, nếu bạn muốn dọn dẹp chúng:

1. Điều hướng đến Task Definitions
2. Chọn task definition bạn muốn xóa
3. Nhấp vào **Actions** (Hành Động)
4. Chọn **Deregister** (Hủy Đăng Ký)
5. Xác nhận việc hủy đăng ký

**Lưu ý:** Việc hủy đăng ký task definitions là tùy chọn vì chúng không tốn chi phí.

## Những Điểm Cần Lưu Ý

- **Thời Gian Chờ:** Luôn đợi CloudFormation hoàn thành quá trình xóa trước khi chuyển sang bước tiếp theo
- **Quản Lý Chi Phí:** Dừng và xóa tài nguyên kịp thời giúp tránh các chi phí AWS không cần thiết
- **Phụ Thuộc:** Tuân theo thứ tự xóa để tránh xung đột phụ thuộc
- **Task Definitions:** Chúng miễn phí để giữ lại và có thể hữu ích cho tham khảo trong tương lai

## Tóm Tắt

Thứ tự xóa đúng đắn là:
1. Giảm service xuống 0 task
2. Xóa ECS service
3. Đợi CloudFormation hoàn thành
4. Xóa ECS cluster
5. (Tùy chọn) Hủy đăng ký task definitions

Bằng cách tuân theo các bước này, bạn đảm bảo việc xóa sạch sẽ tất cả các tài nguyên ECS và các thành phần cơ sở hạ tầng liên quan.

## Kết Luận

Vậy là xong! Bạn đã dọn dẹp thành công các tài nguyên ECS của mình. Quy trình này đảm bảo rằng không có tài nguyên nào còn sót lại sẽ tiếp tục phát sinh chi phí trên tài khoản AWS của bạn.