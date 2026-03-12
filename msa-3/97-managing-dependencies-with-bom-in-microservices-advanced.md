# Quản Lý Dependencies với BOM trong Microservices - Khái Niệm Nâng Cao

## Tổng Quan

Hướng dẫn này trình bày các kỹ thuật nâng cao để quản lý dependencies trong microservices sử dụng Bill of Materials (BOM), bao gồm ghi đè phiên bản, quản lý dependencies chung, và tạo Docker image với cấu hình BOM.

## Ghi Đè Phiên Bản trong Từng Microservice

Mặc dù BOM cho phép kiểm soát phiên bản tập trung từ `pom.xml` cha, các microservice riêng lẻ vẫn có thể linh hoạt sử dụng các phiên bản khác nhau khi cần thiết.

### Cách Ghi Đè Phiên Bản

Thay vì tham chiếu phiên bản từ BOM cha, bạn có thể định nghĩa phiên bản riêng trong microservice:

**Ví dụ: Ghi Đè Phiên Bản Lombok trong Loans Microservice**

Xóa tham chiếu thuộc tính và chỉ định phiên bản của bạn:

```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.8.32</version>
</dependency>
```

Ngay cả khi BOM cha định nghĩa phiên bản `1.8.34`, loans microservice có thể sử dụng `1.8.32`.

### Lưu Ý Quan Trọng

- Cách tiếp cận này hoạt động với bất kỳ dependency nào (Spring Boot dependencies hoặc thư viện bên thứ ba)
- Bạn có toàn quyền tự do ghi đè phiên bản khi cần thiết
- Sử dụng khả năng này một cách thận trọng để duy trì tính nhất quán giữa các microservices

## Quản Lý Dependencies Chung với BOM

### Vấn Đề

Trong kiến trúc microservices, nhiều service thường sử dụng cùng các thư viện. Ví dụ, tất cả microservices thường bao gồm:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
</dependency>
```

Việc lặp lại dependency này trong `pom.xml` của mỗi microservice tạo ra gánh nặng bảo trì.

### Giải Pháp: Tập Trung Dependencies Chung

Định nghĩa dependencies chung một lần trong BOM cha, và tất cả microservices con sẽ tự động kế thừa chúng.

### Các Bước Triển Khai

#### Bước 1: Xóa Dependency khỏi Tất Cả Microservices

Xóa dependency `spring-boot-starter-test` khỏi:
- Gateway
- Message microservice
- Cards microservice
- Config Server
- Eureka Server
- Accounts microservice

Sau khi xóa, reload Maven changes cho mỗi microservice.

#### Bước 2: Hiểu về Dependency Management vs Dependencies

**Sự Khác Biệt Quan Trọng:**

- `<dependencyManagement>`: Chỉ sử dụng cho quản lý phiên bản
- `<dependencies>`: Dependencies thực tế được kế thừa bởi các project con

Nếu bạn chỉ định nghĩa dependencies dưới `<dependencyManagement>`, các microservices con sẽ không tự động import chúng.

#### Bước 3: Thêm Dependency Chung vào BOM Cha

Trong `pom.xml` của project `eazy-bom`, thêm dependency dưới phần `<dependencies>` (không phải `<dependencyManagement>`):

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
    </dependency>
</dependencies>
```

#### Bước 4: Reload và Xác Minh

1. Lưu các thay đổi trong BOM `pom.xml`
2. Reload Maven changes cho project `eazy-bom`
3. Tất cả microservices con sẽ tự động fetch dependency chung
4. Build project để xác minh các lỗi compilation đã được giải quyết

### Lợi Ích

- **Giảm Trùng Lặp**: Định nghĩa dependencies chung một lần
- **Bảo Trì Dễ Dàng Hơn**: Cập nhật phiên bản ở một vị trí duy nhất
- **Tính Nhất Quán**: Đảm bảo tất cả microservices sử dụng cùng phiên bản
- **Code Sạch Hơn**: POM của các microservice riêng lẻ tập trung vào các dependencies độc đáo

## Tạo Docker Image với BOM

### Xác Minh Cấu Hình BOM với Docker

Sau khi triển khai BOM, quan trọng là phải xác minh rằng việc tạo Docker image không bị ảnh hưởng.

### Kiểm Tra Tạo Docker Image

#### Bước 1: Tạo Docker Image

Điều hướng đến thư mục microservice (ví dụ: Config Server):

```bash
cd config-server
mvn compile jib:dockerBuild
```

Docker image sẽ được tạo thành công mà không có bất kỳ vấn đề nào.

#### Bước 2: Xác Minh Image trong Docker Desktop

Kiểm tra Docker Desktop cho image mới tạo:
- Tên image: `config-server`
- Tag: `S20`
- Kích thước: ~354 MB (không ảnh hưởng đến kích thước image)

#### Bước 3: Kiểm Tra Khởi Động Container

Chạy container để đảm bảo nó khởi động đúng cách:

```bash
docker run -p 8071:8071 config-server:S20
```

**Kết Quả Mong Đợi:**
- Ứng dụng Spring Boot khởi động không có vấn đề
- Ứng dụng sử dụng phiên bản Spring Boot được chỉ định trong BOM cha (ví dụ: 3.3.2)
- Container xuất hiện trong Docker Desktop với logs đầy đủ

### Điểm Xác Minh

✅ Docker image được tạo thành công  
✅ Kích thước image vẫn tối ưu  
✅ Container khởi động không có lỗi  
✅ Ứng dụng sử dụng phiên bản từ BOM  
✅ Tất cả chức năng hoạt động như mong đợi  

## Thực Hành Tốt Nhất

1. **Áp Dụng BOM trong Production**: Luôn triển khai Bill of Materials trong các dự án microservices doanh nghiệp
2. **Giảm Thiểu Thay Đổi Thủ Công**: BOM giảm quản lý phiên bản thủ công giữa các services
3. **Sử Dụng Ghi Đè Phiên Bản Một Cách Tiết Kiệm**: Chỉ ghi đè phiên bản khi thực sự cần thiết
4. **Tập Trung Dependencies Chung**: Định nghĩa các dependencies được chia sẻ trong BOM cha
5. **Kiểm Tra Tích Hợp Docker**: Xác minh việc tạo Docker image sau khi triển khai BOM
6. **Ghi Chép Quyết Định Phiên Bản**: Theo dõi bất kỳ ghi đè phiên bản nào và lý do của chúng

## Tóm Tắt

Mô hình Bill of Materials (BOM) cung cấp:

- **Kiểm Soát Phiên Bản Tập Trung**: Quản lý tất cả phiên bản dependency từ một parent POM duy nhất
- **Linh Hoạt**: Các microservice riêng lẻ có thể ghi đè phiên bản khi cần
- **Quản Lý Dependency Chung**: Định nghĩa dependencies được chia sẻ một lần
- **Giảm Bảo Trì**: Loại bỏ các khai báo dependency lặp lại
- **Tương Thích Docker**: Hoạt động liền mạch với quy trình containerization
- **Sẵn Sàng Doanh Nghiệp**: Cách tiếp cận đã được chứng minh cho kiến trúc microservices quy mô lớn

Bằng cách triển khai BOM đúng cách, bạn tạo ra một hệ sinh thái microservices dễ bảo trì, nhất quán và có khả năng mở rộng hơn.

## Kết Luận

Cấu hình BOM nâng cao phát triển microservices bằng cách cung cấp chiến lược quản lý dependency mạnh mẽ. Nó loại bỏ các điều chỉnh thủ công, đảm bảo tính nhất quán về phiên bản, và đơn giản hóa việc bảo trì trên tất cả các services trong kiến trúc của bạn.

---

**Chủ Đề Liên Quan:**
- Tạo BOM Project cho Microservices
- Thực Hành Tốt Nhất cho Quản Lý Dependency Microservices
- Tối Ưu Hóa Docker Image trong Spring Boot