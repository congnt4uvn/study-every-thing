# AWS Study Notes — Integrating Amazon ECS with AWS X-Ray

Based on the lecture transcript in `file.txt`.

## Goal
Understand *how to run the X-Ray daemon with ECS* and the **three practical deployment options**.

## Key idea: what the X-Ray daemon does
Your application SDK sends trace data (UDP) to the **X-Ray daemon**. The daemon then forwards segments/subsegments to the X-Ray service.

The lecture’s repeated “takeaway” is:
- Expose **UDP port 2000** on the X-Ray daemon container
- Point your application to the daemon using **`AWS_XRAY_DAEMON_ADDRESS`** (or “AWS X-Ray Daemon Address” in the slide)
- Ensure the app and daemon can **reach each other on the network**

---

## Option 1 — ECS on EC2: X-Ray daemon as a *Daemon task* (one per EC2 instance)
**When you control the EC2 instances** in the ECS cluster, you can run the X-Ray daemon as an ECS **Daemon service**.

### How it works
- You have an ECS cluster backed by EC2 instances (you manage the instances).
- You run an **X-Ray daemon container as a daemon task**.
- ECS ensures **exactly one** daemon task runs on **every** EC2 instance in the cluster.

### Mental model
If you have 10 EC2 instances, you get **10 X-Ray daemon containers** (one per instance).

### Pros / cons (study)
- Pros: One daemon per host; app tasks on the host can share it.
- Cons: EC2-only; requires networking rules so app containers can send UDP to the host daemon.

---

## Option 2 — ECS on EC2: *Sidecar pattern* (one per app task/container)
Instead of one daemon per host, run a daemon **alongside** your app.

### How it works
- Each app task includes:
  - your **application container**
  - an **xray-daemon container** in the same task definition

### Mental model
If an EC2 instance runs 20 app containers/tasks, you might end up with **20 X-Ray sidecars**.

### Pros / cons (study)
- Pros: Isolation per task; easier “co-located” networking.
- Cons: More overhead (more daemon containers overall).

---

## Option 3 — ECS on Fargate: Sidecar pattern (required)
In **Fargate**, you do **not** control the underlying instances.

### Implication
- You **cannot** run a host-level daemon task across instances.
- You **must** run X-Ray as a **sidecar container** in each Fargate task.

---

## Example: What to look for in a task definition (from the lecture)
The lecture highlights 3 critical details.

### 1) X-Ray daemon container port mapping
- Container port: **2000**
- Protocol: **UDP**

### 2) App container environment variable
Set the daemon address so the app knows where to send trace data.

Common patterns:
- `AWS_XRAY_DAEMON_ADDRESS=xray-daemon:2000` (matches the lecture’s “hostname + port” idea)
- `AWS_XRAY_DAEMON_ADDRESS=127.0.0.1:2000` (often used when both containers share the same task network)

### 3) Networking connectivity between containers
The transcript mentions linking the containers so the hostname resolves (example: `links: ["xray-daemon"]`).

> Study takeaway: regardless of the exact ECS network mode, **the app must be able to reach the daemon on UDP/2000**.

---

## Mini checklist (memorize)
- [ ] Decide launch type: **EC2** vs **Fargate**
- [ ] Choose pattern:
  - [ ] EC2: **Daemon task** (1 per instance) OR **Sidecar** (1 per app)
  - [ ] Fargate: **Sidecar**
- [ ] Ensure daemon listens on **UDP/2000**
- [ ] Set `AWS_XRAY_DAEMON_ADDRESS` in the app
- [ ] Validate connectivity (security groups / network mode / task definition)

---

## Quick self-quiz
1. Why can’t you use an EC2-style daemon task on Fargate?
2. In the daemon-task approach, how many X-Ray daemon containers run if you have 12 EC2 instances?
3. In the sidecar approach, what’s the typical relationship between app tasks and daemon containers?
4. What port and protocol does the lecture emphasize for the X-Ray daemon?
5. Which single environment variable is called out to point the app to the daemon?
