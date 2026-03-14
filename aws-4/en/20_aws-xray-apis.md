# AWS X-Ray APIs (Exam Notes)

## What AWS X-Ray collects (quick context)
- **Trace**: end-to-end view of a single request as it moves through services.
- **Segment**: a JSON document describing work done by one service/component.
- **Subsegment**: a smaller unit of work inside a segment (e.g., a downstream call).
- The **X-Ray daemon / agent** buffers and sends segment data to the X-Ray service.

---

## Write side (daemon -> X-Ray service)
In exams, “write” actions are mostly **`Put*`** actions, plus a few **sampling `Get*`** actions needed by the daemon.

### Managed policy (concept)
- Often referenced as **X-Ray Write Only / Daemon write access**.
- Used by the **X-Ray daemon** (or SDK/agent) so it can send data to X-Ray.

### Key API actions
#### `xray:PutTraceSegments`
- Uploads **segment documents** to AWS X-Ray.
- Core permission required to write trace/segment data.

#### `xray:PutTelemetryRecords`
- Uploads daemon **telemetry** (how many segments were received/rejected, backend connection errors, etc.).
- Supports operational/health metrics for the daemon.

### Why are there `Get*` actions in “write” permissions?
X-Ray uses **sampling rules** to decide which requests to record.
- When sampling rules change in the console, daemons/agents need to **fetch the latest rules**.

#### `xray:GetSamplingRules`
- Fetches the sampling rules so the daemon knows what to send.

#### `xray:GetSamplingTargets`
- Advanced sampling support: obtains sampling targets from X-Ray.

#### `xray:GetSamplingStatisticSummaries`
- Advanced sampling support: retrieves summaries/statistics related to sampling.

### Exam tip
- If the question is about the **daemon sending segments**, think: **`PutTraceSegments`**.
- If the question is about **daemon health/metrics**, think: **`PutTelemetryRecords`**.
- If the question is about **sampling decisions**, think: **`GetSampling*`**.

---

## Read side (console / troubleshooting / analytics)
Read permissions are mostly **`Get*`** and **`BatchGet*`**.

### Managed policy (concept)
- Often referenced as **X-Ray Read Only access**.
- Used by users/roles that need to view X-Ray data (console, troubleshooting tools).

### Key API actions
#### `xray:GetServiceGraph`
- Retrieves the **main service graph** shown in the console.

#### `xray:GetTraceSummaries`
- Lists trace IDs and metadata (including annotations) for traces in a specified time range.
- Typical flow: **get summaries first**, then fetch full traces.

#### `xray:BatchGetTraces`
- Retrieves full trace data for a list of trace IDs.
- Each trace is a collection of segment documents for a single request.

#### `xray:GetTraceGraph`
- Retrieves a **service graph** for one or more specific trace IDs.

### Common read workflow (remember this)
1. `GetTraceSummaries` (find interesting trace IDs)
2. `BatchGetTraces` (pull the full traces)
3. Optional: `GetTraceGraph` / `GetServiceGraph` (visualize relationships)

---

## Quick “recognize it on the exam” table
| Situation | Likely API action(s) |
|---|---|
| Daemon/agent uploads trace segments | `PutTraceSegments` |
| Daemon uploads telemetry about segments/errors | `PutTelemetryRecords` |
| Daemon needs updated sampling rules | `GetSamplingRules`, `GetSamplingTargets`, `GetSamplingStatisticSummaries` |
| Console shows overall service map | `GetServiceGraph` |
| Find trace IDs for a time window | `GetTraceSummaries` |
| Fetch full trace details by IDs | `BatchGetTraces` |
| Graph for specific traces | `GetTraceGraph` |
