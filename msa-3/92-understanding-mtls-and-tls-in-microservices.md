# Hiểu về mTLS và TLS trong Microservices

## Giới thiệu

Bài giảng này giải thích mTLS (Mutual Transport Layer Security) là gì và tại sao nó lại quan trọng để bảo mật giao tiếp giữa các microservices. Để hiểu đầy đủ về mTLS, trước tiên chúng ta cần nắm vững cách TLS hoạt động, vì mTLS là một biến thể của TLS.

## TLS là gì?

**TLS (Transport Layer Security)** là một giao thức mã hóa đã thay thế SSL (Secure Socket Layer) đã bị loại bỏ và hiện đang được sử dụng trong giao tiếp HTTPS.

### Tại sao TLS quan trọng

Khi một client (như trình duyệt) giao tiếp với máy chủ backend, chúng cần giao tiếp trong môi trường bảo mật bằng định dạng mã hóa. Nếu không có giao thức HTTPS:

- Bất kỳ ai lắng nghe lưu lượng mạng đều có thể thấy văn bản thuần túy di chuyển từ trình duyệt đến máy chủ backend
- Dữ liệu nhạy cảm như thông tin thẻ tín dụng có thể dễ dàng bị đánh cắp trong quá trình truyền
- Không có cách nào xác minh danh tính của máy chủ

### Hạn chế của TLS trong Microservices

Mặc dù TLS bảo mật hiệu quả giao tiếp từ trình duyệt đến máy chủ, nhưng nó có những hạn chế đối với microservices:

- Trong TLS, chỉ có máy chủ backend (chủ sở hữu tên miền) chứng minh danh tính của mình thông qua chứng chỉ
- Microservices không sử dụng trình duyệt để giao tiếp - chúng sử dụng giao tiếp API
- Trong môi trường microservices, **cả hai microservices đều cần chứng minh danh tính của mình**
- TLS đơn thuần không thể bảo mật các microservices nội bộ trong cụm Kubernetes

## Hiểu về mTLS (Mutual TLS)

**mTLS (Mutual Transport Layer Security)** khắc phục những hạn chế của TLS bằng cách yêu cầu cả hai bên (cả hai ứng dụng) phải xác thực lẫn nhau trước khi giao tiếp có thể diễn ra.

### Môi trường Zero Trust (Không tin cậy)

mTLS thường được sử dụng trong **framework bảo mật không tin cậy (zero trust)**, trong đó:

- Mặc dù các microservices được triển khai trong cụm Kubernetes của riêng bạn, bạn không tin tưởng lưu lượng nội bộ theo mặc định
- Không có người dùng, thiết bị hoặc lưu lượng nào được tự động tin cậy
- Tất cả các thành phần phải chứng minh danh tính của chúng trước khi giao tiếp

### Tại sao Zero Trust quan trọng

Hãy xem xét những rủi ro bảo mật này:

1. **Lỗ hổng từ bên thứ ba**: Một thư viện bên thứ ba trong container của bạn có thể có lỗ hổng bảo mật, có khả năng để lộ lưu lượng không mã hóa
2. **Giao tiếp trái phép**: Một container microservice có thể cố gắng giao tiếp với container khác mà nó không được phép truy cập
3. **Mối đe dọa nội bộ**: Chỉ vì lưu lượng là nội bộ không có nghĩa là nó an toàn

## Cách TLS hoạt động

Trước khi hiểu mTLS, hãy xem xét quy trình TLS một cách chi tiết.

### Tổng quan về TLS

TLS được sử dụng rộng rãi trên internet để mã hóa. Bạn có thể nghe "SSL" và "TLS" được sử dụng thay thế cho nhau, nhưng TLS là tiêu chuẩn hiện tại - SSL đã bị loại bỏ do các vấn đề bảo mật.

### Certificate Authorities (Tổ chức phát hành chứng chỉ)

**Certificate Authorities (CAs)** là các tổ chức đáng tin cậy:

- Phát hành chứng chỉ cho các tổ chức sau khi xác minh quyền sở hữu tên miền
- Xác thực chứng chỉ được trình bày bởi máy chủ
- Cung cấp nền tảng tin cậy cho giao tiếp HTTPS

### Quy trình TLS Handshake

Hãy xem xét cách TLS bảo mật giao tiếp giữa trình duyệt và amazon.com:

#### Bước 1: TCP Handshake
Trình duyệt và máy chủ web thiết lập kết nối TCP để xác nhận không có vấn đề mạng.

#### Bước 2: Thông điệp Hello
Trình duyệt gửi thông điệp "hello" yêu cầu máy chủ chứng minh danh tính của nó.

#### Bước 3: Trình bày Chứng chỉ
Máy chủ web chia sẻ chứng chỉ của nó (chứa khóa công khai) với trình duyệt.

#### Bước 4: Xác thực Chứng chỉ
- Trình duyệt xác thực chứng chỉ với Certificate Authorities
- Nếu hợp lệ, trình duyệt hiển thị biểu tượng ổ khóa cho biết kết nối an toàn
- Nếu không hợp lệ, trình duyệt cảnh báo người dùng không nhập thông tin nhạy cảm

#### Bước 5: Thiết lập Mã hóa Bất đối xứng
Chứng chỉ chứa hai loại khóa:

- **Khóa Công khai (Public Key)**: Được chia sẻ với trình duyệt; được sử dụng để mã hóa dữ liệu
- **Khóa Riêng tư (Private Key)**: Được giữ bí mật bởi máy chủ; được sử dụng để giải mã dữ liệu

Điều này được gọi là **mã hóa bất đối xứng (asymmetric encryption)** vì mã hóa và giải mã sử dụng các thành phần khác nhau.

#### Bước 6: Tạo Session Key (Khóa phiên)
Trình duyệt tạo một **session key** và mã hóa nó bằng khóa công khai của máy chủ, sau đó gửi nó đến máy chủ. Ngay cả khi ai đó chặn khóa phiên được mã hóa này, họ cũng không thể giải mã nó nếu không có khóa riêng tư.

#### Bước 7: Giải mã Session Key
Máy chủ web giải mã khóa phiên bằng khóa riêng tư của nó và xác nhận đã nhận với trình duyệt.

#### Bước 8: Giao tiếp Mã hóa Đối xứng
Bây giờ cả hai bên đều có cùng một khóa phiên. Họ sử dụng nó cho giao tiếp dữ liệu thực tế, được gọi là **mã hóa đối xứng (symmetric encryption)** vì cùng một khóa được sử dụng cho cả mã hóa và giải mã.

### Tại sao chuyển từ Mã hóa Bất đối xứng sang Đối xứng?

Mã hóa bất đối xứng có những hạn chế cho giao tiếp đang diễn ra:

1. **Mã hóa một chiều**: Chỉ trình duyệt có thể gửi dữ liệu được mã hóa đến máy chủ
2. **Không giải mã phản hồi**: Trình duyệt không có khóa riêng tư để giải mã các phản hồi được mã hóa
3. **Chi phí hiệu suất**: Mã hóa bất đối xứng chậm hơn mã hóa đối xứng

Ưu điểm của mã hóa đối xứng:

- **Hiệu suất tốt hơn**: Nhanh hơn mã hóa bất đối xứng
- **Bảo mật hai chiều**: Cả hai bên đều có thể mã hóa và giải mã dữ liệu
- **Bí mật được chia sẻ**: Chỉ trình duyệt và máy chủ biết khóa phiên

### Xem TLS trong thực tế

Khi bạn truy cập bất kỳ trang web HTTPS nào (như amazon.com):

1. Trình duyệt xác thực chứng chỉ ở hậu trường
2. Biểu tượng ổ khóa xuất hiện cho biết kết nối an toàn
3. Bạn có thể nhấp vào ổ khóa để xem chi tiết chứng chỉ
4. Chứng chỉ cho thấy nó đã được xác thực và phát hành cho chủ sở hữu tên miền hợp pháp

### Mô hình Xác thực TLS

Trong TLS tiêu chuẩn:

- **Client (trình duyệt) yêu cầu máy chủ chứng minh danh tính của nó** thông qua chứng chỉ
- **Máy chủ không bao giờ yêu cầu trình duyệt chứng minh danh tính của nó**
- Người dùng chứng minh danh tính thông qua xác thực tên người dùng/mật khẩu
- Điều này hoạt động vì có hàng tỷ trình duyệt tồn tại - chứng chỉ cá nhân không thực tế

## Tại sao cần mTLS cho Microservices?

Mô hình TLS truyền thống không hoạt động cho giao tiếp ứng dụng với ứng dụng vì:

1. Cả hai ứng dụng đều là các bên tham gia quan trọng ngang nhau
2. Không có người dùng tham gia để cung cấp thông tin xác thực
3. Cả hai bên cần xác minh danh tính của nhau
4. Kiến trúc service mesh yêu cầu xác thực lẫn nhau

## Các bước tiếp theo

Trong bài giảng tiếp theo, chúng ta sẽ khám phá cách mTLS hoạt động trong thực tế với các triển khai service mesh trong môi trường Kubernetes.

## Tóm tắt

- **TLS** bảo mật giao tiếp từ trình duyệt đến máy chủ thông qua xác thực máy chủ dựa trên chứng chỉ
- **mTLS** mở rộng điều này bằng cách yêu cầu cả hai bên xác thực lẫn nhau
- **Bảo mật không tin cậy (Zero trust)** giả định không có lưu lượng nội bộ nào an toàn theo mặc định
- **Mã hóa bất đối xứng** được sử dụng cho handshake ban đầu và trao đổi khóa
- **Mã hóa đối xứng** được sử dụng cho giao tiếp dữ liệu thực tế do lợi ích về hiệu suất
- **mTLS là thiết yếu** để bảo mật giao tiếp microservice-to-microservice trong cụm Kubernetes

---

*Tài liệu này dựa trên bài giảng kỹ thuật về bảo mật microservices sử dụng Spring Boot và Kubernetes.*