# AWS Study Notes: Multi-account Event Aggregation with Amazon EventBridge

## Goal
Aggregate events from multiple AWS accounts (e.g., EC2 instance state changes) into a **central account** so you can manage routing/notifications in one place.

## Core idea (from the lecture)
- Each **source account** (Account A/B/C/…) creates an **EventBridge rule** that matches events (for example, EC2 state-change events).
- The rule’s **target** can be an **event bus in a different account** (the central account).
- The **central account event bus** must have a **resource-based policy** that allows source accounts to send events to it.
- In the central account, you then create rules on that bus to fan out to **SNS**, **Lambda**, or other targets.

## Architecture overview
1. **Central account**
   - Creates/uses an EventBridge event bus (often a custom bus like `central-bus`).
   - Adds an **event bus policy** to allow `events:PutEvents` from other accounts.
   - Defines centralized rules and targets (SNS/Lambda/etc.).

2. **Each source account**
   - Creates a rule with an **event pattern** (e.g., EC2 instance state changes).
   - Sets the rule target to the **central account event bus ARN**.

## Step-by-step setup (high level)
### 1) Central account: create or choose an event bus
- You can use a **custom event bus** for better separation (recommended in many setups).

### 2) Central account: allow cross-account `PutEvents`
Add a resource policy to the central bus to accept events from source accounts.

Conceptually, the policy grants:
- **Action**: `events:PutEvents`
- **Principal**: the source AWS account IDs (or specific roles, depending on your setup)
- **Resource**: the central event bus ARN

Example policy (illustrative):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPutEventsFromOtherAccounts",
      "Effect": "Allow",
      "Principal": { "AWS": ["111111111111", "222222222222"] },
      "Action": "events:PutEvents",
      "Resource": "arn:aws:events:REGION:CENTRAL_ACCOUNT_ID:event-bus/central-bus"
    }
  ]
}
```

### 3) Source account(s): create an event rule (EC2 example)
Event pattern example for EC2 instance state changes:
```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"]
}
```

### 4) Source account(s): set the rule target to the central event bus
- Target type: **Event bus in another account**
- Target ARN: `arn:aws:events:REGION:CENTRAL_ACCOUNT_ID:event-bus/central-bus`

### 5) Central account: create routing rules and targets
On the central bus, create rules like:
- “If EC2 state becomes `stopped` → publish to SNS”
- “If state becomes `terminated` → invoke Lambda for cleanup”

## What to verify (quick checklist)
- Central bus policy includes all source accounts you expect.
- Source rules match the events you care about (test with a known state change).
- Source rule target points to the correct **region** + **bus name** + **account ID**.
- Central account rules are attached to the correct bus (custom bus vs default).

## Common gotchas
- **Wrong bus**: creating rules on the default bus when events land on a custom bus.
- **Region mismatch**: EventBridge is regional; ensure source and central are aligned with your design.
- **Missing permission**: without the central bus policy, cross-account `PutEvents` will fail.

## Study prompts
- Why use a custom event bus in the central account?
- Where do you place event filtering: source accounts, central account, or both?
- What targets would you use for alerting vs automation (SNS vs Lambda vs SQS)?
