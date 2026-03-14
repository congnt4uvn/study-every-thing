# CloudWatch Logs Metric Filters (Study Notes)

## What problem this solves
A **CloudWatch Logs metric filter** scans log events in a log group and, when a pattern matches, it **publishes a data point** to a **CloudWatch metric** (often a custom metric in a custom namespace). You can then build **CloudWatch Alarms** and notifications/automation on top of that metric.

Typical use case: detect **HTTP 4xx/5xx** patterns in web access logs and alarm when errors spike.

## Scenario (from `file.txt`)
- Source logs: NGINX access logs shipped into **CloudWatch Logs**.
- Goal: detect occurrences of **HTTP 400** responses.
- Action:
  1) Create a metric filter matching `400`
  2) Publish value `1` on each match
  3) Create an alarm on that metric

## Key concepts
- **Log group / log stream**: where your application logs land.
- **Filter pattern**: expression used to match log events.
- **Metric namespace**: a container for custom metrics (e.g., `MetricFilters`).
- **Metric name**: the metric emitted by the filter (e.g., `MyDemoFilter`).
- **Metric value**: the value published per match (commonly `1`).
- **Default value**: value used when no matches occur (commonly `0`).

## Step-by-step: create a metric filter (Console)
1. Open **CloudWatch** → **Logs** → select your **log group**.
2. Choose **Actions** → **Create metric filter** (or go to **Metric filters** and create).
3. Enter a **Filter pattern**.
   - Simplest (demo): `400`
4. Test your pattern:
   - Use **Test pattern** against sample events.
   - Confirm it reports a reasonable match count (e.g., “14 matches out of 50 events”).
5. Configure metric:
   - **Filter name**: e.g., `MetricFilter400Code`
   - **Metric namespace**: e.g., `MetricFilters`
   - **Metric name**: e.g., `MyDemoFilter`
   - **Metric value**: `1`
   - **Default value**: `0`
6. Create the filter.

## Important behavior
- **Metric filters are not retroactive**.
  - They do **not backfill** metrics for historical log events.
  - Metrics start appearing only **after** the filter is created and new matching logs arrive.

## Generate fresh log events (to see data)
If the metric is flat at 0, trigger new logs:
- Restart app servers / redeploy / send test traffic (e.g., hit `/test`).
- Wait a few minutes, then check **CloudWatch → Metrics**.
- Look under your custom namespace (e.g., `MetricFilters`).

## Create an alarm on the metric
1. CloudWatch → **Metrics** → find your metric in the namespace.
2. Select the metric → **Create alarm**.
3. Choose conditions:
   - Example (demo): **Static threshold** “Greater than 50”.
   - For real systems, choose a threshold that reflects expected traffic (and use periods/statistics appropriately).
4. Choose notifications:
   - SNS topic (email/SMS) or other actions.
5. Name the alarm (e.g., `DemoMetricFilterAlarm`).

## Pattern tips (practical)
- Start simple, then tighten patterns to reduce false positives.
- Prefer matching structured fields when possible (JSON logs) rather than raw substrings.
- For access logs, consider matching the **status code field** (more precise than substring searching).

## Troubleshooting checklist
- No metric points after creation:
  - Confirm new logs are arriving.
  - Confirm the pattern matches new events.
  - Wait for CloudWatch metric publishing delays (a few minutes).
- Too many matches:
  - Pattern is too broad; refine it.
- Alarm not firing:
  - Verify period/statistic and evaluation settings.
  - Confirm metric is actually breaching threshold.

## Exam / interview takeaways
- Metric filter → publishes **custom metric** based on log pattern.
- Alarm → triggers **notifications/automation** based on metric.
- No historical backfill: **not retroactive**.
