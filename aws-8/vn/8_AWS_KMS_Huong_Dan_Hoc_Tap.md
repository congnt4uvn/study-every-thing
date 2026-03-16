# Hướng Dẫn Học Tập AWS KMS (Key Management Service)

## Giới Thiệu về AWS KMS

AWS Key Management Service (KMS) là một dịch vụ được quản lý giúp bạn tạo và quản lý các khóa mã hóa được sử dụng để mã hóa dữ liệu của bạn trên các dịch vụ AWS khác nhau.

---

## Các Loại Khóa KMS

### 1. Khóa Quản Lý Bởi AWS (AWS Managed Keys)
- **Định Nghĩa**: Các khóa được tạo và quản lý bởi AWS cho các dịch vụ AWS cụ thể
- **Chi Phí**: Không tính phí thêm
- **Cách Sử Dụng**: Tự động xuất hiện trong KMS khi bạn sử dụng mã hóa KMS với các dịch vụ AWS
- **Ví Dụ**: Khóa quản lý bởi AWS cho EBS

#### Các Đặc Điểm Chính:
- Dành riêng cho từng dịch vụ (ví dụ: EBS, SQS, RDS)
- Được xác định bằng chính sách khóa giới hạn sử dụng cho dịch vụ cụ thể
- Chỉ đọc (bạn không thể sửa đổi chính sách khóa)

#### Ví Dụ Chính Sách Khóa:
```
{
  "Principal": "Service",
  "Service": "ec2.amazonaws.com",
  "Action": "kms:*",
  "Condition": {
    "StringEquals": {
      "kms:ViaService": "ec2.region.amazonaws.com"
    }
  }
}
```

**Yêu Cầu Điều Kiện**:
- Tài khoản người gọi phải là tài khoản của bạn
- Via Service phải là dịch vụ AWS phù hợp (EC2 cho EBS, SQS cho hàng đợi SQS, v.v.)

---

### 2. Khóa Quản Lý Bởi Khách Hàng (Customer Managed Keys)
- **Định Nghĩa**: Các khóa do bạn tạo và quản lý trong KMS
- **Chi Phí**: $1 mỗi tháng cho mỗi khóa
- **Tính Linh Hoạt**: Kiểm soát hoàn toàn chính sách khóa và cách sử dụng
- **Tốt Nhất Cho**: Các yêu cầu mã hóa tùy chỉnh

#### Khi Nào Sử Dụng:
- Cần kiểm soát nhiều hơn đối với mã hóa
- Muốn hạn chế quyền truy cập khóa cho các người dùng/vai trò cụ thể
- Xây dựng các giải pháp mã hóa tùy chỉnh

---

### 3. Kho Khóa Tùy Chỉnh (Custom Key Store)
- **Định Nghĩa**: Sử dụng AWS CloudHSM để lưu trữ khóa
- **Phạm Vi**: Không nằm trong phạm vi của hướng dẫn này (chủ đề nâng cao)

---

## Tạo Khóa Quản Lý Bởi Khách Hàng

### Bước 1: Chọn Loại Khóa
- **Khóa Đối Xứng (Symmetric Key)**: Một khóa duy nhất cho cả mã hóa và giải mã
  - Phổ biến nhất
  - Hiệu quả hơn
  - Được sử dụng cho mã hóa/giải mã chung

- **Khóa Không Đối Xứng (Asymmetric Key)**: Khóa công khai và khóa bí mật riêng biệt
  - Được sử dụng cho mã hóa/giải mã HOẶC ký/xác minh
  - Nằm ngoài phạm vi của bài giảng này

### Bước 2: Các Tùy Chọn Nâng Cao
- **Nguồn Gốc Khóa (Key Origin)**: Nơi tạo ra vật liệu khóa
  - **KMS**: AWS KMS tạo vật liệu khóa (được khuyến nghị)
  - **Bên Ngoài**: Nhập vật liệu khóa từ các nguồn bên ngoài
  - **Kho Khóa Tùy Chỉnh**: Sử dụng CloudHSM (ngoài phạm vi)

### Bước 3: Cấu Hình Khu Vực
- **Khóa Một Khu Vực (Single Region Key)**: Khóa chỉ tồn tại ở một khu vực (phổ biến nhất)
- **Khóa Nhiều Khu Vực (Multi-Region Key)**: Khóa được sao chép trên các khu vực

### Bước 4: Thêm Bí Danh Khóa
- Tên thân thiện cho khóa (ví dụ: "tutorial")
- Giúp dễ dàng nhận diện khóa

### Bước 5: Xác Định Quản Trị Viên Khóa
- Chỉ định ai có thể quản lý khóa
- Bỏ qua nếu sử dụng chính sách khóa mặc định

### Bước 6: Xác Định Người Dùng Khóa
- Chỉ định ai có thể sử dụng khóa
- **Chính Sách Mặc Định**: Cho phép bất kỳ ai có quyền IAM sử dụng khóa
- **Chính Sách Tùy Chỉnh**: Giới hạn cho các người dùng/vai trò cụ thể

---

## Chính Sách Khóa (Key Policies)

### Chính Sách Khóa Mặc Định
- Cho phép quyền người dùng IAM
- Cho phép bất kỳ tài nguyên nào sử dụng KMS với quyền IAM thích hợp
- Cấu hình phổ biến nhất

### Cấu Trúc Chính Sách Khóa
Chính sách khóa xác định:
- Ai có thể sử dụng khóa
- Những hành động nào họ có thể thực hiện
- Dưới những điều kiện nào

### Các Trường Hợp Sử Dụng

#### Chia Sẻ Snapshots Được Mã Hóa
- Thêm tài khoản AWS khác vào chính sách khóa
- Cho phép truy cập liên tài khoản vào các snapshots EBS được mã hóa

#### Truy Cập Giữa Các Tài Khoản
- Thêm ID tài khoản AWS bên ngoài vào principal
- Xác định quyền cụ thể cho tài khoản đó

---

## Cấu Hình Mã Hóa

### Cấu Hình Khóa Đối Xứng
- **Loại**: Đối Xứng
- **Nguồn Gốc**: KMS
- **Hoạt Động**: Mã Hóa và Giải Mã
- **Đặc Điểm**:
  - Một khóa duy nhất cho cả hai hoạt động
  - Rất hiệu quả
  - An toàn nhất khi khóa được bảo vệ đúng cách

---

## Những Điểm Chính Cần Ghi Nhớ

1. **Khóa Quản Lý Bởi AWS**: Miễn phí, dành riêng cho dịch vụ, do AWS duy trì
2. **Khóa Quản Lý Bởi Khách Hàng**: $1/tháng, kiểm soát hoàn toàn, chính sách tùy chỉnh
3. **Loại Khóa**: Đối Xứng (phổ biến nhất) vs Không Đối Xứng
4. **Chính Sách Khóa**: Xác định quyền truy cập và cách sử dụng
5. **Phạm Vi Khu Vực**: Chọn giữa khóa một khu vực và nhiều khu vực
6. **Thực Hành Tốt Nhất**: Sử dụng khóa quản lý bởi AWS trừ khi bạn cần kiểm soát tùy chỉnh

---

## Bảng So Sánh Tóm Tắt

| Tính Năng | Quản Lý Bởi AWS | Quản Lý Bởi Khách Hàng |
|---------|-----------|------------------|
| Chi Phí | Miễn phí | $1/tháng |
| Kiểm Soát | Hạn Chế | Toàn Bộ |
| Chính Sách | Chỉ Đọc | Có Thể Tùy Chỉnh |
| Trường Hợp Sử Dụng | Dành Riêng Cho Dịch Vụ | Nhu Cầu Tùy Chỉnh |
| Quản Trị | AWS | Bạn |

