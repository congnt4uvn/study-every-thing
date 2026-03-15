# Hướng Dẫn Học Tập AWS CodeCommit

## Tổng Quan
AWS CodeCommit là dịch vụ kiểm soát mã nguồn được quản lý hoàn toàn, lưu trữ các kho lưu trữ Git an toàn. Đây là dịch vụ kho lưu trữ Git riêng tư cho phép các nhóm cộng tác trên mã nguồn trong một hệ sinh thái an toàn và có khả năng mở rộng cao.

## Khái Niệm Kiểm Soát Phiên Bản

### Kiểm Soát Phiên Bản Là Gì?
- **Định nghĩa**: Khả năng hiểu các thay đổi khác nhau xảy ra với mã nguồn theo thời gian và có thể khôi phục về trước
- **Lợi ích**:
  - Xem những gì đã xảy ra trong quá khứ
  - Theo dõi ai đã commit code và khi nào
  - Xem những gì đã thay đổi, những gì được thêm hoặc xóa
  - Khôi phục về các phiên bản trước

### Công Nghệ Git
- Git là công nghệ cơ bản cho kiểm soát phiên bản
- Kho lưu trữ Git có thể được đồng bộ hóa cục bộ trên máy tính
- Thường được tải lên kho lưu trữ trực tuyến trung tâm để cộng tác
- Cho phép hàng trăm nghìn nhà phát triển làm việc trên cùng một mã nguồn đồng thời
- Đảm bảo mã được sao lưu trên đám mây
- Có thể xem và kiểm tra hoàn chỉnh

## Tại Sao Sử Dụng AWS CodeCommit?

### Xem Xét Chi Phí
- Các dịch vụ Git của bên thứ ba (GitHub, GitLab, Bitbucket) có thể tốn kém
- CodeCommit cung cấp giải pháp thay thế hiệu quả về chi phí trên AWS

### Ưu Điểm Chính
1. **Kho Lưu Trữ Riêng Tư**: Mã nguồn của bạn nằm và ở lại trong VPC của bạn trên AWS cloud
2. **Không Giới Hạn Kích Thước**: Mở rộng lên gigabyte mã nguồn
3. **Quản Lý Hoàn Toàn**: Cơ sở hạ tầng có tính sẵn sàng cao
4. **Bảo Mật**: Mã chỉ ở lại trong AWS cloud để tăng cường bảo mật và tuân thủ
5. **Mã Hóa**: Được mã hóa khi lưu trữ bằng KMS
6. **Kiểm Soát Truy Cập**: Sử dụng IAM để xác thực và phân quyền
7. **Tích Hợp**: Hoạt động với Jenkins, CodeBuild và các công cụ CI khác

## Tính Năng Bảo Mật

### Xác Thực
- **SSH Keys**: Cấu hình SSH keys để truy cập kho lưu trữ Git
- **HTTPS**: Sử dụng đăng nhập và mật khẩu tiêu chuẩn cho kho lưu trữ Git
- Sử dụng dòng lệnh Git tiêu chuẩn với xác thực bổ sung

### Phân Quyền
- Chính sách IAM quản lý quyền của người dùng và vai trò đối với các kho lưu trữ cụ thể
- Quản lý bảo mật tập trung thông qua AWS IAM

### Mã Hóa
- **Khi Lưu Trữ**: Mã được mã hóa bằng AWS KMS (Key Management Service)
- **Khi Truyền Tải**: Mã hóa qua giao thức HTTPS hoặc SSH

### Truy Cập Giữa Các Tài Khoản
- Không chia sẻ SSH keys hoặc thông tin đăng nhập
- Tạo vai trò IAM trong tài khoản của bạn
- Sử dụng STS AssumeRole API để truy cập các kho lưu trữ CodeCommit

## So Sánh CodeCommit vs GitHub

### Điểm Giống Nhau
- Cả hai đều hỗ trợ đánh giá mã nguồn (pull requests)
- Cả hai đều tích hợp với CodeBuild
- Cả hai đều hỗ trợ xác thực với SSH và HTTPS

### Điểm Khác Nhau

| Tính Năng | CodeCommit | GitHub |
|-----------|------------|--------|
| **Xác thực** | Người dùng và vai trò IAM | Người dùng GitHub, SSO (Enterprise) |
| **Lưu trữ** | Chỉ trên AWS | Máy chủ GitHub hoặc tại chỗ (Enterprise) |
| **Giao diện** | Giao diện tối giản | Giao diện đầy đủ tính năng |
| **Tích hợp** | Tích hợp sâu với AWS | Dịch vụ bên thứ ba |
| **Tuân thủ** | Mã ở trong hệ sinh thái AWS | Mã trên cơ sở hạ tầng GitHub |

## Các Trường Hợp Sử Dụng

### Khi Nào Sử Dụng CodeCommit
- Cần giữ mã trong hệ sinh thái AWS để tuân thủ
- Muốn tích hợp sâu với các dịch vụ AWS
- Dự án nhạy cảm về chi phí
- Yêu cầu bảo mật quy định chỉ lưu trữ trên AWS
- Sử dụng các công cụ phát triển AWS khác (CodeBuild, CodePipeline)

### Khi Nào Cân Nhắc Các Giải Pháp Thay Thế
- Cần tính năng giao diện nâng cao
- Nhóm đã sử dụng quy trình làm việc GitHub/GitLab
- Yêu cầu tích hợp bên thứ ba cụ thể
- Chiến lược đa đám mây

## Thực Hành Tốt Nhất
1. Sử dụng vai trò IAM để quản lý quyền truy cập
2. Bật mã hóa với KMS
3. Triển khai các quy tắc bảo vệ nhánh
4. Sử dụng pull requests để đánh giá mã nguồn
5. Tích hợp với quy trình CI/CD
6. Giám sát hoạt động của kho lưu trữ
7. Lập kế hoạch sao lưu và phục hồi thảm họa thường xuyên

## Những Điểm Chính Cần Nhớ
- CodeCommit là dịch vụ Git được quản lý của AWS
- Cung cấp các kho lưu trữ riêng tư, an toàn, có khả năng mở rộng
- Tích hợp sâu với hệ sinh thái AWS
- Hiệu quả về chi phí cho các quy trình làm việc tập trung vào AWS
- Bảo mật mạnh mẽ với IAM, KMS và mã hóa
- Phù hợp cho các nhóm yêu cầu tuân thủ AWS
