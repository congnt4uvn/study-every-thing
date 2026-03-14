# AWS Study Notes — CloudWatch X-Ray Sampling Rules

## Where to configure
- AWS Console → **CloudWatch**
- Left sidebar → **Settings**
- Under **CloudWatch settings** → **Traces**
- Open **Sampling rules** (you may also see encryption rules and group rules here)

## What sampling rules do (X-Ray)
Sampling rules control how many requests get recorded as **AWS X-Ray traces**, helping you balance:
- Observability (more traces)
- Cost / storage / noise (fewer traces)

## Default sampling rule
- There is a **default rule** with priority **10,000**.
- It matches **everything** (all requests).
- You **cannot edit the matching criteria** of the default rule.
- You *can* adjust its **limits**, such as:
  - **Reservoir size** (max requests sampled per second)
  - **Fixed rate** (percentage of additional requests sampled)

## Creating a custom sampling rule
In **Create sampling rule** you can set:

### 1) Rule name
Example: `DemoSampling`

### 2) Priority
- Range: **1–9,999**
- **Lower number = higher priority**
- Example: priority **5,000** overrides the default (**10,000**) when both match

### 3) Sampling limits
- **Reservoir size**: maximum requests to sample **per second**
  - Example: reservoir size **1**
- **Fixed rate**: percentage sampling (e.g., **100%**)

### 4) Matching criteria (targeting)
To sample only specific traffic, specify fields like:
- **Service name** (example shown: `MYSERVICE`)
- **HTTP method** (example: `POST`)
- **URL path**

This lets you, for example, capture every `POST` request to a specific path for one service.

## Operational behavior (important)
- After creating the rule, you **do not need to restart X-Ray daemons**.
- The new rule is applied automatically, and you should see its effect in the **X-Ray console**.

## Quick review questions
1. Where in CloudWatch do you find X-Ray sampling rules?
2. What can you change on the default rule vs what can’t you change?
3. If two rules match, which one wins: priority 5,000 or 10,000?
4. What’s the difference between reservoir size and fixed rate?
5. Name three matching criteria you can use to target traffic.
