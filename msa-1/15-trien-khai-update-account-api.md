# Triển Khai Update Account API

## Tổng Quan

Trong bài học này, chúng ta sẽ xây dựng REST API cho phép ứng dụng khách cập nhật thông tin tài khoản trong Accounts Microservice. API này bổ sung cho các API tạo và lấy thông tin tài khoản đã có.

## Yêu Cầu

### Các Trường Có Thể Cập Nhật
- Tên khách hàng
- Địa chỉ email
- Số điện thoại
- Loại tài khoản
- Địa chỉ chi nhánh

### Quy Tắc Nghiệp Vụ: Số Tài Khoản Không Thể Thay Đổi
**Quan trọng**: Sau khi số tài khoản được tạo, nó **không thể được cập nhật** bởi người dùng cuối. Số tài khoản đóng vai trò là định danh chính và phải luôn không đổi.

## Các Bước Triển Khai

### 1. Tầng Service - Interface IAccountService

Đầu tiên, tạo một phương thức trừu tượng trong interface `IAccountService`:

```java
boolean updateAccount(CustomerDto customerDto);
```

**Chi Tiết Phương Thức:**
- **Kiểu Trả Về**: `boolean` - cho biết thao tác cập nhật có thành công hay không
- **Tham Số**: `CustomerDto` - chứa dữ liệu đã cập nhật từ ứng dụng khách

### 2. Triển Khai Service - Class AccountService

Override phương thức `updateAccount` trong class `AccountService`:

#### Logic Triển Khai

1. **Khởi Tạo Cờ Kết Quả**
   ```java
   boolean isUpdated = false;
   ```

2. **Trích Xuất Thông Tin Tài Khoản**
   - Lấy `AccountsDto` từ `CustomerDto`
   - Trích xuất số tài khoản từ DTO

3. **Lấy Tài Khoản Hiện Có**
   - Sử dụng số tài khoản làm tiêu chí tìm kiếm (vì nó là primary key)
   - Dùng phương thức `findById()` từ Spring Data JPA
   - Annotation `@Id` đánh dấu số tài khoản là primary key
   - Nếu không tìm thấy bản ghi, ném ra `ResourceNotFoundException`

4. **Cập Nhật Dữ Liệu Tài Khoản**
   - Ánh xạ dữ liệu từ DTO sang Accounts entity bằng `mapper()`
   - Gọi phương thức `save()` trên `AccountsRepository`
   - Tài khoản đã cập nhật được trả về và lưu trữ

5. **Lấy và Cập Nhật Khách Hàng**
   - Trích xuất `customerId` từ đối tượng Accounts đã cập nhật
   - Sử dụng `findById()` với `CustomerRepository`
   - Nếu không có bản ghi khách hàng, ném ra `ResourceNotFoundException`
   - Ánh xạ dữ liệu cập nhật từ DTO sang Customer entity
   - Gọi phương thức `save()` trên `CustomerRepository`

6. **Trả Về Trạng Thái Thành Công**
   - Đặt `isUpdated = true`
   - Trả về giá trị boolean cho tầng controller

#### Hiểu Về Phương Thức save() Của Spring Data JPA

Phương thức `save()` rất thông minh:
- **Nếu không có giá trị primary key**: Thực hiện thao tác **INSERT**
- **Nếu có giá trị primary key**: Thực hiện thao tác **UPDATE**

### 3. Tầng Controller - AccountsController

Tạo một phương thức mới để xử lý các yêu cầu cập nhật:

```java
@PutMapping("/update")
public ResponseEntity<ResponseDto> updateAccountDetails(@RequestBody CustomerDto customerDto) {
    boolean isUpdated = iAccountService.updateAccount(customerDto);
    
    if (isUpdated) {
        return ResponseEntity
            .status(HttpStatus.OK)
            .body(new ResponseDto(StatusCode.STATUS_200, "Yêu cầu đã được xử lý thành công"));
    } else {
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ResponseDto(StatusCode.STATUS_500, 
                "Đã xảy ra lỗi. Vui lòng thử lại hoặc liên hệ đội phát triển"));
    }
}
```

**Chi Tiết Endpoint:**
- **Phương Thức HTTP**: PUT
- **Đường Dẫn**: `/api/update`
- **Request Body**: `CustomerDto` với thông tin đã cập nhật
- **Phản Hồi Thành Công**: 200 OK - "Yêu cầu đã được xử lý thành công"
- **Phản Hồi Lỗi**: 500 Internal Server Error

## Kiểm Thử

### Test Case Tích Cực

1. **Tạo tài khoản** bằng create API
2. **Lấy tài khoản** bằng get API với số điện thoại
3. **Cập nhật tài khoản** bằng cách sửa đổi dữ liệu phản hồi:
   - Thay đổi tên (ví dụ: "Madan Reddy" → "Madan Mohan")
   - Thay đổi email (ví dụ: "tutor@eazybytes.com" → "madan@eazybytes.com")
   - Thay đổi số điện thoại
   - Thay đổi loại tài khoản (ví dụ: "Savings" → "Current")
   - Thay đổi địa chỉ chi nhánh
4. **Gửi yêu cầu PUT** đến `/api/update`
5. **Xác minh**: Lấy lại tài khoản với số điện thoại mới
6. **Kết quả**: Tất cả các trường đã cập nhật phải phản ánh giá trị mới

### Test Case Tiêu Cực

1. **Cung cấp một số tài khoản không tồn tại** trong yêu cầu
2. **Gửi yêu cầu PUT**
3. **Kết Quả Mong Đợi**: Phản hồi lỗi với thông báo "Không tìm thấy tài khoản với số tài khoản: [giá trị]"

## Vấn Đề Đã Biết: Các Trường Auditing

### Lỗi Hiện Tại
Khi cập nhật bản ghi, các trường `updatedAt` và `updatedBy` **không được tự động cập nhật**. Điều này là do chúng ta không điền thủ công các giá trị này khi lưu bản ghi vào cơ sở dữ liệu.

### Giải Pháp (Sắp Tới)
Lỗi này sẽ được khắc phục trong các bài học sắp tới bằng cách triển khai **các thay đổi liên quan đến auditing**. Spring Data JPA framework sẽ tự động xử lý:
- `createdAt`
- `createdBy`
- `updatedAt`
- `updatedBy`

Hiện tại, chúng ta có thể chấp nhận lỗi nhỏ này tạm thời.

## Những Điểm Chính Cần Nhớ

1. **Tính Bất Biến Của Số Tài Khoản**: Số tài khoản không thể thay đổi sau khi được tạo, đảm bảo tính toàn vẹn dữ liệu
2. **Sử Dụng Primary Key**: Việc dùng `findById()` tận dụng primary key để truy vấn cơ sở dữ liệu hiệu quả
3. **Phương Thức save() Thông Minh**: Tự động xác định thực hiện insert hay update dựa trên sự hiện diện của primary key
4. **Xử Lý Lỗi Đúng Cách**: Ném `ResourceNotFoundException` cho các bản ghi bị thiếu
5. **Kiến Trúc Phân Lớp**: Tách biệt các mối quan tâm giữa tầng service và controller

## Tiếp Theo Là Gì?

Trong bài học tiếp theo, chúng ta sẽ triển khai **Delete Account API** để hoàn thành các thao tác CRUD cho Accounts Microservice.

---

**Lưu ý**: Các ví dụ code đầy đủ có thể tìm thấy trong kho lưu trữ GitHub được đề cập trong bài học.