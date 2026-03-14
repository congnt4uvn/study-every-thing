# AWS Distro for OpenTelemetry (ADOT) — Study Notes

## What you’re studying
This note summarizes **AWS Distro for OpenTelemetry (ADOT)** based on the source transcript in `file.txt`.

## OpenTelemetry (OTel) in one minute
**OpenTelemetry** is an open-source standard that provides:
- A single set of **APIs, libraries, agents, and collector services**
- To collect **distributed traces** and **metrics** from applications
- Plus the ability to collect **metadata/context** from AWS resources and services

Think of it as “standardized telemetry instrumentation” you can apply across many runtimes and environments.

## What is AWS Distro for OpenTelemetry (ADOT)?
**ADOT** is an **AWS-supported distribution** of the OpenTelemetry project, described as **secure** and **production-ready**.

Practically, ADOT helps you:
- Instrument apps using the OpenTelemetry standard
- Collect traces/metrics at scale
- Send telemetry to **AWS services** and **partner monitoring solutions**

## Where you can run it (instrumented apps)
The transcript highlights workloads running on AWS and on-premises, including:
- **EC2**
- **ECS**
- **EKS**
- **Fargate**
- **Lambda**
- **On-premises** applications

## What data is collected
- **Traces**: end-to-end request flow across distributed systems
- **Metrics**: measurements emitted by services (latency, error counts, etc.)
- **Contextual AWS resource data** (via the AWS distro)

## Where the data can be sent (destinations)
Examples called out in the transcript:
- **AWS X-Ray** (traces)
- **Amazon CloudWatch** (metrics)
- **Amazon Managed Service for Prometheus** (traces/metrics supported by OpenTelemetry)
- **Partner solutions** (example mentioned: Datadog)

Key idea: OpenTelemetry supports sending telemetry to **multiple destinations**.

## OpenTelemetry vs AWS X-Ray (as described)
OTel is described as **similar to X-Ray**, but:
- **OTel is open-source and standardized**
- You might migrate from X-Ray to ADOT if you want:
  - Standardization on open-source APIs
  - The ability to export to **multiple destinations simultaneously**

## Auto-instrumentation (why it matters)
Agents can be **auto-instrumented** to collect traces **without changing your code** (similar in feel to X-Ray-style instrumentation).

## Exam-focused takeaway
If this appears in an AWS exam context, it’s likely a **high-level** question. Remember:
- ADOT = AWS-supported OTel distribution
- OTel collects **traces + metrics** (and AWS context/metadata)
- Exports to X-Ray/CloudWatch/Prometheus/partners
- Differentiator vs X-Ray: **open standard + multi-destination export**

## Quick self-check (flash questions)
1. What does OpenTelemetry provide (components)?
2. What are the two main telemetry signal types mentioned?
3. Name 3 environments where instrumented apps can run.
4. Name 2 AWS destinations and 1 partner destination for telemetry.
5. Why would you choose ADOT over only using X-Ray?
