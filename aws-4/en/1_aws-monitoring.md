# AWS Monitoring Study Notes (Logs, Metrics, Tracing, Auditing)

These notes are based on the ideas in `file.txt`: when an app is “running in the cloud,” you still need monitoring so you can quickly answer **what happened** (especially during an outage).

## Why monitoring matters
- Helps you detect incidents early and reduce time-to-recovery.
- Gives visibility into **what the system is doing** (behavior) and **who changed what** (audit trail).
- Turns “it’s down” at 2:00 a.m. into actionable signals and evidence.

## Four pillars mentioned in the source
### 1) Logs
**What:** Time-ordered records of events (application logs, system logs, access logs).

**Use for:**
- Debugging errors and unexpected behavior
- Root cause analysis after an incident
- Security investigations (when combined with audit logs)

**Typical AWS service:** Amazon **CloudWatch Logs**

### 2) Metrics
**What:** Numeric time series (CPU, memory, latency, error rate, queue depth).

**Use for:**
- Health monitoring and alerting
- Capacity planning
- Detecting performance regressions

**Typical AWS service:** Amazon **CloudWatch Metrics** (+ **Alarms**)

### 3) Tracing
**What:** End-to-end request flow across services (where time is spent, which dependency failed).

**Use for:**
- Microservices / distributed systems debugging
- Identifying slow dependencies or bottlenecks

**Typical AWS service:** AWS **X-Ray**

### 4) Auditing
**What:** Records of actions taken in your AWS account (API calls, console actions), answering “who did what, when, from where.”

**Use for:**
- Compliance and governance
- Security incident response
- Change tracking (explaining outages caused by configuration changes)

**Typical AWS service:** AWS **CloudTrail**

## Practical checklist (minimal, high-value)
- Enable centralized logging (send app logs to CloudWatch Logs).
- Define key metrics for your app (latency, 4xx/5xx rate, saturation signals).
- Create CloudWatch alarms on those metrics and route notifications (often via Amazon SNS).
- Enable tracing for critical services/paths (X-Ray) and propagate trace IDs.
- Enable CloudTrail (ideally org-wide) to capture API activity.

## Common “2:00 a.m.” outage questions you should be able to answer
- Did error rate or latency spike? (metrics)
- What error messages appeared around the time of the incident? (logs)
- Which downstream call slowed/faulted? (tracing)
- Was there a deployment/config/IAM change shortly before the issue? (auditing)

## Quick self-test
1) Which pillar answers “who changed what in AWS?”
2) Which pillar best helps find a slow dependency across microservices?
3) Give three example metrics you would alarm on for a web API.
