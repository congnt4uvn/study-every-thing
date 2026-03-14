# AWS X-Ray — Study Notes

## What it is
**AWS X-Ray** is a distributed tracing service that helps you **visualize**, **analyze**, and **debug** how requests flow through your application—especially across **microservices**.

### Why it matters (problem it solves)
Debugging production the “old way” often means:
- Reproducing locally (hard/impossible)
- Adding lots of log statements
- Redeploying and sifting through logs

This becomes painful at scale because:
- Many services log in different formats
- CloudWatch Logs navigation/analytics can be hard
- In microservices, there’s no single “end-to-end view” of one request

X-Ray provides that **end-to-end request view** (service map + traces).

## What you get (outputs)
- **Service map (graph)** of your architecture as X-Ray observes it
- Visibility into:
  - Error rates (e.g., which downstream dependency is failing)
  - Latency and bottlenecks
  - Dependencies between services
  - Per-request behavior (errors/exceptions by trace)

## Core concepts (exam-friendly)
### Tracing
Tracing means following a **single request** through all components that handle it.

### Segment / Subsegment
- A **trace** is made of **segments**.
- Segments can contain **subsegments**.
- Each component (API, app server, DB, queue, etc.) contributes information to the trace.

### Annotations
Add searchable key/value metadata to traces to provide extra context (e.g., tenant, user type, orderId).

### Sampling
You don’t have to trace every request. You can:
- Trace a percentage of total requests, or
- Limit to a certain rate (e.g., a few traces per minute)

## Compatibility / where it works
X-Ray integrates with many AWS compute and networking services, including:
- AWS Lambda
- Elastic Beanstalk
- Amazon ECS
- Elastic Load Balancing (ELB)
- Amazon API Gateway
- Amazon EC2

It can also be used with **on-premises** applications.

## How X-Ray works (high level)
1. Your app receives a request.
2. Instrumented code captures trace data for:
   - AWS SDK calls
   - HTTP/HTTPS calls
   - DB calls (MySQL, PostgreSQL, DynamoDB)
   - (and other supported integrations like queues)
3. Trace data is sent to X-Ray (often via the daemon, depending on platform).
4. X-Ray computes a **service map** from collected segments.

## Enabling X-Ray (most tested)
There are two key steps:

### 1) Instrument your code (X-Ray SDK)
- Your application must import/use the **AWS X-Ray SDK**.
- Languages mentioned: Java, Python, Go, Node.js, .NET.
- Usually “little code modification,” but not zero.

The SDK can capture:
- Calls to AWS services via AWS SDK
- HTTP/HTTPS requests
- DB calls for MySQL/PostgreSQL/DynamoDB

### 2) Ensure the “daemon/integration” is present
Two common scenarios:

**A. EC2 / on-prem / your own servers**
- You must **install and run the X-Ray daemon**.
- The daemon is a small program that receives trace data (described as a low-level UDP packet interceptor) and **batches/sends** it to AWS X-Ray (commonly every second).

**B. Managed integrations (e.g., Lambda and some AWS services)**
- The platform can run the daemon/integration for you.
- You mostly focus on enabling tracing and instrumenting your code.

### IAM permissions (required)
Your app (or the service execution role) must have IAM permissions to **write trace data** to X-Ray.

## Troubleshooting checklists
### “Works locally but not on EC2”
Most likely causes:
- X-Ray daemon is running locally, but **not running on the EC2 instance**
- EC2 instance role missing the required **X-Ray write permissions**

Quick EC2 checklist:
- [ ] App includes X-Ray SDK instrumentation
- [ ] X-Ray daemon installed + running on the instance
- [ ] Instance IAM role allows publishing trace data

### Lambda tracing not working
Typical checks:
- [ ] Lambda execution role includes needed X-Ray permissions
- [ ] Code imports/uses X-Ray SDK/instrumentation where required
- [ ] **Active tracing** is enabled for the Lambda function

## Typical exam prompts to prepare for
- “How do you enable X-Ray on EC2 vs Lambda?”
- “Why does X-Ray work on my laptop but not after deploying to EC2?”
- “What does the X-Ray daemon do?”
- “What is a segment vs a subsegment?”
- “What’s the value of service maps in microservices?”

## Quick self-quiz (answers from this note)
1. What problem does X-Ray solve that logs alone struggle with in microservices?
2. Name the two main steps to enable X-Ray.
3. When do you need to install the X-Ray daemon yourself?
4. What permissions are required for X-Ray to work?
5. What’s the difference between a segment and a subsegment?
