# Triển Khai Delete Account API

## Tổng Quan
Trong phần này, chúng ta sẽ tạo một REST API trong accounts microservice để xóa thông tin khách hàng và tài khoản hiện có dựa trên số điện thoại di động.

## Thiết Kế API
API xóa sẽ:
- Nhận số điện thoại di động làm tham số đầu vào
- Tải thông tin customer entity từ cơ sở dữ liệu bằng số điện thoại
- Trích xuất customerId từ customer entity
- Xóa các bản ghi từ cả hai bảng accounts và customer sử dụng customerId

## Các Bước Triển Khai

### 1. Tạo Phương Thức Trong Service Interface
Đầu tiên, tạo một phương thức mới trong interface `IAccountService`:

```java
boolean deleteAccount(String mobileNumber);
```

Phương thức này:
- Trả về giá trị boolean cho biết thao tác xóa có thành công hay không
- Nhận số điện thoại di động làm tham số đầu vào

### 2. Triển Khai Phương Thức Service
Trong class `AccountService`, triển khai phương thức `deleteAccount()`:

```java
@Override
public boolean deleteAccount(String mobileNumber) {
    Customer customer = customerRepository.findByMobileNumber(mobileNumber)
        .orElseThrow(() -> new ResourceNotFoundException("Customer", "mobileNumber", mobileNumber));
    
    accountsRepository.deleteByCustomerId(customer.getCustomerId());
    customerRepository.deleteById(customer.getCustomerId());
    
    return true;
}
```

**Chi Tiết Triển Khai:**
1. Lấy thông tin customer sử dụng `findByMobileNumber()` từ `CustomerRepository`
2. Nếu không tồn tại bản ghi, throw `ResourceNotFoundException`
3. Lấy customerId từ customer entity
4. Xóa bản ghi account sử dụng `deleteByCustomerId()`
5. Xóa bản ghi customer sử dụng `deleteById()`

### 3. Tạo Phương Thức Delete Tùy Chỉnh Trong Repository
Thêm phương thức delete tùy chỉnh trong `AccountsRepository`:

```java
@Transactional
@Modifying
void deleteByCustomerId(Long customerId);
```

**Các Annotation Quan Trọng:**
- `@Transactional`: Đảm bảo query chạy trong một transaction
- `@Modifying`: Thông báo cho Spring Data JPA rằng phương thức này sẽ thay đổi dữ liệu

**Tại Sao Cần Các Annotation Này:**
- Các phương thức tùy chỉnh update hoặc delete dữ liệu cần các annotation này
- `@Transactional` đảm bảo rằng nếu có lỗi xảy ra khi runtime, mọi thay đổi một phần sẽ được rollback
- Các phương thức framework như `deleteById()` đã có các annotation này tích hợp sẵn
- Các phương thức tùy chỉnh cần annotation rõ ràng để thông báo cho framework về việc sửa đổi dữ liệu

**Tại Sao Không Sử Dụng `deleteById()` Cho Accounts?**
- `deleteById()` yêu cầu primary key (account number trong trường hợp này)
- Để sử dụng `deleteById()`, chúng ta cần thực hiện một query bổ sung để lấy account number
- Sử dụng `deleteByCustomerId()` hiệu quả hơn vì chúng ta đã có customerId

### 4. Tạo Phương Thức Controller
Thêm endpoint delete trong controller class:

```java
@DeleteMapping("/delete")
public ResponseEntity<ResponseDto> deleteAccountDetails(@RequestParam String mobileNumber) {
    boolean isDeleted = iAccountService.deleteAccount(mobileNumber);
    
    if (isDeleted) {
        return ResponseEntity
            .status(HttpStatus.OK)
            .body(new ResponseDto(StatusConstants.STATUS_200, StatusConstants.MESSAGE_200));
    } else {
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ResponseDto(StatusConstants.STATUS_500, StatusConstants.MESSAGE_500));
    }
}
```

**Chi Tiết Controller:**
- Sử dụng annotation `@DeleteMapping` cho phương thức HTTP DELETE
- Đường dẫn API: `/api/delete`
- Nhận số điện thoại di động làm query parameter
- Trả về:
  - Status 200 với thông báo thành công nếu xóa thành công
  - Status 500 với thông báo lỗi nếu xóa thất bại

## Kiểm Thử API

### Kịch Bản 1: Xóa Thành Công
1. Tạo một tài khoản mới với số điện thoại
2. Xác minh tài khoản tồn tại bằng GET API
3. Gọi DELETE API: `/api/delete?mobileNumber={mobileNumber}`
4. Nhận phản hồi thành công (Status 200)
5. Xác minh việc xóa bằng cách gọi GET API - sẽ trả về 404 Not Found

### Kịch Bản 2: Xóa Bản Ghi Không Tồn Tại
1. Gọi DELETE API với số điện thoại không tồn tại
2. Sẽ nhận lỗi 404 Not Found
3. Đây là hành vi mong đợi vì không có dữ liệu để xóa

## Các Khái Niệm Chính

### Phương Thức Delete Tùy Chỉnh Trong Spring Data JPA
- Mẫu tên phương thức: `deleteBy{TênTrường}`
- Spring Data JPA tự động tạo delete query
- Tương tự như `findBy` cho SELECT query, `deleteBy` chỉ định DELETE query

### Quản Lý Transaction
- Tất cả các thao tác xóa nên chạy trong một transaction
- Nếu có lỗi xảy ra, transaction sẽ được rollback
- Ngăn chặn việc xóa dữ liệu một phần (ví dụ: xóa account nhưng không xóa customer)

### Tính Toàn Vẹn Dữ Liệu
- Cả bản ghi customer và account đều được xóa cùng nhau
- Sử dụng customerId đảm bảo tính toàn vẹn tham chiếu
- Transaction đảm bảo thao tác nguyên tử

## Tóm Tắt
Chúng ta đã triển khai thành công thao tác DELETE, hoàn thành tất cả bốn thao tác CRUD:
- **C**reate - Create account API
- **R**ead - Fetch account API
- **U**pdate - Update account API
- **D**elete - Delete account API

## Các Bước Tiếp Theo
Các chủ đề quan trọng sau sẽ được đề cập tiếp theo:
1. Xử lý RuntimeException đúng cách
2. Audit các cột metadata với Spring Data JPA
3. Tài liệu hóa REST APIs

## Lưu Ý
Khi khởi động lại ứng dụng với H2 database, tất cả dữ liệu sẽ bị mất. Đây là tạm thời trong quá trình phát triển. Sau này, khi chuyển sang MySQL database, dữ liệu sẽ được duy trì lâu dài.