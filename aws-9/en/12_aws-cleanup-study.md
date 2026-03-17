# AWS Study Note: Post-Lab Cleanup Checklist

## Why Cleanup Matters
After finishing AWS hands-on practice, you should remove unused resources to:
- Avoid unexpected costs.
- Keep your account organized.
- Build good cloud operations habits.

Always check every region where you created resources (example: Paris `eu-west-3`, N. Virginia `us-east-1`).

## Recommended Cleanup Order
1. Review regions used during labs.
2. Delete high-cost compute and data services first.
3. Delete networking and integration resources.
4. Delete monitoring and CI/CD leftovers.
5. Delete IAM-related items last (because many services depend on IAM roles/policies).

## Service-by-Service Checklist

### 1. EC2 and Related Services
- Terminate EC2 instances.
- Delete Auto Scaling groups.
- Delete Load Balancers and target groups.
- Remove unused EBS volumes/snapshots if any.

### 2. Lambda
- Delete Lambda functions not needed.
- (Lambda may cost little when idle, but cleanup is still best practice.)

### 3. Elastic Beanstalk
- Delete environments.
- Delete applications.

### 4. S3
- Review all buckets.
- Delete large/unneeded files.
- Delete empty buckets that are no longer used.

### 5. Databases
- RDS: delete DB instances/snapshots you do not need.
- DynamoDB: delete unused tables/indexes.
- For DynamoDB free tier awareness, avoid exceeding provisioned capacity limits (e.g., 10 RCU / 10 WCU in the context of this note).

### 6. API and Integration
- API Gateway: delete unused APIs/stages.
- SNS: remove test topics/subscriptions.
- SQS: delete test queues.
- Step Functions / SWF: remove test workflows/state machines.

### 7. Developer Tools
- Clean up CodeCommit repositories.
- Delete CodeBuild projects.
- Remove CodeDeploy applications/deployment groups.
- Delete CodePipeline pipelines.

### 8. Observability and Infrastructure as Code
- CloudWatch: remove alarms, dashboards, events/rules.
- CloudFormation: delete stacks (easy way to remove grouped resources).
- Systems Manager Parameter Store: delete lab parameters.

### 9. Streaming / Analytics
- Kinesis: delete streams that were created for testing.
- Important: Kinesis can become expensive and is typically not in free tier.

### 10. Security and Identity
- Cognito: remove test user pools/identity pools.
- IAM: delete lab users/roles/policies only after dependent resources are gone.

## Quick Final Verification
- Switch region by region and confirm no active paid resources remain.
- Recheck billing dashboard and cost explorer for new charges.
- Keep one personal checklist and reuse it after every lab/project.

## Key Lesson
The goal is not only passing an exam but also learning safe, cost-aware cloud operations. Cleanup is part of real AWS practice.
