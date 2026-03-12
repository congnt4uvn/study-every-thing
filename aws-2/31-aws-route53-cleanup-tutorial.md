# Hướng Dẫn Dọn Dẹp AWS Route 53 và EC2

## Tổng Quan

Hướng dẫn này sẽ giúp bạn dọn dẹp các tài nguyên AWS đã tạo trong các bài thực hành về Route 53 để tránh chi phí không cần thiết. Chúng ta sẽ xóa hosted zones, EC2 instances, và Application Load Balancers trên nhiều regions.

---

## Các Yếu Tố Chi Phí

### Tên Miền (Domain Name)
- Tên miền bạn đã mua sẽ vẫn còn trong tài khoản
- Chi phí gia hạn hàng năm: **$12/năm** (hoặc cao hơn đối với tên miền cao cấp)
- Bản thân đăng ký tên miền không thể xóa, chỉ có thể để nó hết hạn

### Route 53 Hosted Zone
- Nếu bạn không sử dụng hosted zone, bạn nên xóa nó
- Chi phí: **$0.50/tháng** nếu giữ hoạt động
- Số lượng records trong hosted zone không ảnh hưởng đến chi phí
- Bạn có thể giữ nguyên các records mà không tốn thêm phí

---

## Các Bước Dọn Dẹp

### 1. Xóa Route 53 Hosted Zone

Để xóa hosted zone của bạn:

1. Truy cập Route 53 trong AWS Console
2. Chọn hosted zone của bạn
3. **Đầu tiên, xóa tất cả các records** (ngoại trừ NS và SOA records mặc định)
4. Sau đó xóa hosted zone

> **Lưu ý:** Bạn phải xóa hết tất cả custom records trước khi có thể xóa hosted zone.

### 2. Xóa EC2 Instances

Trong bài hướng dẫn này, chúng ta đã tạo EC2 instances ở ba regions khác nhau. Bạn cần dọn dẹp từng region riêng biệt:

#### Region 1: Frankfurt (eu-central-1)
1. Truy cập EC2 console ở region Frankfurt
2. Chọn và terminate EC2 instance

#### Region 2: US East (us-east-1)
1. Chuyển sang region US East
2. Chọn và terminate EC2 instance

#### Region 3: Singapore (ap-southeast-1)
1. Chuyển sang region Singapore
2. Chọn và terminate EC2 instance

### 3. Xóa Application Load Balancer

Ở region mà bạn đã tạo ALB (trong ví dụ này là Frankfurt):

1. Truy cập EC2 → Load Balancers
2. Chọn Application Load Balancer của bạn
3. Xóa load balancer
4. Xóa **target group** liên quan

> **Quan trọng:** Đảm bảo xóa cả load balancer VÀ target group của nó để tránh bị tính phí.

---

## Danh Sách Kiểm Tra Dọn Dẹp Theo Region

Thực hiện các bước sau ở mỗi region mà bạn đã triển khai tài nguyên:

- [ ] Terminate EC2 instances
- [ ] Xóa Application Load Balancers
- [ ] Xóa các target groups liên quan
- [ ] Xác nhận không còn tài nguyên nào đang chạy

---

## Sau Khi Dọn Dẹp

Sau khi hoàn thành tất cả các bước dọn dẹp:

✅ Bạn sẽ không phải trả thêm chi phí nào từ bài hướng dẫn này  
✅ Chỉ còn phí đăng ký tên miền (nếu bạn chọn giữ tên miền)  
✅ Chi phí hosted zone sẽ dừng sau khi xóa

---

## Tóm Tắt

Bằng cách làm theo hướng dẫn dọn dẹp này, bạn đã thành công:

- Hiểu được các tác động chi phí của tài nguyên Route 53
- Xóa hosted zone để tránh chi phí hàng tháng
- Terminate EC2 instances trên nhiều regions
- Xóa Application Load Balancers và target groups
- Đảm bảo không có chi phí không cần thiết từ tài nguyên bài hướng dẫn

Cảm ơn bạn đã theo dõi phần này. Hẹn gặp lại ở bài giảng tiếp theo!