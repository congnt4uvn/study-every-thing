# AWS X-Ray with Elastic Beanstalk (EB) — Study Notes

## Goal
Enable AWS X-Ray tracing for an Elastic Beanstalk environment, ensuring:
- The X-Ray daemon runs on the EB EC2 instances.
- The EC2 instance profile has permissions to publish traces.
- Your application code is instrumented to send segments/subsegments.

## Key idea
Elastic Beanstalk platforms already include the X-Ray daemon binary, so you typically **don’t need to bundle it** yourself. You mainly need to **enable it** and ensure **IAM + instrumentation** are correct.

## Prerequisites
- An Elastic Beanstalk environment (single-instance or scaled).
- An EC2 instance profile (IAM role) attached to the EB instances.
- Application instrumented with the AWS X-Ray SDK (or a supported auto-instrumentation approach for your language/framework).

## Option A — Enable X-Ray in the Elastic Beanstalk Console
1. Create or open an EB environment.
2. Go to **Configuration**.
3. Find the **Monitoring** section (wording can vary by platform/version).
4. Enable **Amazon X-Ray** / **X-Ray daemon**.
5. Apply changes.

Result: the X-Ray daemon runs on your EB EC2 instances.

## Option B — Enable via `.ebextensions` config
If you prefer enabling it through configuration in your source bundle:

- Create folder: `.ebextensions/`
- Add a config file, e.g. `.ebextensions/xray-daemon.config`

Example minimal config (conceptually “enable daemon”):

```yaml
option_settings:
  aws:elasticbeanstalk:xray:
    XRayEnabled: true
```

Notes:
- The exact namespace/key is platform-dependent, but the lecture’s point is: **a minimal EB extension can enable the daemon**.
- Keep the file extension as `.config`.

## IAM — Instance profile permissions (critical)
The X-Ray daemon needs permission to write trace data to X-Ray.

Commonly, EB’s default EC2 role (often named like **aws-elasticbeanstalk-ec2-role**) includes policies such as a “Web Tier” policy that already grants X-Ray permissions.

If you use a **custom instance profile**, ensure it includes permissions for X-Ray actions (publish trace segments, telemetry, and read sampling rules, etc.).

Checklist:
- EB environment is using the intended **EC2 instance profile**.
- That role has the required X-Ray permissions.

## Application instrumentation (also critical)
Enabling the daemon is not enough by itself—your app must send trace data.

Checklist:
- Add the AWS X-Ray SDK (or equivalent) to your app.
- Instrument inbound requests and outbound calls (HTTP clients, DB calls, AWS SDK calls) per your language.
- Ensure the app sends segments/subsegments to the local daemon.

## Multi-container / Docker caveat
If you run **multi-container Docker** on Elastic Beanstalk, you may need to manage the X-Ray daemon yourself (for example, running it as a sidecar container), similar to patterns you’ll see with ECS.

## Verify
- Generate traffic to the application.
- Open the **AWS X-Ray console** and look for:
  - Service map entries
  - Traces appearing for your EB service

If you only see the default “Congratulations” page without instrumentation, you may not see useful traces.

## Cleanup
- Don’t forget to terminate the EB environment when done to avoid ongoing charges.

## Quick self-check
- What 3 things must be true for end-to-end tracing to work? (Daemon enabled, IAM permissions, app instrumentation)
- What changes when you use multi-container Docker? (You may need to run/manage the daemon yourself)
