# AWS WebSocket APIs với API Gateway

## WebSocket là gì?

WebSocket là giao thức **truyền thông tương tác hai chiều** giữa trình duyệt của người dùng và máy chủ. Khác với HTTP truyền thống, máy chủ có thể chủ động đẩy thông tin đến client mà không cần client gửi yêu cầu.

### Đặc điểm chính
- **Truyền thông hai chiều**: Máy chủ có thể chủ động đẩy dữ liệu đến client
- **Có trạng thái (Stateful)**: Duy trì kết nối liên tục
- **Thời gian thực**: Cho phép truyền dữ liệu tức thời

## Các trường hợp sử dụng phổ biến

WebSocket APIs thường được sử dụng trong các ứng dụng thời gian thực:
- 💬 **Ứng dụng chat**
- 🤝 **Nền tảng cộng tác**
- 🎮 **Game nhiều người chơi**
- 📈 **Nền tảng giao dịch tài chính**

## Kiến trúc WebSocket API

### Vòng đời kết nối

1. **Thiết lập kết nối**
   - Client kết nối đến WebSocket API trên API Gateway
   - Thiết lập một **kết nối liên tục** (không phải nhiều kết nối)
   - Lambda function `onConnect` được gọi
   - Connection ID có thể được lưu trữ trong DynamoDB để theo dõi

2. **Gửi tin nhắn**
   - Client gửi tin nhắn qua kết nối liên tục
   - Các tin nhắn được gọi là **frames** (khung)
   - Lambda function `sendMessage` được gọi
   - Connection ID giữ nguyên trong suốt quá trình

3. **Ngắt kết nối**
   - Client gửi tín hiệu ngắt kết nối
   - Lambda function `onDisconnect` được gọi
   - Kết nối bị chấm dứt

### Các tùy chọn tích hợp Backend

API Gateway WebSocket có thể tích hợp với:
- ⚡ Lambda functions
- 🗄️ DynamoDB tables
- 🌐 HTTP endpoints
- Các dịch vụ AWS khác

## Cấu trúc WebSocket URL

```
wss://{unique-id}.execute-api.{region}.amazonaws.com/{stage-name}
```

- `wss://` - Giao thức WebSocket được mã hóa
- ID duy nhất được gán cho API của bạn
- Triển khai trên vùng AWS cụ thể
- Tên stage (dev, prod, v.v.)

## Cách WebSocket hoạt động với API Gateway

### Truyền thông từ Client đến Server

1. Client kết nối bằng WebSocket URL
2. Kết nối liên tục được thiết lập
3. Connection ID được gán và lưu trữ
4. Client gửi frames (tin nhắn) qua cùng một kết nối
5. Lambda functions xử lý tin nhắn
6. Connection ID không đổi trong suốt phiên làm việc

### Truyền thông từ Server đến Client (Callback)

Để gửi dữ liệu về client mà không cần yêu cầu:

**Định dạng Connection URL Callback:**
```
wss://{api-url}/@connections/{connectionId}
```

- Lambda function thực hiện yêu cầu **HTTP POST**
- Phải được ký bằng **IAM SigV4**
- Nhắm đến Connection ID cụ thể
- Đẩy dữ liệu trực tiếp đến client

## Khái niệm quan trọng cho kỳ thi

- ✅ WebSocket duy trì **kết nối liên tục** (không phải nhiều kết nối)
- ✅ Tin nhắn gửi qua WebSocket được gọi là **frames** (khung)
- ✅ **Connection ID** không đổi trong suốt phiên làm việc
- ✅ Ba Lambda trigger chính: `onConnect`, `sendMessage`, `onDisconnect`
- ✅ Server push yêu cầu **connection URL callback** với IAM SigV4
- ✅ Metadata kết nối thường được lưu trong **DynamoDB**

## Mẫu kiến trúc điển hình

```
Client (Trình duyệt)
    ↕️ (kết nối liên tục)
API Gateway (WebSocket API)
    ↕️
Lambda Functions (onConnect, sendMessage, onDisconnect)
    ↕️
DynamoDB (Connection IDs, Messages, User Metadata)
```

## Những điểm chính cần nhớ

1. **WebSocket = Truyền thông hai chiều** với kết nối liên tục
2. **Ứng dụng thời gian thực** là trường hợp sử dụng chính
3. **Connection ID** là mã định danh chính trong suốt phiên làm việc
4. **Callback URL** cho phép server chủ động gửi thông báo đến client
5. **Ký IAM SigV4** bắt buộc cho tin nhắn do server khởi tạo
