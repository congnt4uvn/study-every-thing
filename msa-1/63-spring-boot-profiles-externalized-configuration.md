# Spring Boot Profiles và Cấu Hình Bên Ngoài (Externalized Configuration)

## Tổng Quan

Hướng dẫn này trình bày cách kích hoạt Spring Boot profiles sử dụng các phương pháp cấu hình bên ngoài. Những kỹ thuật này cho phép bạn triển khai cùng một Docker image trên nhiều môi trường khác nhau mà không cần build lại, giúp microservices của bạn trở nên bất biến (immutable).

## Các Phương Pháp Cấu Hình Bên Ngoài

Spring Boot hỗ trợ ba phương pháp chính cho cấu hình bên ngoài (theo thứ tự ưu tiên):

1. **Command Line Arguments - Tham số dòng lệnh** (Ưu tiên cao nhất)
2. **JVM System Variables - Biến hệ thống JVM**
3. **Environment Variables - Biến môi trường**

## Demo: Kích Hoạt Profiles Sử Dụng IDE

### Yêu Cầu Tiên Quyết

- Ứng dụng Spring Boot với class chính `AccountsApplication`
- IDE (IntelliJ IDEA hoặc tương tự)
- File `application.yml` với nhiều profiles (QA, Prod)

## Phương Pháp 1: Command Line Arguments (Tham Số Dòng Lệnh)

### Các Bước:

1. Nhấp chuột phải vào class `AccountsApplication`
2. Chọn **Modify Run Configuration**
3. Trong trường **Program Arguments**, thêm:
   ```
   --spring.profiles.active=prod --build.version=1.1
   ```

### Cú Pháp:
- Sử dụng tiền tố **double hyphens** (`--`)
- Định dạng: `--property.name=value`

### Ví Dụ:
```
--spring.profiles.active=prod --build.version=1.1
```

### Kiểm Tra:

- **Contact Info API**: Trả về dữ liệu từ prod profile (production APIs, thông tin product owner)
- **Build Info API**: Trả về `1.1` (giá trị được ghi đè, không phải `1.0` mặc định từ prod profile)

## Phương Pháp 2: JVM System Variables (Biến Hệ Thống JVM)

### Các Bước:

1. Nhấp chuột phải vào `AccountsApplication`
2. Chọn **Modify Run Configuration**
3. Xóa command line arguments
4. Click **Modify Options** → **Add VM Options**
5. Trong trường **VM Options**, thêm:
   ```
   -Dspring.profiles.active=prod -Dbuild.version=1.3
   ```

### Cú Pháp:
- Sử dụng tiền tố `-D` cho mỗi property
- Định dạng: `-Dproperty.name=value`

### Ví Dụ:
```
-Dspring.profiles.active=prod -Dbuild.version=1.3
```

### Kiểm Tra:

- **Contact Info API**: Trả về dữ liệu từ prod profile
- **Build Info API**: Trả về `1.3`

## Phương Pháp 3: Environment Variables (Biến Môi Trường)

### Các Bước:

1. Nhấp chuột phải vào `AccountsApplication`
2. Chọn **Modify Run Configuration**
3. Xóa VM arguments
4. Trong trường **Environment Variables**, thêm:
   ```
   SPRING_PROFILES_ACTIVE=prod;BUILD_VERSION=1.8
   ```

### Quy Tắc Cú Pháp:
- **Không cần tiền tố**
- **Chỉ sử dụng chữ IN HOA**
- Thay dấu chấm (`.`) bằng dấu gạch dưới (`_`)
- Phân cách nhiều biến bằng dấu chấm phẩy (`;`)

### Ví Dụ:
```
SPRING_PROFILES_ACTIVE=prod;BUILD_VERSION=1.8
```

### Kiểm Tra:

- **Contact Info API**: Trả về dữ liệu từ prod profile
- **Build Info API**: Trả về `1.8`

## Kiểm Tra Thứ Tự Ưu Tiên Cấu Hình

### Kịch Bản: Cấu Hình Cả Ba Phương Pháp

Cấu hình cả ba phương pháp với các giá trị khác nhau:

```
Command Line Args:     --build.version=1.3
VM Options:           -Dbuild.version=1.1
Environment Variables: BUILD_VERSION=1.8
```

### Kết Quả:

1. **Với cả ba phương pháp được cấu hình**: Kết quả là `1.3` (Command line arguments thắng)
2. **Không có command line args**: Kết quả là `1.1` (JVM system variables thắng)
3. **Không có command line args và VM options**: Kết quả là `1.8` (Environment variables thắng)
4. **Không có cấu hình bên ngoài nào**: Kết quả là `1.0` (Mặc định từ prod profile)

## Thứ Tự Ưu Tiên (Từ Cao Đến Thấp)

1. ✅ **Command Line Arguments** (`--property=value`)
2. ✅ **JVM System Variables** (`-Dproperty=value`)
3. ✅ **Environment Variables** (`PROPERTY=value`)
4. ✅ **Profile-Specific Properties** (application-{profile}.yml)
5. ✅ **Default Properties** (application.yml)

## Lợi Ích

- **Microservices Bất Biến**: Triển khai cùng một Docker image trên nhiều môi trường
- **Không Cần Build Lại**: Thay đổi cấu hình mà không cần build lại Docker images
- **Cấu Hình Theo Môi Trường**: Dễ dàng chuyển đổi giữa dev, QA và prod
- **Linh Hoạt Ghi Đè**: Ghi đè bất kỳ property nào tại runtime

## Hạn Chế

Mặc dù phương pháp này hoạt động cho các trường hợp cơ bản, nhưng nó có một số nhược điểm:

- Không phù hợp cho kiến trúc microservices phức tạp
- Khả năng mở rộng hạn chế khi quản lý nhiều microservices
- Thay đổi cấu hình yêu cầu khởi động lại ứng dụng
- Không có quản lý cấu hình tập trung
- Khó theo dõi các thay đổi cấu hình

## Bước Tiếp Theo

Áp dụng cấu hình tương tự cho:
- **Loans Microservice**
- **Cards Microservice**

Trong các bài giảng tiếp theo, chúng ta sẽ khám phá các phương pháp quản lý cấu hình nâng cao hơn để giải quyết những hạn chế này.

## Những Điểm Chính Cần Nhớ

✅ Spring Boot profiles cho phép cấu hình theo môi trường cụ thể  
✅ Cấu hình bên ngoài cho phép ghi đè properties tại runtime  
✅ Command line arguments có độ ưu tiên cao nhất  
✅ Phương pháp này hoạt động cho các trường hợp cơ bản nhưng có hạn chế  
✅ Cần các giải pháp quản lý cấu hình nâng cao cho môi trường production  

## Chủ Đề Liên Quan

- Spring Boot Profiles
- Triển Khai Docker Image
- Quản Lý Cấu Hình trong Microservices
- Cấu Hình CI/CD Pipeline