# Amazon EventBridge — Study Notes (EN)

## 1) What EventBridge is (mental model)
Amazon EventBridge is an event-routing service.

- **Producers (event sources)** send events
- **Event buses** receive events
- **Rules / Pipes / Schedules** match or create events
- **Targets** receive events (SNS, SQS, Lambda, Step Functions, etc.)

From `file.txt`, the main EventBridge features to know:
- **Rules with event patterns** (react to events)
- **Schedules / EventBridge Scheduler** (run something on a time basis)
- **Pipes** (source → optional filter/enrichment → target)
- **Schema registry** (understand event shape)
- **Event buses** (default/custom) + **archive & replay**
- **Partner event sources** and **API destinations**

---

## 2) EventBridge Rules (event pattern)
A **rule** listens on an event bus and matches events using an **event pattern**.

### Example from `file.txt`: alert when EC2 is shutting down or terminated
Use the AWS-managed event type:
- **EC2 Instance State-change Notification**

Filter on the event field:
- `detail.state` equals **"shutting-down"** or **"terminated"**

A typical event pattern looks like:

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["shutting-down", "terminated"]
  }
}
```

### Target from `file.txt`: SNS Topic
To receive alerts:
- Choose **SNS Topic** as the target (e.g., a demo topic)
- EventBridge needs permissions to publish to SNS, so an **IAM role** is created/used

### What to verify in hands-on
- Trigger the event (stop/terminate an EC2 instance)
- Confirm the SNS subscription receives a message
- Review rule metrics / logs (as applicable)

---

## 3) Schedules (time-based triggers)
EventBridge can also run actions on a schedule.

From `file.txt`:
- Create schedule e.g., **InvokeLambdaEveryHour**
- **One-time** or **recurring**
- Use **cron-based** or **rate** schedule
- Example: **rate = 1 hour**
- Option: **no flexible time window**

Targets can include:
- Run an **ECS task**
- Put records into **Kinesis Data Firehose**
- Invoke a **Lambda function**

Study tip: be clear on when you should use a schedule (no event source needed) vs. a rule (reacting to events).

---

## 4) Event buses
From `file.txt`:

- **Default event bus**: receives AWS-generated events
- **Custom event bus**: your applications can publish custom events for your own workflows

Key ideas to remember:
- Your rule/pipes typically attach to a specific event bus
- Custom buses are common in event-driven architectures

---

## 5) Archive and replay
From `file.txt`:
- You can **archive** events from a bus
- Later, you can **replay** events from the archive to re-process history

Use cases:
- Debugging / incident replay
- Reprocessing after a bug fix
- Backfilling downstream systems

---

## 6) Partner event sources
From `file.txt`:
- Third-party partners can send events into your AWS account (example mentioned: Auth0)

You can then route those partner events to targets (e.g., Lambda) to react to actions like logins.

---

## 7) API destinations
From `file.txt`:
- EventBridge can route an event to an **external HTTP destination**

This is useful for integrating AWS events with non-AWS systems or your own infrastructure.

---

## 8) Schemas / Schema Registry
From `file.txt`:
- View schemas for AWS events
- Create your own custom registry for your own events

Why it matters:
- Helps you understand fields you can filter on (like `detail.state`)
- Helps producers/consumers agree on event shape

---

## 9) Quick checklist (exam + real work)
- Can I describe the flow: **source → bus → rule/pattern → target**?
- Do I know how to filter on event fields (e.g., EC2 state values)?
- Do I know when to use **Schedule** vs. **Rule**?
- Do I understand **default** vs. **custom** event bus?
- Do I understand what **archive/replay** is for?
- Can I explain **partner sources** and **API destinations** at a high level?

---

## 10) Mini-lab (recommended)
1. Create an SNS topic + email subscription.
2. Create an EventBridge rule using the EC2 state-change event pattern (shutting-down/terminated).
3. Terminate a test EC2 instance.
4. Confirm you receive the SNS notification.
5. Create a schedule that invokes a Lambda every hour (or every 5 minutes for testing).

