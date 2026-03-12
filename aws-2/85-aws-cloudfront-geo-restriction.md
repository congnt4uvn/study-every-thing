# AWS CloudFront Geo Restriction (Hạn Chế Địa Lý)

## Tổng Quan

CloudFront geo restriction cho phép bạn kiểm soát ai có thể truy cập distribution của bạn dựa trên vị trí địa lý (quốc gia) mà họ cố gắng truy cập. Tính năng này sử dụng cơ sở dữ liệu geo IP của bên thứ ba để khớp địa chỉ IP của người dùng với quốc gia tương ứng.

## Cách Thức Hoạt Động

Tính năng hạn chế địa lý xác định quốc gia của người dùng bằng cách:
- Khớp địa chỉ IP của người dùng với cơ sở dữ liệu geo IP của bên thứ ba
- Xác định quốc gia liên quan đến địa chỉ IP đó
- Áp dụng các quy tắc cho phép hoặc chặn đã được cấu hình

## Tùy Chọn Cấu Hình

Bạn có thể cấu hình geo restriction theo hai cách:

### 1. Allow List (Danh Sách Cho Phép)
Xác định danh sách các quốc gia được phê duyệt có thể truy cập nội dung của bạn. Chỉ người dùng từ các quốc gia này mới có thể truy cập distribution.

### 2. Block List (Danh Sách Chặn)
Xác định danh sách các quốc gia bị cấm không thể truy cập nội dung của bạn. Người dùng từ các quốc gia này sẽ bị từ chối quyền truy cập vào distribution.

## Trường Hợp Sử Dụng

Trường hợp sử dụng chính cho geo restriction là:
- **Tuân Thủ Luật Bản Quyền**: Kiểm soát quyền truy cập nội dung dựa trên các thỏa thuận cấp phép địa lý và hạn chế bản quyền

## Yêu Cầu Thiết Lập

### Yêu Cầu Gói Dịch Vụ
Để sử dụng chức năng chặn lưu lượng truy cập theo địa lý, bạn cần:
- Gói thanh toán **Pay as You Go** (Trả theo mức sử dụng), hoặc
- Gói CloudFront trả phí

Lưu ý: Gói miễn phí không hỗ trợ tính năng geo restriction.

### Các Bước Cấu Hình

1. Điều hướng đến CloudFront distribution của bạn
2. Vào phần **Security** (Bảo mật)
3. Chọn **CloudFront geographic restrictions** (Hạn chế địa lý CloudFront)
4. Chọn một trong hai:
   - **Allow list**: Chọn các quốc gia được phép
   - **Block list**: Chọn các quốc gia bị chặn
5. Chọn các quốc gia bạn muốn thêm vào danh sách
6. Lưu thay đổi của bạn

## Lưu Ý Quan Trọng

- Hạn chế địa lý chỉ khả dụng trên các gói Pay as You Go hoặc gói trả phí
- Gói miễn phí (manage free plan) không bao gồm chức năng chặn lưu lượng truy cập theo địa lý
- Các thay đổi đối với geo restrictions có thể mất một thời gian để lan truyền
- Tính năng này dựa vào dữ liệu định vị địa lý IP của bên thứ ba, có thể không chính xác 100%

## Thực Hành Tốt Nhất

- Thường xuyên xem xét cài đặt geo restriction của bạn để đảm bảo chúng phù hợp với các thỏa thuận cấp phép nội dung
- Kiểm tra các hạn chế của bạn từ các vị trí khác nhau để xác minh chúng hoạt động như mong đợi
- Lưu ý rằng VPN và proxy có thể ảnh hưởng đến độ chính xác của việc phát hiện địa lý
- Ghi chúng các chính sách geo restriction của bạn cho mục đích tuân thủ và kiểm toán