# Mô Hình Trách Nhiệm Chia Sẻ AWS IAM

## Tổng Quan

Trong suốt kỳ thi AWS Certified Cloud Practitioner (CCP), bạn sẽ gặp rất nhiều câu hỏi về **Mô Hình Trách Nhiệm Chia Sẻ** (Shared Responsibility Model). Hiểu rõ mô hình này là rất quan trọng vì nó xác định rõ ràng AWS chịu trách nhiệm về điều gì và bạn, với tư cách là khách hàng, chịu trách nhiệm về điều gì.

## Trách Nhiệm Của AWS

AWS chịu trách nhiệm về các khía cạnh nền tảng của hạ tầng đám mây:

- **Quản Lý Hạ Tầng**: AWS quản lý toàn bộ hạ tầng vật lý cung cấp sức mạnh cho các dịch vụ của họ
- **Bảo Mật Mạng Toàn Cầu**: Đảm bảo an toàn cho hạ tầng mạng lưới trên toàn thế giới
- **Cấu Hình và Phân Tích Lỗ Hổng**: Đánh giá và bảo trì thường xuyên các dịch vụ của họ
- **Xác Thực Tuân Thủ**: Đáp ứng các tiêu chuẩn và chứng nhận tuân thủ khác nhau mà AWS cam kết

## Trách Nhiệm Của Khách Hàng Đối Với IAM

Khi nói đến Quản Lý Danh Tính và Truy Cập (IAM), khách hàng phải chịu trách nhiệm đáng kể về bảo mật và cấu hình phù hợp:

### Quản Lý Người Dùng và Quyền Truy Cập
- **Tạo và Quản Lý Người Dùng**: Bạn phải tự tạo các IAM users, groups, roles và policies
- **Quản Lý Chính Sách**: Chịu trách nhiệm về việc quản lý và giám sát liên tục các chính sách này
- **Xem Xét Quyền Truy Cập**: Phân tích thường xuyên các mẫu truy cập và xem xét quyền hạn trên toàn bộ tài khoản của bạn

### Thực Hành Bảo Mật Tốt Nhất
- **Xác Thực Đa Yếu Tố (MFA)**: Bạn có trách nhiệm kích hoạt MFA trên tất cả các tài khoản và thực thi biện pháp bảo mật này trong toàn tổ chức
- **Luân Chuyển Khóa**: Đảm bảo rằng các access keys và credentials được luân chuyển thường xuyên
- **Quản Lý Quyền Hạn**: Sử dụng các công cụ IAM để áp dụng quyền hạn phù hợp dựa trên nguyên tắc đặc quyền tối thiểu

## Điểm Chính Cần Nhớ

Mô Hình Trách Nhiệm Chia Sẻ có thể được tóm tắt như sau:
- **AWS chịu trách nhiệm** bảo mật hạ tầng và chính đám mây
- **Bạn chịu trách nhiệm** về cách bạn sử dụng hạ tầng đó và bảo mật các tài nguyên của bạn trong đám mây

Đây là một khái niệm cơ bản xuất hiện xuyên suốt các kỳ thi chứng chỉ AWS và rất quan trọng để duy trì môi trường đám mây an toàn.

---

*Bài giảng này cung cấp sự hiểu biết cơ bản về Mô Hình Trách Nhiệm Chia Sẻ của AWS áp dụng cho Quản Lý Danh Tính và Truy Cập.*