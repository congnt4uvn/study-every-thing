# AWS Monitoring, Troubleshooting & Auditing (CloudWatch, X-Ray, CloudTrail)

This note is based on the ideas in `file.txt`: users only care your app works, so you must **monitor latency, outages, and trends**—and ideally detect issues **before** users do.

## Why monitoring matters

Your deployment method (IaC, Beantalk, etc.) is invisible to customers. What matters:

- **Latency**: does response time increase? where and why?
- **Availability/outages**: can you detect and recover quickly?
- **Proactive detection**: alert *before* customers complain.
- **Performance and cost**: understand utilization and spending trends.
- **Trends & learning**: spot scaling patterns and recurring failures.

## The 3 services: when to use which

### CloudWatch = metrics, logs, events, alarms
CloudWatch helps you observe *what is happening*.

- **Metrics**: time-series numbers (CPU, request count, error rate, latency).
- **Logs**: collect and search application/system logs.
- **Events / EventBridge**: react to changes (instance state changes, scheduled rules, service events).
- **Alarms**: trigger actions when thresholds are met (notify SNS, scale, stop/terminate, run automation).

Common use cases:
- Dashboard for **latency / error rate / throughput**
- Alarm on **5xx spike**, **p95 latency**, **queue depth**, **CPU/memory**, **DLQ messages**
- Centralize logs from EC2/containers/Lambda and query during incidents

### X-Ray = distributed tracing (latency + errors across services)
X-Ray helps you understand *why it’s happening*, especially for microservices.

- Shows **end-to-end request traces** and **service map**
- Breaks down latency by segment (e.g., API → Lambda → DynamoDB → S3)
- Highlights **errors**, **faults**, and **throttles**

Use X-Ray when:
- You have multiple services calling each other
- You need **root cause** for latency (which dependency is slow?)
- You want live visibility of **where errors happen**

### CloudTrail = API auditing (who did what, when, from where)
CloudTrail is for governance and security: it records **API calls** and changes.

- Tracks actions by users/roles/services (CreateBucket, PutPolicy, TerminateInstances, etc.)
- Key questions it answers:
  - Who changed a security group?
  - Which role deleted a resource?
  - When was a policy modified?

Use CloudTrail when:
- You need an audit trail for compliance
- You’re investigating suspicious activity or configuration drift

## How they fit together (mental model)

- **CloudWatch**: detect symptoms (high latency, error rate, CPU, queue depth).
- **X-Ray**: trace the request path to find the slow/failing component.
- **CloudTrail**: confirm whether a change (policy, SG, IAM, deployment) caused it.

## Practical study checklist

### CloudWatch checklist
- Understand: metrics vs logs vs alarms
- Know how to:
  - Create an **alarm** on a metric (e.g., ALB 5xx, Lambda errors)
  - Create **log metric filters** (turn log patterns into metrics)
  - Build a **dashboard**

### X-Ray checklist
- Understand: traces, segments/subsegments, service map
- Know when to use distributed tracing (microservices)
- Practice conceptually: identify which dependency adds latency

### CloudTrail checklist
- Understand: event history vs trail, management vs data events (high-level)
- Know what it is used for: **auditing API calls and changes**

## Quick self-quiz

1. Your app is slow. Which service helps you see which downstream call is slow?  
2. You need to alert on error rate spike. Which service and feature do you use?  
3. A security group rule changed and caused outage. Which service tells you who changed it?  
4. How do CloudWatch + X-Ray + CloudTrail complement each other during an incident?
