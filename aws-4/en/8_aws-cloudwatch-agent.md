# AWS CloudWatch Agent (Logs Agent vs Unified Agent)

## 1) Big idea
- By default, your EC2 instance does **not** send OS/application log files to CloudWatch.
- To send logs, you install and start a **CloudWatch Agent** (a small program) on the instance to **push the log files you choose** into **CloudWatch Logs**.
- The same agent approach can also be used on **on‑premises servers** (e.g., virtual machines), not only EC2.

## 2) Prerequisite (permission)
- The EC2 instance needs an **IAM role** that allows it to **send logs to CloudWatch Logs**.

## 3) Two agent options
### A) CloudWatch Logs Agent (older)
- Older agent.
- **Only** sends **logs** to **CloudWatch Logs**.

### B) CloudWatch Unified Agent (newer)
- Newer agent.
- Sends **logs** to **CloudWatch Logs**.
- Also collects **additional system‑level metrics** (more detailed than default EC2 monitoring).
- Supports easier, centralized configuration using **SSM Parameter Store**.

## 4) What extra metrics can the Unified Agent collect?
> You don’t need to memorize every sub-metric name; the point is the **granularity** and the **extra categories** (like memory/swap/processes).

- **CPU** (more granular): active, guest, idle, system, user, steal
- **Disk**: free, used, total
- **Disk I/O**: writes, reads, bytes, IOPS
- **RAM**: free, inactive, used, total, cached
- **Netstats**: TCP/UDP connections, packets, bytes
- **Processes**: counts / states such as dead, blocked, idle, running, sleep
- **Swap space**: free, used, used %

## 5) When should you think “Unified Agent”?
- When you want **more detailed metrics** than the default EC2 monitoring.
- Default EC2 monitoring gives high-level **CPU / disk / network** metrics, but **not memory and swap**.

## 6) Quick self-check (study)
- Why doesn’t an EC2 instance send logs to CloudWatch by default?
- What IAM capability must the instance have to ship logs?
- What is the main difference between the Logs Agent and the Unified Agent?
- Name 3 metric categories the Unified Agent adds beyond default EC2 monitoring.
