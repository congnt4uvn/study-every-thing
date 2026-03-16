# AWS Step Functions - Study Notes

## 1. What is AWS Step Functions?
AWS Step Functions is a service to **orchestrate workflows** using a **state machine** model.

- One workflow = one state machine
- You define the workflow in JSON (Amazon States Language)
- The workflow is visualized and execution history is tracked

Typical use cases:
- Order fulfillment
- Data processing pipelines
- Web application backend workflows
- Any multi-step process with branching and retries

## 2. Core idea
Step Functions lets you define:
- What happens first
- What happens next
- Which branch to follow based on conditions
- How long to wait between steps
- When to stop with success or failure

It is not just executing logic itself; it is mostly coordinating other AWS services.

## 3. How workflows start
A Step Functions workflow can be started by:
- AWS SDK / API call
- API Gateway
- CloudWatch Events / Amazon EventBridge
- Manual start from AWS Console

## 4. Task state (most important)
A **Task** state does actual work via integrated services.

Common Task integrations:
- Invoke AWS Lambda
- Submit AWS Batch job
- Run Amazon ECS task and wait for completion
- Write item to Amazon DynamoDB
- Publish message to Amazon SNS or Amazon SQS
- Start another Step Functions workflow

You can also use **Activities**:
- An external worker (EC2, ECS, or on-prem server) polls Step Functions for work
- Worker executes the task and returns result

## 5. Example Task (Lambda invoke)
A task typically includes:
- `Type: Task`
- `Resource`: Lambda invoke integration ARN
- `Parameters`: function name and payload
- `Next`: next state
- `TimeoutSeconds`: timeout control

## 6. Important state types
- **Task**: run work in AWS service or worker
- **Choice**: branch by condition
- **Wait**: delay for time or until timestamp
- **Pass**: pass input to output or inject fixed data
- **Parallel**: run branches at the same time
- **Map**: iterate over items dynamically
- **Succeed**: stop with success
- **Fail**: stop with failure

Exam-focus reminder:
- Task and Parallel are commonly emphasized

## 7. Execution visualization pattern
Typical pattern shown in the source:
1. Submit job
2. Wait X seconds
3. Get job status
4. If not complete -> loop back to Wait
5. If complete -> fetch final status
6. End

This visual execution is one of Step Functions' key strengths.

## 8. Why use Step Functions instead of one big Lambda?
- Better readability for complex workflows
- Native branching, waiting, retries, and error paths
- Built-in execution history and visualization
- Cleaner orchestration across many services

## 9. Quick review questions
1. What is the role of a Task state?
2. When would you use Choice vs Parallel?
3. How can a workflow be triggered?
4. Why is execution history useful in production?
5. What is the difference between direct service integration and Activities?
