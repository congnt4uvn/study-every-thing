# AWS Step Functions: Activity Tasks (Study Notes)

## 1) What is an Activity Task?
An Activity Task in AWS Step Functions lets external workers pull work from a state machine and report the result back.

External workers can run on:
- EC2 instances
- Lambda functions
- Mobile or on-prem applications

## 2) Core Flow
1. Worker polls Step Functions using `GetActivityTask`.
2. Step Functions returns task input and a task token (if work exists).
3. Worker processes the task.
4. Worker sends result using:
- `SendTaskSuccess`, or
- `SendTaskFailure`

## 3) Pull vs Push Model
### Activity Task = Pull model
- Worker actively pulls work from Step Functions.
- Network design is usually simpler because worker only needs outbound access to Step Functions.

### Callback with Wait for Task Token = Push model
- Step Functions can push events out (for example to SQS/EventBridge).
- External system must handle pushed event and later call back to Step Functions with task token.

## 4) Important Timing Settings
### `TimeoutSeconds`
- Maximum time a task can stay in progress before Step Functions marks it as failed.

### `HeartbeatSeconds`
- Maximum interval Step Functions waits for a heartbeat signal.
- Worker should call `SendTaskHeartbeat` regularly (for example every 5s if `HeartbeatSeconds` is 10s).

## 5) Long-Running Task Behavior
- With large `TimeoutSeconds` and continuous heartbeats, an Activity Task can run for up to 1 year.

## 6) Quick Comparison
| Feature | Activity Task | Wait for Task Token Callback |
|---|---|---|
| Work delivery | Pull (`GetActivityTask`) | Push event + callback |
| External worker role | Poll and execute | Consume event and callback |
| Network pattern | Usually simpler outbound polling | Often more integration components |
| Completion API | `SendTaskSuccess` / `SendTaskFailure` | `SendTaskSuccess` / `SendTaskFailure` |

## 7) Exam/Interview Memory Aids
- Activity Task = external worker polling Step Functions.
- Callback pattern = Step Functions emits event, then waits for callback with token.
- Heartbeat keeps long tasks alive; timeout defines hard upper bound.
