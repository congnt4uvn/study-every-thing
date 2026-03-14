# Amazon EventBridge — Ghi chú học tập (VI)

## 1) EventBridge là gì? (mô hình tư duy)
Amazon EventBridge là dịch vụ **định tuyến sự kiện (event routing)**.

- **Nguồn phát (event source)** tạo/sinh sự kiện
- **Event bus** nhận sự kiện
- **Rules / Pipes / Schedules** dùng để lọc/tạo/đẩy sự kiện
- **Targets** nhận kết quả (SNS, SQS, Lambda, Step Functions, ...)

Theo nội dung trong `file.txt`, các mảng chính cần nắm:
- **Rule + event pattern** (phản ứng theo sự kiện)
- **Schedules / EventBridge Scheduler** (chạy theo thời gian)
- **Pipes** (source → lọc/enrichment → target)
- **Schema registry** (xem cấu trúc/schema của event)
- **Event buses** (default/custom) + **archive & replay**
- **Partner event sources** và **API destinations**

---

## 2) EventBridge Rule (event pattern)
**Rule** lắng nghe trên event bus và dùng **event pattern** để lọc sự kiện.

### Ví dụ trong `file.txt`: cảnh báo khi EC2 tắt hoặc bị terminate
Dùng loại event phổ biến:
- **EC2 Instance State-change Notification**

Lọc theo trường:
- `detail.state` bằng **"shutting-down"** hoặc **"terminated"**

Ví dụ event pattern:

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["shutting-down", "terminated"]
  }
}
```

### Target trong `file.txt`: SNS Topic
Để nhận cảnh báo:
- Chọn **SNS Topic** làm target (ví dụ một topic demo)
- EventBridge cần quyền publish vào SNS nên sẽ có **IAM role** được tạo/dùng

### Cần kiểm tra khi thực hành
- Tạo event bằng cách stop/terminate một EC2 instance test
- Xác nhận SNS subscription nhận được thông báo

---

## 3) Schedule (kích hoạt theo thời gian)
EventBridge cũng có thể chạy tác vụ theo lịch.

Theo `file.txt`:
- Tạo schedule, ví dụ **InvokeLambdaEveryHour**
- Có thể **one-time** hoặc **recurring**
- Chọn **cron-based** hoặc **rate**
- Ví dụ: **rate = 1 giờ**
- Tùy chọn: **không dùng flexible time window**

Target có thể là:
- Chạy **ECS task**
- Ghi record vào **Kinesis Data Firehose**
- Gọi **Lambda function**

Gợi ý học: phân biệt khi nào dùng schedule (không cần event nguồn) và khi nào dùng rule (phản ứng theo event).

---

## 4) Event bus
Theo `file.txt`:

- **Default event bus**: nhận các event do AWS sinh ra
- **Custom event bus**: ứng dụng của bạn có thể tự publish event để làm workflow riêng

Ý chính:
- Rule/pipes thường gắn với một event bus cụ thể
- Custom bus hay dùng trong kiến trúc event-driven

---

## 5) Archive và replay
Theo `file.txt`:
- Có thể **archive** event phát sinh trên bus
- Có thể **replay** event trong quá khứ từ archive để xử lý lại

Use case:
- Debug / điều tra sự cố
- Xử lý lại sau khi fix bug
- Backfill dữ liệu cho hệ thống downstream

---

## 6) Partner event sources
Theo `file.txt`:
- Có thể nhận event từ đối tác bên thứ ba (ví dụ được nhắc: Auth0)

Sau đó bạn route event sang Lambda/target khác để xử lý, ví dụ sau khi user đăng nhập.

---

## 7) API destinations
Theo `file.txt`:
- Có thể gửi event ra **HTTP endpoint bên ngoài**

Hữu ích khi tích hợp AWS với hệ thống không nằm trong AWS hoặc hạ tầng riêng.

---

## 8) Schemas / Schema Registry
Theo `file.txt`:
- Xem schema của các AWS events
- Tạo registry riêng cho event custom

Tại sao quan trọng:
- Biết event có field nào để filter (ví dụ `detail.state`)
- Giúp producer/consumer thống nhất format

---

## 9) Checklist nhanh (thi + làm thực tế)
- Mô tả được luồng: **source → bus → rule/pattern → target**
- Biết filter theo field (ví dụ state của EC2)
- Biết chọn **Schedule** hay **Rule**
- Hiểu **default bus** vs **custom bus**
- Hiểu mục đích của **archive/replay**
- Nắm khái niệm **partner sources** và **API destinations**

---

## 10) Mini-lab (khuyến nghị)
1. Tạo SNS topic + email subscription.
2. Tạo EventBridge rule với EC2 state-change pattern (shutting-down/terminated).
3. Terminate một EC2 instance test.
4. Xác nhận nhận được thông báo qua SNS.
5. Tạo schedule gọi Lambda mỗi giờ (hoặc mỗi 5 phút để test).

