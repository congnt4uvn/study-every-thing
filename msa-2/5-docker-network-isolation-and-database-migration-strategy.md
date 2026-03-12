# Cô Lập Mạng Docker và Chiến Lược Di Chuyển Cơ Sở Dữ Liệu

## Tổng Quan

Bài giảng này trình bày các khái niệm về mạng Docker và giải thích quyết định chiến lược di chuyển từ MySQL sang cơ sở dữ liệu H2 cho môi trường phát triển trong kiến trúc microservices.

## Minh Họa Mạng Docker

### Cấu Hình Mạng Hiện Tại

Tất cả microservices và containers hiện đang được cấu hình để chạy trong cùng một mạng Docker có tên **EazyBank**. Điều này đạt được thông qua cấu hình `network-deploy-service` mà tất cả các services đều kế thừa.

### Kiểm Tra Cô Lập Mạng

Để minh họa cô lập mạng:

1. **Tách Container Cơ Sở Dữ Liệu**: Loại bỏ cấu hình mạng khỏi các database containers bằng cách sửa file `common-config.yaml`
2. **Kết Quả Mong Đợi**: Microservices sẽ không thể giao tiếp với database containers
3. **Xác Thực**: Sử dụng profile QA để kiểm tra kịch bản này

### Các Lệnh Chính

```bash
# Dừng tất cả containers đang chạy
docker compose down

# Khởi động containers với profile QA
docker compose up -d

# Liệt kê các mạng Docker
docker network ls

# Kiểm tra mạng của container
docker inspect <container-id>
```

### Hành Vi Quan Sát Được

Khi databases bị tách khỏi mạng EazyBank:
- Các database containers (loans, accounts, cards) khởi động thành công
- Config server microservice khởi động thành công
- Các application microservices (accounts, loans, cards) ban đầu khởi động nhưng sau đó thoát
- Xảy ra lỗi kết nối vì các containers nằm trên các mạng khác nhau

### Kiến Trúc Mạng

- **Mạng Mặc Định**: Khi không chỉ định mạng, Docker Compose gán containers vào mạng `qa_default`
- **Mạng Tùy Chỉnh**: Microservices được cấu hình sử dụng mạng EazyBank
- **Nguyên Tắc Cô Lập**: Các containers trên các mạng khác nhau không thể giao tiếp trừ khi được cấu hình rõ ràng

## Di Chuyển từ MySQL sang Cơ Sở Dữ Liệu H2

### Thách Thức Kiến Trúc Hiện Tại

Hiện tại, cấu hình Docker Compose bao gồm:
- 3 database containers (các instances MySQL)
- 1 config server
- 3 microservices (accounts, loans, cards)
- **Tổng cộng: 7 containers đang chạy**

### Mối Quan Ngại về Mở Rộng Tương Lai

Các thành phần bổ sung sẽ được thêm vào:
- Eureka Server
- Gateway Server
- Grafana monitoring containers
- Các cơ sở hạ tầng microservices khác

**Kết Quả Dự Kiến**: 10-12+ containers chạy đồng thời

### Cân Nhắc về Hiệu Suất

**Vấn Đề**: Chạy nhiều containers đồng thời gây ra:
- Hệ thống chậm đáng kể
- Các vấn đề runtime tiềm ẩn
- Khó khăn trong debugging
- Mất động lực phát triển

**Tác Động**: Đặc biệt nghiêm trọng trên các hệ thống có 8GB RAM

### Giải Pháp: Di Chuyển sang H2 Database

**Quyết Định**: Di chuyển trở lại cơ sở dữ liệu H2 in-memory cho phát triển

**Lý Do**:
- Giảm số lượng containers (loại bỏ 3 MySQL containers)
- Cải thiện hiệu suất laptop
- Duy trì năng suất phát triển
- Ngăn chặn cạn kiệt tài nguyên hệ thống

### Tính Linh Hoạt

**Tùy Chọn cho Developers**:
- **Khuyến Nghị**: Sử dụng H2 database để có hiệu suất tối ưu
- **Thay Thế**: Tiếp tục với MySQL nếu sử dụng laptop cao cấp với đủ tài nguyên

Lựa chọn phụ thuộc vào khả năng phần cứng của bạn và sự sẵn sàng quản lý các vấn đề hiệu suất tiềm ẩn.

## Các File Cấu Hình

### Kế Thừa network-deploy-service

```yaml
microservices-db-config:
  extends:
    service: network-deploy-service
```

Cấu hình này đảm bảo tất cả containers khởi động trong mạng được chỉ định (EazyBank).

### Dọn Dẹp Biến Môi Trường

Loại bỏ các biến môi trường RabbitMQ đã lỗi thời từ:
- `common-config.yml` (profile QA)
- `common-config.yml` (profile mặc định)

## Những Điểm Chính Cần Nhớ

1. **Cô Lập Mạng Docker**: Docker cung cấp sự cô lập hoàn toàn giữa các mạng - giao tiếp chỉ hoạt động khi containers chia sẻ cùng một mạng
2. **Hiệu Suất vs Tính Năng**: Cân bằng giữa việc sử dụng cơ sở hạ tầng giống production (MySQL) và duy trì hiệu quả phát triển
3. **Quản Lý Tài Nguyên**: Cân nhắc tài nguyên hệ thống khi thiết kế môi trường phát triển local
4. **Tính Linh Hoạt**: Kiến trúc nên hỗ trợ cả cấu hình nhẹ (H2) và giống production (MySQL)

## Các Bước Tiếp Theo

Từ phần tiếp theo trở đi, khóa học sẽ sử dụng cơ sở dữ liệu H2 cho phát triển local trong khi vẫn duy trì tùy chọn sử dụng MySQL cho những người có đủ tài nguyên hệ thống.

---

**Lưu Ý**: Các nguyên tắc đã học với tích hợp MySQL database vẫn có giá trị và có thể được áp dụng khi triển khai lên môi trường production.