# AWS X-Ray — Advanced Concepts (Study Notes)

> Source: notes distilled from `file.txt` (instrumentation, segments/subsegments/traces, annotations vs metadata, sampling rules, daemon cross-account).

## 1) Instrumentation (what it means)
**Instrumentation** in software engineering means adding measurement hooks to:
- Measure a system’s performance
- Diagnose errors
- Emit trace information

In AWS X-Ray terms, instrumentation usually means **adding the X-Ray SDK** (and sometimes small config changes) so your application emits traces to the X-Ray service.

## 2) Instrumenting code with the X-Ray SDK (Node.js / Express)
The idea: you add minimal SDK code so requests are wrapped in segments and reported.

Example pattern (Express):

```js
const express = require('express');
const AWSXRay = require('aws-xray-sdk');

const app = express();

// Start a segment per incoming request
app.use(AWSXRay.express.openSegment('MyService'));

app.get('/health', (req, res) => res.send('ok'));

// End the segment
app.use(AWSXRay.express.closeSegment());

app.listen(3000);
```

### Customizing traces (advanced)
Beyond the “minimal” setup, you can customize how X-Ray behaves in your code using constructs like:
- Interceptors
- Filters
- Handlers
- Middleware

Goal: change what’s captured, add extra context, or adjust how data is emitted.

## 3) Segments, Subsegments, Traces
- **Segment**: the core unit your application/service sends to X-Ray (what you’ve likely been viewing so far).
- **Subsegment**: more granular detail *inside* a segment (use when you need deeper visibility).
- **Trace**: the end-to-end picture formed by collecting related segments together for a single request/call.

## 4) Annotations vs Metadata (important)
Both are key–value pairs, but they behave differently:

- **Annotations**
  - Indexed
  - Used for filtering/searching traces
  - Best for fields you want to query (e.g., `customerTier=premium`, `region=ap-southeast-1`)

- **Metadata**
  - Not indexed
  - Not usable for searching/filtering
  - Best for additional context you just want to record

## 5) X-Ray daemon/agent and cross-account tracing
The X-Ray daemon/agent can be configured to **send traces across AWS accounts**.
- Ensure IAM permissions are correct.
- The agent can assume the appropriate role so you can centralize tracing/logging into a “central” account.

## 6) Sampling (cost + control)
Sampling reduces how many requests get recorded and sent to X-Ray.
- More traces sent ⇒ higher cost.
- You can often change sampling behavior **without changing application code** by modifying sampling rules.

### Default sampling rule (as described in the source)
- Record **the first request each second** (the **reservoir**)
- Then record **5%** of additional requests (the **rate**)

Definitions:
- **Reservoir**: guarantees a minimum number of traces (e.g., at least 1 trace/second while serving).
- **Rate**: percentage of requests beyond the reservoir that are sampled.

### Custom sampling rules
You can create rules and choose reservoir + rate per traffic type.
Example described in the source:
- For `POST` requests: reservoir = **10** requests/second
- Then sample **10%** of additional requests

## Study checklist
- Explain “instrumentation” in your own words.
- Describe when you’d add subsegments.
- State the difference between annotations and metadata.
- Explain why sampling exists and how it affects cost.
- Define reservoir vs rate and give the default values.

## Quick self-quiz
1. What does instrumentation enable you to do in production systems?
2. What’s the difference between a segment and a trace?
3. Why are annotations “extremely important” for searching?
4. What two knobs define an X-Ray sampling rule?
5. In the default rule, what is guaranteed each second?
