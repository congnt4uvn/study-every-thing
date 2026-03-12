# Khởi Động Microservices với Docker Compose

## Tổng Quan

Trong bài học này, chúng ta sẽ tìm hiểu cách khởi động tất cả các microservices bằng lệnh Docker Compose. Docker Compose cho phép chúng ta quản lý nhiều container với một lệnh duy nhất, giúp làm việc với kiến trúc microservices dễ dàng hơn.

## Yêu Cầu Trước Khi Bắt Đầu

- Đã cài đặt Docker Desktop
- File cấu hình Docker Compose YAML đã được thiết lập
- Các microservices (accounts, loans, cards) sẵn sàng để chạy

## Lỗi Thường Gặp: Chạy Docker Compose Từ Thư Mục Sai

Khi thực hiện lệnh Docker Compose, bạn phải ở trong thư mục chứa file `docker-compose.yaml`.

### Ví Dụ Về Lỗi

Nếu bạn đang ở trong thư mục cards microservice mà không có file Docker Compose và chạy:

```bash
docker compose up
```

Bạn sẽ nhận được lỗi:
```
no configuration file provided, not found
```

### Giải Pháp

Di chuyển đến thư mục chứa file `docker-compose.yaml` (ví dụ: thư mục accounts):

```bash
cd accounts
ls  # Xác nhận file docker-compose.yaml có mặt
```

## Khởi Động Microservices với Docker Compose

### Lệnh Cơ Bản

```bash
docker compose up
```

Lệnh này khởi động tất cả các container được định nghĩa trong file Docker Compose YAML. Tuy nhiên, lệnh này sẽ giữ terminal của bạn bận với các log.

### Chế Độ Detached (Khuyến Nghị)

Để khởi động containers ở chế độ nền:

```bash
docker compose up -d
```

Cờ `-d` chạy containers ở chế độ detached, giải phóng terminal của bạn.

### Kiểm Tra Containers Đang Chạy

Kiểm tra các containers đang chạy bằng:

```bash
docker ps
```

Kết quả mong đợi hiển thị:
- Ba microservices đang chạy
- Các cổng: 8080, 8090, 9000
- Tên containers như đã cấu hình

### Xem Trong Docker Desktop

Trong Docker Desktop:
1. Điều hướng đến **Containers**
2. Bạn sẽ thấy một thư mục cha (được đặt tên theo thư mục nơi bạn chạy lệnh)
3. Dưới thư mục này, cả ba microservices xuất hiện:
   - Loans microservice
   - Cards microservice
   - Accounts microservice

**Lưu ý**: Có thể có lỗi hiển thị nơi "accounts-ms" hiển thị chỉ là "ms" trong Docker Desktop, nhưng CLI hiển thị tên đúng.

## Kiểm Tra Các Microservices

Sau khi khởi động containers, kiểm tra từng microservice:

### Tạo Account
- Cổng: 8080
- Gửi request → Phản hồi thành công ✓

### Tạo Loan
- Cổng: 8090
- Gửi request → Phản hồi thành công ✓

### Tạo Card
- Cổng: 9000
- Gửi request → Phản hồi thành công ✓

## Dừng Microservices với Docker Compose

### Dừng và Xóa Containers (Khuyến Nghị)

```bash
docker compose down
```

Lệnh này:
- Dừng tất cả containers
- Xóa tất cả containers
- Dọn dẹp tài nguyên

**Lưu ý**: Cờ `-d` không áp dụng cho `docker compose down`.

### Dừng Mà Không Xóa

```bash
docker compose stop
```

Lệnh này chỉ dừng containers mà không xóa chúng. Tuy nhiên, nên sử dụng `docker compose down` để dọn dẹp tài nguyên.

### Xác Nhận

Kiểm tra Docker Desktop sau khi chạy `docker compose down`:
- Tất cả containers đã được xóa
- Không còn containers nào trong danh sách

## Tóm Tắt Các Lệnh Docker Compose Chính

| Lệnh | Mục Đích |
|---------|---------|
| `docker compose up` | Khởi động tất cả containers (chế độ foreground) |
| `docker compose up -d` | Khởi động tất cả containers (chế độ nền/detached) |
| `docker compose down` | Dừng và xóa tất cả containers |
| `docker compose stop` | Dừng containers mà không xóa |
| `docker ps` | Liệt kê các containers đang chạy |

## Mạng (Networking)

Một mạng Docker có tên `easybank` đã được tạo trong cấu hình Docker Compose. Mạng này cho phép:
- Giao tiếp giữa các containers
- Phát hiện dịch vụ (Service discovery)
- Cách ly mạng

Chúng ta sẽ khám phá chi tiết về giao tiếp mạng giữa các containers trong các phần tiếp theo sử dụng mạng bridge driver.

## Thực Hành Tốt Nhất

### Cấu Trúc File YAML

1. **Thụt Lề Rất Quan Trọng**: Mỗi khoảng trắng đều có ý nghĩa trong file YAML
2. **Xác Thực Cú Pháp**: Đảm bảo cấu trúc đúng trước khi chạy
3. **Kiểm Soát Phiên Bản**: Lưu docker-compose.yaml trong kho GitHub của bạn
4. **Tính Nhất Quán**: Tuân theo cấu trúc đã thiết lập cho tất cả các dịch vụ

### Lưu Ý Quan Trọng

⚠️ **Luôn chạy lệnh Docker Compose từ thư mục chứa file `docker-compose.yaml`**

⚠️ **Chú ý đến thụt lề YAML** - khoảng cách không đúng sẽ gây lỗi

⚠️ **Sử dụng `docker compose down`** thay vì `stop` để dọn dẹp tài nguyên đúng cách

## Ưu Điểm Của Docker Compose

- **Quản Lý Bằng Một Lệnh**: Khởi động/dừng nhiều microservices cùng lúc
- **Cấu Hình Nhất Quán**: Tất cả dịch vụ được định nghĩa trong một file
- **Dễ Dàng Sao Chép**: Chia sẻ cấu hình giữa các nhóm
- **Quản Lý Mạng**: Tự động tạo và cấu hình mạng
- **Ánh Xạ Cổng**: Cấu hình cổng tập trung

## Các Bước Tiếp Theo

Trong các bài học tiếp theo, chúng ta sẽ đi sâu hơn vào:
- Mạng container và giao tiếp giữa các dịch vụ
- Cấu hình Docker Compose nâng cao
- Phụ thuộc dịch vụ và thứ tự khởi động
- Cấu hình theo môi trường cụ thể

## Kết Luận

Docker Compose đơn giản hóa việc quản lý microservices bằng cách cho phép bạn:
- Khởi động nhiều dịch vụ với `docker compose up -d`
- Dừng và dọn dẹp với `docker compose down`
- Quản lý các ứng dụng đa container phức tạp một cách hiệu quả

Hãy chắc chắn rằng bạn hiểu cấu trúc và cú pháp của file Docker Compose YAML, vì nó là nền tảng để làm việc với các microservices được container hóa.

---

**Cảm ơn bạn, và hẹn gặp lại trong bài học tiếp theo!**