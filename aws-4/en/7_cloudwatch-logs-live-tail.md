# CloudWatch Logs — Live Tail (Study Notes)

## What it is
**Live Tail** is a CloudWatch Logs feature that lets you stream log events in near real-time into a dedicated UI, filtered by **log group** and optionally **log stream**. It’s useful for **debugging** when events are being published continuously.

## When to use it
- Confirm an application is emitting logs as expected
- Debug issues while reproducing them (watch logs live)
- Observe high-volume streams without repeatedly refreshing the log stream view

## Key terms
- **Log group**: A container for log streams (often per application/service).
- **Log stream**: A sequence of log events from a single source (e.g., one instance/container).
- **Log event**: A single log record (message + timestamp).

## Hands-on: Create logs and verify with Live Tail
### 1) Create a log group
1. Open **CloudWatch** → **Logs**.
2. Create a **log group**.
   - Example name: `demo log group`

### 2) Create a log stream
1. Open the log group.
2. Create a **log stream**.
   - Example name: `DemoLogStream`

### 3) Start Live Tail
1. In CloudWatch Logs, open **Live Tail**.
2. Filter by:
   - **Log group**: select `demo log group`
   - **Log stream**: optional (select `DemoLogStream` to narrow)
3. Apply filter and **Start tailing**.
4. Leave Live Tail open and generate log events in a separate tab.

### 4) Publish a test log event
1. Return to the log stream view.
2. Choose **Actions** → **Create log event**.
3. Enter a message (e.g., `hello world`) and post it.
4. Confirm the event appears in **Live Tail**.

## What to look for in the Live Tail UI
- Matching events appear as they’re ingested
- You can inspect metadata (timestamp, group/stream)
- You can click through to jump to the originating log stream

## Cost / usage notes
The transcript mentions limited **free Live Tail usage per day** (e.g., about an hour/day). Treat Live Tail as a potentially billable feature:
- **Stop/close** the Live Tail session when finished to avoid unexpected charges.

## Common troubleshooting
- No events appear:
  - Verify you selected the correct log group/stream
  - Confirm events are actually being posted to that stream
  - Relax filters (don’t pin to a single stream) and try again

## Quick self-check
1. What’s the difference between a log group and a log stream?
2. Why might you choose to filter by log stream?
3. What should you do after debugging to control cost?
