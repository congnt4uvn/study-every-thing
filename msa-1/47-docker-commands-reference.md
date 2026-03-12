# Các Lệnh Docker Cơ Bản Sử Dụng Hàng Ngày

## Tổng Quan

Hướng dẫn này bao gồm các lệnh Docker quan trọng nhất mà bạn sẽ sử dụng hàng ngày khi làm việc với microservices. Các lệnh này cũng thường được hỏi trong các buổi phỏng vấn kỹ thuật.

## Các Lệnh Quản Lý Image

### 1. Liệt Kê Docker Images

```bash
docker images
```

Liệt kê tất cả các Docker images có trong Docker server cục bộ của bạn.

### 2. Kiểm Tra Chi Tiết Docker Image

```bash
docker image inspect <image_id>
```

Hiển thị thông tin chi tiết về một image cụ thể. Bạn có thể sử dụng 3-4 ký tự đầu tiên của image ID thay vì ID đầy đủ.

**Lưu ý:** Docker đủ thông minh để phát hiện toàn bộ image ID hoặc container ID dựa trên giá trị ngắn được cung cấp.

### 3. Xóa Docker Image

```bash
docker image rm <image_id>
```

Xóa một hoặc nhiều Docker images. Bạn có thể chỉ định nhiều image IDs cách nhau bởi dấu cách.

**Lệnh thay thế:**
```bash
docker rmi <image_id>
```

### 4. Build Docker Image

```bash
docker build -t <image_name> .
```

Tạo Docker image dựa trên Dockerfile. Cờ `-t` chỉ định tag (tên image).

**Quan trọng:** Đảm bảo Dockerfile có trong cùng vị trí mà bạn chạy lệnh này.

### 5. Push Docker Image

```bash
docker image push <image_name>
```

Đẩy Docker image từ hệ thống cục bộ lên repository từ xa (ví dụ: Docker Hub).

### 6. Pull Docker Image

```bash
docker image pull <image_name>
```

Kéo Docker image từ repository từ xa về hệ thống cục bộ.

### 7. Xóa Images Không Sử Dụng

```bash
docker image prune
```

Xóa tất cả images không được sử dụng. Một image được coi là không sử dụng nếu không có container nào liên kết (đang chạy hoặc đã dừng).

### 8. Xem Lịch Sử Image

```bash
docker history <image_name>
```

Hiển thị tất cả các lớp trung gian và các lệnh được thực thi trong quá trình build image. Hữu ích cho việc debug các vấn đề build image.

## Các Lệnh Quản Lý Container

### 9. Chạy Container

```bash
docker run -p <host_port>:<container_port> <image_name>
```

Khởi động Docker container dựa trên một image với ánh xạ port.

### 10. Liệt Kê Containers Đang Chạy

```bash
docker ps
```

Hiển thị tất cả containers đang chạy.

### 11. Liệt Kê Tất Cả Containers

```bash
docker ps -a
```

Hiển thị tất cả containers, bao gồm cả đang chạy và đã dừng.

### 12. Khởi Động Container

```bash
docker container start <container_id>
```

Khởi động một container đã dừng trước đó. Bạn có thể chỉ định nhiều container IDs cách nhau bởi dấu cách.

### 13. Dừng Container

```bash
docker container stop <container_id>
```

Dừng container đang chạy một cách nhẹ nhàng. Docker server cho container khoảng 5 giây để đóng các tài nguyên (kết nối database, file systems, v.v.) trước khi dừng.

### 14. Kill Container

```bash
docker container kill <container_id>
```

Kill một hoặc nhiều containers đang chạy ngay lập tức mà không đợi graceful shutdown.

**Sự khác biệt giữa Stop và Kill:**
- **Stop:** Cho container ~5 giây để đóng các tài nguyên
- **Kill:** Kết thúc container ngay lập tức

### 15. Tạm Dừng Container

```bash
docker container pause <container_id>
```

Tạm dừng container tạm thời để nó ngừng nhận traffic.

### 16. Tiếp Tục Container

```bash
docker container unpause <container_id>
```

Tiếp tục container đã tạm dừng để nó bắt đầu nhận requests trở lại.

### 17. Khởi Động Lại Container

```bash
docker container restart <container_id>
```

Khởi động lại một hoặc nhiều containers.

### 18. Kiểm Tra Chi Tiết Container

```bash
docker container inspect <container_id>
```

Hiển thị thông tin chi tiết về một container.

### 19. Xem Logs Container

```bash
docker container logs <container_id>
```

Lấy tất cả logs của một container.

**Mẹo:** Sử dụng Docker Desktop thuận tiện hơn để xem logs theo thời gian thực.

### 20. Theo Dõi Logs Container

```bash
docker container logs -f <container_id>
```

Liên tục theo dõi đầu ra logs của container trong terminal. Cờ `-f` yêu cầu Docker theo dõi đầu ra logs liên tục.

### 21. Xem Thống Kê Container

```bash
docker container stats
```

Hiển thị thống kê container bao gồm CPU utilization, memory usage, và I/O usage.

### 22. Thực Thi Lệnh Trong Container Đang Chạy

```bash
docker exec -it <container_id> sh
```

Mở shell bên trong container đang chạy, cho phép bạn thực thi các lệnh trong môi trường của container.

### 23. Xóa Container

```bash
docker rm <container_id>
```

Xóa một hoặc nhiều containers. Bạn có thể chỉ định nhiều container IDs cách nhau bởi dấu cách.

### 24. Xóa Tất Cả Containers Đã Dừng

```bash
docker container prune
```

Xóa tất cả containers đã dừng bằng một lệnh duy nhất. Bạn không cần chỉ định container IDs.

## Các Lệnh Bảo Trì Hệ Thống

### 25. Dọn Dẹp Toàn Hệ Thống

```bash
docker system prune
```

Xóa tất cả:
- Containers đã dừng
- Images không sử dụng
- Networks không sử dụng
- Volumes không sử dụng
- Build cache

### 26. Đăng Nhập Docker Hub

```bash
docker login -u <username>
```

Đăng nhập vào Docker Hub từ CLI. Bạn sẽ được nhắc nhập mật khẩu.

**Lưu ý:** Nếu bạn đang sử dụng Docker Desktop, bạn có thể đăng nhập qua trình duyệt, và CLI của bạn sẽ tự động kết nối với tài khoản Docker Hub.

### 27. Đăng Xuất Docker Hub

```bash
docker logout
```

Đăng xuất khỏi tài khoản Docker Hub Container Registry.

## Các Lệnh Docker Compose

### 28. Khởi Động Services Với Docker Compose

```bash
docker compose up
```

Tạo và khởi động containers dựa trên file Docker Compose.

### 29. Dừng và Xóa Services

```bash
docker compose down
```

Dừng và xóa containers được định nghĩa trong file Docker Compose.

### 30. Dừng Services (Không Xóa)

```bash
docker compose stop
```

Dừng containers mà không xóa chúng.

### 31. Khởi Động Services Đã Tồn Tại

```bash
docker compose start
```

Khởi động containers đã được tạo trước đó (không tạo containers từ đầu).

## Các Thực Hành Tốt Nhất

1. **Sử Dụng Docker Desktop:** Cách thuận tiện nhất để tương tác với Docker images và containers, vì nó cung cấp giao diện người dùng thân thiện.

2. **IDs Ngắn:** Bạn có thể sử dụng 3-4 ký tự đầu tiên của bất kỳ ID nào (image hoặc container) thay vì ID đầy đủ.

3. **Graceful Shutdown:** Ưu tiên `docker container stop` hơn `docker container kill` để cho phép dọn dẹp tài nguyên đúng cách.

4. **Dọn Dẹp Định Kỳ:** Sử dụng các lệnh prune thường xuyên để giải phóng không gian đĩa.

5. **Giám Sát Logs:** Sử dụng Docker Desktop để xem logs theo thời gian thực trong quá trình phát triển.

## Tóm Tắt

Các lệnh Docker này rất cần thiết cho công việc phát triển microservices hàng ngày và thường được đề cập trong các buổi phỏng vấn kỹ thuật. Hãy giữ tài liệu tham khảo này trong tầm tay, và cũng kiểm tra trang GitHub repository để có thêm tài nguyên.

Nhớ rằng: Chọn cách tiếp cận phù hợp nhất với bạn—lệnh CLI hoặc giao diện Docker Desktop UI!