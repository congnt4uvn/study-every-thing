# CloudWatch Synthetics Canaries — Study Notes (AWS)

## What it is
CloudWatch Synthetics uses **canaries**: configurable scripts that run from **Amazon CloudWatch** to continuously monitor:
- **APIs** (availability + latency)
- **URLs / websites** (end-to-end customer flows)

A canary script programmatically reproduces what a real customer does (for example: open product page → add to cart → checkout), so you can detect issues **before users do**.

## What you can measure / capture
- Availability and latency of endpoints
- Page / endpoint load-time data
- **Screenshots** of the UI (useful for debugging)

## How it runs
- Script languages: **Node.js** or **Python**
- Includes access to a **headless Google Chrome** browser (so you can automate browser interactions)
- Run options: **once** or on a **regular schedule**

## Typical operational pattern (example)
1. App is deployed in one region (e.g., `us-east-1`).
2. A **Synthetics canary** monitors the app.
3. If the canary fails, a **CloudWatch Alarm** triggers.
4. The alarm invokes an **AWS Lambda** function.
5. Lambda updates a **Route 53** DNS record to fail over to another region (e.g., `us-west-2`).

This is one example of automated remediation / failover.

## Built-in blueprints (from the transcript)
- **Heartbeat Monitor**: loads a URL, stores screenshots + HTTP archive (HAR), validates it works.
- **API Canary**: tests basic read/write functions for REST APIs.
- **Broken Link Checker**: scans links on a page and detects broken links.
- **Visual Monitoring**: compares the current screenshot to a baseline screenshot.
- **Canary Recorder**: uses the CloudWatch Synthetics Recorder to record actions on a website and generate a script.
- **GUI Workflow Builder**: verifies UI actions/flows (e.g., login form flow).

## When to choose Synthetics (exam-style cues)
Pick CloudWatch Synthetics Canaries when you need:
- **Proactive monitoring** of user journeys (not just server metrics)
- **Synthetic** checks from CloudWatch on a schedule
- Browser-based checks (headless Chrome) + screenshots
- API availability/latency checks without relying on real users

## Quick self-check
- What languages can canary scripts be written in?
- What kind of browser access do you get?
- Name 3 blueprints and what each one does.
- How can a canary failure trigger automated failover?
