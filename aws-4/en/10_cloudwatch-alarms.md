# AWS CloudWatch Alarms — Study Notes (EN)

## What a CloudWatch Alarm is
- A CloudWatch Alarm watches a **metric** and can **trigger a notification/action** when the metric crosses a threshold.
- Alarms can be configured with different evaluation options (e.g., statistic choices such as maximum, and other settings depending on the metric).

## Alarm states
CloudWatch Alarms have 3 states:
- **OK**: The alarm is not triggered.
- **INSUFFICIENT_DATA**: Not enough data to determine the state.
- **ALARM**: Threshold is breached; a notification/action is triggered.

## Period (evaluation window)
- The **period** is how long the alarm evaluates the metric for.
- It can be short or long depending on your needs.
- It can also apply to **high-resolution custom metrics**, e.g. **10s**, **30s**, or multiples of **60s**.

## Alarm targets (what alarms can do)
CloudWatch Alarms commonly target:
1) **EC2 instance actions**
   - Stop, terminate, reboot, or recover an instance.
2) **Auto Scaling actions**
   - Scale out / scale in.
3) **Notifications via SNS**
   - Send to **Amazon SNS**, and from SNS you can hook to **AWS Lambda** to execute custom logic.

## Composite Alarms
### Why Composite Alarms
- A standard CloudWatch Alarm is typically on a **single metric**.
- If you want logic across **multiple metrics**, use **Composite Alarms**.

### How they work
- A **Composite Alarm** monitors the **states of other alarms**.
- You can combine alarms with **AND / OR** logic.

### Benefit: reduce alarm noise
- Helps reduce noisy alerts by expressing more specific conditions.
- Example idea: alert only when certain combinations happen, instead of every single metric spike.

### Example pattern
- Alarm A: monitors **EC2 CPU**.
- Alarm B: monitors **EC2 IOPS**.
- Composite Alarm: `AlarmA AND AlarmB` (or `AlarmA OR AlarmB`) depending on your desired condition.
- When the composite condition becomes true, the Composite Alarm can trigger an action (e.g., SNS notification).

## EC2 instance recovery via alarms
### Status checks
- **Instance status check**: checks the EC2 virtual machine.
- **System status check**: checks the underlying host/hardware layer.
- **Attached EBS status check**: checks health of attached EBS volumes.

### Recovery behavior
- You can create a CloudWatch Alarm on these checks.
- If breached, you can trigger **EC2 instance recovery** (move instance to another host).
- After recovery, the instance keeps:
  - same **private IP**, **public IP**, and **Elastic IP**
  - same **metadata**
  - same **placement group**
- You can also notify an **SNS topic** to alert you that recovery happened.

## Alarms from CloudWatch Logs metric filters
- You can create an alarm on top of a **CloudWatch Logs metric filter**.
- Common pattern: count occurrences of a word like **"error"** in logs.
- When occurrences exceed a threshold, trigger an alarm and send an SNS notification.

## Testing alarms & notifications
- You can test by using the CLI command **SetAlarmState** (commonly referred to as "set alarm state") to force an alarm state for testing, even if the metric didn’t actually breach the threshold.

## Quick self-check questions
- What are the 3 CloudWatch Alarm states?
- What does the alarm **period** control?
- Name 3 target types/actions an alarm can trigger.
- When would you use a **Composite Alarm** instead of a normal alarm?
- Which EC2 checks (instance/system/EBS) map to which layer of failure?
