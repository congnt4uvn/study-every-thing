# AWS Study Notes: Step Functions Wait for Task Token

## Overview
`waitForTaskToken` is a Step Functions integration pattern used when a workflow must pause and wait for an external callback before continuing.

You use this when your process depends on:
- Another AWS service
- Human approval
- Third-party systems
- Legacy systems outside Step Functions

## How It Works
In a Task state, append `.waitForTaskToken` to the `Resource` field.

Example concept:
- `sqs:sendMessage.waitForTaskToken`

When this pattern is used, the workflow pauses until one of these API calls returns with the correct token:
- `SendTaskSuccess`
- `SendTaskFailure`

## Typical Workflow
1. Step Functions starts execution.
2. A task (for example credit check) requires external processing.
3. Step Functions sends a message to SQS and includes:
- Business input payload
- Task token
4. An external worker reads from SQS (Lambda, ECS, EC2, or third-party server).
5. The worker processes the task.
6. The worker calls Step Functions callback API with the same token:
- Success path: `SendTaskSuccess` + output
- Failure path: `SendTaskFailure`
7. Step Functions validates token and resumes the workflow.

## Why This Pattern Is Useful
- Decouples orchestration from external processing systems
- Supports asynchronous and long-running tasks
- Enables human-in-the-loop workflows
- Integrates non-AWS and legacy systems safely

## Key Points to Remember
- Always pass the task token to the external processor.
- Callback must use the exact same token.
- Without callback, execution remains paused (or eventually times out if configured).
- Use clear error handling for `SendTaskFailure` paths.

## Quick Review Questions
1. Why would you use `waitForTaskToken` instead of a normal Task?
2. What two callback APIs can complete the paused task?
3. Which data must be included in the outbound message to external workers?
4. What happens if the external system never sends a callback?
