# AWS CloudTrail — Study Notes (Practitioner)

## What CloudTrail is
- **AWS CloudTrail** records **API calls and user activity** within your AWS account.
- Think of it as an **audit trail**: it helps you answer “**who did what, where, and when**?”

## What you can see in the console (Event history)
- In the CloudTrail console, **Event history** shows **management events** for the **last 90 days**.
- You can browse the timeline of API activity and open an event to see its details.

## Example from the transcript: terminating an EC2 instance
When an EC2 instance is terminated, CloudTrail can show an event such as **TerminateInstances**.

Typical fields you’ll see in an event (as described in the transcript):
- **Event source** (e.g., **EC2**)
- **Access key** used
- **Region** used
- The full event payload (all event details)

## Why this matters (common use cases)
- **Security / auditing**: investigate suspicious actions.
- **Operations**: troubleshoot changes (e.g., “why did the instance disappear?”).
- **Compliance**: demonstrate accountability and traceability.

## Practitioner exam-friendly takeaways
- CloudTrail is about **tracking actions (API calls)**, not about monitoring CPU/memory.
- If someone performs an action in AWS (console/CLI/SDK), CloudTrail can help you **find the related API event**.
- **Event history** is a quick way to see recent activity (last **90 days** of management events).

## Quick self-check (Q&A)
1. What does CloudTrail primarily record?
   - API calls / account activity.
2. Where do you quickly look up recent management activity?
   - CloudTrail **Event history**.
3. After terminating an EC2 instance, what kind of CloudTrail event might appear?
   - A **TerminateInstances** API call.

## Mini flashcards
- CloudTrail → *audit log of API activity*
- Event history → *last 90 days (management events)*
- Terminate EC2 instance → *TerminateInstances event appears*
