# AWS Study Notes — CloudWatch Alarms (EC2 CPU → Terminate)

## What this lab demonstrates
You can use **Amazon CloudWatch Alarms** to watch a metric (for example **EC2 CPUUtilization**) and trigger an **action** (for example **terminate an EC2 instance**) when the metric breaches a threshold for a configured duration.

This is a common pattern:
- Observe: CloudWatch **Metrics**
- Decide: CloudWatch **Alarm** evaluation rules
- Act: **Alarm actions** (SNS notifications, Auto Scaling, EC2 actions, Systems Manager, etc.)

## Concepts to know
### Metric & dimensions
- **Namespace**: where the metric lives (for EC2, this is typically `AWS/EC2`).
- **Metric name**: e.g. `CPUUtilization`.
- **Dimensions**: key/value selectors that scope the metric, e.g. `InstanceId=i-...`.

### Statistic & period
- **Statistic**: how to aggregate raw datapoints (Average/Sum/Maximum/Minimum, etc.).
- **Period**: the length of each datapoint used for evaluation (commonly 1 min, 5 min).
  - If you don’t enable **detailed monitoring** on EC2, many metrics are reported at **5-minute** granularity.

### Evaluation logic
Alarm evaluation is based on:
- **Threshold type**: Static threshold vs Anomaly Detection.
- **Comparison operator**: `GreaterThanThreshold`, etc.
- **Datapoints to alarm** and **evaluation periods**.
  - Example: “**3 out of 3** periods > 95%” with a 5-minute period means roughly **15 minutes** of sustained high CPU.

### Alarm states
- **OK**: within threshold.
- **ALARM**: breaching conditions met.
- **INSUFFICIENT_DATA**: not enough datapoints yet (common for new instances/metrics).

## Step-by-step (Console)
1. Launch a small EC2 instance (e.g. `t2.micro`) for testing.
2. Open **CloudWatch → Alarms → Create alarm**.
3. **Select metric**:
   - Choose **EC2 metrics**.
   - Use **Per-Instance Metrics**.
   - Search by your `InstanceId`.
   - Select **CPUUtilization**.
4. Configure the metric settings:
   - Statistic: commonly **Average**.
   - Period: **5 minutes** (matches basic monitoring frequency).
5. Configure conditions:
   - Static threshold.
   - Example: `CPUUtilization > 95`.
   - Example evaluation: **3 out of 3** datapoints.
6. Configure actions:
   - On **ALARM** state, choose an **EC2 action → Terminate instance**.
7. Name the alarm (example): `EC2 on high CPU`.
8. Create the alarm.

Notes:
- Right after creation, the alarm may show **INSUFFICIENT_DATA** until CloudWatch receives enough datapoints.

## Testing without waiting (CLI)
If you don’t want to actually drive CPU to 95%+ for 15 minutes, you can set the alarm state manually for testing.

Command pattern:
```bash
aws cloudwatch set-alarm-state \
  --alarm-name "EC2 on high CPU" \
  --state-value ALARM \
  --state-reason "testing"
```

What to expect:
- The alarm state changes to **ALARM**.
- The configured action executes (in this lab: it terminates the EC2 instance).
- You can verify in:
  - CloudWatch Alarm **History**
  - EC2 instance state transitions (shutting down → terminated)

## Safety notes (important)
- **Termination is destructive.** Use this only on disposable instances.
- Use IAM least privilege; terminating instances typically requires `ec2:TerminateInstances`.
- Consider safer actions first (notify, auto-recover, restart, scale out) before termination in production.

## Quick checklist / troubleshooting
- Don’t see metrics yet?
  - Wait a few minutes after launch; metrics can take time to appear.
- Alarm stuck in `INSUFFICIENT_DATA`?
  - Wait for enough datapoints (depends on period and evaluation periods).
- Wrong period?
  - Basic monitoring commonly uses 5-minute data; detailed monitoring supports 1-minute.
- Action didn’t run?
  - Check alarm **History**, ensure the alarm actually entered **ALARM** and the action is configured.

## Practice questions
1. If period is 1 minute and you set “5 out of 5”, how long must CPU be above the threshold?
2. What’s the operational difference between choosing `Maximum` vs `Average` for CPUUtilization?
3. When would you choose Anomaly Detection over a static threshold?

## Mini-lab extensions (optional)
- Replace termination with:
  - SNS notification
  - Auto Scaling policy
  - SSM Automation action
- Create a second alarm for `StatusCheckFailed` and compare behavior.
