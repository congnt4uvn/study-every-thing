# AWS Step Functions: Activity Task (Ghi chú học tập)

## 1) Activity Task là gì?
Activity Task trong AWS Step Functions cho phép worker bên ngoài chủ động kéo (pull) công việc từ state machine và gửi kết quả về sau khi xử lý xong.

Worker bên ngoài có thể chạy trên:
- EC2
- Lambda
- Ứng dụng mobile hoặc hệ thống on-prem

## 2) Luồng xử lý chính
1. Worker gọi `GetActivityTask` để polling Step Functions.
2. Nếu có việc, Step Functions trả về input và task token.
3. Worker xử lý tác vụ.
4. Worker gửi kết quả bằng:
- `SendTaskSuccess`, hoặc
- `SendTaskFailure`

## 3) Pull model và Push model
### Activity Task = Pull model
- Worker chủ động kéo việc từ Step Functions.
- Mô hình mạng thường đơn giản hơn vì worker chỉ cần kết nối outbound tới Step Functions.

### Callback với Wait for Task Token = Push model
- Step Functions có thể đẩy sự kiện ra ngoài (ví dụ SQS/EventBridge).
- Hệ thống bên ngoài nhận sự kiện rồi callback ngược về Step Functions bằng task token.

## 4) Các tham số thời gian quan trọng
### `TimeoutSeconds`
- Thời gian tối đa một task được ở trạng thái in-progress trước khi bị đánh dấu fail.

### `HeartbeatSeconds`
- Khoảng chờ tối đa giữa các heartbeat.
- Worker nên gọi `SendTaskHeartbeat` định kỳ (ví dụ 5 giây/lần nếu `HeartbeatSeconds` = 10).

## 5) Hành vi với tác vụ chạy lâu
- Nếu `TimeoutSeconds` lớn và heartbeat được gửi liên tục, Activity Task có thể chạy tối đa tới 1 năm.

## 6) So sánh nhanh
| Tiêu chí | Activity Task | Callback Wait for Task Token |
|---|---|---|
| Cách nhận việc | Pull (`GetActivityTask`) | Push event + callback |
| Vai trò worker ngoài | Polling và xử lý | Nhận event rồi callback |
| Mô hình mạng | Thường đơn giản hơn | Thường nhiều thành phần tích hợp hơn |
| API hoàn tất | `SendTaskSuccess` / `SendTaskFailure` | `SendTaskSuccess` / `SendTaskFailure` |

## 7) Mẹo ghi nhớ
- Activity Task = worker bên ngoài polling Step Functions.
- Callback pattern = Step Functions phát event, sau đó chờ callback có token.
- Heartbeat giúp task sống lâu; timeout là giới hạn cứng.
