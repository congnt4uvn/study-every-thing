# AWS Study Notes — Amazon CloudWatch Metrics

## What CloudWatch Metrics Are
- **CloudWatch Metrics** provide time-series measurements for many AWS services.
- Metrics help you **understand service behavior** and do **basic troubleshooting**.
- Metric names often explain their meaning (examples: `CPUUtilization`, `NetworkIn`).

## Core Concepts (Terms You Must Know)
### Namespace
- Metrics are grouped into **namespaces** (often aligned with a service).
- In the console, you’ll see namespaces such as **EC2**, **EBS**, **ELB**, **Auto Scaling**, **EFS**, etc.

### Dimension
- A **dimension** is an attribute that further identifies a metric.
- Examples: **InstanceId**, **Environment**, etc.
- You can use dimensions to filter metrics down to a specific resource.
- You can choose **up to 30 dimensions per metric**.

### Timestamps
- Metrics are **time-stamped** data points.
- The period (granularity) determines how often you get points (e.g., 5 minutes vs 1 minute).

## Dashboards
- You can build **CloudWatch Dashboards** from metrics to monitor key signals.
- Common chart types include line, stacked area, number, and pie.

## EC2 Metric Frequency (Default vs Detailed Monitoring)
### Default monitoring
- EC2 instances publish metrics every **5 minutes** by default.

### Detailed monitoring (paid)
- If you enable **Detailed Monitoring**, EC2 publishes metrics every **1 minute**.
- Benefit: you can **react faster** to changes.
- It can help **Auto Scaling Groups (ASG)** scale out/in faster if you use alarm-driven policies.
- Note mentioned in the source: detailed monitoring allows **10 detailed monitoring metrics**.

## Custom Metrics (Important Gotcha)
- **Memory/RAM usage is NOT pushed by default** for EC2.
- To see RAM, you must publish it as a **custom metric** from the instance (agent/script).

## How to Explore Metrics in the Console (Hands-on)
1. Open **CloudWatch**.
2. Go to **Metrics**.
3. Pick a **namespace** (e.g., **EC2**).
4. Choose a per-resource view (e.g., **Per-Instance Metrics**).
5. Select a metric (example from the source: **CPU credit balance**).
6. Set a time range (e.g., **1 month**) and inspect the pattern.
7. Try different visualization options and filters.
8. Optional: add the chart to a **Dashboard**.
9. Optional: **Download CSV** or **Share**.

## How to Interpret a Metric (Study Pattern)
- Identify what the metric means from its name.
- Check the trend over time and correlate with events (deployments, scaling, traffic spikes).
- Compare multiple metrics when troubleshooting (CPU + Network + disk signals).

## Quick Self-Check Questions
- What is a CloudWatch **namespace**? Give 2 examples.
- What is a **dimension**, and why is it useful?
- What is EC2 default metric frequency? What changes with detailed monitoring?
- Why isn’t RAM visible by default in CloudWatch metrics for EC2?
- When might 1-minute metrics be meaningfully better than 5-minute metrics?

## Mini Lab (10–15 minutes)
- Pick one EC2 instance and graph these over a 1-week range:
  - `CPUUtilization`
  - `NetworkIn`
  - Any burst-related credit metric you have (if applicable)
- Change the graph period and compare how “noisy” vs “smooth” the chart looks.
- Save the chart into a new CloudWatch dashboard.
