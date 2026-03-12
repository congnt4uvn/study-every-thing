# AWS CloudFormation Rollbacks và Xử Lý Lỗi

## Giới Thiệu

Hiểu rõ về rollback trong CloudFormation là rất quan trọng cho kỳ thi chứng chỉ AWS và triển khai thực tế. Hướng dẫn này bao gồm các tình huống rollback khác nhau và cách xử lý lỗi stack một cách hiệu quả.

## Lỗi Khi Tạo Stack

Khi bạn tạo một CloudFormation stack và quá trình tạo thất bại, bạn có hai tùy chọn:

### Tùy Chọn 1: Roll Back Tất Cả Tài Nguyên Stack (Mặc Định)

- **Hành vi**: Mọi thứ được rollback và xóa
- **Ưu điểm**: Trạng thái sạch, không có tài nguyên thừa
- **Hạn chế**: Không thể kiểm tra trực tiếp các tài nguyên bị lỗi
- **Trường hợp sử dụng**: Khi bạn không cần khắc phục sự cố ở mức tài nguyên

Bạn có thể xem log CloudFormation để hiểu điều gì đã xảy ra và tại sao nó thất bại, nhưng bản thân các tài nguyên đã bị xóa.

### Tùy Chọn 2: Giữ Lại Các Tài Nguyên Được Tạo Thành Công

- **Hành vi**: Các tài nguyên được tạo thành công được giữ lại; chỉ các tài nguyên thất bại được rollback
- **Ưu điểm**: Cho phép khắc phục sự cố các tài nguyên đã tạo
- **Hạn chế**: Để lại các tài nguyên phải được dọn dẹp thủ công
- **Trường hợp sử dụng**: Khi bạn cần điều tra cấu hình tài nguyên cụ thể

**Lưu Ý Quan Trọng**: Nếu bạn chọn giữ lại tài nguyên, bạn không thể chỉ đơn giản cập nhật stack để sửa lỗi. Bạn phải xóa toàn bộ stack để dọn dẹp.

## Lỗi Khi Cập Nhật Stack

Khi cập nhật stack thất bại:

- **Hành vi mặc định**: Tự động rollback về trạng thái ổn định cuối cùng
- **Quy trình**: Bất kỳ tài nguyên mới nào được tạo trong quá trình cập nhật sẽ bị xóa
- **Log**: Thông báo lỗi có sẵn trong log CloudFormation
- **Kiểm tra**: Bạn có thể xem log để hiểu vấn đề

## Lỗi Rollback

Trong một số trường hợp, cập nhật stack có thể thất bại và quá trình rollback tiếp theo cũng có thể thất bại. Điều này thường xảy ra khi:

- Tài nguyên đã được thay đổi thủ công bên ngoài CloudFormation
- Các phụ thuộc hoặc quyền đã thay đổi
- Các yếu tố bên ngoài ngăn cản việc xóa hoặc sửa đổi tài nguyên

### Giải Quyết Lỗi Rollback

1. **Xác định vấn đề**: Tìm ra tài nguyên nào đã bị thay đổi thủ công
2. **Sửa thủ công**: Sửa chữa tài nguyên thủ công để CloudFormation có thể quản lý lại
3. **Tiếp tục rollback**: Sử dụng thao tác `ContinueUpdateRollback`

Bạn có thể kích hoạt điều này thông qua:
- AWS Console
- AWS API
- AWS CLI: `aws cloudformation continue-update-rollback`

## Ví Dụ Thực Hành: Kiểm Tra Lỗi Khi Tạo

### Kịch Bản 1: Tạo Stack Với Lỗi Có Chủ Ý

1. **Tạo stack** với file template tên `trigger-failure.yaml`
2. **Vấn đề**: Template chứa AMI ID không hợp lệ cho EC2 instance
3. **Tên Stack**: TriggerCreationFailure
4. **Tùy chọn lỗi stack**: Chọn "Preserve successfully provisioned resources" (Giữ lại tài nguyên được tạo thành công)

**Kết quả**:
- SSH security group: ✓ Tạo thành công
- Server security group: ✗ Thất bại (thiếu group description)
- Kết quả: SSH security group được giữ lại để khắc phục sự cố

### Kịch Bản 2: Tạo Stack Hoạt Động Tốt

1. **Tạo stack** sử dụng template đúng: `just-ec2.yaml`
2. **Tên Stack**: FailureOnUpdate
3. **Kết quả**: Stack được tạo thành công

### Kịch Bản 3: Lỗi Cập Nhật Với Rollback

1. **Cập nhật stack** bằng cách thay thế template bằng `trigger-failure.yaml`
2. **Thêm group description**: "hello"
3. **Tùy chọn lỗi stack**: Roll back tất cả tài nguyên stack

**Kết quả**:
- Security groups được tạo ban đầu
- Tạo EC2 instance thất bại (AMI không hợp lệ)
- Rollback hoàn toàn xảy ra
- SSH và server security groups bị xóa
- Stack trở về trạng thái ổn định trước đó

### Kịch Bản 4: Lỗi Cập Nhật Giữ Lại Tài Nguyên

1. **Cập nhật stack** lần nữa với `trigger-failure.yaml`
2. **Tùy chọn lỗi stack**: Giữ lại tài nguyên được tạo thành công

**Kết quả**:
- SSH và server security groups được tạo
- Cập nhật stack thất bại
- Security groups **KHÔNG** được rollback
- Tài nguyên vẫn còn để khắc phục sự cố

## Thực Hành Tốt Nhất

1. **Chọn tùy chọn phù hợp**: 
   - Sử dụng rollback mặc định cho môi trường production
   - Chỉ sử dụng tùy chọn giữ lại khi cần khắc phục sự cố

2. **Dọn dẹp**: Luôn xóa stack có tài nguyên được giữ lại sau khi khắc phục sự cố

3. **Theo dõi log**: Xem log sự kiện CloudFormation để hiểu nguyên nhân thất bại

4. **Tránh thay đổi thủ công**: Không sửa đổi thủ công các tài nguyên do CloudFormation quản lý để tránh lỗi rollback

5. **Kiểm tra lỗi**: Thực hành các kịch bản lỗi trong môi trường không phải production để hiểu hành vi

## Tóm Tắt

CloudFormation cung cấp các tùy chọn linh hoạt để xử lý lỗi stack:

- **Lỗi khi tạo**: Chọn giữa rollback hoàn toàn hoặc giữ lại tài nguyên
- **Lỗi khi cập nhật**: Tự động rollback về trạng thái ổn định cuối cùng
- **Lỗi rollback**: Sử dụng `ContinueUpdateRollback` sau khi sửa thủ công
- **Tùy chọn lỗi stack**: Có sẵn trong cả quá trình tạo và cập nhật stack

Hiểu rõ các hành vi này giúp bạn đưa ra quyết định sáng suốt khi quản lý infrastructure as code với CloudFormation.

## Dọn Dẹp

Khi bạn hoàn thành việc kiểm tra hoặc khắc phục sự cố, luôn xóa stack để đảm bảo tất cả tài nguyên được dọn dẹp đúng cách.

---

*Ghi nhớ: Cả hai hành vi rollback đều có thể mong muốn tùy thuộc vào trường hợp sử dụng cụ thể và yêu cầu của bạn.*