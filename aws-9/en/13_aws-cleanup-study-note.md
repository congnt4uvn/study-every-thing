# AWS Cleanup Study Note

## Purpose
Use this note to review AWS services and practice safe cleanup after labs or projects.

## How to Study
1. Learn what the service does.
2. Identify common resources created during labs.
3. Practice finding those resources in AWS Console and AWS CLI.
4. Check dependencies before deleting anything.
5. Verify billing and monitoring after cleanup.

## Cleanup Checklist by Service

### Compute and Scaling
- EC2 Instances: Stop or terminate unused instances; verify attached EBS and security groups.
- Elastic Load Balancer: Delete unused ALB/NLB/CLB and target groups.
- Launch Configurations: Remove old launch configurations not used by Auto Scaling.
- Auto Scaling Groups: Scale down and delete unused groups.
- Elastic IPs: Release unassociated Elastic IP addresses.
- Security Groups: Remove unused groups after confirming no network interface uses them.
- EBS Volumes: Delete unattached volumes and old snapshots if no longer needed.
- Key Pairs: Remove unused key pairs from account and local machine.
- ECS Environments (Cluster, Service, Task Definition, ECR): Delete services, scale tasks to zero, remove task definitions and unneeded ECR images.
- Elastic Beanstalk Applications and Environments: Terminate environments and remove old app versions.
- AWS Lambda Functions: Delete obsolete functions and old function versions.

### Storage and Databases
- S3 Files and Buckets: Empty buckets, then delete buckets not needed.
- RDS Database: Snapshot if needed, then delete test databases and read replicas.
- DynamoDB Tables and Indexes: Remove unused tables and GSIs/LSIs created for testing.
- ElastiCache Cluster: Delete inactive Redis/Memcached clusters.

### Networking and Integration
- Route 53: Remove unused hosted zones and records.
- API Gateway: Delete deprecated APIs, stages, and custom domain mappings.
- Kinesis Streams: Delete streams not used by producers/consumers.
- SNS Topics: Remove test topics and unused subscriptions.
- SQS Queues: Delete queues and dead-letter queues no longer required.

### DevOps and Monitoring
- CodeCommit: Archive or delete unused repositories.
- CodeBuild: Remove obsolete projects and build artifacts.
- CodePipeline: Delete inactive pipelines and related resources.
- CloudWatch Logs: Set retention and remove unnecessary log groups.
- CloudWatch Metrics: Review custom metrics that may generate cost.
- CloudWatch Dashboards: Delete outdated dashboards.
- CloudWatch Alerts: Remove stale alarms or update thresholds.
- CloudWatch Rules (EventBridge Rules): Disable/delete unused scheduled or event rules.
- CloudFormation Stacks: Delete failed/old stacks and investigate retained resources.
- SSM Parameter Store: Remove stale parameters and secure sensitive ones.

### Identity and Access
- IAM Users, Groups, Roles, Policies: Remove unused identities and over-permissive policies.

## Safe Cleanup Flow
1. Tag resources before labs (for example: Project=Lab, Owner=YourName, ExpireDate=YYYY-MM-DD).
2. Use Resource Groups or AWS Config to find tagged resources.
3. Delete in dependency order:
   - App layer (APIs, services)
   - Compute layer (EC2, ASG, Lambda, ECS)
   - Data layer (RDS, DynamoDB, S3 backups)
   - Networking and IAM artifacts
4. Validate:
   - Billing dashboard trends down.
   - No unexpected CloudWatch alarms.
   - No production resources removed by mistake.

## Practice Tasks
- Build a small architecture (EC2 + ALB + RDS + S3), then fully clean it up.
- Write a CLI checklist script for listing resources by tag.
- Compare monthly cost before and after cleanup.

## Quick Review Questions
- Which AWS resources commonly continue costing money even when idle?
- Why should you snapshot RDS before deletion?
- What dependencies must be checked before deleting security groups?
- Why is tagging important for cleanup automation?

Great job reaching this stage. A consistent cleanup habit is an essential AWS skill.
