# AWS Step Functions: Workflow Types (Study Notes)

## 1) Overview
AWS Step Functions provides **3 workflow options**:

1. **Standard Workflow** (default)
2. **Express Workflow - Asynchronous**
3. **Express Workflow - Synchronous**

---

## 2) Standard Workflow

### Key characteristics
- Maximum duration: **up to 1 year**
- Execution model: **exactly-once**
- Throughput: around **2,000 executions/second**
- Execution history in console: up to **90 days**
- Long-term logging: use **CloudWatch Logs** with retention settings

### Pricing
- Charged by **number of state transitions**
  - A state transition means moving from one state to another.

### Typical use case
- Best for **non-idempotent** operations, for example:
  - Payment processing

---

## 3) Express Workflow (General)

### Key characteristics
- Maximum duration: **up to 5 minutes**
- Very high scale: **100,000+ executions/second**
- No detailed execution tracking in console
- Observability mainly through **CloudWatch Logs**

### Pricing
- Charged by:
  - Number of executions
  - Execution duration
  - Memory consumption

### Typical use cases
- IoT data ingestion
- Streaming data processing
- Mobile/backend high-volume APIs

---

## 4) Express Asynchronous vs Synchronous

## 4.1 Express Asynchronous
- Invocation returns quickly; caller **does not wait** for final result
- Execution guarantee: **at least once**
- If failures happen, Step Functions may retry automatically
- Because of retries, duplicate processing can happen
- You should design **idempotent** actions

### When to use
- When immediate response is not required
- Example: fire-and-forget messaging/event processing

## 4.2 Express Synchronous
- Caller waits until workflow completes and returns a result
- Execution guarantee: **at most once**
- If failure happens, Step Functions does **not** automatically restart execution
- Retry logic must be implemented by your application

### When to use
- When immediate result is required
- Example: microservice orchestration behind API Gateway or Lambda

---

## 5) Quick Comparison Table

| Feature | Standard | Express Async | Express Sync |
|---|---|---|---|
| Max duration | Up to 1 year | Up to 5 minutes | Up to 5 minutes |
| Execution guarantee | Exactly-once | At least once | At most once |
| Throughput | ~2,000/sec | 100,000+/sec | 100,000+/sec |
| Wait for result | Yes (normal flow) | No | Yes |
| Best for | Long, reliable, non-idempotent flows | Fire-and-forget, high-volume events | Request/response, real-time orchestration |
| Pricing basis | State transitions | Executions + duration + memory | Executions + duration + memory |

---

## 6) Exam-Focused Memory Points
- **Standard = exactly-once, long-running (up to 1 year)**
- **Express = short-running (up to 5 minutes), massive scale**
- **Async Express = at least once**
- **Sync Express = at most once**
- For Async retries, think about **idempotency**

---

## 7) Self-Check Questions
1. Which workflow type should you choose for payment processing, and why?
2. Why can Async Express cause duplicate effects if your action is not idempotent?
3. Which Express mode is better if an API caller must receive the final workflow result immediately?
4. How do pricing models differ between Standard and Express?
