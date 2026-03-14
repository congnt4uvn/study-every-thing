# AWS X-Ray APIs (Ghi chú ôn thi)

## X-Ray thu thập gì? (ngữ cảnh nhanh)
- **Trace**: cái nhìn end-to-end của **một request** khi đi qua nhiều service.
- **Segment**: tài liệu JSON mô tả công việc của **một service/thành phần**.
- **Subsegment**: phần nhỏ hơn bên trong segment (ví dụ: một downstream call).
- **X-Ray daemon / agent** sẽ buffer rồi gửi segment lên dịch vụ AWS X-Ray.

---

## Phía ghi (daemon -> dịch vụ X-Ray)
Trong đề thi, “ghi” thường là các action **`Put*`**, nhưng vẫn có một số **`Get*`** liên quan đến **sampling** mà daemon bắt buộc phải gọi.

### Managed policy (ý tưởng)
- Thường được nhắc như **X-Ray Write Only / quyền ghi cho daemon**.
- Gán cho **X-Ray daemon** (hoặc SDK/agent) để có thể gửi dữ liệu lên X-Ray.

### Các API/action quan trọng
#### `xray:PutTraceSegments`
- Upload **segment documents** lên AWS X-Ray.
- Đây là quyền cốt lõi để “ghi” dữ liệu trace/segment.

#### `xray:PutTelemetryRecords`
- Upload **telemetry** của daemon (số segment nhận/reject, lỗi kết nối backend, …).
- Hỗ trợ theo dõi tình trạng/metrics của daemon.

### Vì sao “quyền ghi” lại có `Get*`?
X-Ray dùng **sampling rules** để quyết định request nào được ghi.
- Khi bạn đổi sampling rules trên console, daemon/agent cần **tải rule mới** về để biết lúc nào nên gửi dữ liệu.

#### `xray:GetSamplingRules`
- Lấy danh sách sampling rules để daemon biết nên sample như thế nào.

#### `xray:GetSamplingTargets`
- Hỗ trợ sampling nâng cao: lấy “sampling targets” từ X-Ray.

#### `xray:GetSamplingStatisticSummaries`
- Hỗ trợ sampling nâng cao: lấy summary/thống kê liên quan đến sampling.

### Mẹo làm bài
- Nếu câu hỏi nói về **daemon gửi segment**, nghĩ ngay: **`PutTraceSegments`**.
- Nếu câu hỏi nói về **metrics/tình trạng daemon**, nghĩ: **`PutTelemetryRecords`**.
- Nếu câu hỏi nói về **sampling**, nghĩ: **`GetSampling*`**.

---

## Phía đọc (console / troubleshooting / phân tích)
Quyền đọc chủ yếu là **`Get*`** và **`BatchGet*`**.

### Managed policy (ý tưởng)
- Thường được nhắc như **X-Ray Read Only access**.
- Dùng cho user/role cần xem dữ liệu X-Ray (console, công cụ debug/troubleshoot).

### Các API/action quan trọng
#### `xray:GetServiceGraph`
- Lấy **service graph tổng** (bản đồ service) hiển thị trên console.

#### `xray:GetTraceSummaries`
- Lấy danh sách trace ID + metadata (bao gồm annotations) trong một khoảng thời gian.
- Luồng thường gặp: **lấy summaries trước**, rồi mới lấy trace đầy đủ.

#### `xray:BatchGetTraces`
- Lấy **chi tiết trace đầy đủ** theo danh sách trace ID.
- Mỗi trace là tập các segment documents bắt nguồn từ một request.

#### `xray:GetTraceGraph`
- Lấy **service graph** cho một hoặc nhiều trace ID cụ thể.

### Workflow đọc thường gặp (rất hay ra)
1. `GetTraceSummaries` (tìm trace ID đáng chú ý)
2. `BatchGetTraces` (kéo trace đầy đủ)
3. Tuỳ chọn: `GetTraceGraph` / `GetServiceGraph` (xem quan hệ/đồ thị)

---

## Bảng nhận diện nhanh khi đi thi
| Tình huống | API action(s) phù hợp |
|---|---|
| Daemon/agent upload segment | `PutTraceSegments` |
| Daemon upload telemetry về segment/lỗi | `PutTelemetryRecords` |
| Daemon cần cập nhật sampling rules | `GetSamplingRules`, `GetSamplingTargets`, `GetSamplingStatisticSummaries` |
| Console hiển thị service map tổng | `GetServiceGraph` |
| Tìm trace ID theo thời gian | `GetTraceSummaries` |
| Lấy trace đầy đủ theo IDs | `BatchGetTraces` |
| Graph cho trace cụ thể | `GetTraceGraph` |
