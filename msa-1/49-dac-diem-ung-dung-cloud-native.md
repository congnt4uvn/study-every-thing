# Ứng Dụng Cloud Native - Các Đặc Điểm Chính

## Giới Thiệu

Trong bài giảng này, chúng ta sẽ tìm hiểu về các đặc điểm quan trọng của ứng dụng cloud-native. Khi bạn nhìn thấy những đặc điểm này trong bất kỳ ứng dụng nào, bạn có thể dễ dàng xác định chúng là ứng dụng cloud-native.

## Các Đặc Điểm Chính

### 1. Kiến Trúc Microservices

Đặc điểm chính đầu tiên của ứng dụng cloud-native là **microservices**.

- Xây dựng ứng dụng dựa trên microservice có tính **liên kết lỏng lẻo** và **kích thước nhỏ gọn**
- Cung cấp tính linh hoạt để phát triển chúng **song song**
- Cho phép **triển khai và mở rộng độc lập**
- Đây là lợi thế chính của ứng dụng cloud-native
- Ứng dụng cloud-native là một chủ đề rộng hơn, và microservices là một trong những tính năng quan trọng của nó

### 2. Containerization (Đóng Gói Container)

Sau khi xây dựng microservices và tách biệt logic nghiệp vụ, bạn sẽ đóng gói ứng dụng của mình với sự trợ giúp của **Docker** hoặc phần mềm containerization khác.

**Lợi Ích của Container:**
- Ứng dụng được đóng gói và triển khai bằng Docker containers
- Cung cấp **môi trường nhẹ và nhất quán** để chạy ứng dụng
- Làm cho ứng dụng **có tính di động cao** trên các nền tảng và hạ tầng đám mây khác nhau
- Code hoạt động tương tự bất kể môi trường đám mây nào (hệ thống local, AWS, GCP, Azure)
- Tất cả các nền tảng đám mây sẽ hoạt động theo cách rất tương tự

**So Sánh với Ứng Dụng Monolithic:**
- Ứng dụng monolithic không cung cấp sự linh hoạt như vậy
- Đòi hỏi nỗ lực đáng kể để mang lại tính nhất quán trên tất cả các nền tảng đám mây

### 3. Khả Năng Mở Rộng và Đàn Hồi

Ứng dụng cloud-native cung cấp khả năng mở rộng và đàn hồi tuyệt vời.

- Ứng dụng được xây dựng trên microservices và containers có thể dễ dàng **mở rộng theo chiều ngang**
- Có thể xử lý bất kỳ loại lưu lượng truy cập nào đến ứng dụng của bạn
- Việc thêm nhiều instances của dịch vụ cực kỳ dễ dàng
- Có thể đạt được tự động với các nền tảng điều phối container như **Kubernetes**
- Có thể tự động mở rộng ứng dụng microservice với Kubernetes

### 4. Thực Hành DevOps

Ứng dụng cloud-native tuân theo các thực hành DevOps bằng cách áp dụng các nguyên tắc DevOps.

**Lợi Ích:**
- Thúc đẩy **văn hóa hợp tác** giữa các nhóm phát triển và vận hành
- Không có sự đổ lỗi giữa các nhà phát triển và nhóm vận hành
- Tích hợp **continuous integration (CI)**
- Hỗ trợ **continuous delivery (CD)**
- Kích hoạt **quy trình triển khai tự động**
- Tối ưu hóa quy trình phát triển và triển khai phần mềm
- Cung cấp sự linh hoạt hoàn toàn cho tổ chức để lựa chọn:
  - Chỉ Continuous Integration
  - Continuous Delivery
  - Continuous Deployment

### 5. Khả Năng Phục Hồi và Chịu Lỗi

Các ứng dụng được phát triển với các nguyên tắc cloud-native có tính phục hồi và chịu lỗi cao.

**Tính Năng Chính:**
- Có thể chịu đựng mọi loại lỗi
- Sử dụng các kỹ thuật như:
  - Kiến trúc phân tán
  - Cân bằng tải (Load balancing)
  - Khôi phục lỗi tự động
- Đảm bảo **tính sẵn sàng cao** và **khả năng chịu lỗi**

**Ví Dụ Thực Tế:**
- Triển khai một microservice ở nhiều vị trí
- Nếu một vị trí bị ngừng hoạt động (mất điện hoặc sự cố internet), microservice vẫn tiếp tục hoạt động từ các vị trí khác
- Các nền tảng như Kubernetes có thể tự động:
  - Tắt các instances microservice không hoạt động
  - Khởi động các instances mới tự động
- Đảm bảo khôi phục lỗi tự động và khả năng chịu lỗi

### 6. Tận Dụng Các Dịch Vụ Cloud-Native

Ứng dụng cloud-native tận dụng các dịch vụ cloud-native ở mức độ lớn.

**Ưu Điểm:**
- Được phát triển để **tận dụng môi trường đám mây** một cách rộng rãi
- Tổ chức không phải tập trung vào hạ tầng
- Tất cả các dịch vụ được **giám sát và duy trì** bởi nhà cung cấp nền tảng đám mây
- Các nhà phát triển và tổ chức có thể tập trung nhiều hơn vào:
  - Logic ứng dụng
  - Cải thiện logic nghiệp vụ
- Ít tập trung hơn vào các thành phần hạ tầng

## Kết Luận

Đây là tất cả các đặc điểm quan trọng của ứng dụng cloud-native. Trong suốt khóa học này, chúng ta sẽ khám phá tất cả các đặc điểm này trong các phần khác nhau.

Khi bạn thấy một ứng dụng tuân theo tất cả các đặc điểm này, bạn có thể tự tin khẳng định đó là một ứng dụng cloud-native.

---

*Ghi chú: Tài liệu này là một phần của khóa học toàn diện về microservices với Spring Boot và ứng dụng cloud-native.*