# Amazon EventBridge (formerly CloudWatch Events) — Study Notes

## What it is
Amazon EventBridge is an event routing service that sits in the middle between **event sources** and **targets (destinations)**.

## Core capabilities
- **Schedule / cron**: run something on a timer (e.g., every hour, every 4 hours, every Monday 8:00 AM, first Monday of the month).
- **Event pattern matching**: react when an AWS service does something (an event occurs).

## Typical flow (mental model)
1. **Sources** generate events (or a schedule triggers an event).
2. **EventBridge rule** filters/selects events (e.g., only events for a specific S3 bucket).
3. EventBridge delivers an **event JSON document** (payload with details like resource ID, time, IP, etc.).
4. The event is sent to one or more **targets**.

## Event sources (examples)
- **EC2** instance state changes (start/stop/terminate)
- **CodeBuild** build failures
- **S3** object upload events
- **Trusted Advisor** findings (e.g., security-related)
- **CloudTrail + EventBridge**: intercept *any API call* made in your AWS account (powerful audit/automation pattern)

## Targets / destinations (examples)
EventBridge can route events to many services, including:
- **AWS Lambda** (run code)
- **SNS / SQS** (notifications / queueing)
- **Kinesis Data Streams**
- **Step Functions**
- **CodePipeline / CodeBuild** (CI/CD automation)
- **ECS task / AWS Batch job**
- **SSM Automation**
- **EC2 actions** (start/stop/restart)

## Event buses
- **Default event bus**: AWS services publish events here by default.
- **Partner event bus**: SaaS partners can send events into your account (examples mentioned: Zendesk, Datadog, Auth0; availability depends on the partner list).
- **Custom event bus**: your own applications publish their own events here.

## Cross-account
Event buses can be accessed **cross-account** using **resource-based policies**.

## Practical examples to remember
- **Security alert**: if the **IAM root user signs in**, send to **SNS** so you receive an email notification.
- **Hourly automation**: every hour trigger a **Lambda** function to run a script.
- **S3 automation**: when an object is uploaded to a bucket, trigger downstream processing.

## Exam cues / keywords
If you see:
- “**cron**”, “scheduled rule”, “run every X” → think **EventBridge schedule**
- “react to AWS service events”, “event pattern” → think **EventBridge rule**
- “route to Lambda/SNS/SQS/Step Functions/CodePipeline” → think **EventBridge targets**
- “SaaS partner events” → think **Partner event bus**
- “your app emits events” → think **Custom event bus**
