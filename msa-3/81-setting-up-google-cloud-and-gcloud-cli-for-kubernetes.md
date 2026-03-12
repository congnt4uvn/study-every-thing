# Thiết Lập Google Cloud và gcloud CLI để Triển Khai Kubernetes

## Tổng Quan

Hướng dẫn này sẽ giúp bạn thiết lập tài khoản Google Cloud với credit miễn phí và cấu hình Google Cloud CLI (gcloud) trên hệ thống local. Đây là bước quan trọng để triển khai microservices lên Kubernetes cluster trong Google Cloud.

## Yêu Cầu Trước Khi Bắt Đầu

- Tài khoản Gmail (tốt nhất là tài khoản mới để nhận $300 credit miễn phí)
- Thẻ tín dụng để xác minh (không tự động tính phí sau khi hết trial)
- Hiểu biết cơ bản về cloud computing

## Tại Sao Chọn Google Cloud?

Google Cloud được chọn cho việc triển khai microservices vì:
- **$300 Credit Miễn Phí**: Người dùng mới nhận $300 credit có hiệu lực trong 90 ngày
- **Google Kubernetes Engine (GKE)**: Được hỗ trợ trong free tier
- **Không Tự Động Tính Phí**: Không tự động billing sau khi hết free trial
- **Free Tier Tốt Hơn**: So với AWS và Azure cho việc thử nghiệm Kubernetes

## Bước 1: Tạo Tài Khoản Google Cloud

### 1.1 Truy Cập Google Cloud Console

1. Truy cập [cloud.google.com](https://cloud.google.com)
2. Đăng nhập bằng tài khoản Gmail của bạn
3. Nếu bạn là người dùng mới, bạn sẽ thấy ưu đãi $300 credit miễn phí

**Quan Trọng**: Nếu bạn đã từng sử dụng Gmail với Google Cloud trước đây, hãy tạo tài khoản Gmail mới để đủ điều kiện nhận credit miễn phí.

### 1.2 Kích Hoạt Free Trial

1. Click vào banner "$300 free credit"
2. Xem lại các sản phẩm free tier, bao gồm **Google Kubernetes Engine**
3. Click nút "Console" để truy cập Google Cloud Console
4. Click "Try for free" để bắt đầu quá trình kích hoạt

### 1.3 Hoàn Tất Đăng Ký

1. Chọn quốc gia và loại hình kinh doanh (ví dụ: "Business idea/Startup")
2. Chọn checkbox Terms of Service (Điều khoản dịch vụ)
3. Click "Continue"
4. Nhập thông tin thẻ tín dụng để xác minh

**Cảnh Báo**: 
- Các nhà cung cấp cloud yêu cầu xác minh thẻ tín dụng
- Hãy cẩn thận khi tạo các tài nguyên không cần thiết
- Luôn xóa các tài nguyên sau khi khám phá để bảo toàn credit miễn phí
- Nếu không thoải mái cung cấp thông tin thẻ tín dụng, bạn có thể theo dõi mà không cần tạo tài nguyên

### 1.4 Xác Minh Thiết Lập Tài Khoản

1. Đợi thông báo "Setting up your billing" và "Setting up your free trial"
2. Bạn sẽ được chuyển hướng đến trang chủ Google Cloud Console (hoặc truy cập [console.cloud.google.com](https://console.cloud.google.com))
3. Google Cloud tự động tạo một project mặc định có tên "My First Project"

## Bước 2: Cài Đặt Google Cloud SDK

### 2.1 Tại Sao Cần Cài Google Cloud SDK?

Google Cloud SDK cho phép bạn:
- Kết nối với Kubernetes clusters trong Google Cloud từ hệ thống local
- Thực thi commands trực tiếp từ terminal local
- Cài đặt và quản lý Helm charts từ local
- Giao tiếp với các sản phẩm Google Cloud mà không cần dùng web console

### 2.2 Tải Và Cài Đặt

1. Truy cập [cloud.google.com/sdk](https://cloud.google.com/sdk)
2. Click "Get started"
3. Xác minh các yêu cầu:
   - ✅ Đã tạo Google Cloud project (My First Project)
   - ✅ Đã bật billing (đã thêm thẻ tín dụng)
4. Làm theo các bước cài đặt dựa trên hệ điều hành của bạn:
   - **Windows**: Tải installer và chạy
   - **macOS**: Dùng installer hoặc Homebrew
   - **Linux**: Dùng package manager hoặc cài thủ công

### 2.3 Xác Minh Cài Đặt

Mở terminal và chạy:

```bash
gcloud --version
```

Bạn sẽ thấy output hiển thị phiên bản Google Cloud SDK đã cài đặt và các components.

## Bước 3: Cấu Hình Google Cloud CLI

### 3.1 Khởi Tạo gcloud

Chạy lệnh khởi tạo:

```bash
gcloud init
```

### 3.2 Các Bước Cấu Hình

1. **Chọn tùy chọn cấu hình**: Chọn option 3 để khởi tạo lại cấu hình "default" hiện có
2. **Đợi kết nối mạng**: CLI sẽ thiết lập kết nối với Google Cloud
3. **Prompt đăng nhập**: Khi được hỏi "Do you want to log in", gõ `Y` (Yes) và nhấn Enter
4. **Xác thực qua trình duyệt**: 
   - Trình duyệt sẽ tự động mở
   - Chọn tài khoản Gmail bạn đã dùng để tạo Google Cloud account
   - Cấp quyền bằng cách click "Allow"
5. **Xác nhận thành công**: Bạn sẽ thấy "You are now authenticated with the Google Cloud CLI"

### 3.3 Chọn Project

1. CLI sẽ hiển thị các Google Cloud projects có sẵn
2. Chọn project của bạn bằng cách nhập số tương ứng (ví dụ: `1` cho "liquid-muse-397814")
3. Nhấn Enter để xác nhận

### 3.4 Xác Minh Cấu Hình

Bạn sẽ thấy output xác nhận:
- ✅ "Your Google Cloud SDK is configured and ready to use"
- Email account của bạn
- Tên và ID của project đã kết nối

## Các Bước Tiếp Theo

Với tài khoản Google Cloud và CLI đã được cấu hình, bạn đã sẵn sàng để:
1. Tạo Kubernetes cluster trong Google Cloud
2. Triển khai microservices lên cluster
3. Quản lý tài nguyên bằng kubectl và Helm

## Những Điều Quan Trọng Cần Nhớ

### Quản Lý Chi Phí
- Theo dõi việc sử dụng $300 credit trong Google Cloud Console
- Xóa tài nguyên khi không sử dụng để bảo toàn credit
- Thiết lập cảnh báo billing để theo dõi chi tiêu

### Best Practices (Thực Hành Tốt Nhất)
- Sử dụng các sản phẩm free tier bất cứ khi nào có thể
- Khám phá các tính năng Google Kubernetes Engine trong 90 ngày trial
- Cập nhật gcloud CLI thường xuyên để có features và bảo mật mới nhất

### Các Lệnh Hữu Ích

```bash
# Kiểm tra phiên bản gcloud
gcloud --version

# Xem cấu hình hiện tại
gcloud config list

# Chuyển đổi giữa các projects
gcloud config set project PROJECT_ID

# Liệt kê các projects có sẵn
gcloud projects list

# Xem trợ giúp cho bất kỳ lệnh nào
gcloud help
```

## Khắc Phục Sự Cố

### Lệnh gcloud không tìm thấy
- Đảm bảo cài đặt hoàn tất thành công
- Thêm gcloud vào system PATH
- Khởi động lại terminal

### Vấn đề xác thực
- Chạy `gcloud auth login` để xác thực lại
- Kiểm tra kết nối internet
- Xác minh quyền của tài khoản Gmail

### Project không hiển thị
- Đảm bảo bạn đã tạo project trong Google Cloud Console
- Chạy `gcloud projects list` để xem tất cả projects có sẵn
- Xác minh billing đã được bật cho project

## Tóm Tắt

Bạn đã thành công:
- ✅ Tạo tài khoản Google Cloud với $300 credit miễn phí
- ✅ Thiết lập billing không tự động tính phí sau trial
- ✅ Cài đặt Google Cloud CLI trên hệ thống local
- ✅ Xác thực và cấu hình gcloud với tài khoản Google
- ✅ Kết nối với Google Cloud project của bạn

Bây giờ bạn đã sẵn sàng để tạo và quản lý Kubernetes cluster cho việc triển khai các Spring Boot microservices!

---

**Các Chủ Đề Liên Quan**:
- Tạo Kubernetes cluster trong Google Cloud
- Triển khai microservices với Helm charts
- Cấu hình kubectl cho GKE clusters
- Quản lý tài nguyên Google Cloud hiệu quả