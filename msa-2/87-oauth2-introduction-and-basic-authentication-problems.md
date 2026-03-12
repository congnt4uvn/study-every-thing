# Giới thiệu OAuth2 và Vấn đề của Xác thực Cơ bản

## Tổng quan

Tài liệu này giải thích các khái niệm cơ bản về OAuth2, các vấn đề mà nó giải quyết, và lý do tại sao nó được ưu tiên hơn phương thức xác thực cơ bản truyền thống trong việc bảo mật microservices và ứng dụng web.

## OAuth2 là gì?

OAuth2 là một tiêu chuẩn bảo mật hoặc đặc tả bảo mật mà bất kỳ tổ chức nào cũng có thể tuân theo để bảo mật:
- Ứng dụng web
- Ứng dụng di động
- Microservices

Các tổ chức có thể tận dụng đặc tả OAuth2 để bảo mật ứng dụng của họ bất kể loại ứng dụng nào.

## Vấn đề với Xác thực Cơ bản

### Cách Xác thực Cơ bản Hoạt động

Trong những ngày đầu phát triển web, xác thực tuân theo quy trình sau:

1. Các trang web yêu cầu thông tin đăng nhập của người dùng thông qua biểu mẫu HTML
2. Người dùng nhập thông tin đăng nhập của họ
3. Thông tin đăng nhập được gửi đến máy chủ backend
4. Máy chủ backend thực hiện xác thực
5. Sau khi xác thực thành công, máy chủ tạo ra một giá trị phiên (session)
6. Phiên được lưu trữ trong cookie của trình duyệt
7. Người dùng có thể truy cập các tài nguyên được bảo vệ trong khi phiên còn hoạt động

### Nhược điểm của Xác thực Cơ bản

#### 1. Sự Kết hợp Chặt chẽ giữa Logic Nghiệp vụ và Logic Xác thực

- Máy chủ backend chứa cả logic nghiệp vụ và logic xác thực được kết hợp chặt chẽ
- Thay đổi logic xác thực đòi hỏi phải kiểm tra cẩn thận để đảm bảo logic nghiệp vụ không bị ảnh hưởng
- Cần kiểm thử hồi quy rộng rãi
- Không thân thiện với thiết bị di động hoặc REST API

#### 2. Không có Giải pháp Thích hợp cho Quyền truy cập Tạm thời của Bên thứ ba

**Ví dụ Tình huống:**
- Bạn lưu trữ ảnh trong Google Photos
- Một trang web bên thứ ba cung cấp tính năng chỉnh sửa ảnh (collage, bộ lọc, v.v.)
- Để sử dụng các tính năng này, bạn cần nhập ảnh từ Google Photos

**Vấn đề:**
- Với xác thực cơ bản, bạn phải chia sẻ thông tin đăng nhập Google của mình với trang web bên thứ ba
- Bạn phải tin tưởng rằng họ sẽ không lạm dụng thông tin đăng nhập của bạn
- Đây là một rủi ro bảo mật nghiêm trọng

**Giải pháp OAuth2:**
- OAuth2 cung cấp cơ chế thích hợp để tạm thời cấp quyền truy cập vào Google Photos
- Không cần chia sẻ thông tin đăng nhập Google thực tế của bạn
- Bên thứ ba nhận được quyền truy cập hạn chế, tạm thời

## Các Vấn đề mà OAuth2 Giải quyết

### Vấn đề 1: Xác thực và Ủy quyền Tập trung

**Ví dụ Thực tế: Các Sản phẩm của Google**

Google có nhiều sản phẩm:
- Gmail
- Google Maps
- YouTube
- Google Photos
- Google Drive

**Làm thế nào Google cho phép sử dụng cùng một tài khoản trên tất cả các sản phẩm?**

Google sử dụng framework OAuth2 với các tính năng chính sau:

1. **Máy chủ Ủy quyền Riêng biệt**: Tất cả logic xác thực và ủy quyền được tách ra thành một thành phần chuyên dụng gọi là máy chủ ủy quyền (authorization server hoặc authentication server)

2. **Điểm Xác thực Duy nhất**: Khi người dùng đăng nhập vào bất kỳ sản phẩm Google nào, thông tin đăng nhập được gửi đến cùng một auth server

3. **Lợi ích**:
   - Vị trí duy nhất cho logic bảo mật bất kể số lượng ứng dụng/microservices
   - Thay đổi logic bảo mật diễn ra ở một nơi
   - Dễ dàng bảo trì và cập nhật hơn

### Vấn đề 2: Truy cập Bên thứ ba An toàn Không cần Chia sẻ Thông tin Đăng nhập

**Ví dụ Thực tế: Đăng ký StackOverflow**

Khi đăng ký StackOverflow, bạn có nhiều tùy chọn:
- Truyền thống: Nhập tên, email và mật khẩu
- OAuth2: Đăng ký với Google, GitHub hoặc Facebook

**Cách OAuth2 Hoạt động trong Tình huống này:**

1. **Hành động của Người dùng**: Nhấp vào "Đăng ký với GitHub" trên StackOverflow
2. **Chuyển hướng**: Người dùng được chuyển hướng đến GitHub.com
3. **Xác thực**: Người dùng nhập thông tin đăng nhập GitHub trên trang web GitHub (không phải trên StackOverflow)
4. **Bảo mật Thông tin Đăng nhập**: StackOverflow không bao giờ thấy thông tin đăng nhập GitHub của bạn
5. **Chia sẻ Tài nguyên**: Sau khi xác thực thành công, GitHub chia sẻ thông tin cơ bản (tên, email) với StackOverflow
6. **Access Token**: GitHub phát hành một access token cho StackOverflow
7. **Đặc quyền Hạn chế**: Access token có đặc quyền hạn chế (ví dụ: chỉ đọc thông tin hồ sơ)
8. **Không có Quyền truy cập Nâng cao**: StackOverflow không thể thực hiện các thao tác nâng cao như tạo repositories

**Lợi ích Chính:**
- Không chia sẻ thông tin đăng nhập với ứng dụng bên thứ ba
- Quyền truy cập tạm thời với đặc quyền hạn chế
- Thông tin đăng nhập chính vẫn an toàn
- Bên thứ ba chỉ có thể truy cập các tài nguyên được cấp phép rõ ràng
- Có thể đăng nhập tự động bằng access token trong các phiên tương lai

## Tóm tắt

OAuth2 giải quyết các vấn đề bảo mật quan trọng mà xác thực cơ bản không thể xử lý:

1. **Tách biệt Mối quan tâm**: Tách rời xác thực/ủy quyền khỏi logic nghiệp vụ
2. **Bảo mật Tập trung**: Một auth server duy nhất cho tất cả ứng dụng và microservices
3. **Ủy quyền An toàn**: Quyền truy cập tạm thời, hạn chế mà không cần chia sẻ thông tin đăng nhập
4. **Thân thiện với Di động và REST API**: Được thiết kế cho kiến trúc ứng dụng hiện đại
5. **Tích hợp Bên thứ ba**: Cách an toàn để tích hợp với các dịch vụ bên ngoài

## Kết luận

OAuth2 đã trở thành tiêu chuẩn thực tế để bảo mật các ứng dụng hiện đại vì nó giải quyết các vấn đề cơ bản mà xác thực cơ bản không thể giải quyết. Bằng cách triển khai OAuth2, các tổ chức có thể cung cấp bảo mật tốt hơn, bảo trì dễ dàng hơn và tích hợp bên thứ ba an toàn hơn.

---

**Bước tiếp theo**: Trong các bài giảng tiếp theo, chúng ta sẽ đi sâu hơn vào các thành phần OAuth2, các luồng hoạt động và chi tiết triển khai cho microservices sử dụng Spring Boot.