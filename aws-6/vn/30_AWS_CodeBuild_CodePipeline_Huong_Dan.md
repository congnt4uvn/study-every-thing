# Hướng Dẫn Học AWS CodeBuild và CodePipeline

## Tổng Quan
Hướng dẫn này bao gồm việc tích hợp AWS CodeBuild với GitHub và các kiến thức cơ bản về CI/CD pipeline sử dụng các dịch vụ AWS.

## Các Khái Niệm Chính

### 1. AWS CodeBuild
- **Mục đích**: Dịch vụ build được quản lý hoàn toàn, biên dịch mã nguồn, chạy tests, và tạo ra các gói phần mềm
- **Tính năng chính**: Dịch vụ tích hợp liên tục (CI) tự động mở rộng quy mô

### 2. File buildspec.yaml
File `buildspec.yaml` là file cấu hình cho CodeBuild biết cách chạy một build.

#### Cấu trúc của buildspec.yaml
```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      nodejs: latest
    commands:
      - echo "installing something"
  
  pre_build:
    commands:
      - echo "we are in the pre_build phase"
  
  build:
    commands:
      - echo "we are in the build block"
      - echo "we will run some test"
      - grep -Fq "Congratulations" index.html
  
  post_build:
    commands:
      - echo "we are in the post_build phase"
```

### 3. Các Giai Đoạn Build

#### Trình tự các giai đoạn:
1. **Submitted** - Công việc build được gửi
2. **Queued** - Build đang chờ trong hàng đợi
3. **Provisioning** - Thiết lập môi trường build
4. **Download_source** - Tải mã nguồn từ repository
5. **Install** - Cài đặt dependencies và runtimes
6. **Pre_build** - Các lệnh trước khi build (ví dụ: đăng nhập vào registries)
7. **Build** - Các lệnh build chính và tests
8. **Post_build** - Các lệnh sau build (ví dụ: đóng gói)
9. **Upload_artifacts** - Upload kết quả build
10. **Finalizing** - Các thao tác dọn dẹp
11. **Completed** - Build hoàn tất

### 4. Tích Hợp GitHub

#### Cấu hình Webhook
- CodeBuild có thể được tự động kích hoạt khi code được push lên GitHub
- GitHub Hook gửi thông báo đến CodeBuild khi có sự kiện push
- Các build tự động bắt đầu khi commits được thực hiện vào repository

#### Thiết lập:
1. Tạo file `buildspec.yaml` trong thư mục gốc của GitHub repository
2. Cấu hình CodeBuild project để kết nối với GitHub
3. Thiết lập webhook để tự động kích hoạt
4. Commit thay đổi trực tiếp vào nhánh main

### 5. Testing trong Giai Đoạn Build

#### Ví dụ Lệnh Test:
```bash
grep -Fq "Congratulations" index.html
```

**Giải thích**:
- `grep`: Tìm kiếm patterns trong files
- `-F`: Tìm kiếm chuỗi cố định (không phải regex)
- `-q`: Chế độ im lặng (chỉ trả về exit status)
- Trả về thành công nếu tìm thấy "Congratulations" trong index.html
- Build thất bại nếu không tìm thấy văn bản

### 6. Giám Sát và Logs

#### Tích hợp CloudWatch
- Tất cả logs của build tự động được gửi đến CloudWatch Logs
- Bạn có thể xem logs theo hai cách:
  1. **CodeBuild Console**: Trình xem log inline
  2. **CloudWatch Console**: Console log đầy đủ với khả năng tìm kiếm

#### Xem Logs:
- Click vào build ID để xem chi tiết build
- Điều hướng đến "Phase details" để xem trạng thái của từng giai đoạn
- Click "View entire Log" để mở CloudWatch console

### 7. Tích Hợp CodePipeline
- CodePipeline điều phối toàn bộ quy trình CI/CD
- Có thể bao gồm nhiều stages: Source → Build → Test → Deploy
- CodeBuild thường được sử dụng như stage Build

## Thực Hành Tốt Nhất

1. **Echo Statements**: Sử dụng lệnh echo để theo dõi tiến trình qua các giai đoạn build
2. **Runtime Versions**: Chỉ định rõ ràng phiên bản runtime hoặc sử dụng "latest"
3. **Testing**: Bao gồm automated tests trong giai đoạn build
4. **Error Handling**: Giám sát phase details để xác định lỗi
5. **Log Analysis**: Sử dụng CloudWatch để debug chi tiết

## Quy Trình Làm Việc Thông Thường

1. Developer push code lên GitHub
2. GitHub webhook kích hoạt CodeBuild
3. CodeBuild tải source từ GitHub
4. Cài đặt các runtime cần thiết (ví dụ: Node.js 20)
5. Thực thi các lệnh trong từng giai đoạn
6. Chạy tests để xác thực build
7. Tạo artifacts
8. Upload lên vị trí được chỉ định
9. Báo cáo trạng thái build

## Xử Lý Sự Cố

### Build Thất Bại
- Kiểm tra phase details để xác định giai đoạn nào thất bại
- Xem lại CloudWatch logs để tìm thông báo lỗi
- Xác minh cú pháp buildspec.yaml
- Đảm bảo các lệnh test đúng

### Vấn Đề Download Source
- Xác minh quyền truy cập GitHub repository
- Kiểm tra cấu hình webhook
- Xác nhận tên nhánh đúng

## Những Điểm Cần Nhớ

- `buildspec.yaml` là thiết yếu cho cấu hình CodeBuild
- Quy trình build có nhiều giai đoạn riêng biệt
- Tích hợp GitHub cho phép CI/CD tự động
- CloudWatch cung cấp logging toàn diện
- Testing nên được tích hợp vào giai đoạn build
- CodePipeline điều phối toàn bộ workflow

## Các Bước Tiếp Theo

- Tìm hiểu về các stages của CodePipeline
- Khám phá quản lý artifacts
- Nghiên cứu các chiến lược deployment
- Thực hành tạo custom buildspec files
- Triển khai các chiến lược automated testing
