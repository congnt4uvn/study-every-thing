# Các Lệnh Docker Compose: Start, Stop, Up và Down

## Tổng Quan

Trong bài giảng này, chúng ta sẽ khám phá các lệnh Docker Compose khác nhau và hiểu khi nào nên sử dụng từng lệnh. Chúng ta sẽ tìm hiểu sự khác biệt chính giữa `docker compose up`, `docker compose down`, `docker compose start` và `docker compose stop`.

## Các Lệnh Docker Compose

### Docker Compose Up

Lệnh `docker compose up` được sử dụng để **tạo và khởi động container từ đầu**.

```bash
docker compose up
```

- Tạo các container mới dựa trên cấu hình docker-compose.yml của bạn
- Nếu container chưa tồn tại, nó sẽ tạo chúng
- Nếu container đã tồn tại với cùng tên, nó sẽ sử dụng các container có sẵn đó
- Sử dụng cờ `-d` để chạy ở chế độ detached (chạy nền)

```bash
docker compose up -d
```

### Docker Compose Down

Lệnh `docker compose down` được sử dụng để **dừng và xóa container**.

```bash
docker compose down
```

- Dừng tất cả các container đang chạy
- Xóa hoàn toàn các container
- Giải phóng tài nguyên hệ thống

### Docker Compose Stop

Lệnh `docker compose stop` được sử dụng để **dừng container mà không xóa chúng**.

```bash
docker compose stop
```

- Dừng tất cả các container đang chạy được khởi động bằng docker compose
- Các container vẫn còn trong hệ thống (không bị xóa)
- Hữu ích khi bạn muốn tạm dừng dịch vụ của mình
- Nếu không có container nào đang chạy, lệnh này không có tác dụng gì

### Docker Compose Start

Lệnh `docker compose start` được sử dụng để **khởi động các container đã dừng có sẵn**.

```bash
docker compose start
```

- Tìm kiếm các container có sẵn và khởi động chúng
- KHÔNG tạo container mới
- Chỉ hoạt động nếu container đã tồn tại
- Nếu không có container nào tồn tại, lệnh sẽ thất bại

## Sự Khác Biệt Chính

### `docker compose up` vs `docker compose start`

- **`docker compose up`**: Tạo container từ đầu nếu chúng chưa tồn tại, hoặc sử dụng container có sẵn nếu đã có
- **`docker compose start`**: Chỉ khởi động các container đã dừng có sẵn; thất bại nếu không có container nào tồn tại

### `docker compose down` vs `docker compose stop`

- **`docker compose down`**: Dừng VÀ xóa hoàn toàn các container
- **`docker compose stop`**: Chỉ dừng container; giữ chúng để sử dụng sau

## Ví Dụ Thực Tế

Đây là quy trình làm việc điển hình:

1. **Thiết lập ban đầu**: Tạo và khởi động container
   ```bash
   docker compose up -d
   ```

2. **Tạm dừng**: Dừng container mà không xóa chúng
   ```bash
   docker compose stop
   ```

3. **Tiếp tục làm việc**: Khởi động lại các container đã dừng
   ```bash
   docker compose start
   ```

4. **Dọn dẹp**: Dừng và xóa tất cả container
   ```bash
   docker compose down
   ```

## Thực Hành Tốt Nhất

- **Sử dụng `docker compose up` và `docker compose down`** cho hầu hết các hoạt động hàng ngày
- Luôn xóa container khi bạn không cần chúng để giải phóng không gian hệ thống
- Chỉ sử dụng `docker compose stop` và `docker compose start` khi bạn cần bảo toàn trạng thái container tạm thời

## Các Dịch Vụ Ví Dụ

Trong phần demo, chúng ta làm việc với ba microservice:
- **accounts-ms** (Microservice Tài khoản)
- **loans-ms** (Microservice Khoản vay)
- **cards-ms** (Microservice Thẻ)

## Kiểm Tra

Bạn có thể kiểm tra trạng thái container của mình bằng cách:
- Giao diện Docker Desktop
- Dòng lệnh với `docker ps` (cho container đang chạy)
- Dòng lệnh với `docker ps -a` (cho tất cả container, bao gồm cả đã dừng)

## Tóm Tắt

Hiểu được sự khác biệt giữa các lệnh Docker Compose này là rất quan trọng cho việc quản lý container hiệu quả:

- `docker compose up`: Tạo và khởi động (từ đầu hoặc từ container có sẵn)
- `docker compose down`: Dừng và xóa
- `docker compose start`: Khởi động các container đã dừng có sẵn
- `docker compose stop`: Dừng mà không xóa

Chọn lệnh phù hợp dựa trên việc bạn muốn bảo toàn hay xóa container của mình.