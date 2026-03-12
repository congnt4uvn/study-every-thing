# Đọc Thuộc Tính Môi Trường với Environment Interface

## Tổng Quan

Bài giảng này trình bày cách thức thứ hai để đọc các thuộc tính trong microservices Spring Boot sử dụng interface `Environment`. Phương pháp này đặc biệt hữu ích cho việc truy cập các biến môi trường được định nghĩa trong môi trường triển khai.

## Tại Sao Sử Dụng Biến Môi Trường?

### Vấn Đề Bảo Mật

- **Thông Tin Nhạy Cảm**: Mật khẩu và dữ liệu nhạy cảm khác không nên được lưu trong file `application.yaml`
- **Bảo Mật Cấu Hình**: Biến môi trường ngăn chặn việc lộ thông tin nhạy cảm
- **Kiểm Soát Truy Cập**: Chỉ quản trị viên máy chủ mới có quyền truy cập vào biến môi trường production
- **Thực Hành Tốt Nhất**: Luôn định nghĩa các chi tiết cấu hình nhạy cảm dưới dạng biến môi trường

## Các Bước Triển Khai

### 1. Autowire Environment Interface

Thêm interface Environment vào controller của bạn:

```java
import org.springframework.core.env.Environment;
import org.springframework.beans.factory.annotation.Autowired;

@Autowired
private Environment environment;
```

**Quan Trọng**: Đảm bảo bạn import đúng Environment interface:
- ✅ Đúng: `org.springframework.core.env.Environment` (Spring Core Framework)
- ❌ Sai: Environment interface của Hibernate

### 2. Tạo REST API để Đọc Thuộc Tính Môi Trường

Ví dụ: Đọc Phiên Bản Java từ JAVA_HOME

```java
@GetMapping("/java-version")
@Operation(
    summary = "Lấy Phiên Bản Java",
    description = "Lấy thông tin phiên bản Java được cài đặt trong accounts microservice"
)
public ResponseEntity<String> getJavaVersion() {
    String javaHome = environment.getProperty("JAVA_HOME");
    return ResponseEntity.ok(javaHome);
}
```

### 3. Kiểm Tra API

**Endpoint**: `/api/java-version`  
**Phương Thức**: `GET`  
**Phản Hồi**: Trả về giá trị của biến môi trường JAVA_HOME

Ví dụ phản hồi:
```
C:\Users\YourUser\.sdkman\candidates\java\current
```

## Ví Dụ Bổ Sung

### Đọc Đường Dẫn Cài Đặt Maven

```java
String mavenHome = environment.getProperty("MAVEN_HOME");
```

**Ví Dụ Phản Hồi**: 
```
C:\apache-maven-3.8.6
```

Điều này cho thấy rõ ràng phiên bản Maven (3.8.6) được cài đặt trên hệ thống.

## Quy Trình Kiểm Tra

1. **Build Ứng Dụng**: Biên dịch dự án sau khi thực hiện thay đổi
2. **Khởi Động Lại Ứng Dụng**: Khởi động lại ở chế độ debug để kiểm tra
3. **Kiểm Tra với Postman**: Gửi yêu cầu GET đến `/api/java-version`
4. **Xác Minh Phản Hồi**: Kiểm tra rằng giá trị biến môi trường được trả về

## Ưu Điểm

- ✅ Truy cập vào các biến môi trường hệ thống
- ✅ Xử lý an toàn thông tin nhạy cảm
- ✅ Triển khai đơn giản với phương thức `getProperty()`

## Nhược Điểm

- ❌ Chỉ có thể đọc một thuộc tính tại một thời điểm
- ❌ Yêu cầu hardcode tên khóa thuộc tính trong mã Java
- ❌ Không được khuyến nghị cho việc đọc nhiều thuộc tính
- ❌ Không mở rộng tốt cho các ứng dụng có nhiều biến môi trường

## Khi Nào Sử Dụng Phương Pháp Này

**Phù Hợp Cho**:
- Đọc 1-2 thuộc tính môi trường
- Truy cập nhanh các biến cấp hệ thống
- Nhu cầu cấu hình đơn giản

**Không Khuyến Nghị Cho**:
- Ứng dụng có nhiều thuộc tính môi trường
- Quản lý cấu hình phức tạp
- Đọc thuộc tính quy mô lớn (sử dụng các phương pháp nâng cao thay thế)

## Điểm Chính Cần Nhớ

1. Interface `Environment` cung cấp truy cập trực tiếp vào các biến môi trường hệ thống
2. Luôn sử dụng Environment interface của Spring Core Framework, không phải của Hibernate
3. Phương pháp này lý tưởng cho việc đọc thuộc tính quy mô nhỏ
4. Đối với nhu cầu phức tạp hơn, hãy xem xét các phương pháp cấu hình nâng cao
5. Biến môi trường tăng cường bảo mật bằng cách giữ dữ liệu nhạy cảm ra khỏi file cấu hình

## Các Bước Tiếp Theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá **Phương Pháp Thứ Ba** để đọc thuộc tính, giải quyết một số hạn chế của phương pháp này và cung cấp các giải pháp mở rộng hơn cho quản lý cấu hình.

---

**Lưu Ý**: Trong môi trường production, các bản cài đặt Java thường hiển thị đường dẫn thư mục đầy đủ bao gồm tên phiên bản, giúp dễ dàng xác định phiên bản Java chính xác đang được sử dụng.