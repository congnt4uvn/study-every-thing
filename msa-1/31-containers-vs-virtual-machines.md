# Container so với Máy ảo trong Triển khai Microservices

## Giới thiệu

Trong bài giảng này, chúng ta sẽ làm rõ sự khác biệt cơ bản giữa container và máy ảo truyền thống, đồng thời hiểu tại sao container là lựa chọn ưu tiên cho việc triển khai microservices.

## Triển khai Server Truyền thống (Trước thời đại Cloud)

### Cài đặt Server Vật lý
- Các tổ chức mua phần cứng riêng
- Cài đặt hệ điều hành trên phần cứng vật lý
- Server kết nối với mạng công cộng
- Code được triển khai sử dụng web server hoặc application server
- Địa chỉ IP công khai được gán cho server
- Ánh xạ DNS cho truy cập tên miền

## Máy ảo trong Cloud Computing

### Máy ảo là gì?
- Server ảo được cung cấp bởi các nhà cung cấp cloud (AWS, Azure, GCP)
- Không thể nhìn thấy vật lý - chỉ có thể truy cập qua internet
- Được tạo từ phần cứng vật lý trong data center

### Cách tạo Máy ảo

**Cơ sở hạ tầng vật lý:**
- Phần cứng/server vật lý ở tầng dưới cùng
- Nhà cung cấp cloud sử dụng công nghệ **Hypervisor**
- Một server vật lý được chia thành nhiều VM (VM1, VM2, VM3)

**Phân phối tài nguyên:**
- Tài nguyên vật lý (RAM, ổ cứng) được phân phối ảo
- Ví dụ: Server 64GB RAM, 4TB ổ cứng chia sẻ cho nhiều VM
- Mỗi VM có thể có hệ điều hành khác nhau:
  - VM1: Windows OS
  - VM2: Linux OS
  - VM3: Mac OS

### Triển khai Microservices với Máy ảo

**Quy trình cài đặt:**
1. Tạo máy ảo với guest OS
2. Cài đặt thủ công các binary và thư viện cần thiết (JDK, web server, Maven)
3. Triển khai microservice
4. Truy cập qua địa chỉ IP công khai

**Ví dụ kịch bản:**
- AccountService → VM1
- LoanService → VM2
- CardService → VM3

## Vấn đề với Máy ảo cho Microservices

### 1. **Vấn đề về Khả năng mở rộng**
- 100 microservices = 100 VM? Không khả thi!
- Chi phí cloud cao
- Lãng phí tài nguyên (VM 16GB RAM cho microservice nhỏ)

### 2. **Xung đột phụ thuộc**
Khi triển khai nhiều service trong một VM:
- AccountService cần Java 8
- LoanService cần Java 17
- CardService cần Python
- **Kết quả:** Các phụ thuộc không tương thích trong cùng môi trường

### 3. **Rủi ro về tính sẵn sàng**
- Khởi động lại VM ảnh hưởng tất cả các service
- Không có rủi ro downtime chấp nhận được

### 4. **Mở rộng chậm**
Mở rộng từ 1 lên 3 instance yêu cầu:
- Tạo VM mới
- Cài đặt guest OS
- Cài đặt binary và thư viện
- **Tổng thời gian:** ~15 phút
- Đến lúc đó, traffic có thể đã bình thường
- Thu nhỏ quy mô cũng mất 5-10 phút

## Container: Giải pháp

### Kiến trúc Container

**Các tầng cơ sở hạ tầng:**
1. **Phần cứng vật lý** (server)
2. **Hệ điều hành chủ** (Windows/Linux/Mac)
3. **Container Engine** (Docker)
4. **Containers** (AccountService, LoanService, CardService)

### Ưu điểm chính của Container

#### 1. **Nhẹ**
- Không cần hệ điều hành guest riêng
- Chia sẻ hệ điều hành chủ
- Thao tác nhanh (giây, không phải phút):
  - Tạo container
  - Xóa container
  - Khởi động lại container

#### 2. **Môi trường cô lập**
Nhiều container trên cùng server, mỗi container có:
- Container1: Java 8
- Container2: Java 17
- Container3: Python
- Mạng ảo cô lập
- Các container không biết về môi trường của nhau

#### 3. **Tự chứa**
- Tất cả phụ thuộc được đóng gói cùng nhau
- JDK + thư viện Spring Boot được bao gồm
- Không cần cài đặt thủ công

#### 4. **Tính di động**
- Đưa container đóng gói đến bất kỳ môi trường nào
- Chuyển đổi thành container đang chạy với một lệnh duy nhất
- Không cần:
  - Cài đặt Java
  - Download thư viện Spring Boot
  - Cấu hình thủ công

#### 5. **Cô lập tài nguyên**
Mỗi container có riêng:
- Mạng
- Tài nguyên
- Bộ nhớ
- Lưu trữ
- Cô lập trừ khi được cho phép rõ ràng

#### 6. **Triển khai dễ dàng**
- Các thành phần nhẹ
- Khởi động lại/tạo/xóa nhanh chóng
- Downtime tối thiểu

## Máy ảo so với Container: Tóm tắt

| Khía cạnh | Máy ảo | Container |
|-----------|--------|-----------|
| **Guest OS** | Bắt buộc | Không bắt buộc (chia sẻ host OS) |
| **Kích thước** | Nặng (GBs) | Nhẹ (MBs) |
| **Thời gian khởi động** | Phút | Giây |
| **Phân phối tài nguyên** | Hypervisor | Container Engine (Docker) |
| **Cô lập** | Cô lập toàn bộ OS | Cô lập cấp độ process |
| **Tính di động** | Phức tạp | Đơn giản (đóng gói) |
| **Khả năng mở rộng** | Chậm (15 phút) | Nhanh (giây) |
| **Triển khai** | Cần cài đặt thủ công | Một lệnh duy nhất |

## Kết luận

**Điểm chính:** Khi triển khai microservices, nói KHÔNG với máy ảo và nói CÓ với container!

Container giải quyết các thách thức chính của triển khai dựa trên VM:
- ✅ Nhẹ và nhanh
- ✅ Môi trường cô lập
- ✅ Dễ dàng di chuyển
- ✅ Mở rộng nhanh chóng
- ✅ Lãng phí tài nguyên tối thiểu

Trong các bài giảng tiếp theo, chúng ta sẽ thấy những lợi ích này trong thực tế khi chúng ta chuyển đổi microservices của mình thành Docker container.

---

**Bước tiếp theo:** Chuyển đổi microservices thành Docker container và trải nghiệm trực tiếp các ưu điểm.