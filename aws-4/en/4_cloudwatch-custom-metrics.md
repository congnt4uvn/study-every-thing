# AWS CloudWatch – Custom Metrics (PutMetricData)

## What “custom metrics” are
CloudWatch provides many **built-in metrics** from AWS services (EC2, ELB, RDS, etc.). When you need metrics that AWS doesn’t publish by default (for example **RAM usage**, **disk usage**, or **application KPIs** like *number of logged-in users*), you can publish **custom metrics** to CloudWatch.

You publish them using the CloudWatch API/CLI call **`PutMetricData`**.

---

## Key concepts you need to know

### 1) Namespace
- Custom metrics live under a **namespace** you choose (e.g., `MyNamespace`).
- AWS service metrics use AWS-managed namespaces; **custom namespaces are user-defined**.

### 2) Metric name, value, and unit
- A metric has a **metric name** (e.g., `MemoryUsage`) and one or more **data points** (values).
- Provide a **unit** when possible (e.g., `Percent`, `Bytes`, `Count`).

### 3) Dimensions (attributes)
- You can add **dimensions** (key/value pairs) to slice and filter the metric.
- Examples:
  - `InstanceId=i-1234567890abcdef0`
  - `InstanceType=t3.micro`
  - `Environment=prod`
- Dimensions are entirely up to you—choose names that match how you’ll query/graph/alert.

### 4) Resolution (standard vs high-resolution)
CloudWatch custom metrics can be published at:
- **Standard resolution**: 1-minute granularity (**60s**)
- **High-resolution**: publish every **1s, 5s, 10s, or 30s**

In `PutMetricData`, this is controlled by `--storage-resolution` (1 for high-resolution, 60 for standard).

---

## Exam / gotcha: timestamps in the past or future
CloudWatch accepts custom metric timestamps:
- Up to **2 weeks in the past**
- Up to **2 hours in the future**

This means **time synchronization matters** (e.g., EC2 instances should have correct time/NTP) so your metrics line up with real time and dashboards/alarms behave as expected.

---

## CLI example (AWS CloudShell or any machine with AWS CLI)
Publish a single data point:

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

High-resolution example (1-second):

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

Timestamp example (explicit timestamp):

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

## How it shows up in the console
After publishing:
- CloudWatch → **Metrics** → **All metrics**
- You’ll see your **custom namespace** (e.g., `MyNamespace`)
- Then your metric appears grouped by the **dimensions** you used

---

## Practical notes
- A script on an EC2 instance can publish metrics on a schedule (cron/systemd/agent).
- The **CloudWatch Unified Agent** ultimately uses `PutMetricData`-style publishing to send metrics to CloudWatch.

---

## Quick checklist
- Pick a clear **namespace** and **metric name**
- Use meaningful **dimensions** (but don’t explode cardinality)
- Choose **standard vs high-resolution** intentionally
- Ensure instance/system **time is correct**
