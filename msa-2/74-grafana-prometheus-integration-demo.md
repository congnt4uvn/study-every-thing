# Demo Tích Hợp Grafana và Prometheus

## Tổng Quan

Hướng dẫn này trình bày cách tích hợp giữa Grafana và Prometheus để giám sát các microservices. Grafana cung cấp khả năng trực quan hóa mạnh mẽ cho các số liệu được thu thập bởi Prometheus, giúp việc giám sát và phân tích kiến trúc microservices của bạn trở nên dễ dàng hơn.

## Yêu Cầu Trước Khi Bắt Đầu

- Grafana đang chạy trên cổng 3000
- Prometheus đã được cấu hình và đang chạy
- Các microservices đã được cấu hình với các endpoint metrics của Prometheus

## Truy Cập Grafana

1. Mở trình duyệt và truy cập Grafana tại cổng 3000
2. Bạn sẽ thấy trang chủ của Grafana

## Quản Lý Kết Nối Nguồn Dữ Liệu

### Xem Các Kết Nối Hiện Có

1. Nhấp vào biểu tượng **menu** trong Grafana
2. Điều hướng đến **Connections** (Kết nối)
3. Trong phần Connections, bạn có thể:
   - Tạo kết nối mới
   - Xem các kết nối hiện có trong **Data Sources** (Nguồn Dữ Liệu)

### Các Nguồn Dữ Liệu Đã Cấu Hình

Hiện tại, đã có hai kết nối được cấu hình:
- **Loki** - Để tổng hợp và tìm kiếm log
- **Prometheus** - Để thu thập và trực quan hóa metrics

## Cấu Hình Prometheus

### Chi Tiết Kết Nối

Kết nối Prometheus được cấu hình bằng cách sử dụng file `datasource.yml` nằm trong thư mục `observability/grafana`. Các thông tin cấu hình chính:

- **URL**: `prometheus:9090`
- Kết nối giữa Prometheus và Grafana được thiết lập sử dụng các cài đặt này

### Xem Cấu Hình Prometheus

1. Nhấp vào tab **Prometheus** trong phần Data Sources
2. Xem lại tất cả chi tiết cấu hình từ file `datasource.yml`

## Khám Phá Metrics với Prometheus

### Truy Cập Trang Explore

1. Điều hướng đến trang **Home** (Trang chủ)
2. Nhấp vào nút **Explore** (Khám phá)

### Truy Vấn System CPU Usage

#### Tạo Truy Vấn Cơ Bản

1. Chọn **Prometheus** làm nguồn dữ liệu
2. Trong phần **Metric**, chọn `system_cpu_usage`
3. Chọn **Label** là `application`
4. Tùy chọn, lọc theo microservice cụ thể hoặc để trống để xem tất cả các services
5. Nhấp **Run Query** (Chạy Truy Vấn)

#### Xem Kết Quả

- Biểu đồ sẽ hiển thị dữ liệu cho một giờ gần nhất theo mặc định
- Mỗi màu đại diện cho một microservice khác nhau:
  - Accounts service
  - Cards service
  - Config Server
  - Eureka Server
  - Loans service
  - Gateway Server

#### Tùy Chỉnh Khoảng Thời Gian

- Thay đổi khoảng thời gian (ví dụ: 15 phút) để cập nhật biểu đồ tương ứng
- Biểu đồ sẽ tự động làm mới với khoảng thời gian mới

### Tùy Chọn Trực Quan Hóa

Grafana cung cấp nhiều kiểu trực quan hóa:

- **Lines** - Biểu đồ đường
- **Bars** - Biểu đồ cột
- **Points** - Hiển thị điểm dữ liệu
- **Stack Lines** - Biểu đồ đường xếp chồng
- **Stacked Bars** - Biểu đồ cột xếp chồng

Chọn kiểu phù hợp nhất với nhu cầu giám sát của bạn.

## Truy Vấn Nâng Cao

### Thêm Nhiều Metrics

1. Nhấp vào nút **Add Query** để tạo các truy vấn bổ sung
2. Ví dụ: Thêm metric `up`
   - Chọn metric: `up`
   - Chọn label: `job`
   - Chạy truy vấn

### Xem Các Metrics Kết Hợp

Khi có nhiều truy vấn đang hoạt động:
- Biểu đồ hiển thị thông tin kết hợp từ tất cả các metrics
- Các metrics khác nhau được hiển thị rõ ràng trong chế độ xem dạng đường
- Đường ở trên cùng có thể chỉ ra một metric (ví dụ: `up`)
- Các biểu đồ phía dưới hiển thị các metrics khác (ví dụ: `system_cpu_usage`)

### Các Phương Pháp Tốt Nhất

- Mặc dù bạn có thể thêm nhiều metrics, nhưng nên **tìm kiếm một metric tại một thời điểm** để rõ ràng hơn
- Cách tiếp cận này giúp phân tích trở nên đơn giản và dễ hiểu hơn

## Những Điểm Chính Cần Nhớ

- **Grafana** cung cấp khả năng trực quan hóa vượt trội so với giao diện tích hợp của Prometheus
- **Prometheus** thu thập và lưu trữ dữ liệu metrics
- **Tích hợp** giữa hai công cụ tạo ra một giải pháp giám sát mạnh mẽ
- File `datasource.yml` quản lý cấu hình kết nối
- Nhiều microservices có thể được giám sát đồng thời
- Các tùy chọn truy vấn và trực quan hóa linh hoạt cho phép giám sát toàn diện

## Các Bước Tiếp Theo

Demo này bao gồm các kiến thức cơ bản về tích hợp Grafana và Prometheus. Còn rất nhiều điều để khám phá với cả hai công cụ, bao gồm:

- Tạo dashboard tùy chỉnh
- Thiết lập cảnh báo
- Kỹ thuật truy vấn nâng cao
- Chia sẻ và cộng tác dashboard

Tiếp tục khám phá các công cụ mạnh mẽ này để xây dựng giải pháp giám sát toàn diện cho kiến trúc microservices của bạn.

---

**Lưu ý**: Hướng dẫn này là một phần của loạt bài về giám sát microservices sử dụng các ứng dụng Java Spring Boot.