# Các Khái Niệm Nâng Cao về AWS SQS FIFO

## Giới Thiệu

Hướng dẫn này bao gồm các khái niệm nâng cao về Amazon SQS FIFO (First-In-First-Out - Vào Trước Ra Trước), bao gồm khử trùng lặp tin nhắn và các chiến lược nhóm tin nhắn.

## Khử Trùng Lặp Tin Nhắn (Message Deduplication)

### Khoảng Thời Gian Khử Trùng Lặp

Hàng đợi SQS FIFO có **khoảng thời gian khử trùng lặp là 5 phút**. Nếu bạn gửi cùng một tin nhắn hai lần trong khoảng thời gian này, tin nhắn thứ hai sẽ bị từ chối.

### Các Phương Pháp Khử Trùng Lặp

Có hai phương pháp để khử trùng lặp tin nhắn:

#### 1. Khử Trùng Lặp Dựa Trên Nội Dung (Content-Based Deduplication)

Khi bạn gửi tin nhắn đến SQS, một mã băm được tính toán bằng **thuật toán SHA-256** trên nội dung tin nhắn. Nếu cùng một nội dung tin nhắn được gặp hai lần, cùng một mã băm sẽ được tạo ra, và tin nhắn thứ hai sẽ bị từ chối.

**Cách hoạt động:**
- Người gửi gửi tin nhắn "hello world"
- SQS FIFO tạo ra một mã băm SHA-256 của tin nhắn
- Nếu người gửi gửi lại chính xác tin nhắn đó, nó sẽ được băm thành cùng một giá trị
- SQS FIFO nhận ra bản sao và từ chối tin nhắn thứ hai

#### 2. ID Khử Trùng Lặp Tin Nhắn (Message Deduplication ID)

Bạn có thể cung cấp rõ ràng một **ID khử trùng lặp tin nhắn** khi gửi tin nhắn. Nếu cùng một ID khử trùng lặp được gặp hai lần trong khoảng thời gian khử trùng lặp, tin nhắn trùng lặp sẽ bị từ chối.

## Nhóm Tin Nhắn (Message Grouping)

### Tổng Quan

Nhóm tin nhắn cho phép bạn kiểm soát thứ tự và cho phép xử lý song song trong hàng đợi SQS FIFO.

### Cách Hoạt Động của Message Group ID

- **Message Group ID** là tham số bắt buộc khi gửi tin nhắn đến hàng đợi FIFO
- Nếu bạn chỉ định cùng một giá trị cho Message Group ID, tất cả tin nhắn sẽ được xử lý bởi một consumer theo thứ tự
- Để cho phép xử lý song song, chỉ định các Message Group ID khác nhau cho các nhóm tin nhắn khác nhau

### Các Đặc Điểm Chính

- Các tin nhắn có cùng Message Group ID được sắp xếp theo thứ tự trong nhóm đó
- Mỗi Message Group ID có thể có một consumer khác nhau
- Điều này cho phép xử lý song song trên hàng đợi SQS FIFO của bạn
- **Thứ tự giữa các nhóm không được đảm bảo**

### Ví Dụ Trường Hợp Sử Dụng

Xem xét một hàng đợi FIFO với ba nhóm tin nhắn: A, B và C:

**Nhóm A:**
- Tin nhắn: A1, A2, A3
- Consumer: Consumer cho Nhóm A

**Nhóm B:**
- Tin nhắn: B1, B2, B3, B4
- Consumer: Consumer cho Nhóm B

**Nhóm C:**
- Tin nhắn: C1, C2
- Consumer: Consumer cho Nhóm C

### Ứng Dụng Thực Tế

Bạn có thể không cần sắp xếp tổng thể tất cả các tin nhắn, mà chỉ cần sắp xếp cho các tập hợp con cụ thể. Ví dụ:

- Sử dụng **ID khách hàng** làm Message Group ID
- Mỗi khách hàng có luồng tin nhắn được sắp xếp riêng của mình
- Bạn có thể có nhiều consumer bằng số lượng người dùng trong ứng dụng của bạn
- Tin nhắn cho mỗi người dùng vẫn theo thứ tự nhờ vào đảm bảo của SQS FIFO

## Hướng Dẫn Thực Hành

### Bước 1: Kích Hoạt Content-Based Deduplication

1. Điều hướng đến hàng đợi SQS FIFO của bạn
2. Nhấp vào **Edit** (Chỉnh sửa)
3. Kích hoạt **Content-Based Deduplication** (Khử trùng lặp dựa trên nội dung)
4. ID khử trùng lặp sẽ được tính toán dưới dạng SHA-256 của tin nhắn
5. Nhấp vào **Save** (Lưu)

### Bước 2: Kiểm Tra Khử Trùng Lặp Tin Nhắn

1. Đi đến **Send and receive messages** (Gửi và nhận tin nhắn)
2. Gửi một tin nhắn: "hello world"
3. Đặt Message Group ID thành "demo"
4. Lưu ý: Message Deduplication ID là tùy chọn khi content-based deduplication được kích hoạt
5. Nhấp vào **Send message** (Gửi tin nhắn)

**Kiểm Tra Khử Trùng Lặp:**
- Gửi cùng một tin nhắn nhiều lần chỉ cho kết quả là một tin nhắn có sẵn
- Tin nhắn đã được SQS nhìn thấy, vì vậy quá trình khử trùng lặp xảy ra
- Gửi một tin nhắn khác (ví dụ: "hello world two") sẽ thêm tin nhắn thứ hai vào hàng đợi

### Bước 3: Sử Dụng Custom Deduplication ID

Bạn có thể cung cấp token khử trùng lặp của riêng mình:
1. Gửi tin nhắn với custom deduplication ID (ví dụ: "1-2-3")
2. Gửi lại tin nhắn với cùng deduplication ID sẽ chỉ tạo ra một tin nhắn trong hàng đợi

### Bước 4: Kiểm Tra Message Grouping

**Tin Nhắn của User 123:**
1. Tin nhắn: "user bought an apple" (người dùng mua một quả táo)
2. Message Group ID: "user123"
3. Tin nhắn: "user bought a banana" (người dùng mua một quả chuối)
4. Message Group ID: "user123"
5. Tin nhắn: "user bought strawberries" (người dùng mua dâu tây)
6. Message Group ID: "user123"

Tất cả các tin nhắn này có cùng Message Group ID và sẽ được xử lý theo thứ tự cho user123.

**Tin Nhắn của User 234:**
1. Tin nhắn: "user bought a green apple" (người dùng mua một quả táo xanh)
2. Message Group ID: "user234"

Các tin nhắn này cho user234 sẽ theo thứ tự cho người dùng đó.

### Kết Quả

Hàng đợi SQS FIFO của bạn giờ đây có thể có nhiều consumer chạy đồng thời, với mỗi consumer xử lý tin nhắn từ một Message Group ID khác nhau.

## Dọn Dẹp

Khi bạn hoàn thành việc kiểm tra:
1. Poll các tin nhắn để xem xét chúng
2. Xóa các tin nhắn khỏi hàng đợi

## Tóm Tắt

- **Khử trùng lặp** ngăn chặn tin nhắn trùng lặp trong khoảng thời gian 5 phút
- **Content-based deduplication** sử dụng băm SHA-256
- **Message Group ID** cho phép xử lý có thứ tự theo nhóm
- **Nhiều consumer** có thể xử lý các nhóm khác nhau song song
- Sử dụng ID khách hàng/người dùng làm Message Group ID để sắp xếp theo từng người dùng

---

*Hướng dẫn này là một phần của loạt bài hướng dẫn AWS SQS.*