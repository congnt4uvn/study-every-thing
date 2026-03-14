# Ghi chú học AWS — Tích hợp Amazon ECS với AWS X-Ray

Tài liệu này được viết **dựa trên nội dung trong** `file.txt` (bài giảng về cách chạy X-Ray daemon trong ECS và 3 lựa chọn triển khai).

## Mục tiêu
Nắm được *cách chạy X-Ray daemon với ECS* và **3 phương án phổ biến**.

## Ý chính: X-Ray daemon làm gì?
Ứng dụng (SDK) sẽ gửi dữ liệu trace (UDP) đến **X-Ray daemon**. Daemon sẽ tổng hợp và gửi tiếp dữ liệu lên dịch vụ AWS X-Ray.

“Takeaway” quan trọng của bài giảng:
- Mở **UDP port 2000** cho container X-Ray daemon
- Cấu hình ứng dụng trỏ đến daemon bằng **`AWS_XRAY_DAEMON_ADDRESS`** (trong slide gọi là “AWS X-Ray Daemon Address”)
- Đảm bảo **kết nối mạng** giữa app container và daemon container

---

## Lựa chọn 1 — ECS chạy trên EC2: X-Ray daemon dạng *Daemon task* (mỗi EC2 một daemon)
**Khi bạn quản lý các EC2 instance** trong ECS cluster, bạn có thể chạy X-Ray daemon dưới dạng **Daemon service/task**.

### Cách hoạt động
- ECS cluster chạy trên EC2 (bạn kiểm soát instance).
- Tạo một daemon task chạy **X-Ray daemon container**.
- ECS đảm bảo **mỗi EC2 instance** sẽ có **1 container daemon**.

### Hình dung nhanh
Nếu có 10 EC2 instance thì sẽ có **10 X-Ray daemon container** (mỗi instance một cái).

### Ưu / nhược (để học)
- Ưu: Ít daemon hơn (1/host); nhiều app trên cùng host có thể dùng chung.
- Nhược: Chỉ áp dụng cho EC2; cần cấu hình mạng để app gửi UDP đến daemon.

---

## Lựa chọn 2 — ECS chạy trên EC2: *Sidecar pattern* (mỗi app một sidecar)
Thay vì chạy 1 daemon/host, bạn chạy daemon **đi kèm** với app.

### Cách hoạt động
- Mỗi task definition gồm:
  - **application container**
  - **xray-daemon container** (sidecar) chạy song song

### Hình dung nhanh
Nếu một EC2 instance chạy 20 app containers/tasks, có thể sẽ có **20 X-Ray sidecar**.

### Ưu / nhược (để học)
- Ưu: “Cùng task” nên dễ liên lạc (tuỳ network mode).
- Nhược: Tốn tài nguyên hơn (nhiều daemon containers hơn).

---

## Lựa chọn 3 — ECS chạy trên Fargate: Sidecar pattern (bắt buộc)
Với **Fargate**, bạn **không kiểm soát** EC2 bên dưới.

### Hệ quả
- Bạn **không thể** chạy X-Ray daemon theo kiểu daemon task trên từng instance.
- Bạn **phải** chạy X-Ray daemon như **sidecar container** trong từng Fargate task.

---

## Ví dụ: 3 điểm cần kiểm tra trong task definition (theo bài giảng)
Bài giảng nhấn mạnh 3 chi tiết quan trọng.

### 1) Port mapping cho X-Ray daemon
- Container port: **2000**
- Protocol: **UDP**

### 2) Biến môi trường trong app container
Cấu hình địa chỉ daemon để ứng dụng biết nơi gửi trace.

Các giá trị hay gặp:
- `AWS_XRAY_DAEMON_ADDRESS=xray-daemon:2000` (đúng tinh thần “hostname + port” của bài)
- `AWS_XRAY_DAEMON_ADDRESS=127.0.0.1:2000` (thường dùng khi 2 containers chia sẻ mạng trong cùng task)

### 3) Kết nối mạng giữa 2 containers
Trong transcript có nhắc việc “link” để resolve hostname (ví dụ `links: ["xray-daemon"]`).

> Điểm cần nhớ: dù dùng network mode nào, **app phải gửi được UDP/2000 tới daemon**.

---

## Checklist ngắn (để thuộc)
- [ ] Xác định launch type: **EC2** hay **Fargate**
- [ ] Chọn pattern:
  - [ ] EC2: **Daemon task** (1/instance) hoặc **Sidecar** (1/app)
  - [ ] Fargate: **Sidecar**
- [ ] Daemon nghe **UDP/2000**
- [ ] App set `AWS_XRAY_DAEMON_ADDRESS`
- [ ] Kiểm tra kết nối mạng (security group / network mode / task definition)

---

## Tự kiểm tra
1. Vì sao Fargate không dùng được daemon task kiểu EC2?
2. Nếu ECS cluster có 12 EC2 instance, theo cách daemon task sẽ có bao nhiêu X-Ray daemon containers?
3. Theo sidecar pattern, mối quan hệ giữa app task và daemon container thường là gì?
4. Port và protocol nào được nhấn mạnh cho X-Ray daemon?
5. Biến môi trường nào được dùng để trỏ app đến daemon?
