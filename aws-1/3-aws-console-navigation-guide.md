# Hướng Dẫn Điều Hướng AWS Console

## Giới Thiệu

Chào mừng bạn đến với Trang Chủ AWS Console. Hướng dẫn này sẽ giúp bạn làm quen với AWS Management Console và hiểu cách điều hướng cũng như sử dụng các tính năng khác nhau một cách hiệu quả.

## Lựa Chọn Region (Vùng)

### Hiểu Về AWS Regions

Ở góc trên bên phải màn hình của bạn, bạn sẽ tìm thấy **bộ chọn vùng** (regions selector). Đây là một thành phần quan trọng để quản lý tài nguyên AWS của bạn.

- **Hiển Thị Vùng Hiện Tại**: Bộ chọn hiển thị vùng bạn đang chọn (ví dụ: "Northern Virginia, US East 1")
- **Thực Hành Tốt Nhất**: Chọn một vùng gần với vị trí địa lý của bạn để có hiệu suất tối ưu
- **Ví Dụ**: Nếu bạn ở châu Âu, hãy cân nhắc chọn "EU West 1" (Ireland); nếu bạn ở châu Phi gần Cape Town, chọn vùng Cape Town

### Những Lưu Ý Quan Trọng Về Vùng

- Bạn không cần phải ở vị trí vật lý của vùng đó để sử dụng nó
- Chọn vùng phù hợp nhất với nhu cầu của bạn
- Chọn vùng gần hơn sẽ cho bạn độ trễ thấp nhất
- Quan trọng là bạn nên duy trì cùng một vùng trong suốt khóa học hoặc hướng dẫn của bạn

## Các Tính Năng Của Console Home

### Dịch Vụ Đã Truy Cập Gần Đây

Console hiển thị danh sách các dịch vụ bạn đã truy cập gần đây. Phần này sẽ trống khi bạn mới bắt đầu sử dụng AWS, nhưng sẽ được điền khi bạn điều hướng qua các dịch vụ khác nhau.

### Bảng Thông Tin

Ở cuối trang chủ, bạn sẽ tìm thấy:
- Thông tin chung về AWS
- Các vấn đề về tình trạng hệ thống (nếu có)
- Thông tin về chi phí và sử dụng cho tài khoản của bạn
- Các hướng dẫn để xây dựng giải pháp

**Lưu Ý**: Trang chủ AWS Console thay đổi thường xuyên. Nếu nó trông khác đáng kể so với những gì bạn thấy trong hướng dẫn, đừng lo lắng - chức năng cốt lõi vẫn giữ nguyên.

## Tìm Kiếm Dịch Vụ AWS

### Phương Pháp 1: Menu Services

1. Nhấp vào **Services** ở góc trên bên trái
2. Duyệt các dịch vụ theo hai cách:
   - **Thứ Tự Bảng Chữ Cái**: Xem tất cả các dịch vụ AWS được sắp xếp từ A-Z
   - **Theo Danh Mục**: Ví dụ, trong mục "Compute" bạn sẽ tìm thấy tất cả các dịch vụ liên quan đến điện toán

### Phương Pháp 2: Thanh Tìm Kiếm

Thanh tìm kiếm là một công cụ mạnh mẽ để nhanh chóng tìm kiếm dịch vụ:

1. Nhập tên dịch vụ (ví dụ: "Route 53")
2. Xem kết quả tìm kiếm bao gồm:
   - Các dịch vụ phù hợp (ví dụ: 4 dịch vụ)
   - Các tính năng trong những dịch vụ đó (ví dụ: 13 tính năng)
   - Liên kết trực tiếp đến các tính năng cụ thể (ví dụ: tên miền trong Route 53)
   - Các blog, bài viết kiến thức và tài liệu liên quan

## Hiểu Về Dịch Vụ Global và Regional

### Dịch Vụ Global (Toàn Cầu)

Một số dịch vụ AWS là **dịch vụ toàn cầu**, nghĩa là chúng không yêu cầu lựa chọn vùng.

**Ví Dụ: Route 53**
- Khi bạn truy cập Route 53, bạn sẽ thấy "Global" ở góc trên bên phải
- Bạn sẽ nhận được cùng một giao diện bất kể vùng bạn đã chọn
- Đây là ngoại lệ chứ không phải là quy tắc

### Dịch Vụ Regional (Theo Vùng)

Hầu hết các dịch vụ AWS là **dịch vụ theo vùng**, nghĩa là chúng hoạt động trong các vùng cụ thể.

**Ví Dụ: EC2**
- Khi bạn truy cập EC2, bạn sẽ thấy vùng đã chọn (ví dụ: "Ireland") ở góc trên bên phải
- Giao diện của bạn sẽ khác nhau dựa trên vùng đã chọn
- Các tài nguyên được tạo trong một vùng sẽ không xuất hiện khi xem vùng khác

## Cơ Sở Hạ Tầng Toàn Cầu AWS

### Tài Liệu Về Dịch Vụ Theo Vùng

Bạn có thể tìm thông tin chi tiết về các dịch vụ AWS theo vùng:

1. Tìm kiếm "AWS global infrastructure" trên Google
2. Điều hướng đến trang **AWS Regional Services**
3. Xem danh sách dịch vụ được sắp xếp theo vùng

### Kiểm Tra Tính Khả Dụng Của Dịch Vụ

Tài nguyên này đặc biệt hữu ích khi:
- Một dịch vụ được đề cập trong khóa học không có sẵn trong vùng của bạn
- Bạn cần xác minh dịch vụ nào có sẵn trong các vùng cụ thể
- Bạn đang lên kế hoạch triển khai tài nguyên trong một vùng mới

**Ví Dụ**: Bạn có thể kiểm tra dịch vụ nào có sẵn ở Cape Town hoặc bất kỳ vùng AWS nào khác.

### Lưu Ý Quan Trọng

Không phải tất cả các dịch vụ AWS đều có sẵn trong mọi vùng. Nếu bạn không thấy dịch vụ bạn cần:
- Kiểm tra trang AWS Regional Services
- Cân nhắc chuyển sang vùng có dịch vụ đó
- Lập kế hoạch kiến trúc của bạn cho phù hợp

## Kết Luận

Hiểu cách điều hướng AWS Console là nền tảng để làm việc hiệu quả với các dịch vụ AWS. Hãy dành thời gian làm quen với:
- Lựa chọn vùng và các tác động của nó
- Các phương pháp khác nhau để tìm dịch vụ
- Sự khác biệt giữa dịch vụ toàn cầu và dịch vụ theo vùng
- Cách xác minh tính khả dụng của dịch vụ trong vùng của bạn

Khi bạn tiếp tục làm việc với AWS, những kỹ năng điều hướng này sẽ trở nên tự nhiên, cho phép bạn tập trung vào việc xây dựng và quản lý cơ sở hạ tầng đám mây của mình một cách hiệu quả.