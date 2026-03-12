# AWS Elastic Beanstalk Lifecycle Policy - Chính Sách Vòng Đời

## Tổng Quan

AWS Elastic Beanstalk có thể lưu trữ tối đa **1,000 phiên bản ứng dụng** trong tài khoản của bạn. Nếu không quản lý phiên bản đúng cách, bạn có thể mất khả năng triển khai ứng dụng mới. Hướng dẫn này sẽ giới thiệu cách quản lý các phiên bản ứng dụng bằng chính sách vòng đời (lifecycle policy).

## Vấn Đề

- Beanstalk lưu trữ tối đa 1,000 phiên bản ứng dụng mỗi tài khoản
- Nếu các phiên bản cũ không được xóa, việc triển khai mới sẽ thất bại
- Quản lý thủ công các phiên bản trở nên không khả thi ở quy mô lớn

## Giải Pháp: Lifecycle Policy (Chính Sách Vòng Đời)

Chính sách vòng đời của Beanstalk giúp bạn tự động loại bỏ các phiên bản ứng dụng cũ dựa trên các tiêu chí được xác định.

### Các Tùy Chọn Cấu Hình

#### 1. Xóa Theo Thời Gian
- Xóa các phiên bản cũ hơn độ tuổi được chỉ định
- Ví dụ: Chỉ giữ các phiên bản từ 180 ngày gần nhất

#### 2. Xóa Theo Số Lượng
- Xóa các phiên bản khi tổng số vượt quá giới hạn
- Ví dụ: Duy trì tối đa 200 phiên bản ứng dụng

### Các Biện Pháp Bảo Vệ Quan Trọng

- **Phiên bản đang hoạt động được bảo vệ**: Các phiên bản hiện đang được sử dụng bởi môi trường của bạn sẽ KHÔNG bị xóa, bất kể độ tuổi hoặc giới hạn số lượng
- **Bảo toàn source bundle**: Bạn có thể chọn giữ lại các source bundle của ứng dụng trong Amazon S3 để tránh mất dữ liệu, ngay cả khi xóa chúng khỏi giao diện Beanstalk

## Hướng Dẫn Thực Hành

### Xem Các Phiên Bản Ứng Dụng

1. Điều hướng đến **Application Versions** trong ứng dụng của bạn (ví dụ: MyApplication)
2. Tìm các phiên bản đã triển khai (ví dụ: MyApplication-blue)
3. Xem chi tiết bao gồm:
   - Nhãn phiên bản
   - Vị trí nguồn
   - Môi trường triển khai

### Hiểu Về Lưu Trữ S3

1. Các phiên bản ứng dụng được lưu trữ trong bucket S3 do Beanstalk tạo
2. Truy cập bucket qua Amazon S3 console
3. Tìm kiếm các bucket "Beanstalk" trong region của bạn (ví dụ: EU Central-1)
4. Tất cả các phiên bản ứng dụng vẫn được đăng ký trong Beanstalk và lưu trữ trong S3

### Cấu Hình Lifecycle Policy

1. Vào **Settings** trong ứng dụng Beanstalk của bạn
2. Kích hoạt **Application Lifecycle Policy**
3. Chọn chiến lược giới hạn của bạn:

#### Tùy Chọn A: Giới Hạn Theo Số Lượng
- Đặt số lượng phiên bản tối đa (ví dụ: 200)
- Các phiên bản cũ nhất sẽ bị xóa khi vượt quá giới hạn

#### Tùy Chọn B: Giới Hạn Theo Tuổi
- Đặt độ tuổi tối đa theo ngày (ví dụ: 180 ngày)
- Các phiên bản cũ hơn độ tuổi chỉ định sẽ bị xóa

### Tùy Chọn Source Bundle Trên S3

Khi xóa các phiên bản khỏi Beanstalk, bạn có hai lựa chọn:

1. **Giữ lại source bundle trong S3**: Bảo toàn các file để có thể khôi phục
2. **Xóa source bundle khỏi S3**: Xóa hoàn toàn các file để tiết kiệm chi phí lưu trữ

### Quyền Cần Thiết

**AWS Elastic Beanstalk service role** phải có quyền thực hiện các thao tác xóa thay mặt cho bạn.

## Các Phương Pháp Hay Nhất

- Bật lifecycle policy để tránh đạt giới hạn 1,000 phiên bản
- Giữ lại S3 source bundles cho các ứng dụng quan trọng để có thể rollback
- Sử dụng giới hạn theo số lượng để quản lý lưu trữ dễ dự đoán
- Sử dụng giới hạn theo tuổi khi các phiên bản có tính thời gian nhạy cảm
- Theo dõi số lượng phiên bản thường xuyên

## Tóm Tắt

Chính sách vòng đời rất quan trọng để duy trì môi trường Elastic Beanstalk khỏe mạnh bằng cách:
- Tự động quản lý các phiên bản ứng dụng
- Ngăn chặn lỗi triển khai do giới hạn phiên bản
- Cung cấp tính linh hoạt trong chiến lược lưu giữ
- Bảo vệ các triển khai đang hoạt động khỏi bị xóa nhầm
- Cung cấp các tùy chọn quản lý lưu trữ S3

Hiểu và cấu hình đúng chính sách vòng đời đảm bảo triển khai liên tục, mượt mà mà không cần can thiệp thủ công.