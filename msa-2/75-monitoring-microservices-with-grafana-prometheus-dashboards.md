# Giám Sát Microservices với Grafana và Prometheus Dashboards

## Tổng Quan

Hướng dẫn này trình bày khả năng mạnh mẽ của Grafana và Prometheus khi làm việc cùng nhau để giám sát các microservices Java Spring Boot. Chúng ta sẽ khám phá cách thiết lập các dashboard có sẵn và tạo các giải pháp giám sát tùy chỉnh cho kiến trúc microservices của bạn.

## Dashboard Có Sẵn Từ Grafana

### Tìm Kiếm Dashboard Template

1. Truy cập [tài liệu Prometheus](https://prometheus.io) → Get Started → tab Visualization
2. Vào phần Grafana cung cấp thông tin về:
   - Cài đặt Grafana
   - Tạo nguồn dữ liệu Prometheus
   - Xây dựng biểu đồ Prometheus với Grafana

3. Truy cập [kho dashboard Grafana](https://grafana.com/grafana/dashboards/) nơi đội ngũ Grafana và cộng đồng mã nguồn mở đã xây dựng nhiều dashboard được cấu hình sẵn

### Các Tùy Chọn Dashboard Có Sẵn

Thư viện dashboard Grafana bao gồm trực quan hóa cho:
- Dữ liệu Jira
- MongoDB
- Kubernetes
- Datadog
- JVM ecosystem
- Và nhiều thành phần khác

## Thiết Lập Dashboard JVM

### Bước 1: Tìm Kiếm Dashboard JVM

1. Tìm kiếm "JVM" trong kho dashboard Grafana
2. Tìm các dashboard có lượng tải xuống cao (ví dụ: 5+ triệu lượt tải)
3. Chọn một dashboard JVM Micrometer phổ biến

### Bước 2: Import Dashboard

1. Đăng nhập vào Grafana instance của bạn:
   - Thông tin đăng nhập mặc định: `admin` / `admin`
   - Bỏ qua thông báo đổi mật khẩu (tùy chọn)

2. Điều hướng đến Menu → New → Import
3. Dán URL dashboard từ kho Grafana
4. Click "Load"
5. Chọn nguồn dữ liệu Prometheus từ dropdown
6. Click "Import"

### Bước 3: Xem Các Chỉ Số Dashboard

Sau khi import, dashboard hiển thị các chỉ số toàn diện bao gồm:

- **Uptime**: Thông tin thời gian hoạt động của service
- **Start Time**: Khi nào service được khởi động
- **Sử Dụng Bộ Nhớ**:
  - Sử dụng Heap
  - Sử dụng Non-heap
- **Chỉ Số Hiệu Suất**:
  - Thời lượng
  - Tỷ lệ sử dụng
  - Tỷ lệ lỗi
- **Chi Tiết JVM**:
  - JVM heap
  - JVM non-heap
  - Thông tin Thread
- **Chỉ Số Hệ Thống**:
  - Sử dụng CPU
  - Sự kiện Log
  - Áp lực Garbage collector
- **Memory Spaces**:
  - Eden Space
  - Survivor Space
  - Tenured Gen

### Giám Sát Nhiều Microservices

- Chuyển đổi giữa các microservices bằng cách chọn các instance khác nhau từ dropdown
- Ví dụ: Xem chỉ số cho microservice `accounts:8080` hoặc `cards`
- Tất cả trực quan hóa dashboard tự động cập nhật dựa trên service đã chọn

## Thiết Lập Dashboard Spring Boot System Monitor

### Bước 1: Tìm Dashboard Spring Boot

1. Điều hướng đến dashboards Grafana
2. Tìm kiếm "Spring Boot"
3. Chọn "Spring Boot 2.1 System Monitor" (492K+ lượt tải)
4. Copy URL dashboard

### Bước 2: Import và Cấu Hình

1. Trong Grafana, vào New → Import
2. Dán URL dashboard
3. Click "Load"
4. Chọn nguồn dữ liệu Prometheus
5. Click "Import"

### Bước 3: Tùy Chỉnh Khoảng Thời Gian

- Chế độ xem mặc định hiển thị dữ liệu giờ gần nhất
- Điều chỉnh theo khoảng thời gian ưa thích (ví dụ: 15 phút gần nhất)
- Chọn các microservices khác nhau để xem chỉ số cụ thể của chúng

## Tạo Dashboard Tùy Chỉnh

### Tại Sao Tạo Dashboard Tùy Chỉnh?

Đôi khi các dashboard có sẵn không đáp ứng các yêu cầu cụ thể. Dashboard tùy chỉnh cho phép bạn:
- Giám sát các chỉ số cụ thể liên quan đến ứng dụng của bạn
- Tổ chức thông tin theo nhu cầu của nhóm
- Tập trung vào các chỉ số hiệu suất chính

### Hướng Dẫn Từng Bước Tạo Dashboard Tùy Chỉnh

#### 1. Tạo Dashboard Mới

1. Điều hướng đến Dashboards → New → New Dashboard
2. Lưu dashboard với tên mô tả (ví dụ: "easybank")
3. Lưu vào thư mục phù hợp (ví dụ: "General")

#### 2. Thêm Row cho Microservice

1. Click "Add" → Chọn "Row"
2. Cấu hình cài đặt row
3. Đặt tiêu đề: "Accounts Microservice"
4. Click "Update"

#### 3. Thêm Trực Quan Hóa Uptime

1. Click "Add" → "Add Visualization"
2. Cấu hình panel:
   - **Tên panel**: "Uptime"
   - **Nguồn dữ liệu**: Prometheus
   - **Metric**: `process_uptime_seconds`
   - **Label**: application
   - **Value**: accounts microservice

3. Chọn loại trực quan hóa:
   - Time series (mặc định)
   - Bar charts
   - Statistics
   - Gauge
   - Bar gauge
   - Pie chart

4. Click "Apply"
5. Kéo panel xuống dưới row "Accounts Microservice"

#### 4. Thêm Trực Quan Hóa Trạng Thái Service

1. Click "Add Visualization"
2. Cấu hình panel:
   - **Nguồn dữ liệu**: Prometheus
   - **Metric**: `up`
   - **Label filter**: job
   - **Value**: accounts
   - **Tiêu đề panel**: "Up"

3. Chọn kiểu "Gauge" cho biểu đồ
4. Click "Apply"
5. Định vị panel phù hợp (ví dụ: kéo sang phía bên phải)

#### 5. Thêm Nhiều Panel Hơn

Tiếp tục thêm các row và panel cần thiết để giám sát:
- Sử dụng bộ nhớ
- Tỷ lệ request
- Tỷ lệ lỗi
- Kết nối database
- Chỉ số ứng dụng tùy chỉnh

### Tổ Chức Panels

- Kéo và thả các panel để sắp xếp chúng một cách logic
- Nhóm các chỉ số liên quan dưới cùng một row
- Thu gọn/mở rộng các row để quản lý độ phức tạp của dashboard

## Quản Lý Dashboard

### Lưu Dashboard

- Click nút "Save" thường xuyên để bảo toàn các thay đổi
- Cung cấp tên mô tả để dễ dàng nhận dạng
- Tổ chức các dashboard trong thư mục

### Truy Cập Dashboard

1. Điều hướng đến menu Dashboards
2. Xem tất cả các dashboard có sẵn
3. Chọn bất kỳ dashboard nào để xem chỉ số thời gian thực

## Lợi Ích của Grafana và Prometheus

### Cho Đội Ngũ Phát Triển

- **Giám Sát Thời Gian Thực**: Khả năng hiển thị tức thì về tình trạng microservice
- **Phân Tích Lịch Sử**: Xem xét hiệu suất trong quá khứ và xác định xu hướng
- **Khắc Phục Sự Cố Nhanh Chóng**: Nhanh chóng xác định vấn đề khi chúng xảy ra

### Cho Đội Ngũ Vận Hành

- **Khả Năng Hiển Thị Toàn Diện**: Giám sát toàn bộ hệ sinh thái microservices
- **Template Có Sẵn**: Tận dụng dashboard cộng đồng để bắt đầu nhanh chóng
- **Tùy Chỉnh**: Tạo dashboard chuyên biệt cho nhu cầu cụ thể

## Thực Hành Tốt Nhất

1. **Bắt Đầu với Dashboard Có Sẵn**: Sử dụng template cộng đồng làm nền tảng
2. **Tùy Chỉnh Dần Dần**: Thêm panel tùy chỉnh khi nhu cầu cụ thể phát sinh
3. **Tổ Chức Hợp Lý**: Nhóm các chỉ số liên quan lại với nhau
4. **Đặt Khoảng Thời Gian Phù Hợp**: Cân bằng chi tiết với hiệu suất
5. **Giám Sát Chỉ Số Chính**: Tập trung vào các chỉ số quan trọng nhất đối với ứng dụng của bạn

## Kết Luận

Grafana và Prometheus cung cấp khả năng giám sát mạnh mẽ cho các microservices Spring Boot. Bằng cách tận dụng các dashboard có sẵn và tạo trực quan hóa tùy chỉnh, đội ngũ phát triển và vận hành có thể duy trì khả năng hiển thị toàn diện vào hệ thống phân tán của họ.

### Điểm Chính Cần Nhớ

- Dashboard có sẵn cung cấp thiết lập nhanh cho nhu cầu giám sát phổ biến
- Dashboard tùy chỉnh cung cấp tính linh hoạt cho yêu cầu cụ thể
- Nhà phát triển nên hiểu các kiến thức cơ bản về giám sát
- Đội ngũ platform/vận hành nên tìm hiểu sâu hơn về khả năng của Grafana

### Học Tập Nâng Cao

Đối với nhà phát triển, những kiến thức cơ bản được đề cập ở đây là đủ cho công việc hàng ngày. Tuy nhiên, nếu bạn quan tâm đến việc trở thành chuyên gia Grafana (đặc biệt cho vai trò platform hoặc vận hành), hãy cân nhắc đăng ký một khóa học Grafana toàn diện bao gồm các chủ đề nâng cao chi tiết.

## Bước Tiếp Theo

Với các dashboard đã được cấu hình, các thành viên trong nhóm có thể nhanh chóng đánh giá tình trạng tổng thể của microservices bất cứ lúc nào. Nền tảng giám sát này cho phép phát hiện vấn đề chủ động và giải quyết sự cố nhanh hơn.