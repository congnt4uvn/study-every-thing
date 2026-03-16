# AWS Study Note: IAM PassRole and Trust Relationships

## Learning Goal
Understand how `iam:PassRole` and role trust policies work together when AWS services (EC2, Lambda, CodePipeline, ECS tasks, etc.) need to assume IAM roles.

## Core Idea
When you attach an IAM role to an AWS service, you are effectively **passing** that role to the service.

To do this safely, AWS requires two things:

1. The caller must have permission to pass the role (`iam:PassRole`).
2. The role's trust policy must allow that target service to assume the role.

Both conditions are required.

## Common Real Examples
- EC2 instance profile role passed to an EC2 instance.
- Lambda execution role passed to a Lambda function.
- CodePipeline service role passed to CodePipeline.
- ECS task role passed to an ECS task.

## Required IAM Permissions
Typically, the user or automation principal needs:
- `iam:PassRole` to pass a specific role.
- `iam:GetRole` (often included) to view role details.

## Example Policy (Who Can Pass Which Role)
This example lets a principal use EC2 actions and pass only one specific role named `S3Access`.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:PassRole",
        "iam:GetRole"
      ],
      "Resource": "arn:aws:iam::123456789012:role/S3Access"
    }
  ]
}
```

## Trust Policy (Which Service May Assume the Role)
Even if someone can pass a role, the role can only be assumed by trusted services defined in the role trust policy.

Example: trust only EC2 service.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Example for Lambda would use `lambda.amazonaws.com` as service principal.

## Important Security Notes
- Scope `iam:PassRole` to specific role ARNs, not `*`.
- Separate roles by workload (EC2 role, Lambda role, pipeline role).
- Use least privilege in both permission policies and trust policies.
- Audit who can pass high-privilege roles.

## Fast Mental Model
Think of role usage as a two-lock system:
- Lock 1: "Can caller pass this role?" -> `iam:PassRole`
- Lock 2: "Can this service assume this role?" -> trust policy

If either lock fails, role usage fails.

## Quick Checklist
Before attaching a role to a service, verify:
- Caller has `iam:PassRole` on that exact role.
- Role trust policy includes the correct service principal.
- Role permission policy grants only required actions.

## Self-Test Questions
1. Why is `iam:PassRole` not enough by itself?
2. What happens if trust policy allows EC2 but you pass role to Lambda?
3. Why is wildcard `iam:PassRole` risky?
4. Which policy controls who can assume a role: permission policy or trust policy?

## Short Answers
1. Because trust policy must also allow the target service to assume the role.
2. Lambda cannot assume it; operation fails.
3. It may let users attach powerful roles broadly, causing privilege escalation.
4. Trust policy.
