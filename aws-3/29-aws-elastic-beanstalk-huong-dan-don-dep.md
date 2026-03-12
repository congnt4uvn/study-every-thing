# AWS Elastic Beanstalk - Hướng Dẫn Dọn Dẹp và Xóa Tài Nguyên

## Tổng Quan

Hướng dẫn này trình bày quy trình dọn dẹp và xóa các ứng dụng AWS Elastic Beanstalk cùng các tài nguyên liên quan để tránh chi phí không cần thiết.

## Tại Sao Cần Dọn Dẹp Tài Nguyên?

Khi chạy nhiều instances, load balancers và các tài nguyên AWS khác đồng thời, chi phí có thể tích lũy nhanh chóng nếu để chạy liên tục. Việc dọn dẹp đúng cách đảm bảo bạn không phát sinh chi phí không cần thiết.

## Xóa Ứng Dụng Elastic Beanstalk

### Quy Trình Từng Bước

1. **Điều Hướng Đến Cấp Độ Ứng Dụng**
   - Truy cập console AWS Elastic Beanstalk
   - Tìm ứng dụng bạn muốn xóa

2. **Khởi Tạo Quá Trình Xóa**
   - Chọn ứng dụng
   - Nhấp vào **Actions** (Hành động)
   - Chọn **Delete Application** (Xóa ứng dụng)

3. **Xác Nhận Xóa**
   - Nhập lại tên ứng dụng khi được yêu cầu
   - Bước xác nhận này ngăn chặn việc xóa nhầm

## Những Gì Sẽ Bị Xóa?

Khi bạn xóa một ứng dụng Elastic Beanstalk, các tài nguyên sau sẽ tự động bị xóa:

- **Tất cả các môi trường** liên quan đến ứng dụng
- **CloudFormation stacks** (chuyển sang trạng thái "delete in progress")
- **Load balancers** (Bộ cân bằng tải)
- **Auto Scaling groups** (Nhóm Auto Scaling)
- **Security groups** (Nhóm bảo mật)
- **Các tài nguyên liên quan khác** được tạo bởi CloudFormation

## Bên Trong: CloudFormation

Quá trình xóa tận dụng **AWS CloudFormation**, được sử dụng bên dưới bởi Elastic Beanstalk. Đây là một trong những lợi ích chính khi sử dụng CloudFormation:

- Tất cả các tài nguyên được tạo thông qua CloudFormation stacks đều được theo dõi tự động
- Khi bạn xóa ứng dụng, CloudFormation xử lý việc dọn dẹp tất cả các tài nguyên liên quan
- Điều này đảm bảo không có tài nguyên bị bỏ lại

## Lưu Ý Quan Trọng

- ⏱️ Quá trình xóa có thể mất vài phút để hoàn tất
- ✅ Sau khi xóa hoàn tất, không cần xóa thủ công gì thêm
- 💰 Xóa tài nguyên kịp thời giúp kiểm soát chi phí AWS
- 🔒 Luôn kiểm tra kỹ trước khi xác nhận xóa để tránh mất ứng dụng quan trọng

## Thực Hành Tốt Nhất

1. **Dọn Dẹp Thường Xuyên**: Xóa các môi trường phát triển và thử nghiệm khi không sử dụng
2. **Giám Sát Chi Phí**: Thường xuyên xem xét các tài nguyên đang chạy
3. **Sử Dụng CloudFormation**: Tận dụng khả năng quản lý tài nguyên tự động của CloudFormation
4. **Xác Minh Xóa**: Kiểm tra console CloudFormation để đảm bảo các stacks đã được xóa hoàn toàn

## Kết Luận

Việc dọn dẹp đúng cách các ứng dụng Elastic Beanstalk là một phần quan trọng trong quản lý tài nguyên AWS. Bằng cách sử dụng tính năng xóa ở cấp độ ứng dụng, bạn có thể xóa hiệu quả tất cả các tài nguyên liên quan mà không cần can thiệp thủ công, nhờ vào khả năng theo dõi tài nguyên tự động của CloudFormation.