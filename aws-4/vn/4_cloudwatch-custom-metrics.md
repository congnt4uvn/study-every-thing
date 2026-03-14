# AWS CloudWatch – Custom Metrics (PutMetricData)

## Custom Metrics là gì?
CloudWatch có sẵn nhiều **metric mặc định** từ các dịch vụ AWS (EC2, ELB, RDS, …). Khi bạn cần các metric mà AWS không cung cấp sẵn (ví dụ **RAM usage**, **disk usage**, hoặc KPI của ứng dụng như *số user đang đăng nhập*), bạn có thể tự **đẩy custom metrics** lên CloudWatch.

Cách đẩy metric là dùng API/CLI **`PutMetricData`**.

---

## Các khái niệm quan trọng

### 1) Namespace
- Custom metrics nằm trong **namespace** do bạn tự đặt (ví dụ `MyNamespace`).
- Metrics của dịch vụ AWS dùng namespace do AWS quản lý; **custom namespace là do bạn tạo**.

### 2) Metric name, value, unit
- Mỗi metric có **tên metric** (ví dụ `MemoryUsage`) và các **data point** (giá trị).
- Nên khai báo **unit** khi phù hợp (ví dụ `Percent`, `Bytes`, `Count`).

### 3) Dimensions (thuộc tính)
- Bạn có thể thêm **dimensions** (cặp key/value) để phân tách và lọc metric.
- Ví dụ:
  - `InstanceId=i-1234567890abcdef0`
  - `InstanceType=t3.micro`
  - `Environment=prod`
- Tên dimension là do bạn tự quyết định — hãy đặt theo cách bạn sẽ query/vẽ chart/đặt alarm.

### 4) Độ phân giải (standard vs high-resolution)
Custom metrics có thể publish theo:
- **Standard resolution**: mỗi **1 phút (60s)**
- **High-resolution**: mỗi **1s, 5s, 10s, hoặc 30s**

Trong `PutMetricData`, điều này được điều khiển bởi `--storage-resolution` (1 cho high-resolution, 60 cho standard).

---

## Điểm dễ ra đề / lưu ý: timestamp quá khứ hoặc tương lai
CloudWatch chấp nhận timestamp của custom metrics:
- Tối đa **2 tuần trong quá khứ**
- Tối đa **2 giờ trong tương lai**

Vì vậy **đồng bộ thời gian rất quan trọng** (ví dụ EC2 cần time/NTP đúng) để metric hiển thị đúng thời điểm và dashboard/alarm hoạt động chuẩn.

---

## Ví dụ AWS CLI (CloudShell hoặc máy có AWS CLI)
Đẩy một data point:

```bash
aws cloudwatch put-metric-data \
  --namespace "MyNamespace" \
  --metric-data '[(
    MetricName="Buffers",
    Dimensions=[{Name="InstanceId",Value="i-1234567890abcdef0"},{Name="InstanceType",Value="t3.micro"}],
    Unit="Bytes",
    Value=123456,
    StorageResolution=60
  )]'
```

Ví dụ high-resolution (1 giây):

```bash
aws cloudwatch put-metric-data \
  --namespace "MyNamespace" \
  --metric-data '[(
    MetricName="RequestLatency",
    Unit="Milliseconds",
    Value=42,
    StorageResolution=1
  )]'
```

Ví dụ chỉ định timestamp:

```bash
aws cloudwatch put-metric-data \
  --namespace "MyNamespace" \
  --metric-data '[(
    MetricName="MemoryUsage",
    Unit="Percent",
    Value=73.2,
    Timestamp="2026-03-13T10:00:00Z",
    StorageResolution=60
  )]'
```

---

## Metric sẽ xuất hiện trên Console như thế nào?
Sau khi publish:
- CloudWatch → **Metrics** → **All metrics**
- Bạn sẽ thấy **custom namespace** (ví dụ `MyNamespace`)
- Metric được nhóm theo các **dimensions** bạn đã gửi

---

## Ghi chú thực tế
- Bạn có thể chạy script trên EC2 theo lịch (cron/systemd/agent) để đẩy metric định kỳ.
- **CloudWatch Unified Agent** về bản chất cũng dùng cơ chế giống `PutMetricData` để gửi metric lên CloudWatch.

---

## Checklist nhanh
- Chọn **namespace** và **metric name** rõ ràng
- Dùng **dimensions** có ý nghĩa (tránh quá nhiều giá trị khác nhau gây “bùng nổ” dimension)
- Quyết định **standard vs high-resolution** phù hợp nhu cầu
- Đảm bảo **thời gian hệ thống** chính xác
