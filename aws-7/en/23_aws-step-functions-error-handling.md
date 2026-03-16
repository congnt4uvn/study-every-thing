# AWS Study Notes: Step Functions Error Handling

## Goal
Learn how AWS Step Functions handles task failures from AWS Lambda using `Retry` and `Catch`.

## Scenario from the lesson
- A Lambda function is created from a Step Functions error blueprint.
- The function intentionally throws an error.
- A state machine invokes this Lambda.
- The workflow routes execution based on error type.

## Lambda behavior
The Lambda first throws a custom error named `CustomError`.

Example idea:
```js
throw new Error("This is a custom error!")
```

Later, the Lambda is changed to throw a different error type (`NotCustomError`) to test another path.

## State machine design
Main flow:
1. Invoke Lambda task.
2. If success, end workflow.
3. If failure, apply retry rules.
4. If retries are exhausted, route with catch rules.

Fallback states used in the lesson:
- `CustomErrorFallback`
- `ReservedTypeFallback`
- `CatchAllFallback`

## Key concepts
### 1) Retry
`Retry` defines automatic re-attempts before failing the state.

Common fields:
- `ErrorEquals`: which errors this retry applies to
- `IntervalSeconds`: delay before first retry
- `MaxAttempts`: total attempts
- `BackoffRate`: multiplier for next wait time

Observed behavior in the demo:
- `CustomError` used fast retries.
- Other error types used slower retries (for example 30s, then 60s).

### 2) Catch
`Catch` handles errors after retries are exhausted.

Routing in the demo:
- `CustomError` -> `CustomErrorFallback`
- Reserved/test type error -> `ReservedTypeFallback`
- Any other error (`States.ALL`) -> `CatchAllFallback`

## What happened during execution
### Case A: `CustomError`
- Lambda failed.
- Step Functions retried quickly.
- After retries were exhausted, execution moved to `CustomErrorFallback`.
- Workflow completed successfully.

### Case B: different error type (`NotCustomError`)
- Lambda failed with a different error.
- Retry timing followed a different policy (longer delays).
- After retries, execution moved to `ReservedTypeFallback`.
- Workflow completed successfully.

## Why this matters
- You can build resilient workflows without manually coding retry loops.
- Different errors can have different recovery strategies.
- Event history in Step Functions helps you debug each retry and transition.

## Clean up
You can delete the created state machine and Lambda if no longer needed.

## Quick exam-style review
1. What is the difference between `Retry` and `Catch` in Step Functions?
2. What does `States.ALL` do?
3. How does `BackoffRate` change retry timing?
4. Why route different error types to different fallback states?
