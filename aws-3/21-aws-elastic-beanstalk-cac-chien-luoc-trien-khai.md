# Các Chiến Lược Triển Khai AWS Elastic Beanstalk

## Tổng Quan

AWS Elastic Beanstalk cung cấp nhiều tùy chọn triển khai khác nhau khi bạn cập nhật ứng dụng. Mỗi chiến lược có các đặc điểm khác nhau về thời gian ngừng hoạt động, tốc độ triển khai, chi phí và khả năng rollback. Hiểu rõ các tùy chọn này giúp bạn chọn phương pháp triển khai phù hợp cho trường hợp sử dụng cụ thể của mình.

## Các Phương Pháp Triển Khai

### 1. All at Once (Tất Cả Cùng Lúc)

**Mô tả:**
Triển khai tất cả các cập nhật cùng một lúc cho tất cả các instance đồng thời.

**Đặc điểm:**
- **Tốc độ:** Phương pháp triển khai nhanh nhất
- **Thời gian ngừng hoạt động:** Có - tất cả instance đều dừng trong quá trình cập nhật
- **Chi phí:** Không có chi phí bổ sung
- **Phù hợp nhất cho:** Lặp lại nhanh trong môi trường phát triển

**Cách hoạt động:**
1. Bắt đầu với các EC2 instance đang chạy phiên bản 1 (v1)
2. Elastic Beanstalk dừng ứng dụng trên tất cả EC2 instance
3. Triển khai phiên bản 2 (v2) lên tất cả instance
4. Tất cả instance hiện đang chạy v2

**Trường hợp sử dụng:** Tuyệt vời cho môi trường phát triển nơi thời gian ngừng hoạt động có thể chấp nhận được và bạn cần lặp lại nhanh chóng.

---

### 2. Rolling (Luân Phiên)

**Mô tả:**
Cập nhật một số instance tại một thời điểm (gọi là một bucket), sau đó chuyển sang nhóm tiếp theo khi bucket đầu tiên khỏe mạnh.

**Đặc điểm:**
- **Tốc độ:** Trung bình (phụ thuộc vào kích thước bucket)
- **Thời gian ngừng hoạt động:** Không có thời gian ngừng hoạt động, nhưng chạy dưới công suất
- **Công suất:** Ứng dụng chạy dưới công suất trong quá trình triển khai
- **Chi phí:** Không có chi phí bổ sung
- **Kích thước Bucket:** Có thể cấu hình

**Cách hoạt động:**
1. Bắt đầu với nhiều instance đang chạy v1
2. Dừng ứng dụng trên bucket đầu tiên của các instance (ví dụ: 2 trong số 4 instance)
3. Cập nhật bucket đầu tiên lên v2
4. Chuyển sang bucket tiếp theo và lặp lại
5. Tiếp tục cho đến khi tất cả instance được cập nhật

**Lưu ý quan trọng:**
- Ứng dụng chạy đồng thời cả hai phiên bản trong quá trình triển khai
- Với kích thước bucket nhỏ và nhiều instance, triển khai có thể rất lâu
- Công suất ứng dụng bị giảm trong quá trình triển khai

---

### 3. Rolling with Additional Batch (Luân Phiên với Batch Bổ Sung)

**Mô tả:**
Tương tự như rolling, nhưng khởi động các instance mới trước để duy trì công suất đầy đủ trong quá trình triển khai.

**Đặc điểm:**
- **Tốc độ:** Trung bình đến dài
- **Thời gian ngừng hoạt động:** Không có thời gian ngừng hoạt động
- **Công suất:** Chạy ở công suất đầy đủ trong suốt quá trình triển khai
- **Chi phí:** Chi phí bổ sung nhỏ (instance tạm thời)
- **Phù hợp nhất cho:** Môi trường production

**Cách hoạt động:**
1. Bắt đầu với các instance đang chạy v1
2. Khởi động các instance mới với v2 (batch bổ sung)
3. Cập nhật các instance hiện có theo batch lên v2
4. Xóa batch bổ sung sau khi triển khai hoàn tất

**Ưu điểm:**
- Luôn chạy ở công suất đầy đủ
- Ứng dụng tiếp tục phục vụ traffic bình thường
- Lựa chọn tốt cho triển khai production

---

### 4. Immutable (Bất Biến)

**Mô tả:**
Triển khai code mới lên các instance hoàn toàn mới trong một Auto Scaling Group tạm thời.

**Đặc điểm:**
- **Tốc độ:** Thời gian triển khai dài nhất
- **Thời gian ngừng hoạt động:** Không có thời gian ngừng hoạt động
- **Chi phí:** Chi phí cao (tăng gấp đôi công suất tạm thời)
- **Rollback:** Rất nhanh - chỉ cần terminate ASG mới
- **Phù hợp nhất cho:** Môi trường production với yêu cầu uptime nghiêm ngặt

**Cách hoạt động:**
1. ASG hiện tại có các instance đang chạy v1
2. Tạo ASG tạm thời
3. Khởi động một instance trong ASG tạm thời với v2 và xác thực
4. Nếu thành công, khởi động các instance còn lại trong ASG tạm thời
5. Hợp nhất các instance của ASG tạm thời vào ASG hiện tại
6. Terminate các instance v1 cũ
7. Xóa ASG tạm thời

**Ưu điểm:**
- Không có thời gian ngừng hoạt động
- Rollback nhanh trong trường hợp thất bại
- Code mới được triển khai lên các instance mới
- Tuyệt vời cho production nếu chi phí không phải là mối quan tâm chính

---

### 5. Blue/Green (Xanh/Xanh Lá)

**Mô tả:**
Tạo một môi trường hoàn toàn mới và chuyển đổi khi sẵn sàng. Đây là quy trình thủ công, không phải tính năng trực tiếp của Elastic Beanstalk.

**Đặc điểm:**
- **Tốc độ:** Quy trình thủ công
- **Thời gian ngừng hoạt động:** Không có thời gian ngừng hoạt động
- **Kiểm thử:** Có thể kiểm thử rộng rãi trước khi chuyển đổi
- **Rollback:** Dễ dàng - chuyển về môi trường blue

**Cách hoạt động:**
1. Môi trường Blue chạy ứng dụng v1
2. Triển khai môi trường Green với ứng dụng v2
3. Cả hai môi trường chạy đồng thời
4. Sử dụng Route 53 weighted routing để chia traffic (ví dụ: 90% blue, 10% green)
5. Giám sát và kiểm thử môi trường green
6. Khi hài lòng, swap URL hoặc điều chỉnh trọng số để chuyển toàn bộ traffic sang green
7. Terminate môi trường blue

**Ưu điểm:**
- Kiểm thử hoàn chỉnh trước khi triển khai đầy đủ
- Rollback dễ dàng
- Rủi ro tối thiểu cho traffic production

**Lưu ý:** Đây là phương pháp thủ công hơn và không được tích hợp đầy đủ vào Elastic Beanstalk.

---

### 6. Traffic Splitting (Chia Traffic) - Canary Testing

**Mô tả:**
Triển khai phiên bản mới lên ASG tạm thời và gửi một phần trăm nhỏ traffic để kiểm thử. Đây là canary testing tự động.

**Đặc điểm:**
- **Tốc độ:** Quy trình tự động
- **Thời gian ngừng hoạt động:** Không có thời gian ngừng hoạt động
- **Chi phí:** Tăng gấp đôi công suất tạm thời
- **Giám sát:** Giám sát sức khỏe tự động
- **Rollback:** Rất nhanh và tự động

**Cách hoạt động:**
1. ASG chính chạy v1 với công suất cụ thể (ví dụ: 3 instance)
2. Tạo ASG tạm thời với cùng công suất chạy v2
3. Application Load Balancer chia traffic (ví dụ: 90% cho ASG chính, 10% cho ASG tạm thời)
4. Giám sát sức khỏe triển khai trên ASG tạm thời
5. Nếu phát hiện vấn đề, rollback tự động xảy ra
6. Nếu thành công, di chuyển các instance từ ASG tạm thời sang ASG chính
7. Terminate các instance v1 cũ

**Ưu điểm:**
- Canary testing hoàn toàn tự động
- Rollback tự động nhanh chóng khi thất bại
- Không có thời gian ngừng hoạt động của ứng dụng
- ASG chính vẫn chạy để rollback ngay lập tức
- Phiên bản cải tiến của blue/green với tự động hóa

**Mẹo thi:** Nếu bạn thấy "canary testing" trong bài thi, hãy nghĩ đến traffic splitting.

---

## So Sánh Các Phương Pháp Triển Khai

| Phương Pháp | Thời Gian Ngừng | Thời Gian Triển Khai | Chi Phí | Tốc Độ Rollback | Triển Khai Code Đến |
|-------------|----------------|---------------------|---------|-----------------|-------------------|
| All at Once | Có | Nhanh nhất | Không | Thủ công | Instance hiện có |
| Rolling | Không | Trung bình | Không | Thủ công | Instance hiện có |
| Rolling with Additional Batch | Không | Trung bình-Dài | Nhỏ | Thủ công | Instance hiện có + Mới |
| Immutable | Không | Dài nhất | Cao | Rất nhanh | Instance mới |
| Blue/Green | Không | Thủ công | Cao | Nhanh | Môi trường mới |
| Traffic Splitting | Không | Trung bình | Cao | Tự động & Nhanh | Instance mới |

## Chọn Chiến Lược Phù Hợp

### Sử dụng All at Once khi:
- Làm việc trong môi trường phát triển
- Cần triển khai nhanh nhất
- Thời gian ngừng hoạt động có thể chấp nhận được

### Sử dụng Rolling khi:
- Không yêu cầu thời gian ngừng hoạt động
- Ngân sách hạn chế (không có chi phí bổ sung)
- Có thể chấp nhận công suất giảm

### Sử dụng Rolling with Additional Batch khi:
- Môi trường production
- Phải duy trì công suất đầy đủ
- Ngân sách cho phép chi phí bổ sung nhỏ

### Sử dụng Immutable khi:
- Môi trường production với yêu cầu uptime quan trọng
- Cần khả năng rollback nhanh
- Ngân sách cho phép chi phí cao hơn

### Sử dụng Blue/Green khi:
- Cần kiểm thử rộng rãi trước khi triển khai đầy đủ
- Muốn kiểm soát thủ công việc chuyển đổi traffic
- Có thể quản lý nhiều môi trường

### Sử dụng Traffic Splitting khi:
- Cần canary testing tự động
- Muốn rollback tự động
- Môi trường production với yêu cầu giám sát nghiêm ngặt

## Những Điểm Cần Lưu Ý Cho Kỳ Thi

Kỳ thi AWS thường bao gồm các câu hỏi dựa trên kịch bản về các phương pháp triển khai Elastic Beanstalk. Các điểm chính cần nhớ:

1. **All at Once** = Nhanh nhất nhưng có thời gian ngừng hoạt động
2. **Rolling** = Không có chi phí bổ sung nhưng công suất giảm
3. **Rolling with Additional Batch** = Chi phí bổ sung nhỏ, duy trì công suất
4. **Immutable** = Chi phí cao, rollback nhanh nhất
5. **Traffic Splitting** = Canary testing với rollback tự động
6. **Blue/Green** = Thủ công nhưng cho phép kiểm thử rộng rãi

Hiểu rõ sự đánh đổi giữa tốc độ, chi phí, thời gian ngừng hoạt động và khả năng rollback là điều cần thiết để chọn chiến lược triển khai phù hợp.

## Tài Nguyên Bổ Sung

Để biết thông tin chi tiết hơn, tham khảo [Tài Liệu Triển Khai AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.deploy-existing-version.html) cung cấp bảng so sánh toàn diện về tất cả các phương pháp triển khai.

---

**Tóm tắt:** Bây giờ bạn đã hiểu các chiến lược triển khai Elastic Beanstalk khác nhau và có thể chọn phương pháp phù hợp dựa trên yêu cầu của ứng dụng, hạn chế ngân sách và nhu cầu uptime của bạn.