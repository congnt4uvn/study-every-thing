# AWS Elastic Beanstalk Extensions

## Tổng quan

Elastic Beanstalk Extensions (EB Extensions) cho phép bạn cấu hình và tùy chỉnh môi trường Elastic Beanstalk của mình bằng code thay vì sử dụng giao diện console. Tất cả các tham số có thể được thiết lập trong UI đều có thể được cấu hình theo cách lập trình bằng các file cấu hình.

## Các khái niệm chính

### EB Extensions là gì?

Khi bạn tạo một gói triển khai (file zip) cho Elastic Beanstalk, bạn có thể bao gồm các file EB extension cùng với code ứng dụng của mình. Các file này cho phép bạn:

- Cấu hình các thiết lập môi trường theo cách lập trình
- Chỉnh sửa các cấu hình mặc định
- Thêm các tài nguyên AWS bổ sung vào môi trường của bạn

## Yêu cầu cấu hình

### Cấu trúc thư mục

Tất cả các file cấu hình EB extension phải được đặt trong một thư mục cụ thể:

```
.ebextensions/
```

Thư mục này phải được đặt ở **thư mục gốc của source code** của bạn.

### Định dạng file

Các file EB extension phải tuân theo các yêu cầu sau:

1. **Định dạng**: YAML hoặc JSON
2. **Phần mở rộng file**: Phải kết thúc bằng `.config`
3. **Ví dụ**: `logging.config`, `environment-variables.config`

Mặc dù phần mở rộng file là `.config`, nội dung phải ở định dạng YAML hoặc JSON.

## Khả năng cấu hình

### Option Settings

Bạn có thể chỉnh sửa các thiết lập mặc định bằng cách sử dụng tài liệu `option_settings`. Điều này cho phép bạn cấu hình các khía cạnh khác nhau của môi trường Elastic Beanstalk.

### Thêm tài nguyên AWS

EB extensions cho phép bạn thêm các tài nguyên AWS bổ sung như:

- Amazon RDS (Relational Database Service)
- ElastiCache
- DynamoDB
- Các dịch vụ AWS khác không thể cấu hình trực tiếp qua console Elastic Beanstalk

### Lưu ý quan trọng về vòng đời tài nguyên

⚠️ **Cảnh báo**: Bất kỳ tài nguyên nào được quản lý bởi EB extensions sẽ **bị xóa khi môi trường bị xóa**.

Ví dụ, nếu bạn tạo một instance ElastiCache như một phần của môi trường Elastic Beanstalk của mình bằng EB extensions, nó sẽ tự động bị xóa khi bạn xóa môi trường Elastic Beanstalk.

## Ví dụ thực hành: Thiết lập biến môi trường

### Cấu trúc dự án

```
nodejs-v3-ebextensions/
└── .ebextensions/
    └── environment-variables.config
```

### Ví dụ file cấu hình

**File**: `.ebextensions/environment-variables.config`

```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    DB_URL: "your-database-url-here"
    DB_USER: "username"
```

### File cấu hình này làm gì

File EB extension này:

1. Thiết lập các biến môi trường cho ứng dụng
2. Định nghĩa `DB_URL` cho kết nối database
3. Định nghĩa `DB_USER` cho xác thực database

Các biến môi trường này sẽ được sử dụng để kết nối với một database bên ngoài, chẳng hạn như một instance PostgreSQL RDS.

## Quy trình triển khai

### Các bước triển khai với EB Extensions

1. **Tạo thư mục `.ebextensions`** trong thư mục gốc dự án của bạn
2. **Thêm các file cấu hình** với phần mở rộng `.config`
3. **Nén ứng dụng của bạn** bao gồm cả thư mục `.ebextensions`
4. **Upload và triển khai** thông qua console Elastic Beanstalk hoặc CLI

### Xác minh

Sau khi triển khai, bạn có thể xác minh rằng các EB extensions đã được áp dụng:

1. Điều hướng đến môi trường của bạn trong console Elastic Beanstalk
2. Vào phần **Configuration**
3. Cuộn xuống **Environment properties**
4. Kiểm tra xem các giá trị được cấu hình của bạn (ví dụ: `DB_URL`, `DB_USER`) có hiện diện không

Các giá trị này sẽ được thiết lập tự động từ các file cấu hình, không phải thủ công qua console.

## Lợi ích của EB Extensions

- **Infrastructure as Code**: Quản lý cấu hình môi trường thông qua các file được kiểm soát phiên bản
- **Khả năng lặp lại**: Dễ dàng tái tạo các môi trường với cùng cấu hình
- **Tự động hóa**: Giảm các bước cấu hình thủ công
- **Tính nhất quán**: Đảm bảo tất cả các môi trường có cùng cấu hình cơ bản

## Những điểm chính cần nhớ

1. EB extensions phải nằm trong thư mục `.ebextensions/` ở thư mục gốc dự án
2. Các file phải ở định dạng YAML hoặc JSON với phần mở rộng `.config`
3. Bạn có thể cấu hình option settings và thêm tài nguyên AWS
4. Các tài nguyên được quản lý bởi EB extensions sẽ bị xóa cùng với môi trường
5. Các biến môi trường có thể được thiết lập theo cách lập trình bằng EB extensions

## Mẹo cho kỳ thi

- Hiểu yêu cầu về cấu trúc thư mục (`.ebextensions/`)
- Nhớ yêu cầu về phần mở rộng file (`.config`)
- Biết rằng các tài nguyên EB extension sẽ bị xóa cùng với môi trường
- Quen thuộc với mẫu cấu hình `option_settings`

---

*Lưu ý: Tài liệu này bao gồm các khái niệm cơ bản về Elastic Beanstalk Extensions cần thiết cho các kỳ thi chứng chỉ AWS.*