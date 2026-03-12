# Hướng Dẫn Amazon SQS FIFO Queues

## Giới Thiệu

Amazon SQS FIFO (First-In-First-Out) queues đảm bảo thứ tự của thông điệp và xử lý chính xác một lần, khiến chúng trở nên lý tưởng cho các ứng dụng mà trình tự của các hoạt động và sự kiện là rất quan trọng.

## FIFO Là Gì?

**FIFO** là viết tắt của **First In, First Out** (Vào trước, Ra trước), đề cập đến thứ tự của các thông điệp trong hàng đợi. Khi một producer gửi các thông điệp theo một thứ tự cụ thể (1, 2, 3, 4), các consumer lấy thông điệp từ SQS FIFO queue sẽ nhận và xử lý các thông điệp này theo đúng thứ tự đó.

### Sự Khác Biệt Chính So Với Standard SQS Queue

- **FIFO Queue**: Các thông điệp được đảm bảo nhận theo đúng thứ tự chúng được gửi
- **Standard SQS Queue**: Các thông điệp có thể nhận không theo thứ tự

## Tính Năng Của FIFO Queue

### 1. Đảm Bảo Thứ Tự

Các thông điệp được xử lý theo thứ tự bởi consumer, với thứ tự được đảm bảo ở mức **message group ID**. Bạn phải cung cấp message group ID khi gửi thông điệp đến FIFO queue, đảm bảo tất cả các thông điệp trong nhóm đó được xử lý tuần tự.

### 2. Khả Năng Gửi Chính Xác Một Lần

FIFO queue hỗ trợ **exactly-once send** (gửi chính xác một lần), nghĩa là các bản sao có thể được tự động loại bỏ ở cấp độ hàng đợi.

**Cách hoạt động:**
- Cung cấp một **deduplication ID** với mỗi thông điệp
- Nếu cùng một deduplication ID xuất hiện hai lần trong **khoảng thời gian 5 phút**, thông điệp trùng lặp sẽ tự động bị loại bỏ
- Điều này đảm bảo không có xử lý trùng lặp trong khoảng thời gian khử trùng

### 3. Giới Hạn Throughput

Do đảm bảo thứ tự, FIFO queue có các giới hạn về throughput:
- **300 thông điệp mỗi giây** không có batching
- **3,000 thông điệp mỗi giây** với batching

## Hướng Dẫn Thực Hành: Tạo và Sử Dụng FIFO Queue

### Bước 1: Tạo FIFO Queue

1. Điều hướng đến Amazon SQS console
2. Nhấp **Create queue**
3. Chọn **FIFO** làm loại queue
4. Đặt tên queue với hậu tố `.fifo` (ví dụ: `DemoQueue.fifo`)
   - **Quan trọng**: Tên phải kết thúc bằng `.fifo` nếu không queue không thể được tạo

### Bước 2: Cấu Hình Queue

Cấu hình tương tự như standard queue, với một cài đặt bổ sung:

- **Content-based deduplication**: Cho phép khử trùng tự động nếu cùng một nội dung thông điệp được gửi hai lần trong khoảng thời gian 5 phút
- **Access policy**: Cấu hình theo nhu cầu (có thể sử dụng mặc định)
- **Encryption**: Cấu hình theo nhu cầu (có thể sử dụng mặc định)

### Bước 3: Gửi Thông Điệp

Khi gửi thông điệp đến FIFO queue, bạn phải cung cấp:

1. **Message body**: Nội dung thông điệp thực tế
2. **Message group ID**: Nhóm các thông điệp để xử lý theo thứ tự
3. **Deduplication ID**: Ngăn chặn thông điệp trùng lặp trong vòng 5 phút

**Ví dụ:**
```
Thông điệp 1:
- Body: "Hello World 1"
- Message Group ID: "demo"
- Deduplication ID: "ID1"

Thông điệp 2:
- Body: "Hello World 2"
- Message Group ID: "demo"
- Deduplication ID: "ID2"

Thông điệp 3:
- Body: "Hello World 3"
- Message Group ID: "demo"
- Deduplication ID: "ID3"

Thông điệp 4:
- Body: "Hello World 4"
- Message Group ID: "demo"
- Deduplication ID: "ID4"
```

### Bước 4: Nhận Thông Điệp

1. Nhấp **Send and receive messages**
2. Nhấp **Poll for messages**
3. Các thông điệp sẽ được nhận theo đúng thứ tự chúng được gửi:
   - Thông điệp đầu tiên: "Hello World 1"
   - Thông điệp thứ hai: "Hello World 2"
   - Thông điệp thứ ba: "Hello World 3"
   - Thông điệp thứ tư: "Hello World 4"

### Bước 5: Xóa Thông Điệp

Sau khi xử lý, xóa các thông điệp để loại bỏ chúng khỏi hàng đợi.

## Tóm Tắt

Amazon SQS FIFO queues cung cấp:
- ✅ Đảm bảo thứ tự thông điệp
- ✅ Xử lý chính xác một lần với khử trùng
- ✅ Message group ID để nhóm logic
- ⚠️ Throughput giới hạn (300-3,000 msg/giây)
- ⚠️ Phải sử dụng hậu tố `.fifo` trong tên queue

FIFO queue hoàn hảo cho các tình huống mà thứ tự thông điệp quan trọng, chẳng hạn như giao dịch tài chính, xử lý đơn hàng, và trình tự sự kiện.