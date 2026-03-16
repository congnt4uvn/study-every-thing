# AWS Step Functions with Lambda – Study Guide

## Overview

This guide covers how to create an **AWS Step Functions State Machine** that integrates with **AWS Lambda** functions, including building the workflow, configuring choices, and executing the state machine.

---

## Key Concepts

| Concept | Description |
|---|---|
| **State Machine** | A workflow defined in Step Functions that coordinates services |
| **Lambda Invoke** | A state that calls an AWS Lambda function |
| **Choice State** | A branching state that routes execution based on conditions |
| **Pass State** | A state that passes input to output without doing work |
| **Execution Role** | IAM role automatically created for the state machine to invoke AWS services |
| **ARN** | Amazon Resource Name — unique identifier for AWS resources |

---

## Step-by-Step: Building the State Machine

### 1. Create a New State Machine

- Navigate to **AWS Step Functions** → Click **Create state machine**
- Choose **Blank** format
- Use the **designer** or **Code** tab to define the workflow

### 2. Define the Workflow (state-machine.json)

The workflow consists of three states:

```
Lambda Invoke → Choice State → Is Teacher (Pass)
                             → Not Teacher (Fail)
```

**Flow logic:**
- **Lambda Invoke** — calls `HelloFunction` with an input payload
- **Choice State** — checks if the word `Stephane` is present in the Lambda output
  - If **yes** → go to **Is Teacher** state → output: `"Woohoo!"`
  - If **no** → go to **Not Teacher** state → output: error message

### 3. Create the Lambda Function

- Go to **AWS Lambda** → **Create function** → **Author from scratch**
- **Function name:** `HelloFunction`
- **Runtime:** Node.js (latest)
- **Code logic (function.js):**

```javascript
export const handler = async (event) => {
  const who = event.who;
  return `Hello, ${who}!`;
};
```

**Test cases:**
| Input (`who`) | Output |
|---|---|
| `Stephane` | `Hello, Stephane!` |
| `John` | `Hello, John!` |
| `Alice` | `Hello, Alice!` |

### 4. Link Lambda to the State Machine

- Copy the Lambda function's **ARN**
- In the state machine designer, select the **Lambda Invoke** state
- Paste the ARN into **Enter function name**

### 5. IAM Permissions

- Step Functions **automatically creates an execution role** when the state machine invokes Lambda (and optionally X-Ray)
- This role grants the required permissions without manual setup

### 6. Execute the State Machine

Go to your state machine → **Start execution** → provide input payload:

**Execution 1 — Success path:**
```json
{ "who": "Stephane Maarek" }
```
- Lambda returns: `Hello, Stephane Maarek!`
- Choice State detects `Stephane` → routes to **Is Teacher**
- Final output: `Woohoo!`

**Execution 2 — Error path:**
```json
{ "who": "John Doe" }
```
- Lambda returns: `Hello, John Doe!`
- Choice State does **not** find `Stephane` → routes to **Not Teacher**
- Final output: Error — *"Stephane the teacher wasn't found in the output of the Lambda Function"*

---

## Viewing Execution History

- After execution, select any execution to view:
  - Each **event** step-by-step
  - **Duration** of each state
  - **Input/Output** at each stage
- This is useful for debugging and auditing workflows

---

## Architecture Diagram

```
┌─────────────────┐
│   Input Payload  │
│  { who: "..." }  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Lambda Invoke  │  ──► HelloFunction(event.who)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Choice State   │
└────┬────────┬───┘
     │        │
"Stephane"   Not "Stephane"
found?        found?
     │        │
     ▼        ▼
┌─────────┐ ┌──────────────┐
│Is Teacher│ │ Not Teacher  │
│ Woohoo! │ │  Error Code  │
└─────────┘ └──────────────┘
```

---

## Key Takeaways

1. Step Functions uses **JSON** to define state machines (`state-machine.json`)
2. The **Choice State** enables conditional branching based on output values
3. Lambda functions are linked by their **ARN**
4. Step Functions **auto-creates IAM roles** for Lambda/X-Ray permissions
5. Execution history provides full visibility into each state's input, output, and timing

---

## Practice Questions

1. What format does AWS Step Functions use to define a state machine?
2. What is the purpose of the **Choice State** in this workflow?
3. How does the state machine receive permissions to invoke Lambda?
4. What happens when the Lambda output **does not** contain `Stephane`?
5. Where do you find the ARN of a Lambda function to link it to a state machine?

---

*Topic: AWS Step Functions | AWS Lambda | Serverless Orchestration*
