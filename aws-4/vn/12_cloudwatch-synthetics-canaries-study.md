# CloudWatch Synthetics Canaries — Ghi chú học AWS

## Khái niệm
CloudWatch Synthetics cung cấp **canary**: các script có thể cấu hình, được chạy từ **Amazon CloudWatch** để giám sát liên tục:
- **API** (tính sẵn sàng + độ trễ)
- **URL / website** (các luồng end-to-end như người dùng thật)

Ý tưởng chính: bạn định nghĩa một script để mô phỏng tự động những thao tác mà khách hàng thực hiện (ví dụ: vào trang sản phẩm → thêm vào giỏ → checkout). Nếu script thất bại, bạn phát hiện sự cố **trước khi người dùng gặp phải**.

## Có thể đo/thu thập gì
- Tính sẵn sàng và độ trễ của endpoint
- Dữ liệu thời gian tải (load time)
- **Chụp ảnh màn hình** UI (hữu ích để debug)

## Cách canary chạy
- Ngôn ngữ script: **Node.js** hoặc **Python**
- Có thể dùng **Google Chrome headless** (tự động hóa thao tác trình duyệt)
- Chế độ chạy: **chạy một lần** hoặc theo **lịch định kỳ**

## Mẫu vận hành (ví dụ)
1. Ứng dụng triển khai ở một region (ví dụ `us-east-1`).
2. **Synthetics canary** giám sát ứng dụng.
3. Nếu canary fail → **CloudWatch Alarm** được kích hoạt.
4. Alarm gọi **AWS Lambda**.
5. Lambda cập nhật bản ghi DNS trên **Route 53** để chuyển hướng (failover) sang region khác (ví dụ `us-west-2`).

Đây là một cách tự động khắc phục/failover.

## Các blueprint có sẵn (theo nội dung file)
- **Heartbeat Monitor**: tải URL, lưu screenshot + file HTTP archive (HAR), kiểm tra hoạt động đúng.
- **API Canary**: test các chức năng đọc/ghi cơ bản của REST API.
- **Broken Link Checker**: kiểm tra tất cả liên kết trong trang và phát hiện link hỏng.
- **Visual Monitoring**: so sánh screenshot của lần chạy với screenshot baseline đã lưu trước đó.
- **Canary Recorder**: dùng CloudWatch Synthetics Recorder để ghi lại thao tác trên web và tự sinh script.
- **GUI Workflow Builder**: xác minh các thao tác/luồng trên UI (ví dụ: luồng form đăng nhập).

## Khi nào nên chọn Synthetics (gợi ý kiểu đề thi)
Chọn CloudWatch Synthetics Canaries khi bạn cần:
- Giám sát **chủ động** theo “hành trình người dùng” (không chỉ metrics máy chủ)
- Thực hiện kiểm tra **synthetic** theo lịch từ CloudWatch
- Kiểm tra dựa trên trình duyệt (headless Chrome) + screenshot
- Kiểm tra API availability/latency mà không phụ thuộc vào traffic người dùng thật

## Tự kiểm tra nhanh
- Canary script viết bằng ngôn ngữ nào?
- Canary có truy cập được trình duyệt kiểu gì?
- Kể tên 3 blueprint và chức năng của chúng.
- Canary fail có thể kích hoạt failover tự động theo cách nào?
