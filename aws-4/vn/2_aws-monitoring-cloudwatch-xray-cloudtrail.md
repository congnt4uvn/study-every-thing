# Giám sát, xử lý sự cố & kiểm toán trên AWS (CloudWatch, X-Ray, CloudTrail)

Tài liệu này được viết dựa trên nội dung trong `file.txt`: người dùng không quan tâm bạn deploy bằng IaC/Beanstalk… họ chỉ quan tâm **ứng dụng có chạy ổn không**. Vì vậy phải giám sát **độ trễ, sự cố, xu hướng** và cố gắng phát hiện vấn đề **trước khi** người dùng than phiền.

## Vì sao monitoring quan trọng

- **Độ trễ (latency)**: có tăng theo thời gian không? tăng ở đâu và vì sao?
- **Sẵn sàng (availability)/outage**: phát hiện nhanh và khôi phục nhanh.
- **Chủ động**: không muốn biết lỗi từ khách hàng; muốn cảnh báo sớm.
- **Hiệu năng và chi phí**: theo dõi usage và chi tiêu.
- **Xu hướng & cải tiến**: học từ pattern scaling và lỗi lặp lại.

## 3 dịch vụ: dùng khi nào

### CloudWatch = metrics, logs, events, alarms
CloudWatch giúp bạn quan sát *cái gì đang xảy ra*.

- **Metrics**: số liệu theo thời gian (CPU, số request, error rate, latency).
- **Logs**: thu thập, tìm kiếm và phân tích log.
- **Events / EventBridge**: bắt sự kiện thay đổi trong AWS để kích hoạt hành động.
- **Alarms**: phản ứng theo thời gian thực với metrics/events/logs (gửi SNS, auto scaling, automation…).

Use case phổ biến:
- Dashboard theo dõi **latency / error rate / throughput**
- Alarm cho **5xx tăng**, **p95 latency**, **queue depth**, **Lambda errors**, **DLQ messages**
- Tập trung log để điều tra sự cố

### X-Ray = distributed tracing (độ trễ + lỗi xuyên suốt nhiều service)
X-Ray giúp bạn hiểu *vì sao đang xảy ra*, đặc biệt với kiến trúc microservices.

- Hiển thị **trace end-to-end** và **service map**
- Tách độ trễ theo từng chặng (API → Lambda → DynamoDB → S3…)
- Làm nổi bật **errors**, **faults**, **throttles**

Dùng X-Ray khi:
- Có nhiều service gọi lẫn nhau
- Cần tìm **root cause** về latency (dependency nào chậm?)
- Muốn thấy lỗi phát sinh ở đâu theo luồng request

### CloudTrail = audit API (ai làm gì, lúc nào, từ đâu)
CloudTrail phục vụ governance/security: ghi lại **API calls** và thay đổi cấu hình.

- Theo dõi hành động của user/role/service (CreateBucket, PutPolicy, TerminateInstances…)
- Trả lời các câu hỏi:
  - Ai đã đổi security group?
  - Role nào đã xóa resource?
  - Policy bị sửa lúc nào?

Dùng CloudTrail khi:
- Cần nhật ký kiểm toán cho compliance
- Điều tra hoạt động bất thường hoặc cấu hình bị thay đổi ngoài ý muốn

## Cách kết hợp trong thực tế (mô hình tư duy)

- **CloudWatch**: phát hiện triệu chứng (latency cao, error rate tăng, CPU/queue bất thường).
- **X-Ray**: lần theo request để tìm service/dependency gây chậm hoặc lỗi.
- **CloudTrail**: kiểm tra có ai thay đổi cấu hình/IAM/SG… gây ra sự cố không.

## Checklist ôn tập nhanh

### CloudWatch
- Phân biệt: metrics vs logs vs alarms
- Biết cách:
  - Tạo **alarm** cho metric (VD: ALB 5xx, Lambda errors)
  - Tạo **log metric filter** (biến pattern log thành metric)
  - Tạo **dashboard**

### X-Ray
- Nắm khái niệm: trace, segment/subsegment, service map
- Biết khi nào dùng distributed tracing (microservices)
- Tập suy luận: dependency nào tạo ra latency

### CloudTrail
- Nắm khái niệm mức cao: event history vs trail; management vs data events
- Nhớ mục đích chính: **audit API calls và thay đổi tài nguyên**

## Tự kiểm tra

1. Ứng dụng bị chậm; cần biết call nào trong chuỗi đang chậm nhất → dùng dịch vụ nào?  
2. Cần cảnh báo khi error rate tăng đột biến → dùng dịch vụ nào và tính năng nào?  
3. Outage do security group bị sửa; cần biết ai sửa → dùng dịch vụ nào?  
4. Trong một incident, CloudWatch + X-Ray + CloudTrail bổ trợ nhau như thế nào?
