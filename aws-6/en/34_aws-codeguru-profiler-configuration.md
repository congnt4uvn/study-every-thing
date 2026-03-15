# AWS CodeGuru Profiler - Agent Configuration

## Overview
AWS CodeGuru Profiler uses an agent that can be configured to fine-tune its behavior and performance monitoring capabilities.

## Key Configuration Parameters

### 1. MaxStackDepth
**Purpose:** Determines the amount of code represented in the profile

**How it works:**
- Counts the depth of method calls in your code
- Example: If Method A → Method B → Method C → Method D (depth = 4)
- If MaxStackDepth is set to 2, only Method A and Method B will be profiled

**Important:** If you need to profile deeper call stacks, increase this parameter.

### 2. Memory Usage Limit Percent
**Purpose:** Controls how much memory the profiler agent is allowed to use

**Configuration:** Set as a percentage value to limit profiler's memory consumption

### 3. Minimum Time for Reporting (milliseconds)
**Purpose:** Sets the minimum time interval between sending reports

**Note:** The actual reporting interval will be bounded by this minimum value

### 4. Reporting Interval (milliseconds)
**Purpose:** Tells the agent how frequently to report the profiling data it has collected

**Configuration:** Can be increased based on your monitoring needs

### 5. Sampling Interval (milliseconds)
**Purpose:** Controls the sampling interval used to profile samples

**Key Points:**
- **Lower value** = More frequent sampling = Higher sampling rate
- Higher sampling rate allows you to catch more function/method calls
- Trade-off between detail and performance overhead

## Exam Tips
- You don't need to memorize all parameter values
- Understand how each setting influences the CodeGuru agent behavior
- Be able to identify the correct parameter based on the scenario in exam questions
- Focus on understanding the relationship between:
  - MaxStackDepth → call stack depth coverage
  - Sampling Interval → profiling granularity
  - Reporting Interval → data submission frequency

## Summary
CodeGuru Profiler's agent configuration allows you to balance between:
- **Depth of profiling** (MaxStackDepth)
- **Resource usage** (Memory Usage Limit)
- **Sampling frequency** (Sampling Interval)
- **Reporting frequency** (Reporting Interval)

Configure these parameters based on your application's specific needs and performance requirements.
