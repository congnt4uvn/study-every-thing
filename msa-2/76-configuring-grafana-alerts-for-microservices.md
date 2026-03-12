# Cấu Hình Cảnh Báo Grafana Cho Microservices

## Tổng Quan

Hướng dẫn này trình bày cách cấu hình cảnh báo và thông báo trong Grafana để giám sát microservices. Bạn sẽ học cách thiết lập các quy tắc cảnh báo, định nghĩa ngưỡng và cấu hình các kênh thông báo để nhận cảnh báo khi các điều kiện cụ thể được đáp ứng.

## Yêu Cầu Tiên Quyết

- Grafana đã được cài đặt và đang chạy
- Prometheus làm nguồn dữ liệu
- Microservices với metrics được expose
- Docker Desktop (để kiểm thử)

## Tạo Quy Tắc Cảnh Báo

### Bước 1: Điều Hướng Đến Alerting

1. Mở menu Grafana
2. Chọn tùy chọn **Alerting**
3. Nhấp vào **Alert Rules**
4. Nhấp **Create Alert Rule**

### Bước 2: Cấu Hình Thiết Lập Cảnh Báo Cơ Bản

1. **Rule Name**: Nhập tên mô tả (ví dụ: `accounts`)
2. **Alert Type**: Chọn **Grafana managed alert**
   - Điều này cho phép Grafana quản lý các cảnh báo

### Bước 3: Định Nghĩa Tiêu Chí Cảnh Báo

#### Cấu Hình Nguồn Dữ Liệu

1. **Data Source**: Chọn `Prometheus`
2. **Metric**: Chọn metric `up`
   - Metric này cho biết liệu ứng dụng có đang chạy hay không
   - Giá trị `1` = ứng dụng đang chạy
   - Giá trị `0` = ứng dụng đã dừng

3. **Labels**: Cấu hình như sau:
   - **Label**: `job`
   - **Value**: `accounts microservice`

#### Hàm Reduce

1. Chọn hàm **Reduce**
2. Chọn **Last** làm loại hàm
   - Điều này kích hoạt cảnh báo dựa trên giá trị cuối cùng nhận được
3. Đặt **Input**: Query A
4. Đặt **Mode**: Strict

#### Cấu Hình Ngưỡng

1. Định nghĩa điều kiện cảnh báo: **IS BELOW** `1`
   - Khi giá trị metric `up` giảm xuống dưới 1, cảnh báo được kích hoạt
   - Điều này cho biết microservice đã dừng

## Tổ Chức Cảnh Báo

### Cấu Trúc Thư Mục

1. Tạo thư mục: `accounts`
   - Tổ chức tất cả các cảnh báo liên quan đến accounts

### Nhóm Cảnh Báo

1. Tạo nhóm: `accounts`
2. Đặt **Evaluation Interval**: `10s`
   - Tần suất Grafana đánh giá cảnh báo
   - Giá trị tối thiểu là 10 giây

3. Đặt **Evaluation Period**: `30s`
   - Thời gian chờ trước khi gửi thông báo
   - Ngăn chặn cảnh báo giả

## Chi Tiết Cảnh Báo

### Tóm Tắt và Mô Tả

1. **Summary**: `Account service is down`
2. **Description**: Cung cấp thông tin hành động (ví dụ: `please do something`)

### Lưu Quy Tắc

1. Nhấp **Save rule and exit**
2. Cảnh báo sẽ xuất hiện ở trạng thái **Normal** khi dịch vụ đang chạy

## Cấu Hình Kênh Thông Báo

### Điểm Liên Hệ

Grafana hỗ trợ nhiều kênh thông báo:

- Email
- Webhook
- Slack
- Microsoft Teams
- Telegram
- Discord
- Cisco Webex Teams
- PagerDuty
- Và nhiều hơn nữa

### Thiết Lập Thông Báo Webhook

#### Bước 1: Tạo URL Webhook

1. Truy cập [webhook.site](https://webhook.site) hoặc sử dụng [hookdeck.com](https://hookdeck.com)
2. Nhấp nút **Test Webhook**
3. Sao chép URL webhook được tạo

#### Bước 2: Cấu Hình Contact Point

1. Điều hướng đến **Contact Points**
2. Nhấp **Add Contact Point**
3. **Name**: `EasyBankWebhook`
4. **Integration**: Chọn `Webhook`
5. **URL**: Dán URL webhook
6. Nhấp **Test** để gửi thông báo kiểm tra
7. Nhấp **Save**

### Cấu Hình Chính Sách Thông Báo

1. Vào **Notification Policies**
2. Nhấp **Settings** → **Edit**
3. Đặt **Default Contact Point**: `EasyBankWebhook`

#### Tùy Chọn Thời Gian

Cấu hình thời gian cảnh báo để ngăn spam thông báo:

- **Group Wait**: `10s` (để kiểm tra; mặc định là 30s)
- **Group Interval**: `10s` (để kiểm tra; mặc định là 5 phút)
- **Repeat Interval**: `10s` (để kiểm tra; mặc định là 4 giờ)
  - Thời gian chờ trước khi gửi lại cảnh báo

4. Nhấp **Update Default Policy**

## Kiểm Tra Cảnh Báo

### Kích Hoạt Cảnh Báo

1. Mở Docker Desktop
2. Dừng accounts microservice
3. Quan sát các thay đổi trạng thái cảnh báo:
   - **Normal** → **Pending** (đang chờ giai đoạn đánh giá)
   - **Pending** → **Firing** (cảnh báo được kích hoạt)

### Xác Minh Thông Báo

1. Kiểm tra URL webhook
2. Bạn sẽ nhận được thông báo với:
   - Status: `Firing`
   - Summary: `Account service is down`
   - Description: `please do something`

### Giải Quyết Cảnh Báo

1. Khởi động lại accounts microservice trong Docker Desktop
2. Chờ dịch vụ khởi động hoàn toàn
3. Trạng thái cảnh báo thay đổi: **Firing** → **Normal**
4. Webhook nhận được thông báo trạng thái **Resolved**

## Các Trạng Thái Cảnh Báo

| Trạng Thái | Mô Tả |
|------------|-------|
| **Normal** | Dịch vụ đang chạy bình thường, không phát hiện vấn đề |
| **Pending** | Điều kiện cảnh báo được đáp ứng, đang chờ giai đoạn đánh giá |
| **Firing** | Cảnh báo đang hoạt động và thông báo đang được gửi |
| **Resolved** | Cảnh báo trước đó đã firing đã trở lại bình thường |

## Các Phương Pháp Hay Nhất

1. **Evaluation Intervals**: Đặt khoảng thời gian phù hợp dựa trên nhu cầu giám sát
   - Quá thường xuyên = tăng tải cho Grafana
   - Quá hiếm = phát hiện cảnh báo chậm

2. **Evaluation Periods**: Sử dụng giai đoạn đánh giá để tránh cảnh báo giả
   - Các vấn đề tạm thời sẽ không kích hoạt cảnh báo ngay lập tức

3. **Repeat Intervals**: Cấu hình khoảng lặp lại hợp lý
   - Ngăn chặn mệt mỏi thông báo
   - Môi trường production: khuyến nghị 1-4 giờ

4. **Contact Points**: Sử dụng nhiều kênh thông báo
   - Email cho cảnh báo không khẩn cấp
   - Slack/Teams để nhóm nhận thức
   - PagerDuty cho cảnh báo quan trọng

5. **Tổ Chức Cảnh Báo**: Sử dụng thư mục và nhóm
   - Dễ dàng quản lý nhiều cảnh báo
   - Phân tách logic theo dịch vụ hoặc nhóm

## Khắc Phục Sự Cố

### Cảnh Báo Không Kích Hoạt

- Xác minh nguồn dữ liệu Prometheus được cấu hình đúng
- Kiểm tra tên metric và labels khớp với dịch vụ của bạn
- Đảm bảo evaluation interval và period phù hợp

### Không Nhận Được Thông Báo

- Kiểm tra contact point bằng nút **Test**
- Xác minh URL webhook đúng và có thể truy cập
- Kiểm tra notification policy đang sử dụng contact point đúng

### Cảnh Báo Giả

- Tăng giai đoạn đánh giá
- Điều chỉnh giá trị ngưỡng
- Sử dụng các hàm reduce khác (ví dụ: Average thay vì Last)

## Các Bước Tiếp Theo

- Khám phá cấu hình cảnh báo dựa trên dashboard
- Cấu hình nhiều quy tắc cảnh báo cho các dịch vụ khác nhau
- Thiết lập nhóm và định tuyến cảnh báo
- Triển khai tắt tiếng cảnh báo cho cửa sổ bảo trì

## Kết Luận

Hệ thống cảnh báo của Grafana cung cấp khả năng giám sát mạnh mẽ cho microservices. Bằng cách cấu hình ngưỡng, khoảng đánh giá và kênh thông báo phù hợp, bạn có thể đảm bảo nhận thức kịp thời về các vấn đề dịch vụ và duy trì tính khả dụng cao.